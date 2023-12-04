import collections
import re

from bitshares.instance import shared_bitshares_instance
from PyQt5 import QtGui

from dexbot.config import Config
from dexbot.config_validator import ConfigValidator
from dexbot.helper import find_external_strategies
from dexbot.views.confirmation import ConfirmationDialog
from dexbot.views.errors import gui_error
from dexbot.views.notice import NoticeDialog
from dexbot.views.strategy_form import StrategyFormWidget
from dexbot.translator_strings import TranslatorStrings as TS

class WorkerController:
    def __init__(self, view, bitshares_instance, mode):
        self.view = view
        self.mode = mode
        self.validator = ConfigValidator(Config(), bitshares_instance or shared_bitshares_instance())

    @property
    def strategies(self):
        """
        Defines strategies that are configurable from the GUI.

        key: Strategy location in the project
        name: The name that is shown in the GUI for user
        form_module: If there is custom form module created with QTDesigner

        :return: List of strategies
        """
        strategies = collections.OrderedDict()
        strategies['dexbot.strategies.relative_orders'] = {
            'name': TS.worker_controller[0],
            'form_module': 'dexbot.views.ui.forms.relative_orders_widget_ui',
        }
        strategies['dexbot.strategies.staggered_orders'] = {'name': TS.worker_controller[1], 'form_module': ''}
        strategies['dexbot.strategies.king_of_the_hill'] = {'name': TS.worker_controller[2], 'form_module': ''}
        for desc, module in find_external_strategies():
            strategies[module] = {'name': desc, 'form_module': module}
            # if there is no UI form in the module then GUI will gracefully revert to auto-ui
        return strategies

    @classmethod
    def get_strategies(cls):
        """Class method for getting the strategies."""
        return cls(None, None, None).strategies

    @staticmethod
    def get_unique_worker_name():
        """
        Returns unique worker name "Worker %n".

        %n is the next available index
        """
        index = 1
        workers = Config().workers_data.keys()
        worker_name = TS.worker_controller[3].format(index)
        while worker_name in workers:
            worker_name = TS.worker_controller[3].worker_name.format(index)
            index += 1

        return worker_name

    @staticmethod
    def get_strategy_module(worker_data):
        return worker_data['module']

    @staticmethod
    def get_strategy_mode(worker_data):
        return worker_data['mode']

    @staticmethod
    def get_allow_instant_fill(worker_data):
        return worker_data['allow_instant_fill']

    @staticmethod
    def get_assets(worker_data):
        return re.split("[/:]", worker_data['market'])

    def get_base_asset(self, worker_data):
        return self.get_assets(worker_data)[1]

    def get_quote_asset(self, worker_data):
        return self.get_assets(worker_data)[0]

    @staticmethod
    def get_account(worker_data):
        return worker_data['account']

    @staticmethod
    def handle_save_dialog():
        dialog = ConfirmationDialog(TS.worker_controller[4])
        return dialog.exec_()

    @gui_error
    def change_strategy_form(self, worker_data=None):
        # Make sure the container is empty
        for index in reversed(range(self.view.strategy_container.count())):
            self.view.strategy_container.itemAt(index).widget().setParent(None)

        strategy_module = self.view.strategy_input.currentData()
        self.view.strategy_widget = StrategyFormWidget(self, strategy_module, worker_data)
        self.view.strategy_container.addWidget(self.view.strategy_widget)

        # Resize the dialog to be minimum possible height
        width = self.view.geometry().width()
        self.view.setMinimumHeight(0)
        self.view.resize(width, 1)

    @gui_error
    def validate_form(self):
        error_texts = []
        base_asset = self.view.base_asset_input.text()
        quote_asset = self.view.quote_asset_input.text()
        fee_asset = self.view.fee_asset_input.text()
        worker_name = self.view.worker_name_input.text()
        old_worker_name = None if self.mode == 'add' else self.view.worker_name

        if not self.validator.validate_worker_name(worker_name, old_worker_name):
            error_texts.append(TS.worker_controller[5].format(worker_name))
        if not self.validator.validate_asset(base_asset):
            error_texts.append(TS.worker_controller[6])
        if not self.validator.validate_asset(quote_asset):
            error_texts.append(TS.worker_controller[7])
        if not self.validator.validate_asset(fee_asset):
            error_texts.append(TS.worker_controller[8])
        if not self.validator.validate_market(base_asset, quote_asset):
            error_texts.append(TS.worker_controller[9].format(base_asset, quote_asset))
        if self.mode == 'add':
            account = self.view.account_input.text()
            private_key = self.view.private_key_input.text()
            if not self.validator.validate_account_name(account):
                error_texts.append(TS.worker_controller[10])
            if not self.validator.validate_private_key(account, private_key):
                error_texts.append(TS.worker_controller[11])
            elif private_key and not self.validator.validate_private_key_type(account, private_key):
                error_texts.append(TS.worker_controller[12])

        error_texts.extend(self.view.strategy_widget.strategy_controller.validation_errors())
        error_text = '\n'.join(error_texts)

        if error_text:
            dialog = NoticeDialog(error_text)
            dialog.exec_()
            return False
        else:
            return True

    @gui_error
    def handle_save(self):
        if not self.validate_form():
            return

        if self.mode == 'add':
            # Add the private key to the database
            private_key = self.view.private_key_input.text()

            if private_key:
                self.validator.add_private_key(private_key)

            account = self.view.account_input.text()
        else:  # Edit
            account = self.view.account_name.text()

        base_asset = self.view.base_asset_input.text()
        quote_asset = self.view.quote_asset_input.text()
        fee_asset = self.view.fee_asset_input.text()
        operational_percent_quote = self.view.operational_percent_quote_input.value()
        operational_percent_base = self.view.operational_percent_base_input.value()
        strategy_module = self.view.strategy_input.currentData()

        self.view.worker_data = {
            'account': account,
            'market': '{}/{}'.format(quote_asset, base_asset),
            'module': strategy_module,
            'fee_asset': fee_asset,
            'operational_percent_quote': operational_percent_quote,
            'operational_percent_base': operational_percent_base,
            **self.view.strategy_widget.values,
        }
        self.view.worker_name = self.view.worker_name_input.text()
        self.view.accept()


class UppercaseValidator(QtGui.QValidator):
    @staticmethod
    def validate(string, pos):
        return QtGui.QValidator.Acceptable, string.upper(), pos

from dexbot.strategies.config_parts.base_config import BaseConfig, ConfigElement

from dexbot.translator_strings import TranslatorStrings as TS

class KothConfig(BaseConfig):
    @classmethod
    def configure(cls, return_base_config=True):
        config = [
            ConfigElement(
                'mode',
                'choice',
                'both',
                TS.koth[0], # Mode
                TS.koth[1], # Operational mode
                ([
                    ('both', TS.koth[2]), # Buy + sell
                    ('buy', TS.koth[3]), # Buy only
                    ('sell', TS.koth[4]) # Sell only
                ]),
            ),
            ConfigElement(
                'lower_bound',
                'float',
                0,
                TS.koth[5], # Lower bound
                TS.koth[6], # Do not place sell orders lower than this bound
                (0, 10000000, 8, ''),
            ),
            ConfigElement(
                'upper_bound',
                'float',
                0,
                TS.koth[7], # Upper bound
                TS.koth[8], # Do not place buy orders higher than this bound
                (0, 10000000, 8, ''),
            ),
            ConfigElement(
                'buy_order_amount',
                'float',
                0,
                TS.koth[9], # Amount (BASE)
                TS.koth[10], # Fixed order size for buy orders, expressed in BASE asset, unless "relative order size" selected
                (0, None, 8, ''),
            ),
            ConfigElement(
                'sell_order_amount',
                'float',
                0,
                TS.koth[11], # Amount (QUOTE)
                TS.koth[12], # Fixed order size for sell orders, expressed in QUOTE asset, unless "relative order size" selected
                (0, None, 8, ''),
            ),
            ConfigElement(
                'relative_order_size',
                'bool',
                False,
                TS.koth[13], # Relative order size
                TS.koth[14], # Amount is expressed as a percentage of the account balance of quote/base asset
                None,
            ),
            ConfigElement(
                'buy_order_size_threshold',
                'float',
                0,
                TS.koth[15], # Ignore smaller buy orders
                TS.koth[16], # Ignore buy orders which are smaller than this threshold (BASE). If unset, use own order size as a threshold
                (0, None, 8, ''),
            ),
            ConfigElement(
                'sell_order_size_threshold',
                'float',
                0,
                TS.koth[17], # Ignore smaller sell orders
                TS.koth[18], # Ignore sell orders which are smaller than this threshold (QUOTE). If unset, use own order size as a threshold
                (0, None, 8, ''),
            ),
            ConfigElement(
                'min_order_lifetime',
                'int',
                6,
                TS.koth[19], # Min order lifetime
                TS.koth[20], # Minimum order lifetime before order reset, seconds
                (1, None, ''),
            ),
        ]

        return BaseConfig.configure(return_base_config) + config

    @classmethod
    def configure_details(cls, include_default_tabs=True):
        return BaseConfig.configure_details(include_default_tabs) + []

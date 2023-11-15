from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtGui

from dexbot.views.ui.eye_passwd_ui import Ui_EyePasswd

class EyePasswd(QWidget, Ui_EyePasswd):
    isShowPasswd = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.eye_button.clicked.connect(lambda: self.toogle_show_passwd())

    def toogle_show_passwd(self):
        self.isShowPasswd = not self.isShowPasswd
        self.password_input.setEchoMode(QLineEdit.Normal if self.isShowPasswd else QLineEdit.Password)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/dialog/svg/eye_close.svg" if self.isShowPasswd else ":/dialog/svg/eye_open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.eye_button.setIcon(icon)

    def text(self):
        return self.password_input.text()
    
    def setText(self, text):
        self.password_input.setText(text)
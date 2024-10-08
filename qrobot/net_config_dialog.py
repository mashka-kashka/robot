from PyQt6.QtWidgets import QDialog
from netifaces import interfaces
import platform

from net_config_dialog_ui import Ui_NetConfigDialog
import netifaces as ni

class NetConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NetConfigDialog()
        self.ui.setupUi(self)

        _interfaces = ni.interfaces()
        for _interface in _interfaces:
            try:
                _addr = ni.ifaddresses(_interface)[ni.AF_INET][0]['addr']
                self.ui.cbAddress.addItem(f"{_addr}")
            except:
                continue

    def get_address(self):
        return self.ui.cbAddress.currentText()

    def get_port(self):
        return self.ui.lePort.text()
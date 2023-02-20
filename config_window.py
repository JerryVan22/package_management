import subprocess
import sys

from base_config_window import Ui_Dialog
from PyQt5 import  QtWidgets

import site_sources
from PyQt5.QtCore import pyqtSlot

class config_window(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self) -> None:
        super(config_window,self).__init__()
        self.setupUi(self)
        for k,v in site_sources.site_name.items():
            self.comboBox.addItem(k,v)
        self.buttonBox.accepted.connect(self.change)
    
    @pyqtSlot()
    def change(self):
        subprocess.run(args=[sys.executable,"-m","pip","config","set","global.index-url",str(self.comboBox.currentData())])
        self.close()
from PyQt5.QtWidgets import QWidget
from base_pyinstall_window import Ui_Form
from PyQt5.QtWidgets import QApplication,QFileDialog

from PyQt5.QtCore import pyqtSlot
import sys

import threading
import subprocess
try :
    import PyInstaller
except ModuleNotFoundError:
    print('未下载Pyinstaller,无法打包')
    exit()
class pyinstall_window(QWidget,Ui_Form):
    def __init__(self,execute_path) -> None:
        super(pyinstall_window,self).__init__()
        self.executable_path=execute_path
        self.setupUi(self)
        self.input_file_pushButton.clicked.connect(self.open_input_file)
        self.output_pushButton.clicked.connect(self.open_output_dir)
        self.icon_pushButton.clicked.connect(self.open_icon_file)
        self.start_pushButton.clicked.connect(self.export_exe)
        self.signle_exe_radioButton.setChecked(True)
        self.with_consoleradioButton.setChecked(True)

    @pyqtSlot()
    def open_input_file(self):
        file_path=QFileDialog.getOpenFileName(filter="*.py")[0]
        if file_path!='':
            self.input_file_path.setText(file_path)

    @pyqtSlot()
    def open_output_dir(self):
        dir_path=QFileDialog.getExistingDirectory(self, '打开文件夹','./')
        if dir_path!='':
            self.output_path.setText(dir_path)

    @pyqtSlot()
    def open_icon_file(self):
        icon_path=QFileDialog.getOpenFileName(filter="*.ico")[0]
        if icon_path!='':
            self.icon_path.setText(icon_path)

    @pyqtSlot()
    def export_exe(self):
        self.console_flag=None
        self.dir_flag=None
        if self.with_consoleradioButton.isChecked():
            self.console_flag='--console'
        else :
            self.console_flag='--windowed'

        if self.signle_exe_radioButton.isChecked():
            self.dir_flag='--onefile'
        else:
            self.dir_flag='--onedir'
        package_thread=threading.Thread(target=self.thread_package)
        package_thread.start()
        # print(self.executable_path)
        
        # with open("./log/{}.log".format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),"w",encoding="gbk")as f:
        #     f.write(p.stdout)
            
        # PyInstaller.__main__.run([self.console_flag,self.dir_flag,'--noconfirm','--distpath={}'.format(self.output_path.text()),'--icon={}'.format(self.icon_path.text()),self.input_file_path.text()])
    def thread_package(self):
        subprocess.run(args=[self.executable_path, "-m", "PyInstaller",self.console_flag,self.dir_flag,'--noconfirm','--distpath={}'.format(self.output_path.text()),'--icon={}'.format(self.icon_path.text()),self.input_file_path.text()],encoding="gbk",stdout=subprocess.PIPE)


if __name__=="__main__":
    app = QApplication(sys.argv)
    ui = pyinstall_window(sys.executable)
    ui.show()
    sys.exit(app.exec_())

import os
import sys
import subprocess
import re
import time
import venv

import qdarkstyle
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog,QAction,QLineEdit,QTableWidget,QCompleter,QMessageBox,QTableWidgetItem,QHeaderView

from base_main import Ui_MainWindow
import pyinstall_window
import site_sources
import config_window

class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None) -> None:
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.executable_path=sys.executable

        self.interperter_path_lineEdit.setText(self.executable_path)
        self.interperter_path_lineEdit.setReadOnly(True)

        self.comboBox.addItem("默认","");
        for k,v in site_sources.site_name.items():
            self.comboBox.addItem(k,v)

        horizontalHeader = ["名称","版本"]
        self.query_line_edit.textChanged.connect(self.query_text)

        self.package_table.setColumnCount(2)
        self.package_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.package_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.package_table.setHorizontalHeaderLabels(horizontalHeader)
        self.package_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.update_table()

        self.download_button.clicked.connect(self.download_package)
        self.delete_button.clicked.connect(self.del_package)
        self.create_venv.triggered.connect(self.create_virtual_environment)
        self.open_venv.triggered.connect(self.open_virtual_environment)
        self.pip_download_source.triggered.connect(self.config)
        self.demo=pyinstall_window.pyinstall_window(self.executable_path)
        self.export_exe_action.triggered.connect(self.demo.show)


    @pyqtSlot()
    def download_package(self):
        download_name=self.lineEdit.text()
        download_site=self.comboBox.currentData()
        p=None
        if download_site!="":
            p=subprocess.run(args=[self.executable_path, "-m", "pip","install",download_name,"-i",download_site ],encoding="gbk",stdout=subprocess.PIPE)
        else:
            p=subprocess.run(args=[self.executable_path, "-m", "pip","install",download_name ],encoding="gbk",stdout=subprocess.PIPE)
            
        with open("./log/{}.log".format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),"w",encoding="gbk")as f:
            f.write(p.stdout)
        self.update_table()


    @pyqtSlot()
    def create_virtual_environment(self):
        venv_dir = QFileDialog.getExistingDirectory(self, '创建虚拟环境','./')
        if venv_dir!='':
            venv.create(venv_dir,with_pip=True)

    @pyqtSlot()
    def  open_virtual_environment(self):
        venv_dir=QFileDialog.getOpenFileName(self, '打开python解释器',filter='python.exe')[0]
        if venv_dir!="":
            self.executable_path=venv_dir
            self.demo.executable_path=self.executable_path
            self.interperter_path_lineEdit.setText(self.executable_path)
            self.update_table()
            

    @pyqtSlot()
    def config(self):
        x=config_window.config_window()
        x.show()
        x.exec()

    @pyqtSlot()
    def del_package(self):
        value=QMessageBox.warning(self,'test',"确认删除选择的库?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if value==QMessageBox.Yes:
            with open("./log/{}.log".format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),"w",encoding="gbk")as f:

                for idx in self.package_table.selectedIndexes():
                    p=subprocess.run(args=[self.executable_path, "-m", "pip","uninstall","-y",self.package_table.item(idx.row(),0).text() ],encoding="utf-8",stdout=subprocess.PIPE)
                    f.write(p.stdout)
            self.update_table()
            self.package_table.clearSelection()

    def update_table(self):
        p=subprocess.check_output(args=[self.executable_path, "-m", "pip","list"] ,encoding="utf-8",shell=True)
        res=p.split("\n")
        self.installed_packages=[r.split() for r in res[2:] if r!=""]
        self.query_text()
        self.completer = QCompleter([package[0] for package in self.installed_packages])
        self.completer.setFilterMode(Qt.MatchContains)#内容匹配
        self.query_line_edit.setCompleter(self.completer)

    @pyqtSlot()
    def query_text(self):
        i_str=self.query_line_edit.text()
        i_str.replace(" ", "")
        try :
            pattern=re.compile(r'{}'.format(i_str))
            res=[item for item in self.installed_packages if pattern.search(item[0])!=None]
            self.package_table.setRowCount(len(res))
            idx=0
            for package in res:
                self.package_table.setItem(idx,0,QTableWidgetItem(package[0]))
                self.package_table.setItem(idx,1,QTableWidgetItem(package[1]))
                idx+=1
        except re.error:
            pass






if __name__=="__main__":
    path = os.getcwd() + '\\' + "log" 
    if not os.path.exists(path):
        os.mkdir(path) #没有log文件夹，创造一个
    app = QApplication(sys.argv)

    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.light.palette.LightPalette()))
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

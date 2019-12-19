# imports
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import psutil
import random
import sys
import time

# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("test_pyqt_ui.ui")

# use loaded ui file in the logic class
class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.setMaximum(100)
        self.pushButton.clicked.connect(self.append_table)
        self.pushButton_2.clicked.connect(self.close_app)
        self.count = 0
        self.set_table_init()
        self.start_thread()

    def set_table_init(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(1000)
        self.tableWidget.setHorizontalHeaderLabels(['Date', 'Time', 'Weight (g)'])

    def start_thread(self):
        self.thread = AThread()
        self.thread.change_value.connect(self.mark_val)
        self.thread.change_value.connect(self.display_digit)
        self.thread.change_value.connect(self.set_progress)
        self.thread.start()

    def mark_val(self, val):
        self.val = float(val)

    def display_digit(self, val):
        self.lcdNumber.display(str(val))

    def set_progress(self, val):
        self.progressBar.setValue(float(val))

    def append_table(self):
        self.set_table_val(self.val)
        self.count += 1

    def set_table_val(self, val):
        now = datetime.now()
        td = "%02d"
        y_m_d = "{}-{}-{}".format(td%now.year, td%now.month, td%now.day)
        h_m_s = "{}:{}:{}".format(td%now.hour, td%now.minute, td%now.second)
        self.tableWidget.setItem(self.count,0,QtWidgets.QTableWidgetItem(y_m_d))
        self.tableWidget.setItem(self.count,1,QtWidgets.QTableWidgetItem(h_m_s))
        self.tableWidget.setItem(self.count,2,QtWidgets.QTableWidgetItem(str(val)))

    def close_app(self):
        sys.exit()


class AThread(QtCore.QThread):
    change_value = QtCore.pyqtSignal(str)

    def run(self):
        while 1:
            count=psutil.cpu_percent()
            self.change_value.emit("%.2f"%count)
            time.sleep(.1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Logic(None)
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
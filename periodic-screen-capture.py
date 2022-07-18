
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtCore import pyqtSignal, QThread
import sys

import ui.mainDialog as mainDialog
from config_file import *

import pyautogui
import time
##############global variables
global mon_config
global run_tread

capture_file_name = 'vib_freq_spectrum_'

version = "0.9"

class ThreadWorker(QThread):
    updateValueSignal = pyqtSignal(str)
    updateTextEditSignal = pyqtSignal(str)

    def run(self):
        global mon_config, run_tread
        #self.updateTextEditSignal.emit("Started MODBUS Read...\r\n\r\n")

        while run_tread == 1:
            file_name = "screen_captures\{}{}.png".format(capture_file_name, time.strftime("%Y-%m-%d-%H.%M.%S"))

            self.updateTextEditSignal.emit(f'screen captured and saved to : {file_name}')
            print("screen captured")

            #buttonReply = QMessageBox.question(self, 'READ PASS', f"Reading from {modbus_ip} > Serial no.: {regs[0]}",
            #                                   QMessageBox.Ok)


            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(file_name)

            time.sleep(float(mon_config['screen_capture']['period']))

        if run_tread == 0 :
            self.updateTextEditSignal.emit("Screen capture stopped")
            print("screen capture stopped")

    def stop(self):
        self.terminate()

class MainDialog(QDialog, mainDialog.Ui_mainDialog):

    def __init__(self, parent=None):

        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedWidth(480)
        self.setFixedHeight(250)

        # self.setWindowIcon(QIcon('nissaranayakaralogo.png'))
        self.setWindowTitle(f"Periodic Screen Capture v.{version}")

        self.loadGUI()

        # gui change signals
        self.lineEditFileNameTag.textChanged.connect(self.guiChanged)
        self.spinBoxPeriod.valueChanged.connect(self.guiChanged)

        #pushbuttons
        self.buttonStartCapture.clicked.connect(self.RunThread)
        self.buttonStopCapture.clicked.connect(self.stopCapture)

        self.buttonStopCapture.setEnabled(False)

    def RunThread(self):
        global run_tread
        run_tread = 1
        self.disableGUI()
        self.threadworker = ThreadWorker()
        #self.threadworker.updateValueSignal.connect(self.showdialog)
        self.threadworker.updateTextEditSignal.connect(self.updateText)
        # self.modbusworker.updateListSignal.connect(self.updateList)
        self.threadworker.start()

    def enableGUI(self):
        self.buttonStartCapture.setEnabled(True)
        self.buttonStopCapture.setEnabled(False)
        run_tread = 0

    def disableGUI(self):
        self.buttonStartCapture.setEnabled(False)
        self.buttonStopCapture.setEnabled(True)

    def stopCapture(self):
        global run_tread
        run_tread = 0
        self.enableGUI()

    def updateText(self, new_text):

        previousText = self.textEditStatus.toPlainText()
        lines = self.textEditStatus.document().blockCount()
        if lines > 200 :
            previousText = ""

        self.textEditStatus.setPlainText("{}{}\n".format(previousText, new_text))
        self.textEditStatus.moveCursor(QTextCursor.End)

        if new_text == 'Finished device search':
            self.buttonStartSearch.setEnabled(True)
            self.buttonStopSearch.setEnabled(False)
            self.gui_activate(True)

    def loadGUI(self):
        global mon_config

        self.lineEditFileNameTag.setText(mon_config['screen_capture']['file_name_tag'])
        # print(f"start ip : {int(mon_config['search_device']['start'])}")

        self.spinBoxPeriod.setMinimum(1)
        self.spinBoxPeriod.setMaximum(43200)


        self.spinBoxPeriod.setValue(int(mon_config['screen_capture']['period']))

    def guiChanged(self):
        global mon_config

        mon_config['screen_capture']['period'] = str(self.spinBoxPeriod.value())

        mon_config['screen_capture']['file_name_tag'] = self.lineEditFileNameTag.text()

    def closeEvent(self, event):
        global mon_config

        try:
            print("Saving settings in settings.txt")
            with open('settings.txt', 'w') as configfile:
                mon_config.write(configfile)
        except:
            print("Error : Unable to save settings on : settings.txt")
            
if __name__ == "__main__":
    #writeConfigFile()
    #exit(1)
    #readConfigFile()

    global mon_config

    # writeMonConfigFile('settings.txt')

    mon_config = readMonConfig('settings.txt')

    if mon_config == -1:
        print("Error reading config. file, restoring default settings...")
        writeMonConfigFile('settings.txt')
        mon_config = readMonConfig('settings.txt')

    app = QApplication(sys.argv)
    form = MainDialog()
    form.show()

    ret = app.exec_()
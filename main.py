import sys
import os
from time import sleep

if sys.version_info[0] >= 3:
    try:
        import g_python
        import PyQt5
    except ImportError:
        r = os.system("pip3 install g_python PyQt5")
        if r == 1:
            os.system("python -m pip install g_python PyQt5")
else:
    print("[FFBot] You need python 3.0+ for run this application.")
    exit()

from PyQt5 import QtCore, QtWidgets

from g_python.gextension import Extension
from g_python.hdirection import Direction
from g_python.hpacket import HPacket


class Ui_MainWindow(object):
    def __init__(self):
        extension_info = {
            "title": "FFBot",
            "description": "Bot for FallingFurni",
            "author": "Luizin & Lande",
            "version": "2.0"
        }

        self.extension = Extension(extension_info=extension_info, args=sys.argv)
        self.extension.start()

        def client_type(ext):
            sleep(0.50)
            return ext.connection_info["client_type"]

        self.client_type = client_type(self.extension)

        self.unity_string = "UNITY"
        self.flash_string = "FLASH"

        if str(self.client_type).__contains__(self.unity_string):
            headers = {
                "RoomUserWalk": 'Move',
                "RoomPlaceItem": 'ActiveObjectAdd',
                "UserTyping": 'UserStartTyping',
                "RoomPlaceItem_Wired": 'ActiveObjectUpdate'
            }
        else:
            headers = {
                "RoomUserWalk": 'MoveAvatar',
                "RoomPlaceItem": 'ObjectAdd',
                "UserTyping": 'StartTyping',
                "RoomPlaceItem_Wired": 'ObjectUpdate'
            }

        self.prefix = "!"

        self.disableType = False
        self.isStarted = False
        self.Capture = False
        self.FallingFurni = False
        self.location_x = 0
        self.location_y = 0
        self.specific = False
        self.autoStop = False
        self.isWired = False

        self.RoomPlaceItem = headers["RoomPlaceItem"]
        self.RoomUserWalk = headers["RoomUserWalk"]
        self.UserTyping = headers["UserTyping"]
        self.RoomPlaceItemWired = headers["RoomPlaceItem_Wired"]

        self.extension.intercept(Direction.TO_SERVER, self.DisableType, self.UserTyping)
        self.extension.intercept(Direction.TO_SERVER, self.CaptureTile, self.RoomUserWalk)
        self.extension.intercept(Direction.TO_CLIENT, self.FFBot, self.RoomPlaceItem, mode="async")
        self.extension.intercept(Direction.TO_CLIENT, self.FFBotWithWired, self.RoomPlaceItemWired, mode="async")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(376, 376)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.gridLayout_1.setObjectName("gridLayout_1")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout_3.addWidget(self.checkBox_6, 4, 0, 1, 1)
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout_3.addWidget(self.checkBox_5, 2, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_3.addWidget(self.doubleSpinBox, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.checkBox_7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout_3.addWidget(self.checkBox_7, 5, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 6, 0, 1, 1)
        self.gridLayout_1.addLayout(self.gridLayout_3, 2, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_2.addWidget(self.checkBox_4, 8, 0, 1, 1)
        self.checkBox_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_1.setObjectName("checkBox_1")
        self.gridLayout_2.addWidget(self.checkBox_1, 1, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 3, 0, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setObjectName("label_1")
        self.gridLayout_2.addWidget(self.label_1, 5, 0, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_2.addWidget(self.checkBox_3, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout_1.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_1.addItem(spacerItem2, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_1, 0, 1, 1, 1)
        self.console_log = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.console_log.setReadOnly(True)
        self.console_log.setObjectName("console_log")
        self.gridLayout_5.addWidget(self.console_log, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # -------------------------------------------------------------------------

        self.checkBox_1.clicked.connect(self.ffbot)
        self.checkBox_2.clicked.connect(self.wired)
        self.checkBox_3.clicked.connect(self.fspecific)
        self.checkBox_4.clicked.connect(self.auto_stop)
        self.checkBox_5.clicked.connect(self.capture)
        self.checkBox_6.clicked.connect(self.disabletype)
        self.checkBox_7.clicked.connect(self.TopMost)

    def ffbot(self):
        if self.FallingFurni:
            self.FallingFurni = False
            self.Message("FallingFurni: OFF")
        else:
            self.FallingFurni = True
            self.Message("FallingFurni: ON")

    def wired(self):
        if self.isWired:
            self.isWired = False
            self.Message('FFBot Wired: OFF')
        else:
            self.isWired = True
            self.Message('FFBOT Wired: ON')

    def fspecific(self):
        if self.specific:
            self.specific = False
            self.Message("Specific Tile: OFF")
        else:
            self.specific = True
            self.Message("Specific Tile: ON")

    def auto_stop(self):
        if self.autoStop:
            self.autoStop = False
            self.Message("AUTO STOP: OFF")
        else:
            self.autoStop = True
            self.Message("AUTO STOP: ON")

    def capture(self):
        if self.Capture:
            self.Capture = False
            self.Message("Capture: OFF")
        else:
            self.Capture = True
            self.Message("Capture: ON")

    def disabletype(self):
        if self.disableType:
            self.disableType = False
        else:
            self.disableType = True

        if self.disableType:
            self.Message("IgnoreType: ON")
        else:
            self.Message("IgnoreType: OFF")

    def TopMost(self):
        if self.checkBox_7.isChecked():
            MainWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on=True)
            self.Message("TopMost: ON")
        else:
            MainWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on=False)
            self.Message("TopMost: OFF")
        MainWindow.show()

    def Message(self, msg):
        msg = f'[FallingFurni] ~ {msg}'
        self.console_log.appendPlainText(msg)

    # -----------------------------------------------------------------------------

    def DisableType(self, msg):
        if self.disableType:
            msg.is_blocked = True

    def CaptureTile(self, msg):
        if self.Capture:
            msg.is_blocked = True
            self.Capture = False
            (x, y) = msg.packet.read('ii')
            self.location_x, self.location_y = x, y
            self.checkBox_5.setChecked(False)
            self.label_1.setText(f"Tile : {x} ; {y}")
            self.Message(f"Capture Position: {x},{y}")

    def walk(self, x, y):
        d = self.doubleSpinBox.value()
        sleep(d)
        self.extension.send_to_server(HPacket(self.RoomUserWalk, x, y))
        self.Message(f"Walk to : {x} ; {y} with {d} delay")

        if self.autoStop:
            self.FallingFurni = False
            self.checkBox_1.setChecked(False)
            self.isWired = False
            self.checkBox_2.setChecked(False)

    def FFBot(self, message):
        if self.FallingFurni:
            packet = message.packet

            if self.specific:
                self.walk(self.location_x, self.location_y)
            else:
                if str(self.client_type).__contains__(self.flash_string):
                    (_, _, x, y, _, _, _, _, _, _, _, _, _,) = packet.read('iiiiissiisiii')
                else:
                    (_, _, x, y, _, _, _, _, _, _, _, _, _,) = packet.read('liiiiliiisiil')
                self.walk(x, y)

    def FFBotWithWired(self, message):
        if self.isWired:
            packet = message.packet

            if self.specific:
                self.walk(self.location_x, self.location_y)
            else:
                if str(self.client_type).__contains__(self.flash_string):
                    (_, _, x, y, _, _, _, _, _, _, _, _, _, _,) = packet.read('iiiiissiisiiis')
                else:
                    (_, _, x, y, _, _, _, _, _, _, _, _, _) = packet.read('liiiliiisiils')
                self.walk(x, y)

    # -----------------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FFBot"))
        self.checkBox_6.setText(_translate("MainWindow", "Disable Type"))
        self.checkBox_5.setText(_translate("MainWindow", "Capture"))
        self.label_2.setText(_translate("MainWindow", "Delay :"))
        self.checkBox_7.setText(_translate("MainWindow", "Top Most"))
        self.checkBox_4.setText(_translate("MainWindow", "Auto Stop"))
        self.checkBox_1.setText(_translate("MainWindow", "FFBot"))
        self.checkBox_2.setText(_translate("MainWindow", "Wired"))
        self.label_1.setText(_translate("MainWindow", "Tile : x ; y"))
        self.checkBox_3.setText(_translate("MainWindow", "Specific"))


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())

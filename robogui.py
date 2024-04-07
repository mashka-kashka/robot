# Form implementation generated from reading ui file 'robogui.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(989, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(parent=self.splitter_2)
        self.splitter.setBaseSize(QtCore.QSize(320, 240))
        self.splitter.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.video = QtWidgets.QLabel(parent=self.splitter)
        self.video.setMinimumSize(QtCore.QSize(320, 240))
        self.video.setBaseSize(QtCore.QSize(320, 240))
        self.video.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.video.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.video.setLineWidth(2)
        self.video.setText("")
        self.video.setObjectName("video")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.splitter)
        self.tabWidget.setIconSize(QtCore.QSize(32, 32))
        self.tabWidget.setObjectName("tabWidget")
        self.tabConfig = QtWidgets.QWidget()
        self.tabConfig.setObjectName("tabConfig")
        self.formLayout_2 = QtWidgets.QFormLayout(self.tabConfig)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(parent=self.tabConfig)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.ip_address = QtWidgets.QLineEdit(parent=self.tabConfig)
        self.ip_address.setObjectName("ip_address")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.ip_address)
        self.tabWidget.addTab(self.tabConfig, "")
        self.tabMove = QtWidgets.QWidget()
        self.tabMove.setObjectName("tabMove")
        self.tabWidget.addTab(self.tabMove, "")
        self.log_widget = QtWidgets.QTextEdit(parent=self.splitter_2)
        self.log_widget.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.log_widget.setLineWidth(2)
        self.log_widget.setReadOnly(True)
        self.log_widget.setObjectName("log_widget")
        self.verticalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 989, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionExit = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon.fromTheme("system-shutdown")
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        self.actionConnect = QtGui.QAction(parent=MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.menu.addAction(self.actionConnect)
        self.menu.addAction(self.actionExit)
        self.menubar.addAction(self.menu.menuAction())
        self.toolBar.addAction(self.actionConnect)
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Робот 2.0"))
        self.video.setToolTip(_translate("MainWindow", "Видео"))
        self.label.setText(_translate("MainWindow", "Адрес"))
        self.ip_address.setInputMask(_translate("MainWindow", "000.000.000.000"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabConfig), _translate("MainWindow", "Настройки"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMove), _translate("MainWindow", "Движение"))
        self.menu.setTitle(_translate("MainWindow", "Управление"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionExit.setText(_translate("MainWindow", "Выход"))
        self.actionConnect.setText(_translate("MainWindow", "Подключиться"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1104, 836)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(200, 300))
        self.splitter.setBaseSize(QtCore.QSize(1, 1))
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.splitter)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 480))
        self.tabWidget.setObjectName("tabWidget")
        self.tabCamera = QtWidgets.QWidget()
        self.tabCamera.setObjectName("tabCamera")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/eye.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tabWidget.addTab(self.tabCamera, icon, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.teLog = QtWidgets.QTextEdit(parent=self.splitter)
        self.teLog.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.teLog.setReadOnly(True)
        self.teLog.setObjectName("teLog")
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionStartStop = QtGui.QAction(parent=MainWindow)
        self.actionStartStop.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/play.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon1.addPixmap(QtGui.QPixmap("icons/stop.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.actionStartStop.setIcon(icon1)
        self.actionStartStop.setObjectName("actionStartStop")
        self.actionConfig = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/gear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionConfig.setIcon(icon2)
        self.actionConfig.setObjectName("actionConfig")
        self.actionExit = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/quit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon3)
        self.actionExit.setObjectName("actionExit")
        self.toolBar.addAction(self.actionConfig)
        self.toolBar.addAction(self.actionStartStop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionExit.triggered.connect(MainWindow.close) # type: ignore
        self.actionStartStop.toggled['bool'].connect(MainWindow.on_start_stop) # type: ignore
        self.actionConfig.triggered.connect(MainWindow.on_config) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Робот"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCamera), _translate("MainWindow", "Камера"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionStartStop.setText(_translate("MainWindow", "Запуск"))
        self.actionStartStop.setIconText(_translate("MainWindow", "Запуск"))
        self.actionStartStop.setStatusTip(_translate("MainWindow", "Запустить сервер для передачи данных"))
        self.actionConfig.setText(_translate("MainWindow", "Настройки"))
        self.actionConfig.setStatusTip(_translate("MainWindow", "Открыть окно настроек робота"))
        self.actionExit.setText(_translate("MainWindow", "Выход"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Завершить работу"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+X"))

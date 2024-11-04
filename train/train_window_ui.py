# Form implementation generated from reading ui file 'train_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TrainWindow(object):
    def setupUi(self, TrainWindow):
        TrainWindow.setObjectName("TrainWindow")
        TrainWindow.resize(864, 667)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/ml.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        TrainWindow.setWindowIcon(icon)
        TrainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(parent=TrainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 320))
        self.tabWidget.setObjectName("tabWidget")
        self.tabLabels = QtWidgets.QWidget()
        self.tabLabels.setObjectName("tabLabels")
        self.gridLayout = QtWidgets.QGridLayout(self.tabLabels)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tb_new_labels = QtWidgets.QToolButton(parent=self.tabLabels)
        self.tb_new_labels.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/star.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_new_labels.setIcon(icon1)
        self.tb_new_labels.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_new_labels.setObjectName("tb_new_labels")
        self.horizontalLayout_2.addWidget(self.tb_new_labels)
        self.tb_open_labels = QtWidgets.QToolButton(parent=self.tabLabels)
        self.tb_open_labels.setEnabled(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/open-file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_open_labels.setIcon(icon2)
        self.tb_open_labels.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_open_labels.setObjectName("tb_open_labels")
        self.horizontalLayout_2.addWidget(self.tb_open_labels)
        self.tb_save = QtWidgets.QToolButton(parent=self.tabLabels)
        self.tb_save.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/save.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_save.setIcon(icon3)
        self.tb_save.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_save.setObjectName("tb_save")
        self.horizontalLayout_2.addWidget(self.tb_save)
        self.tb_add = QtWidgets.QToolButton(parent=self.tabLabels)
        self.tb_add.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("plus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_add.setIcon(icon4)
        self.tb_add.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_add.setObjectName("tb_add")
        self.horizontalLayout_2.addWidget(self.tb_add)
        self.toolButton = QtWidgets.QToolButton(parent=self.tabLabels)
        self.toolButton.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("minus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton.setIcon(icon5)
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.tb_edit = QtWidgets.QToolButton(parent=self.tabLabels)
        self.tb_edit.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("edit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_edit.setIcon(icon6)
        self.tb_edit.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_edit.setObjectName("tb_edit")
        self.horizontalLayout_2.addWidget(self.tb_edit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.tv_labels = QtWidgets.QTableView(parent=self.tabLabels)
        self.tv_labels.setStyleSheet("")
        self.tv_labels.setObjectName("tv_labels")
        self.tv_labels.horizontalHeader().setDefaultSectionSize(200)
        self.gridLayout.addWidget(self.tv_labels, 1, 0, 1, 1)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/tags.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tabWidget.addTab(self.tabLabels, icon7, "")
        self.tabData = QtWidgets.QWidget()
        self.tabData.setObjectName("tabData")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabData)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tv_data = QtWidgets.QTableView(parent=self.tabData)
        self.tv_data.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tv_data.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tv_data.setObjectName("tv_data")
        self.tv_data.horizontalHeader().setCascadingSectionResizes(True)
        self.tv_data.horizontalHeader().setDefaultSectionSize(150)
        self.tv_data.horizontalHeader().setStretchLastSection(False)
        self.tv_data.verticalHeader().setCascadingSectionResizes(False)
        self.gridLayout_4.addWidget(self.tv_data, 2, 1, 1, 1)
        self.gv_input = QtWidgets.QGraphicsView(parent=self.tabData)
        self.gv_input.setObjectName("gv_input")
        self.gridLayout_4.addWidget(self.gv_input, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tb_new_data = QtWidgets.QToolButton(parent=self.tabData)
        self.tb_new_data.setIcon(icon1)
        self.tb_new_data.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_new_data.setObjectName("tb_new_data")
        self.horizontalLayout_4.addWidget(self.tb_new_data)
        self.tb_open_data = QtWidgets.QToolButton(parent=self.tabData)
        self.tb_open_data.setIcon(icon2)
        self.tb_open_data.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_open_data.setObjectName("tb_open_data")
        self.horizontalLayout_4.addWidget(self.tb_open_data)
        self.tb_save_data = QtWidgets.QToolButton(parent=self.tabData)
        self.tb_save_data.setEnabled(False)
        self.tb_save_data.setIcon(icon3)
        self.tb_save_data.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_save_data.setObjectName("tb_save_data")
        self.horizontalLayout_4.addWidget(self.tb_save_data)
        self.tb_save_data_as = QtWidgets.QToolButton(parent=self.tabData)
        self.tb_save_data_as.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/save-as.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_save_data_as.setIcon(icon8)
        self.tb_save_data_as.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_save_data_as.setObjectName("tb_save_data_as")
        self.horizontalLayout_4.addWidget(self.tb_save_data_as)
        self.cb_labels = QtWidgets.QComboBox(parent=self.tabData)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_labels.sizePolicy().hasHeightForWidth())
        self.cb_labels.setSizePolicy(sizePolicy)
        self.cb_labels.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cb_labels.setStyleSheet("font: 18pt \"Noto Color Emoji\";")
        self.cb_labels.setIconSize(QtCore.QSize(24, 24))
        self.cb_labels.setObjectName("cb_labels")
        self.horizontalLayout_4.addWidget(self.cb_labels)
        self.tb_add_sample = QtWidgets.QToolButton(parent=self.tabData)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/download.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_add_sample.setIcon(icon9)
        self.tb_add_sample.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_add_sample.setObjectName("tb_add_sample")
        self.horizontalLayout_4.addWidget(self.tb_add_sample)
        self.tb_edit_sample = QtWidgets.QToolButton(parent=self.tabData)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/edit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_edit_sample.setIcon(icon10)
        self.tb_edit_sample.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_edit_sample.setObjectName("tb_edit_sample")
        self.horizontalLayout_4.addWidget(self.tb_edit_sample)
        self.tb_delete_sample = QtWidgets.QToolButton(parent=self.tabData)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("icons/delete.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_delete_sample.setIcon(icon11)
        self.tb_delete_sample.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_delete_sample.setObjectName("tb_delete_sample")
        self.horizontalLayout_4.addWidget(self.tb_delete_sample)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 0, 0, 1, 3)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("icons/pie-chart.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tabWidget.addTab(self.tabData, icon12, "")
        self.tabTrain = QtWidgets.QWidget()
        self.tabTrain.setObjectName("tabTrain")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tabTrain)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_3 = QtWidgets.QLabel(parent=self.tabTrain)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 6, 0, 1, 1)
        self.le_learning_rate = QtWidgets.QLineEdit(parent=self.tabTrain)
        self.le_learning_rate.setObjectName("le_learning_rate")
        self.gridLayout_5.addWidget(self.le_learning_rate, 5, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.tabTrain)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 5, 0, 1, 1)
        self.l_test_size = QtWidgets.QLabel(parent=self.tabTrain)
        self.l_test_size.setObjectName("l_test_size")
        self.gridLayout_5.addWidget(self.l_test_size, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 7, 1, 1, 1)
        self.le_epochs = QtWidgets.QLineEdit(parent=self.tabTrain)
        self.le_epochs.setObjectName("le_epochs")
        self.gridLayout_5.addWidget(self.le_epochs, 6, 1, 1, 1)
        self.le_batch_size = QtWidgets.QLineEdit(parent=self.tabTrain)
        self.le_batch_size.setCursorPosition(3)
        self.le_batch_size.setObjectName("le_batch_size")
        self.gridLayout_5.addWidget(self.le_batch_size, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.tabTrain)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 4, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tb_train_model = QtWidgets.QToolButton(parent=self.tabTrain)
        self.tb_train_model.setEnabled(False)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("icons/model.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tb_train_model.setIcon(icon13)
        self.tb_train_model.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_train_model.setObjectName("tb_train_model")
        self.horizontalLayout.addWidget(self.tb_train_model)
        self.tb_open_model = QtWidgets.QToolButton(parent=self.tabTrain)
        self.tb_open_model.setIcon(icon2)
        self.tb_open_model.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_open_model.setObjectName("tb_open_model")
        self.horizontalLayout.addWidget(self.tb_open_model)
        self.tb_save_model = QtWidgets.QToolButton(parent=self.tabTrain)
        self.tb_save_model.setEnabled(False)
        self.tb_save_model.setIcon(icon3)
        self.tb_save_model.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_save_model.setObjectName("tb_save_model")
        self.horizontalLayout.addWidget(self.tb_save_model)
        self.tb_save_model_as = QtWidgets.QToolButton(parent=self.tabTrain)
        self.tb_save_model_as.setEnabled(False)
        self.tb_save_model_as.setIcon(icon8)
        self.tb_save_model_as.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.tb_save_model_as.setObjectName("tb_save_model_as")
        self.horizontalLayout.addWidget(self.tb_save_model_as)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 4)
        self.le_test_size = QtWidgets.QLineEdit(parent=self.tabTrain)
        self.le_test_size.setObjectName("le_test_size")
        self.gridLayout_5.addWidget(self.le_test_size, 3, 1, 1, 1)
        self.fr_progress = QtWidgets.QFrame(parent=self.tabTrain)
        self.fr_progress.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.fr_progress.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.fr_progress.setObjectName("fr_progress")
        self.gridLayout_5.addWidget(self.fr_progress, 3, 2, 5, 1)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 1)
        self.gridLayout_5.setColumnStretch(2, 3)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("icons/learning.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tabWidget.addTab(self.tabTrain, icon14, "")
        self.tabClassification = QtWidgets.QWidget()
        self.tabClassification.setObjectName("tabClassification")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabClassification)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gv_classification = QtWidgets.QGraphicsView(parent=self.tabClassification)
        self.gv_classification.setObjectName("gv_classification")
        self.gridLayout_3.addWidget(self.gv_classification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabClassification, icon13, "")
        self.teLog = QtWidgets.QTextEdit(parent=self.splitter)
        self.teLog.setFrameShape(QtWidgets.QFrame.Shape.Panel)
        self.teLog.setReadOnly(True)
        self.teLog.setObjectName("teLog")
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        TrainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=TrainWindow)
        self.statusbar.setObjectName("statusbar")
        TrainWindow.setStatusBar(self.statusbar)
        self.actionActivateRobot = QtGui.QAction(parent=TrainWindow)
        self.actionActivateRobot.setCheckable(True)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("../qrobot/icons/robot_green.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon15.addPixmap(QtGui.QPixmap("../qrobot/icons/robot_red.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.actionActivateRobot.setIcon(icon15)
        self.actionActivateRobot.setObjectName("actionActivateRobot")
        self.actionConfig = QtGui.QAction(parent=TrainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("../qrobot/icons/gear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionConfig.setIcon(icon16)
        self.actionConfig.setObjectName("actionConfig")
        self.actionExit = QtGui.QAction(parent=TrainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("../qrobot/icons/quit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon17)
        self.actionExit.setObjectName("actionExit")
        self.actionActivateComputer = QtGui.QAction(parent=TrainWindow)
        self.actionActivateComputer.setCheckable(True)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("../qrobot/icons/chip-green.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon18.addPixmap(QtGui.QPixmap("../qrobot/icons/chip-red.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.actionActivateComputer.setIcon(icon18)
        self.actionActivateComputer.setObjectName("actionActivateComputer")

        self.retranslateUi(TrainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.cb_labels.setCurrentIndex(-1)
        self.actionExit.triggered.connect(TrainWindow.close) # type: ignore
        self.tb_add_sample.clicked.connect(TrainWindow.on_add_sample) # type: ignore
        self.tb_new_data.clicked.connect(TrainWindow.on_new_data) # type: ignore
        self.tb_open_data.clicked.connect(TrainWindow.on_open_data) # type: ignore
        self.tb_save_data.clicked.connect(TrainWindow.on_save_data) # type: ignore
        self.tb_save_data_as.clicked.connect(TrainWindow.on_save_data_as) # type: ignore
        self.tb_edit_sample.clicked.connect(TrainWindow.on_edit_sample) # type: ignore
        self.tv_data.doubleClicked['QModelIndex'].connect(TrainWindow.on_double_clicked_sample) # type: ignore
        self.tb_delete_sample.clicked.connect(TrainWindow.on_delete_sample) # type: ignore
        self.tb_train_model.clicked.connect(TrainWindow.on_train_model) # type: ignore
        self.tabWidget.currentChanged['int'].connect(TrainWindow.on_tab_changed) # type: ignore
        self.tb_open_model.clicked.connect(TrainWindow.on_open_model) # type: ignore
        self.tb_save_model.clicked.connect(TrainWindow.on_save_model) # type: ignore
        self.tb_save_model_as.clicked.connect(TrainWindow.on_save_model_as) # type: ignore
        self.tb_open_labels.clicked.connect(TrainWindow.on_open_labels) # type: ignore
        self.le_epochs.textChanged['QString'].connect(TrainWindow.on_epochs_changed) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(TrainWindow)
        TrainWindow.setTabOrder(self.tabWidget, self.tb_open_labels)
        TrainWindow.setTabOrder(self.tb_open_labels, self.tb_save)
        TrainWindow.setTabOrder(self.tb_save, self.tb_add)
        TrainWindow.setTabOrder(self.tb_add, self.toolButton)
        TrainWindow.setTabOrder(self.toolButton, self.tb_edit)
        TrainWindow.setTabOrder(self.tb_edit, self.tv_labels)
        TrainWindow.setTabOrder(self.tv_labels, self.tv_data)
        TrainWindow.setTabOrder(self.tv_data, self.gv_input)
        TrainWindow.setTabOrder(self.gv_input, self.tb_new_data)
        TrainWindow.setTabOrder(self.tb_new_data, self.tb_open_data)
        TrainWindow.setTabOrder(self.tb_open_data, self.tb_save_data)
        TrainWindow.setTabOrder(self.tb_save_data, self.tb_save_data_as)
        TrainWindow.setTabOrder(self.tb_save_data_as, self.cb_labels)
        TrainWindow.setTabOrder(self.cb_labels, self.tb_add_sample)
        TrainWindow.setTabOrder(self.tb_add_sample, self.tb_edit_sample)
        TrainWindow.setTabOrder(self.tb_edit_sample, self.tb_delete_sample)
        TrainWindow.setTabOrder(self.tb_delete_sample, self.teLog)
        TrainWindow.setTabOrder(self.teLog, self.le_test_size)
        TrainWindow.setTabOrder(self.le_test_size, self.le_batch_size)
        TrainWindow.setTabOrder(self.le_batch_size, self.le_learning_rate)

    def retranslateUi(self, TrainWindow):
        _translate = QtCore.QCoreApplication.translate
        TrainWindow.setWindowTitle(_translate("TrainWindow", "Робот"))
        self.tb_new_labels.setText(_translate("TrainWindow", "Создать"))
        self.tb_open_labels.setText(_translate("TrainWindow", "Открыть"))
        self.tb_save.setText(_translate("TrainWindow", "Сохранить"))
        self.tb_add.setText(_translate("TrainWindow", "Добавить"))
        self.toolButton.setText(_translate("TrainWindow", "Удалить"))
        self.tb_edit.setText(_translate("TrainWindow", "Редактировать"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLabels), _translate("TrainWindow", "Метки"))
        self.tb_new_data.setText(_translate("TrainWindow", "Создать"))
        self.tb_open_data.setText(_translate("TrainWindow", "Открыть"))
        self.tb_save_data.setText(_translate("TrainWindow", "Сохранить"))
        self.tb_save_data_as.setText(_translate("TrainWindow", "Сохранить как ..."))
        self.tb_add_sample.setText(_translate("TrainWindow", "Добавить"))
        self.tb_edit_sample.setText(_translate("TrainWindow", "Изменить"))
        self.tb_delete_sample.setText(_translate("TrainWindow", "Удалить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabData), _translate("TrainWindow", "Данные"))
        self.label_3.setText(_translate("TrainWindow", "Количестов эпох"))
        self.le_learning_rate.setInputMask(_translate("TrainWindow", "0.999"))
        self.le_learning_rate.setText(_translate("TrainWindow", "0.001"))
        self.label_2.setText(_translate("TrainWindow", "Скорость обучения"))
        self.l_test_size.setText(_translate("TrainWindow", "Доля тестовых данных"))
        self.le_epochs.setInputMask(_translate("TrainWindow", "999"))
        self.le_epochs.setText(_translate("TrainWindow", "40"))
        self.le_batch_size.setInputMask(_translate("TrainWindow", "999"))
        self.le_batch_size.setText(_translate("TrainWindow", "1"))
        self.label.setText(_translate("TrainWindow", "Размер пакета"))
        self.tb_train_model.setText(_translate("TrainWindow", "Обучить"))
        self.tb_open_model.setToolTip(_translate("TrainWindow", "Открыть модель"))
        self.tb_open_model.setText(_translate("TrainWindow", "Открыть"))
        self.tb_save_model.setToolTip(_translate("TrainWindow", "Сохранить модель"))
        self.tb_save_model.setText(_translate("TrainWindow", "Сохранить"))
        self.tb_save_model_as.setToolTip(_translate("TrainWindow", "Сохранить модель под другим именем"))
        self.tb_save_model_as.setText(_translate("TrainWindow", "Сохранить как ..."))
        self.le_test_size.setInputMask(_translate("TrainWindow", "9.99"))
        self.le_test_size.setText(_translate("TrainWindow", "0.33"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTrain), _translate("TrainWindow", "Обучение"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabClassification), _translate("TrainWindow", "Распознавание"))
        self.actionActivateRobot.setText(_translate("TrainWindow", "Активировать робота"))
        self.actionActivateRobot.setIconText(_translate("TrainWindow", "Активация"))
        self.actionActivateRobot.setStatusTip(_translate("TrainWindow", "Активировать робота"))
        self.actionConfig.setText(_translate("TrainWindow", "Настройки"))
        self.actionConfig.setStatusTip(_translate("TrainWindow", "Открыть окно настроек робота"))
        self.actionExit.setText(_translate("TrainWindow", "Выход"))
        self.actionExit.setStatusTip(_translate("TrainWindow", "Завершить работу"))
        self.actionExit.setShortcut(_translate("TrainWindow", "Ctrl+X"))
        self.actionActivateComputer.setText(_translate("TrainWindow", "Активировать компьютер"))

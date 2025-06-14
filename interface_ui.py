# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(838, 626)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.remote_monitoring = QtWidgets.QWidget()
        self.remote_monitoring.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remote_monitoring.sizePolicy().hasHeightForWidth())
        self.remote_monitoring.setSizePolicy(sizePolicy)
        self.remote_monitoring.setObjectName("remote_monitoring")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.remote_monitoring)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_11 = QtWidgets.QGroupBox(parent=self.remote_monitoring)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_11.sizePolicy().hasHeightForWidth())
        self.groupBox_11.setSizePolicy(sizePolicy)
        self.groupBox_11.setObjectName("groupBox_11")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_11)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.adapterList = QtWidgets.QListWidget(parent=self.groupBox_11)
        self.adapterList.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adapterList.sizePolicy().hasHeightForWidth())
        self.adapterList.setSizePolicy(sizePolicy)
        self.adapterList.setMinimumSize(QtCore.QSize(300, 0))
        self.adapterList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.adapterList.setObjectName("adapterList")
        self.gridLayout_11.addWidget(self.adapterList, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_11)
        self.groupBox_12 = QtWidgets.QGroupBox(parent=self.remote_monitoring)
        self.groupBox_12.setObjectName("groupBox_12")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_12)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.infoTable = QtWidgets.QTableWidget(parent=self.groupBox_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoTable.sizePolicy().hasHeightForWidth())
        self.infoTable.setSizePolicy(sizePolicy)
        self.infoTable.setMinimumSize(QtCore.QSize(300, 0))
        self.infoTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.infoTable.setObjectName("infoTable")
        self.infoTable.setColumnCount(0)
        self.infoTable.setRowCount(0)
        self.gridLayout_12.addWidget(self.infoTable, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_12)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_14 = QtWidgets.QGroupBox(parent=self.remote_monitoring)
        self.groupBox_14.setObjectName("groupBox_14")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_14)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.timer = QtWidgets.QHBoxLayout()
        self.timer.setObjectName("timer")
        self.measureSpeedButton = QtWidgets.QPushButton(parent=self.groupBox_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.measureSpeedButton.sizePolicy().hasHeightForWidth())
        self.measureSpeedButton.setSizePolicy(sizePolicy)
        self.measureSpeedButton.setMinimumSize(QtCore.QSize(120, 36))
        self.measureSpeedButton.setObjectName("measureSpeedButton")
        self.timer.addWidget(self.measureSpeedButton)
        self.clearGraphs = QtWidgets.QPushButton(parent=self.groupBox_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearGraphs.sizePolicy().hasHeightForWidth())
        self.clearGraphs.setSizePolicy(sizePolicy)
        self.clearGraphs.setMinimumSize(QtCore.QSize(120, 36))
        self.clearGraphs.setObjectName("clearGraphs")
        self.timer.addWidget(self.clearGraphs)
        self.gridLayout_14.addLayout(self.timer, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_14)
        self.checkboxes = QtWidgets.QHBoxLayout()
        self.checkboxes.setContentsMargins(0, -1, -1, -1)
        self.checkboxes.setObjectName("checkboxes")
        self.hideUpload = QtWidgets.QCheckBox(parent=self.remote_monitoring)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hideUpload.sizePolicy().hasHeightForWidth())
        self.hideUpload.setSizePolicy(sizePolicy)
        self.hideUpload.setObjectName("hideUpload")
        self.checkboxes.addWidget(self.hideUpload)
        self.hideDownload = QtWidgets.QCheckBox(parent=self.remote_monitoring)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hideDownload.sizePolicy().hasHeightForWidth())
        self.hideDownload.setSizePolicy(sizePolicy)
        self.hideDownload.setObjectName("hideDownload")
        self.checkboxes.addWidget(self.hideDownload)
        self.verticalLayout.addLayout(self.checkboxes)
        self.graphs_group = QtWidgets.QGroupBox(parent=self.remote_monitoring)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphs_group.sizePolicy().hasHeightForWidth())
        self.graphs_group.setSizePolicy(sizePolicy)
        self.graphs_group.setObjectName("graphs_group")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.graphs_group)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.graphWidget = PlotWidget(parent=self.graphs_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.graphWidget.setObjectName("graphWidget")
        self.gridLayout_13.addWidget(self.graphWidget, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.graphs_group)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.tabWidget.addTab(self.remote_monitoring, "")
        self.pingTab = QtWidgets.QWidget()
        self.pingTab.setObjectName("pingTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.pingTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox = QtWidgets.QGroupBox(parent=self.pingTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pingChoice = QtWidgets.QRadioButton(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pingChoice.sizePolicy().hasHeightForWidth())
        self.pingChoice.setSizePolicy(sizePolicy)
        self.pingChoice.setObjectName("pingChoice")
        self.horizontalLayout.addWidget(self.pingChoice)
        self.tracerChoice = QtWidgets.QRadioButton(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tracerChoice.sizePolicy().hasHeightForWidth())
        self.tracerChoice.setSizePolicy(sizePolicy)
        self.tracerChoice.setObjectName("tracerChoice")
        self.horizontalLayout.addWidget(self.tracerChoice)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addressInput = QtWidgets.QLineEdit(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addressInput.sizePolicy().hasHeightForWidth())
        self.addressInput.setSizePolicy(sizePolicy)
        self.addressInput.setMinimumSize(QtCore.QSize(0, 32))
        self.addressInput.setMaximumSize(QtCore.QSize(16777215, 40))
        self.addressInput.setObjectName("addressInput")
        self.horizontalLayout_2.addWidget(self.addressInput)
        self.pingButton = QtWidgets.QPushButton(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pingButton.sizePolicy().hasHeightForWidth())
        self.pingButton.setSizePolicy(sizePolicy)
        self.pingButton.setMinimumSize(QtCore.QSize(0, 40))
        self.pingButton.setMaximumSize(QtCore.QSize(180, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.pingButton.setFont(font)
        self.pingButton.setObjectName("pingButton")
        self.horizontalLayout_2.addWidget(self.pingButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.groupBox_6 = QtWidgets.QGroupBox(parent=self.pingTab)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.outputList = QtWidgets.QListWidget(parent=self.groupBox_6)
        self.outputList.setObjectName("outputList")
        self.verticalLayout_8.addWidget(self.outputList)
        self.horizontalLayout_16.addWidget(self.groupBox_6)
        self.gridLayout_4.addLayout(self.horizontalLayout_16, 1, 0, 1, 1)
        self.tabWidget.addTab(self.pingTab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_19 = QtWidgets.QGroupBox(parent=self.tab)
        self.groupBox_19.setObjectName("groupBox_19")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.groupBox_19)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.dbTableSelectCombo = QtWidgets.QComboBox(parent=self.groupBox_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dbTableSelectCombo.sizePolicy().hasHeightForWidth())
        self.dbTableSelectCombo.setSizePolicy(sizePolicy)
        self.dbTableSelectCombo.setMinimumSize(QtCore.QSize(240, 24))
        self.dbTableSelectCombo.setObjectName("dbTableSelectCombo")
        self.horizontalLayout_12.addWidget(self.dbTableSelectCombo)
        self.dbRefreshButton = QtWidgets.QPushButton(parent=self.groupBox_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dbRefreshButton.sizePolicy().hasHeightForWidth())
        self.dbRefreshButton.setSizePolicy(sizePolicy)
        self.dbRefreshButton.setMinimumSize(QtCore.QSize(0, 40))
        self.dbRefreshButton.setMaximumSize(QtCore.QSize(180, 40))
        self.dbRefreshButton.setObjectName("dbRefreshButton")
        self.horizontalLayout_12.addWidget(self.dbRefreshButton)
        self.gridLayout.addWidget(self.groupBox_19, 0, 0, 1, 1)
        self.groupBox_21 = QtWidgets.QGroupBox(parent=self.tab)
        self.groupBox_21.setObjectName("groupBox_21")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_21)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.dbDataTable = QtWidgets.QTableWidget(parent=self.groupBox_21)
        self.dbDataTable.setObjectName("dbDataTable")
        self.dbDataTable.setColumnCount(0)
        self.dbDataTable.setRowCount(0)
        self.verticalLayout_12.addWidget(self.dbDataTable)
        self.gridLayout.addWidget(self.groupBox_21, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_11.setTitle(_translate("MainWindow", "Адаптеры"))
        self.groupBox_12.setTitle(_translate("MainWindow", "Параметры адаптера"))
        self.groupBox_14.setTitle(_translate("MainWindow", "Статус"))
        self.measureSpeedButton.setText(_translate("MainWindow", "Начать замер"))
        self.clearGraphs.setText(_translate("MainWindow", "Сбросить"))
        self.hideUpload.setText(_translate("MainWindow", "Скрыть график скорости отдачи"))
        self.hideDownload.setText(_translate("MainWindow", "Скрыть график скорости загрузки"))
        self.graphs_group.setTitle(_translate("MainWindow", "График"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.remote_monitoring), _translate("MainWindow", "Тестирование сети"))
        self.groupBox.setTitle(_translate("MainWindow", "Ввод"))
        self.pingChoice.setText(_translate("MainWindow", "Пинг"))
        self.tracerChoice.setText(_translate("MainWindow", "Трассировка"))
        self.addressInput.setPlaceholderText(_translate("MainWindow", "Введите IP-адрес или имя хоста"))
        self.pingButton.setText(_translate("MainWindow", "Старт"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Журнал событий"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pingTab), _translate("MainWindow", "Диагностика сети"))
        self.groupBox_19.setTitle(_translate("MainWindow", "Таблицы"))
        self.dbRefreshButton.setText(_translate("MainWindow", "Обновить"))
        self.groupBox_21.setTitle(_translate("MainWindow", "Таблица"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Просмотр базы данных"))
from pyqtgraph import PlotWidget

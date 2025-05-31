from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from datetime import datetime
from interface_ui import Ui_MainWindow  # импорт класса из сгенерированного файла
from graph import Graph
from network_monitoring import NetworkMonitoring
from ping_tool import PingTracerTool
from adapter_info_table import AdapterInfoTable
from database.database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Устанавливаем иконку для окна
        self.setWindowIcon(QIcon("icons/icon.png"))

        self.network_monitoring = NetworkMonitoring()
        self.ping_tracer_tool = PingTracerTool(self)
        self.graph = Graph(self.ui.graphWidget)
        self.adapter_info_table = AdapterInfoTable(self.ui.infoTable)
        self.db = Database()
        self.ui.pingButton.setEnabled(False)


        self.load_adapters()
        self.connect_buttons()
        self.init_database_tab()

        # Для хранения заданной длительности замера
        self._timed_measure_duration = None
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_current_adapter)
        self.update_timer.setInterval(1000) 
        # Подключаем сигнал обновления данных
        self.network_monitoring.data_updated.connect(self.on_data_updated)

    def init_database_tab(self):
        """Инициализация вкладки базы данных"""
        # Добавляем таблицы в комбобокс с русскими названиями
        self.ui.dbTableSelectCombo.addItems(['Пинги', 'Трассировки'])
        
        # Подключаем обработчики
        self.ui.dbTableSelectCombo.currentTextChanged.connect(self.load_table_data)
        self.ui.dbRefreshButton.clicked.connect(self.load_table_data)
        
        # Загружаем данные первой таблицы
        self.load_table_data()

    def load_table_data(self):
        """Загрузка данных из выбранной таблицы"""
        table_name = self.ui.dbTableSelectCombo.currentText()
        
        if table_name == 'Пинги':
            data = self.db.get_ping_history(limit=100)
        else:
            data = self.db.get_trace_history(limit=100)
        
        # Настраиваем таблицу
        self.ui.dbDataTable.setColumnCount(3)
        self.ui.dbDataTable.setHorizontalHeaderLabels(['Адрес', 'Время', 'Результат'])
        self.ui.dbDataTable.setRowCount(len(data))
        
        # Заполняем таблицу данными
        for row, (address, timestamp, result) in enumerate(data):
            self.ui.dbDataTable.setItem(row, 0, QTableWidgetItem(address))
            self.ui.dbDataTable.setItem(row, 1, QTableWidgetItem(str(timestamp)))
            self.ui.dbDataTable.setItem(row, 2, QTableWidgetItem(result))
        
        # Подгоняем размеры столбцов под содержимое
        self.ui.dbDataTable.resizeColumnsToContents()

    def load_adapters(self):
        adapters = self.network_monitoring.get_adapters()
        self.ui.adapterList.clear()
        for name in adapters.keys():
            self.ui.adapterList.addItem(name)

    def connect_buttons(self):
        self.ui.addressInput.textChanged.connect(self.toggle_ping_button)
        self.ui.measureSpeedButton.clicked.connect(self.on_measure_speed_clicked)
        self.ui.adapterList.itemClicked.connect(self.on_adapter_selected)
        self.ui.clearGraphs.clicked.connect(self.on_clear_graphs_clicked)
        self.ui.pingButton.clicked.connect(self.execute_ping_trace)
        self.ui.hideDownload.stateChanged.connect(self.graph.toggle_download)
        self.ui.hideUpload.stateChanged.connect(self.graph.toggle_upload)
        self.graph.toggle_download(self.ui.hideDownload.checkState())
        self.graph.toggle_upload(self.ui.hideUpload.checkState())
    
    def toggle_ping_button(self, text):
        self.ui.pingButton.setEnabled(bool(text.strip()))

    def execute_ping_trace(self):
        self.ping_tracer_tool.execute_ping_trace()

    def update_current_adapter(self):
        if self.ui.adapterList.currentItem():
            adapter_name = self.ui.adapterList.currentItem().text()
            info = self.network_monitoring.get_adapter_info_by_name(adapter_name)

            elapsed_time = 0
            if self.network_monitoring._is_measuring and self.network_monitoring._measure_start_time:
                elapsed_time = (datetime.now() - self.network_monitoring._measure_start_time).total_seconds()
                current_download = info.get('current_download', 0)
                current_upload = info.get('current_upload', 0)

                self.graph.update_data(elapsed_time, current_download, current_upload)
            else:
                self.graph.clear()

            self.adapter_info_table.update_info(info, elapsed_time, self.network_monitoring._is_measuring)

    def on_adapter_selected(self, item):
        adapter_name = item.text()
        info = self.network_monitoring.get_adapter_info_by_name(adapter_name)
        self.adapter_info_table.update_info(info, 0, False)

    def on_measure_speed_clicked(self):
        if not self.network_monitoring._is_measuring:
            hours = 0
            minutes = 0
            seconds = 0

            measure_duration = hours * 3600 + minutes * 60 + seconds

            if measure_duration <= 0:
                measure_duration = None

            self._timed_measure_duration = measure_duration

            self.network_monitoring.start_measuring()
            self.graph.clear()
            self.ui.measureSpeedButton.setText("Остановить замер")
            self.update_timer.start()
        else:
            self._timed_measure_duration = None
            self.stop_measurement_and_update_ui()

    def stop_measurement_and_update_ui(self):
        """Останавливает замер и обновляет UI"""
        self.network_monitoring.stop_measuring()
        self.update_timer.stop()
        self.ui.measureSpeedButton.setText("Начать замер")

    def on_clear_graphs_clicked(self):
        """Очищает данные графика после подтверждения"""
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            'Вы уверены, что хотите очистить график?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.graph.clear()
            self._timed_measure_duration = None
            if self.ui.adapterList.currentItem():
                adapter_name = self.ui.adapterList.currentItem().text()
                info = self.network_monitoring.get_adapter_info_by_name(adapter_name)
                self.adapter_info_table.update_info(info, 0, False)

    def on_data_updated(self, info, elapsed_time):
        """Обработчик обновления данных от NetworkMonitoring"""
        if self.ui.adapterList.currentItem() and self.ui.adapterList.currentItem().text() == info['id']:
            current_download = info.get('current_download', 0)
            current_upload = info.get('current_upload', 0)
            self.graph.update_data(elapsed_time, current_download, current_upload)
            self.adapter_info_table.update_info(info, elapsed_time, self.network_monitoring._is_measuring)

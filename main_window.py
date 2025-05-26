from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer
from datetime import datetime

from graph import Graph
from network_monitoring import NetworkMonitoring
from ping_tool import PingTracerTool
from adapter_info_table import AdapterInfoTable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self) 

        self.network_monitoring = NetworkMonitoring()
        self.ping_tracer_tool = PingTracerTool()
        self.graph = Graph(self.graphWidget)
        self.adapter_info_table = AdapterInfoTable(self.infoTable)

        # Инициализация интерфейса
        self.load_adapters()
        self.connect_buttons()

        # Создаем таймер для обновления данных
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_current_adapter)
        self.update_timer.setInterval(1000)  

        # Для хранения заданной длительности замера
        self._timed_measure_duration = None

        # Подключаем сигнал обновления данных
        self.network_monitoring.data_updated.connect(self.on_data_updated)

    def load_adapters(self):
        adapters = self.network_monitoring.get_adapters()
        self.adapterList.clear()
        for name in adapters.keys():
            self.adapterList.addItem(name)

    def connect_buttons(self):
        self.measureSpeedButton.clicked.connect(self.on_measure_speed_clicked)
        self.adapterList.itemClicked.connect(self.on_adapter_selected)
        self.clearGraphs.clicked.connect(self.on_clear_graphs_clicked)
        self.pingButton.clicked.connect(self.execute_ping_trace)

    def execute_ping_trace(self):
        address = self.addressInput.text().strip()
        self.ping_tracer_tool.execute_ping_trace(address)

    def update_current_adapter(self):
        if self.adapterList.currentItem():
            adapter_name = self.adapterList.currentItem().text()
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
            self.measureSpeedButton.setText("Остановить замер")
            self.update_timer.start()
        else:
            self._timed_measure_duration = None
            self.stop_measurement_and_update_ui()

    def stop_measurement_and_update_ui(self):
        """Останавливает замер и обновляет UI"""
        self.network_monitoring.stop_measuring()
        self.measureSpeedButton.setText("Начать замер")
        self.update_timer.stop()

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
            if self.adapterList.currentItem():
                adapter_name = self.adapterList.currentItem().text()
                info = self.network_monitoring.get_adapter_info_by_name(adapter_name)
                self.adapter_info_table.update_info(info, 0, False)

    def on_data_updated(self, info, elapsed_time):
        """Обработчик обновления данных от NetworkMonitoring"""
        if self.adapterList.currentItem() and self.adapterList.currentItem().text() == info['id']:
            current_download = info.get('current_download', 0)
            current_upload = info.get('current_upload', 0)
            self.graph.update_data(elapsed_time, current_download, current_upload)
            self.adapter_info_table.update_info(info, elapsed_time, self.network_monitoring._is_measuring)

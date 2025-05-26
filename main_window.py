from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QListWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer
import pyqtgraph as pg # Импортируем pyqtgraph
from datetime import datetime
import platform
import subprocess

from adapter_managment import NetworkMonitoring

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self) 
        self.load_adapters()
        self.connect_buttons()
        
        # Создаем таймер для обновления данных
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_current_adapter)
        self.update_timer.setInterval(1000)  # Обновление каждую секунду

        # Инициализация графика
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("График скорости", color="b", size="12pt")
        styles = {'color': '#f00', 'font-size': '10pt'}
        self.graphWidget.setLabel('left', 'Скорость (Мбит/с)', **styles)
        self.graphWidget.setLabel('bottom', 'Время (сек)', **styles)
        self.graphWidget.addLegend()
        self.graphWidget.showGrid(x=True, y=True)

        self.time_points = []
        self.download_speeds = []
        self.upload_speeds = []

        self.download_plot = self.graphWidget.plot(self.time_points, self.download_speeds, pen=pg.mkPen(color='b', width=2), name='Загрузка')
        self.upload_plot = self.graphWidget.plot(self.time_points, self.upload_speeds, pen=pg.mkPen(color='r', width=2), name='Отдача')

    def load_adapters(self):
        adapters = NetworkMonitoring.get_adapters()
        self.adapterList.clear()
        for name in adapters.keys():
            self.adapterList.addItem(name)

    def connect_buttons(self):
        self.measureSpeedButton.clicked.connect(self.on_measure_speed_clicked)
        self.adapterList.itemClicked.connect(self.on_adapter_selected)
        self.clearGraphs.clicked.connect(self.on_clear_graphs_clicked)
        self.pingButton.clicked.connect(self.execute_ping_trace)

    def update_current_adapter(self):
        if self.adapterList.currentItem():
            adapter_name = self.adapterList.currentItem().text()
            info = NetworkMonitoring.get_adapter_info_by_name(adapter_name)
            self.update_adapter_info_table(info)

            # Обновляем график, если идет измерение
            if NetworkMonitoring._is_measuring and NetworkMonitoring._measure_start_time:
                elapsed_time = (datetime.now() - NetworkMonitoring._measure_start_time).total_seconds()
                current_download = info.get('current_download', 0)
                current_upload = info.get('current_upload', 0)

                self.time_points.append(elapsed_time)
                self.download_speeds.append(current_download)
                self.upload_speeds.append(current_upload)

                # Ограничиваем количество точек на графике для производительности
                max_points = 100 # Например, последние 100 секунд
                if len(self.time_points) > max_points:
                    self.time_points = self.time_points[-max_points:]
                    self.download_speeds = self.download_speeds[-max_points:]
                    self.upload_speeds = self.upload_speeds[-max_points:]

                self.download_plot.setData(self.time_points, self.download_speeds)
                self.upload_plot.setData(self.time_points, self.upload_speeds)
                
                # Автоматическое масштабирование по Y, но фиксированный диапазон по X
                self.graphWidget.enableAutoRange(axis='y', enable=True)
                if self.time_points:
                    self.graphWidget.setXRange(self.time_points[0], self.time_points[-1])

    def on_adapter_selected(self, item):
        adapter_name = item.text()
        info = NetworkMonitoring.get_adapter_info_by_name(adapter_name)
        self.update_adapter_info_table(info)

    def on_measure_speed_clicked(self):
        if not NetworkMonitoring._is_measuring:
            # Получаем время замера из input полей (часы, минуты, секунды)
            hours = 0
            minutes = 0
            seconds = 0
            try:
                hours = int(self.hoursInput.text()) if self.hoursInput.text() else 0
            except ValueError:
                pass # Оставляем 0
            try:
                minutes = int(self.minutesInput.text()) if self.minutesInput.text() else 0
            except ValueError:
                pass # Оставляем 0
            try:
                seconds = int(self.secondsInput.text()) if self.secondsInput.text() else 0
            except ValueError:
                pass # Оставляем 0

            measure_duration = hours * 3600 + minutes * 60 + seconds

            if measure_duration <= 0:
                measure_duration = None # Если общая длительность 0 или отрицательная, замер бесконечный

            NetworkMonitoring.start_measuring()
            self.measureSpeedButton.setText("Остановить замер")
            self.update_timer.start()

            # Если задана длительность замера, запускаем одноразовый таймер для остановки
            if measure_duration is not None:
                QTimer.singleShot(measure_duration * 1000, self.on_measure_timer_finished)

        else:
            self.stop_measurement_and_update_ui()

    def stop_measurement_and_update_ui(self):
        """Останавливает замер и обновляет UI"""
        NetworkMonitoring.stop_measuring()
        self.measureSpeedButton.setText("Начать замер")
        self.update_timer.stop()
        # Обновляем таблицу последний раз, чтобы показать итоговые avg/max
        if self.adapterList.currentItem():
             adapter_name = self.adapterList.currentItem().text()
             info = NetworkMonitoring.get_adapter_info_by_name(adapter_name)
             self.update_adapter_info_table(info)

    def on_measure_timer_finished(self):
        """Слот, вызываемый по истечении времени замера"""
        if NetworkMonitoring._is_measuring:
            self.stop_measurement_and_update_ui()

    def on_clear_graphs_clicked(self):
        """Очищает данные графика"""
        self.time_points = []
        self.download_speeds = []
        self.upload_speeds = []
        self.download_plot.setData([], [])
        self.upload_plot.setData([], [])
        # Сбрасываем автоматическое масштабирование
        self.graphWidget.enableAutoRange()

    def update_adapter_info_table(self, info):
        # Настраиваем таблицу на 2 столбца
        self.infoTable.setColumnCount(2)
        self.infoTable.setHorizontalHeaderLabels(['Параметр', 'Значение'])

        # Список параметров и их значений
        parameters = [
            ('ID адаптера', info.get('id', '')),
            ('Описание', info.get('description', '')),
            ('Тип интерфейса', info.get('interface_type', '')),
            ('IP адрес', info.get('ip', '')),
            ('MAC адрес', info.get('mac', '')),
            ('Скорость адаптера', f"{info.get('speed', '0')} Мбит/с"),
            ('MTU', str(info.get('mtu', ''))),
            ('Статус', info.get('status', '')),
            ('Время замера', info.get('measurement_time', '')),
            ('Загрузка - текущая', f"{info.get('current_download', '0')} Мбит/с"),
            ('Загрузка - максимальная', f"{info.get('max_download', '0')} Мбит/с"),
            ('Загрузка - средняя', f"{info.get('avg_download', '0')} Мбит/с"),
            ('Отдача - текущая', f"{info.get('current_upload', '0')} Мбит/с"),
            ('Отдача - максимальная', f"{info.get('max_upload', '0')} Мбит/с"),
            ('Отдача - средняя', f"{info.get('avg_upload', '0')} Мбит/с")
        ]

        # Устанавливаем количество строк
        self.infoTable.setRowCount(len(parameters))

        # Заполняем таблицу
        for row, (param, value) in enumerate(parameters):
            self.infoTable.setItem(row, 0, QTableWidgetItem(param))
            self.infoTable.setItem(row, 1, QTableWidgetItem(str(value)))

        # Подгоняем размер столбцов под содержимое
        self.infoTable.resizeColumnsToContents()

    def execute_ping_trace(self):
            address = self.addressInput.text().strip()
            if not address:
                return
            
            try:
                if self.pingChoice.isChecked():
                    # Выполняем ping
                    if platform.system().lower() == "windows":
                        command = ["ping", "-n", "4", address]
                    else:
                        command = ["ping", "-c", "4", address]
                elif self.tracerChoice.isChecked():
                    # Выполняем tracert/traceroute
                    if platform.system().lower() == "windows":
                        command = ["tracert", address]
                    else:
                        command = ["traceroute", address]

                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    encoding='cp866' if platform.system().lower() == "windows" else 'utf-8'
                )

                # Читаем вывод команды
                output, error = process.communicate()
                
                # Очищаем список перед добавлением новых результатов
                #self.outputList.clear()
                
                # Добавляем результаты в outputList
                for line in output.splitlines():
                    item = QListWidgetItem(line)
                    self.outputList.addItem(item)

                if error:
                    error_item = QListWidgetItem(f"Ошибка: {error}")
                    self.outputList.addItem(error_item)

            except Exception as e:
                error_item = QListWidgetItem(f"Ошибка: {str(e)}")
                self.outputList.addItem(error_item)
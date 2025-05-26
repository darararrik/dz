from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer
import pyqtgraph as pg # Импортируем pyqtgraph
from datetime import datetime

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

        # Для хранения заданной длительности замера
        self._timed_measure_duration = None

    def load_adapters(self):
        adapters = NetworkMonitoring.get_adapters()
        self.adapterList.clear()
        for name in adapters.keys():
            self.adapterList.addItem(name)

    def connect_buttons(self):
        self.measureSpeedButton.clicked.connect(self.on_measure_speed_clicked)
        self.adapterList.itemClicked.connect(self.on_adapter_selected)
        self.clearGraphs.clicked.connect(self.on_clear_graphs_clicked)

    def update_current_adapter(self):
        if self.adapterList.currentItem():
            adapter_name = self.adapterList.currentItem().text()
            # Получаем информацию об адаптере из NetworkMonitoring
            info = NetworkMonitoring.get_adapter_info_by_name(adapter_name)

            elapsed_time = 0
            # Обновляем график и рассчитываем прошедшее время только при активном измерении
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
            else:\
                # Если замер не идет, сбрасываем время и графики (если нужно)
                self.time_points = []
                self.download_speeds = []
                self.upload_speeds = []
                self.download_plot.setData([], [])
                self.upload_plot.setData([], [])
                # Сбрасываем автоматическое масштабирование
                self.graphWidget.enableAutoRange()


            # Передаем прошедшее время в секундах для обновления таблицы
            self.update_adapter_info_table(info, elapsed_time)

    def on_adapter_selected(self, item):
        adapter_name = item.text()
        info = NetworkMonitoring.get_adapter_info_by_name(adapter_name)
        # При выборе адаптера, замер не идет, поэтому прошедшее время 0
        self.update_adapter_info_table(info, 0)

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

            # Сохраняем заданную длительность для использования в on_measure_timer_finished
            self._timed_measure_duration = measure_duration

            NetworkMonitoring.start_measuring()

            # Очищаем данные графика и добавляем начальную точку (0,0)
            self.time_points = [0]
            self.download_speeds = [0]
            self.upload_speeds = [0]
            self.download_plot.setData(self.time_points, self.download_speeds)
            self.upload_plot.setData(self.time_points, self.upload_speeds)
            # Сбрасываем масштабирование графика
            self.graphWidget.enableAutoRange()


            self.measureSpeedButton.setText("Остановить замер")
            self.update_timer.start()

            # Если задана длительность замера, запускаем одноразовый таймер для остановки
            if measure_duration is not None:
                QTimer.singleShot(measure_duration * 1000, self.on_measure_timer_finished)

        else:
            # Если замер идет, останавливаем его вручную
            # Сбрасываем сохраненную длительность
            self._timed_measure_duration = None
            self.stop_measurement_and_update_ui()

    def stop_measurement_and_update_ui(self):
        """Останавливает замер и обновляет UI"""
        NetworkMonitoring.stop_measuring()
        self.measureSpeedButton.setText("Начать замер")
        self.update_timer.stop()
        # При ручной остановке обновляем таблицу с прошедшим временем (которое NetworkMonitoring вернет как 0, но avg/max будут последними)
        # Время в таблице будет 00:00:00, так как замер остановлен.
        if self.adapterList.currentItem():
             adapter_name = self.adapterList.currentItem().text()
             info = NetworkMonitoring.get_adapter_info_by_name(adapter_name)
             self.update_adapter_info_table(info, 0)

    def on_measure_timer_finished(self):
        """Слот, вызываемый по истечении времени замера"""
        if NetworkMonitoring._is_measuring:
            # Получаем последние данные адаптера ДО остановки замера
            if self.adapterList.currentItem():
                adapter_name = self.adapterList.currentItem().text()
                info = NetworkMonitoring.get_adapter_info_by_name(adapter_name)

                # Добавляем финальную точку на график с точным временем завершения
                if self._timed_measure_duration is not None:
                    final_time = self._timed_measure_duration
                    current_download = info.get('current_download', 0)
                    current_upload = info.get('current_upload', 0)

                    # Проверяем, чтобы не добавлять дублирующую точку, если таймер сработал точно в конце секунды
                    if not self.time_points or self.time_points[-1] < final_time:
                        self.time_points.append(final_time)
                        self.download_speeds.append(current_download)
                        self.upload_speeds.append(current_upload)

                    self.download_plot.setData(self.time_points, self.download_speeds)
                    self.upload_plot.setData(self.time_points, self.upload_speeds)

                    # Обновляем таблицу с заданной длительностью
                    self.update_adapter_info_table(info, final_time)
                else:\
                    # Если длительность почему-то не сохранилась, просто обновляем как при ручной остановке
                     self.update_adapter_info_table(info, 0)

            # Останавливаем замер и обновляем UI (кнопка и таймер)
            # Сбрасываем сохраненную длительность
            self._timed_measure_duration = None
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
        # Сбрасываем сохраненную длительность
        self._timed_measure_duration = None

    def update_adapter_info_table(self, info, elapsed_time_seconds):
        # Настраиваем таблицу на 2 столбца
        self.infoTable.setColumnCount(2)
        self.infoTable.setHorizontalHeaderLabels(['Параметр', 'Значение'])

        # Форматируем прошедшее время в ЧЧ:ММ:СС
        # Если замер идет ИЛИ если это финальное обновление после таймера (elapsed_time_seconds > 0)
        if NetworkMonitoring._is_measuring or elapsed_time_seconds > 0:
            hours = int(elapsed_time_seconds // 3600)
            minutes = int((elapsed_time_seconds % 3600) // 60)
            seconds = int(elapsed_time_seconds % 60)
            measurement_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            measurement_time_str = '00:00:00'

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
            ('Время замера', measurement_time_str), # Используем отформатированное время
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


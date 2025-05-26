import pyqtgraph as pg
from PyQt6.QtCore import Qt
class Graph:
    def __init__(self, graph_widget):
        self.graph_widget = graph_widget
        self._init_graph_settings()
        self._init_data_structures()
        self._init_plots()

    def _init_graph_settings(self):
        """Инициализация настроек графика"""
        self.graph_widget.setBackground('w')
        self.graph_widget.setTitle("График скорости", color="black", size="16pt")
        styles = {'color': '#000', 'font-size': '12pt', 'bold': True} 
        self.graph_widget.setLabel('left', 'Скорость (Мбит/с)', **styles)
        self.graph_widget.setLabel('bottom', 'Время (сек)', **styles)
        self.graph_widget.showGrid(x=True, y=True)

    def _init_data_structures(self):
        """Инициализация структур данных для хранения точек графика"""
        self.time_points = []
        self.download_speeds = []
        self.upload_speeds = []

    def _init_plots(self):
        """Инициализация линий графика"""
        self.download_plot = self.graph_widget.plot(
            self.time_points, 
            self.download_speeds, 
            pen=pg.mkPen(color='b', width=2), 
            name='Загрузка'
        )
        self.upload_plot = self.graph_widget.plot(
            self.time_points, 
            self.upload_speeds, 
            pen=pg.mkPen(color='r', width=2), 
            name='Отдача'
        )

    def update_data(self, time_point, download_speed, upload_speed, max_points=100):
        """Обновление данных графика"""
        self.time_points.append(time_point)
        self.download_speeds.append(download_speed)
        self.upload_speeds.append(upload_speed)

        # Ограничиваем количество точек для производительности
        if len(self.time_points) > max_points:
            self.time_points = self.time_points[-max_points:]
            self.download_speeds = self.download_speeds[-max_points:]
            self.upload_speeds = self.upload_speeds[-max_points:]

        self._update_plots()

    def _update_plots(self):
        """Обновление отображения графиков"""
        self.download_plot.setData(self.time_points, self.download_speeds)
        self.upload_plot.setData(self.time_points, self.upload_speeds)
        
        # Автоматическое масштабирование по Y
        self.graph_widget.enableAutoRange(axis='y', enable=True)
        
        # Фиксированный диапазон по X
        if self.time_points:
            self.graph_widget.setXRange(self.time_points[0], self.time_points[-1])

    def clear(self):
        """Очистка данных графика"""
        self.time_points = []
        self.download_speeds = []
        self.upload_speeds = []
        self.download_plot.setData([], [])
        self.upload_plot.setData([], [])
        self.graph_widget.enableAutoRange()
    
    def toggle_download(self, state):
        """Включение/выключение отображения линии загрузки"""
        self.download_plot.setVisible(state != Qt.CheckState.Checked.value)

    def toggle_upload(self, state):
        """Включение/выключение отображения линии отдачи"""
        self.upload_plot.setVisible(state != Qt.CheckState.Checked.value)

from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer

from adapter_managment import AdapterManagement

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

    def load_adapters(self):
        adapters = AdapterManagement.get_adapters()
        self.adapterList.clear()
        for name in adapters.keys():
            self.adapterList.addItem(name)

    def connect_buttons(self):
        self.adapterList.itemClicked.connect(self.on_adapter_selected)

    def update_current_adapter(self):
        if self.adapterList.currentItem():
            self.on_adapter_selected(self.adapterList.currentItem())

    def on_adapter_selected(self, item):
        adapter_name = item.text()
        info = AdapterManagement.get_adapter_info_by_name(adapter_name)
        self.update_adapter_info_table(info)

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


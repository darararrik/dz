from PyQt6.QtWidgets import QTableWidgetItem

class AdapterInfoTable:
    def __init__(self, table_widget):
        self.table = table_widget
        self._init_table()

    def _init_table(self):
        """Инициализация таблицы"""
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Параметр', 'Значение'])

    def update_info(self, info, elapsed_time_seconds, is_measuring):
        """Обновление информации в таблице"""
        # Форматируем время замера
        if is_measuring or elapsed_time_seconds > 0:
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
            ('Время замера', measurement_time_str),
            ('Загрузка - текущая', f"{info.get('current_download', '0')} Мбит/с"),
            ('Загрузка - максимальная', f"{info.get('max_download', '0')} Мбит/с"),
            ('Загрузка - средняя', f"{info.get('avg_download', '0')} Мбит/с"),
            ('Отдача - текущая', f"{info.get('current_upload', '0')} Мбит/с"),
            ('Отдача - максимальная', f"{info.get('max_upload', '0')} Мбит/с"),
            ('Отдача - средняя', f"{info.get('avg_upload', '0')} Мбит/с")
        ]

        # Устанавливаем количество строк
        self.table.setRowCount(len(parameters))

        # Заполняем таблицу
        for row, (param, value) in enumerate(parameters):
            self.table.setItem(row, 0, QTableWidgetItem(param))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))

        # Подгоняем размер столбцов под содержимое
        self.table.resizeColumnsToContents() 
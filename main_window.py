from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from PyQt6 import uic

from adapter_managment import AdapterManagement

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self) 
        self.load_adapters()
        self.connect_buttons()

    def load_adapters(self):
        adapters = AdapterManagement.get_adapters()
        self.adapterListWidget.clear()
        for name in adapters.keys():
            self.adapterListWidget.addItem(name)
        print(AdapterManagement.get_adapters_info())

    def connect_buttons(self):
        self.adapterListWidget.itemClicked.connect(self.on_adapter_selected)
    
    def update_adapter_info_table(self, info):
        self.adapterInfoTable.setRowCount(0)  # Очищаем таблицу
        row = 0
        # Добавляем каждый параметр адаптера в таблицу
        for key, value in info.items():
            self.adapterInfoTable.insertRow(row)
            self.adapterInfoTable.setItem(row, 0, QTableWidgetItem(str(key)))
            self.adapterInfoTable.setItem(row, 1, QTableWidgetItem(str(value)))
            row += 1

    def on_adapter_selected(self, item):
        adapter_name = item.text()
        info = AdapterManagement.get_adapter_info_by_name(adapter_name)
        self.update_adapter_info_table(info)


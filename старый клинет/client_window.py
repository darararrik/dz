import os
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt
from .network_client import NetworkClient
import time

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем UI
        ui_file = os.path.join(os.path.dirname(__file__), "client_window.ui")
        uic.loadUi(ui_file, self)

        # Создаем клиент
        self.client = NetworkClient()
        
        # Подключаем сигналы клиента
        self.client.connected.connect(self.on_connected)
        self.client.disconnected.connect(self.on_disconnected)
        self.client.error.connect(self.on_error)
        self.client.log_message.connect(self.update_log)
        self.client.speeds_received.connect(self.update_speeds)
        
        # Подключаем сигналы UI
        self.connectButton.clicked.connect(self.toggle_connection)
        
        # Инициализация UI
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка начального состояния UI"""
        # Устанавливаем начальный статус
        self.statusLabel.setText("Статус: Не подключен")
        
    def toggle_connection(self):
        """Подключение/отключение от сервера"""
        if not self.client.is_connected:
            # Подключаемся
            ip = self.serverIPInput.text()
            try:
                port = int(self.serverPortInput.text())
            except ValueError:
                self.update_log("Ошибка: некорректный порт")
                return
                
            self.client.connect_to_server(ip, port)
        else:
            # Отключаемся
            self.client.disconnect()
            
    def on_connected(self):
        """Обработка успешного подключения"""
        self.connectButton.setText("Отключиться")
        self.statusLabel.setText("Статус: Подключен")
        self.serverIPInput.setEnabled(False)
        self.serverPortInput.setEnabled(False)
        
    def on_disconnected(self):
        """Обработка отключения"""
        self.connectButton.setText("Подключиться")
        self.statusLabel.setText("Статус: Не подключен")
        self.serverIPInput.setEnabled(True)
        self.serverPortInput.setEnabled(True)
        
    def on_error(self, error_msg):
        """Обработка ошибок"""
        self.update_log(f"Ошибка: {error_msg}")
        
    def update_log(self, message):
        """Обновление лога"""
        # Добавляем временную метку
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logWidget.append(f"[{timestamp}] {message}")
        
    def update_speeds(self, speeds):
        """Обновление информации о скорости"""
        # Этот метод теперь должен быть пуст или удален, т.к. таблицы нет
        pass # Просто ничего не делаем

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.client.is_connected:
            self.client.disconnect()
        event.accept() 

    def on_adapter_selected(self, item):
        """Обработка выбора адаптера из списка"""
        # ... (проверки selected_client и item) ...

        adapter = item.text()
        self.selected_adapter = adapter
        # self.log_message(f"Выбран адаптер: {self.selected_adapter}")

        # Запрашиваем информацию об адаптере
        # ... (код запроса) ...

        # Восстанавливаем сохраненные данные для этого клиента и адаптера
        self.restore_client_data() # <--- ВОЗМОЖНЫЙ ИСТОЧНИК ПРОБЛЕМЫ

        # Проверяем, идут ли данные для этого адаптера
        client_key = f"{self.selected_client}:{self.selected_adapter}"
        # Эта проверка определяет, был ли мониторинг уже запущен ДЛЯ ЭТОГО адаптера РАНЬШЕ
        is_receiving_data = client_key in self.clients_data and len(self.clients_data[client_key]['download_speeds']) > 0
        self.is_monitoring = is_receiving_data # <-- Флаг is_monitoring меняется ЗДЕСЬ

        # Включаем кнопку замера скорости и устанавливаем правильный текст
        if hasattr(self.window, "remoteMeasureSpeedButton"):
            self.window.remoteMeasureSpeedButton.setEnabled(True) # <-- Кнопка включается
            # НО текст меняется в зависимости от ВОССТАНОВЛЕННОГО состояния
            self.window.remoteMeasureSpeedButton.setText("Остановить замер" if is_receiving_data else "Начать замер") 
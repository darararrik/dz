import subprocess
import platform
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtCore import Qt

def setup_ping_tab(ui):
    """
    Настройка функционала вкладки ping
    """
    def execute_ping_trace():
        address = ui.addressInput.text().strip()
        if not address:
            return

        # Очищаем предыдущий вывод
        ui.outputList.clear()
        
        try:
            if ui.pingSwitch.isChecked():
                # Выполняем ping
                if platform.system().lower() == "windows":
                    command = ["ping", "-n", "4", address]
                else:
                    command = ["ping", "-c", "4", address]
            else:
                # Выполняем tracert/traceroute
                if platform.system().lower() == "windows":
                    command = ["tracert", address]
                else:
                    command = ["traceroute", address]

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Читаем вывод команды
            output, error = process.communicate()
            
            # Добавляем результаты в outputList
            for line in output.splitlines():
                item = QListWidgetItem(line)
                ui.outputList.addItem(item)

            # Если команда выполнилась успешно, добавляем адрес в список клиентов
            if process.returncode == 0:
                # Проверяем, нет ли уже такого адреса в списке
                items = [ui.pingClientList.item(i).text() for i in range(ui.pingClientList.count())]
                if address not in items:
                    item = QListWidgetItem(address)
                    ui.pingClientList.addItem(item)

        except Exception as e:
            error_item = QListWidgetItem(f"Ошибка: {str(e)}")
            ui.outputList.addItem(error_item)

    # Подключаем обработчик нажатия кнопки
    ui.pingButton.clicked.connect(execute_ping_trace)

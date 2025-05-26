import platform
import subprocess
from PyQt6.QtWidgets import QListWidgetItem
from database import Database

class PingTracerTool:
    def __init__(self, main_window):
        self.main_window = main_window


    def execute_ping_trace(self):
        try:
            if self.main_window.pingChoice.isChecked():
                # Выполняем ping
                if platform.system().lower() == "windows":
                    command = ["ping", "-n", "4", self.main_window.addressInput.text().strip()]
                else:
                    command = ["ping", "-c", "4", self.main_window.addressInput.text().strip()]
            elif self.main_window.tracerChoice.isChecked():
                # Выполняем tracert/traceroute
                if platform.system().lower() == "windows":
                    command = ["tracert", self.main_window.addressInput.text().strip()]
                else:
                    command = ["traceroute", self.main_window.addressInput.text().strip()]

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                encoding='cp866' if platform.system().lower() == "windows" else 'utf-8'
            )

            # Читаем вывод команды
            output, error = process.communicate()
            
            # Сохраняем результат в базу данных
            if self.main_window.pingChoice.isChecked():
                self.main_window.db.save_ping(self.main_window.addressInput.text().strip(), output)
            else:
                self.main_window.db.save_trace(self.main_window.addressInput.text().strip(), output)
            
            # Очищаем список перед добавлением новых результатов
            self.main_window.outputList.clear()
            
            # Добавляем результаты в outputList
            for line in output.splitlines():
                item = QListWidgetItem(line)
                self.main_window.outputList.addItem(item)

            if error:
                error_item = QListWidgetItem(f"Ошибка: {error}")
                self.main_window.outputList.addItem(error_item)

        except Exception as e:
            error_item = QListWidgetItem(f"Ошибка: {str(e)}")
            self.main_window.outputList.addItem(error_item)
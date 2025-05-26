
import platform
import subprocess
from PyQt6.QtWidgets import QListWidgetItem

class PingTool():
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
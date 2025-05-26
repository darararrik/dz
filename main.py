import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Устанавливаем иконку приложения
    app_icon = QIcon("icons/icon.png")
    app.setWindowIcon(app_icon)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
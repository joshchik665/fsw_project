from PySide6.QtWidgets import QApplication, QDialog
from ui.main_window import MainWindow
from ui.connect_dialog import IpEntryDialog
import sys

def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()

def main():
    app = QApplication(sys.argv)
    
    # Load and set stylesheet
    stylesheet = load_stylesheet("styles/style.qss")
    app.setStyleSheet(stylesheet)
    
    ip_dialog = IpEntryDialog()
    if ip_dialog.exec() == QDialog.Accepted:
        config = ip_dialog.config
        window = MainWindow(config)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit()


if __name__ == "__main__":
    main()
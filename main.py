from PySide6.QtWidgets import QApplication, QDialog
from ui.common_gui.main_window import MainWindow
from ui.common_gui.connect_dialog import IpEntryDialog
import sys

def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()

def main():
    app = QApplication(sys.argv)
    
    # Load and set stylesheet
    stylesheet = load_stylesheet(r"styles\style.qss")
    app.setStyleSheet(stylesheet)
    
    ip_dialog = IpEntryDialog()
    if ip_dialog.exec() == QDialog.Accepted:
        config = ip_dialog.config
        visa_timeout = ip_dialog.visa_timeout
        opc_timeout = ip_dialog.opc_timeout
        window = MainWindow(config, visa_timeout, opc_timeout)
        window.show()
        sys.exit(window.close(app.exec()))
    else:
        sys.exit()


if __name__ == "__main__":
    main()
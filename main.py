# main.py

from PySide6.QtWidgets import QApplication, QDialog

from ui.common_gui.main_window import MainWindow
from ui.common_gui.connect_dialog import IpEntryDialog
from pathlib import Path
import sys


def load_stylesheet(filename: Path):
    with filename.open("r") as file:
        return file.read()


def main():
    app = QApplication(sys.argv)
    
    # Load and set stylesheet
    stylesheet_path = Path(r"styles\style.qss")
    stylesheet = load_stylesheet(stylesheet_path)
    app.setStyleSheet(stylesheet)
    
    # Creates the IP entry dialog
    ip_dialog = IpEntryDialog()
    if ip_dialog.exec() == QDialog.Accepted: # When the dialog is closed
        
        config = ip_dialog.config # Gets the config out from the IP dialog
        
        # Creates the main window
        window = MainWindow(config)
        window.show()
        
        sys.exit(window.close(app.exec())) # When the main window closes, exit the app
    else:
        sys.exit()


if __name__ == "__main__":
    main()


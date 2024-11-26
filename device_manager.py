# device_manager.py

from PySide6.QtWidgets import (
    QApplication, 
    QDialog
)
import sys

from device_wizard.dialogs import EntryDialog, CreateDialog, EditDialog
from device_wizard.main_window import MainWindow

def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()

app = QApplication(sys.argv)
stylesheet = load_stylesheet("styles/style.qss")
app.setStyleSheet(stylesheet)

dialog = EntryDialog()
if dialog.exec() == QDialog.Accepted:
    if dialog.choice == "edit":
        next_dialog = EditDialog()
    elif dialog.choice == "create":
        next_dialog = CreateDialog()
    
    if next_dialog.exec() == QDialog.Accepted:
        config_filepath = next_dialog.filepath
    else:
        sys.exit()
    
    if config_filepath:
        window = MainWindow(config_filepath)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit()
else:
    sys.exit()

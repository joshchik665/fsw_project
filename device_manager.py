
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QLineEdit, 
    QLabel, 
    QDialog,
    QButtonGroup,
    QRadioButton,
    QFileDialog
)
from PySide6.QtGui import QIcon
import os
import sys
import json
from pathlib import Path


def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        self.edit_device_button = QPushButton("Edit existing device config")
        self.edit_device_button.pressed.connect(self.edit_device)
        layout.addWidget(self.edit_device_button)
        
        self.create_device_button = QPushButton("Create new device")
        self.create_device_button.pressed.connect(self.create_device)
        layout.addWidget(self.create_device_button)
    
    
    def edit_device(self):
        self.choice = "edit"
        self.accept()
    
    
    def create_device(self):
        self.choice = "Create"
        self.accept()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        with open(r"device_manager_config\\config.json", "r") as file:
            self.device_configs_filepaths = json.load(file)
        
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        
        for key in self.device_configs_filepaths.keys():
            radio_btn = QRadioButton(str(key))
            radio_btn.setChecked(True)
            self.button_group.addButton(radio_btn)
            layout.addWidget(radio_btn)
        
        self.button = QPushButton("Open selected")
        self.button.pressed.connect(self.on_confirm)
        layout.addWidget(self.button)
    
    
    def on_confirm(self):
        selected_button = self.button_group.checkedButton()
        
        if selected_button:
            device = selected_button.text()
            self.filepath = self.device_configs_filepaths[device]
        else:
            self.filepath = ""
        
        self.accept()


class CreateDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        title = QLabel("Enter name of instrument to create: ")
        layout.addWidget(title)
        
        self.name_entry = QLineEdit()
        layout.addWidget(self.name_entry)
        
        self.button = QPushButton("Create new device")
        self.button.pressed.connect(self.select_or_create_folder)
        layout.addWidget(self.button)
    
    
    def select_or_create_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Select or Create Folder", 
            str(Path.home() / "fsw_project" / "configs"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder_path:
            default_json_path = os.path.join(folder_path, "default.json")
            
            default_data = {
                "Device Name": self.name_entry.text()
            }
            
            with open(default_json_path, 'w') as json_file:
                json.dump(default_data, json_file, indent=4)
        
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self, filepath):
        super().__init__()


app = QApplication(sys.argv)
stylesheet = load_stylesheet("styles/style.qss")
app.setStyleSheet(stylesheet)

dialog = Dialog()
if dialog.exec() == QDialog.Accepted:
    if dialog.choice == "edit":
        next_dialog = EditDialog()
    elif dialog.choice == "create":
        next_dialog = CreateDialog()
    
    if next_dialog.exec() == QDialog.Accepted:
        config_filepath = next_dialog.filepath
    
    if config_filepath:
        window = MainWindow(config_filepath)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit()
else:
    sys.exit()

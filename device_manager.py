
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QGridLayout,
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
from pyvisa import ResourceManager


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
        self.choice = "create"
        self.accept()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        with open(r"configs\device_configs\device_types\configs.json", "r") as file:
            self.device_configs = json.load(file)
        
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        
        for key in self.device_configs["Device Default Configs"].keys():
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
            self.filepath = self.device_configs["Device Default Configs"][device]
        else:
            self.filepath = ""
        
        self.accept()


class CreateDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel("Enter name of instrument to create: ")
        layout.addWidget(title)
        
        self.name_entry = QLineEdit()
        layout.addWidget(self.name_entry)
        
        idn_label = QLabel("Enter the IDN from the instrument, if you don't know the IDN, use the search IDN box: ")
        layout.addWidget(idn_label)
        
        self.idn_entry = QLineEdit()
        layout.addWidget(self.idn_entry)
        
        
        ip_layout = QHBoxLayout()
        
        ip_label = QLabel("Enter an IP address to query the IDN of that device, (IP is not recoreded) (Optional, only for getting the IDN): ")
        layout.addWidget(ip_label)
        
        self.ip_entry = QLineEdit()
        ip_layout.addWidget(self.ip_entry)
        
        self.ip_button = QPushButton("Query IDN")
        self.ip_button.pressed.connect(self.query_idn)
        ip_layout.addWidget(self.ip_button)
        
        layout.addLayout(ip_layout)
        
        
        self.mode_edit = DictEdit("Device Modes: ", {"Mode name": "[SCPI command to set this mode]"})
        layout.addWidget(self.mode_edit)
        
        self.button = QPushButton("Create new device")
        self.button.pressed.connect(self.select_or_create_folder)
        layout.addWidget(self.button)
    
    
    def query_idn(self):
        rm = ResourceManager("@py")
        try:
            instr = rm.open_resource(f"TCPIP::{self.ip_entry.text()}::INSTR")
            
            idn = instr.query('*IDN?')
            self.idn_entry.setText(idn)
        except Exception as ex:
            print(f'Error querying the instrument session:\n{ex.args[0]}') # Error
    
    
    def select_or_create_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Select or Create Folder", 
            str(Path.home() / "fsw_project" / "configs" / "device_configs" / "settings"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder_path:
            default_json_path = os.path.join(folder_path, "default.json")
            
            with open(r"configs\device_configs\device_types\configs.json", "r") as file:
                device_types = json.load(file)
            
            device_types["Device IDNs"][self.idn_entry.text()] = self.name_entry.text()
            
            device_types["Device Default Configs"][self.name_entry.text()] = default_json_path
            
            with open(r"configs\device_configs\device_types\configs.json", "w") as file:
                json.dump(device_types, file, indent=4)
            
            default_data = {
                "Device Name": self.name_entry.text(),
                "Default Mode": "",
                "Modes SCPI Commands": self.mode_edit.get_value(),
                "Settings": {}
            }
            
            with open(default_json_path, 'w') as json_file:
                json.dump(default_data, json_file, indent=4)
        
        self.filepath = default_json_path
        
        self.accept()


class DictEdit(QWidget):
    def __init__(self, name:str, dictionary:dict):
        super().__init__()
        
        self.widget_layout = QVBoxLayout()
        
        self.dictionary = dictionary
        
        self.key_widgets = {}
        self.value_widgets = {}
        self.layouts = {}
        self.delete_buttons = {}
        
        layout1 = QHBoxLayout()
        
        self.name_label = QLabel(name)
        layout1.addWidget(self.name_label)
        
        layout1.addStretch(1)
        
        self.add_button = QPushButton("Add entry")
        self.add_button.pressed.connect(self.add_entry)
        layout1.addWidget(self.add_button)
        
        self.widget_layout.addLayout(layout1)
        
        for key, value in self.dictionary.items():
            layout = QHBoxLayout()
            self.layouts[key] = layout
            
            key_widget = QLineEdit()
            key_widget.setText(key)
            self.key_widgets[key] = key_widget
            layout.addWidget(key_widget)
            
            value_widget = QLineEdit()
            value_widget.setText(value)
            self.value_widgets[key] = value_widget
            layout.addWidget(value_widget)
            
            button = QPushButton("Delete")
            self.delete_buttons[key] = button
            button.setObjectName("delete-button")
            button.pressed.connect(lambda: self.delete(key))
            layout.addWidget(button)
            
            self.widget_layout.addLayout(layout)
        
        self.setLayout(self.widget_layout)
    
    
    def add_entry(self):
        layout = QHBoxLayout()
        
        key_widget = QLineEdit()
        layout.addWidget(key_widget)
        
        value_widget = QLineEdit()
        layout.addWidget(value_widget)
        
        button = QPushButton(" Add ")
        button.pressed.connect(lambda: self.add(layout, key_widget, value_widget, button))
        layout.addWidget(button)
        
        self.widget_layout.addLayout(layout)

    
    def add(self, layout, key_widget, value_widget, button):
        key = key_widget.text()
        self.layouts[key] = layout
        self.key_widgets[key] = key_widget
        self.value_widgets[key] = value_widget
        
        button.setObjectName("delete-button")
        button.style().polish(button)
        self.delete_buttons[key] = button
        self.delete_buttons[key].setText("Delete")
        button.pressed.connect(lambda: self.delete(key))
    
    
    def delete(self, key:str):
        self.key_widgets[key].deleteLater()
        self.value_widgets[key].deleteLater()
        self.delete_buttons[key].deleteLater()
        self.widget_layout.removeItem(self.layouts[key])
        
        self.key_widgets.pop(key)
        self.value_widgets.pop(key)
        self.delete_buttons.pop(key)
        self.layouts.pop(key)
    
    
    def get_value(self):
        dict = {}
        for key in self.key_widgets.keys():
            dict[self.key_widgets[key].text()] = self.value_widgets[key].text()
        return dict


class SettingEdit(QWidget):
    def __init__(self, name:str, value:str, requried:bool):
        super().__init__()
        
        self.name = name
        self.required = requried
        
        layout = QHBoxLayout()
        
        label = QLabel(name)
        label.setFixedSize(200, 25)
        layout.addWidget(label)
        
        self.entry = QLineEdit()
        self.entry.setFixedSize(500, 25)
        if self.required:
            self.entry.textEdited.connect(self.set_status)
        self.entry.setText(value)
        layout.addWidget(self.entry)
        
        self.setLayout(layout)
        
        self.set_status()
    
    
    def set_status(self):
        if not self.entry.text():
            self.entry.setStyleSheet("QLineEdit {border-radius: 5px; padding: 5px; border: 1px solid #8f8f91; background-color: #FDACB8;}")
        else:
            self.entry.setStyleSheet("QLineEdit {border-radius: 5px; padding: 5px; border: 1px solid #8f8f91; background-color: white;}")
    
    
    def get_value(self):
        text = self.entry.text()
        if self.required and not text:
            print(f"Setting: {self.name} is required!")
        return text


class MainWindow(QMainWindow):
    def __init__(self, filepath):
        super().__init__()
        
        self.filepath = filepath
        
        with open(filepath, "r") as file:
            self.config = json.load(file)
        
        self.window_layout = QGridLayout()
        
        self.info_layout = QVBoxLayout()
        self.window_layout.addLayout(self.info_layout, 0, 0)
        
        self.settings_layout = QVBoxLayout()
        self.window_layout.addLayout(self.settings_layout, 0, 1)
        
        self._set_info_layout()
        self._set_setting_layout()
        
        container = QWidget()
        container.setLayout(self.window_layout)
        self.setCentralWidget(container)
    
    
    def _create_place_info_setting(self, name:str, parent_layout):
        layout = QHBoxLayout()
        
        label = QLabel(name)
        label.setFixedSize(200, 25)
        layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setFixedSize(500, 25)
        self.info_widgets[name] = entry
        entry.setText(str(self.config[name]))
        layout.addWidget(entry)
        
        parent_layout.addLayout(layout)
    
    
    def _set_info_layout(self):
        self.info_widgets = {}
        
        self.info_widgets["Device Name"] = SettingEdit("Device Name", self.config["Device Name"], True)
        self.info_layout.addWidget(self.info_widgets["Device Name"])
        
        self.info_widgets["Default Mode"] = SettingEdit("Default Mode", self.config["Default Mode"], True)
        self.info_layout.addWidget(self.info_widgets["Default Mode"])
        
        self.info_widgets["Modes SCPI Commands"] = DictEdit("Device Modes and SCPI Commands", self.config["Modes SCPI Commands"])
        self.info_layout.addWidget(self.info_widgets["Modes SCPI Commands"])
        
        self.apply_info_button = QPushButton("Apply Info Settings")
        self.apply_info_button.pressed.connect(self.apply_info)
        self.info_layout.addWidget(self.apply_info_button)
        
        self.info_layout.addStretch(1)
    
    
    def apply_info(self):
        for key, value in self.info_widgets.items():
            self.config[key] = value.get_value()
            
        with open(self.filepath, "w") as file:
            json.dump(self.config, file, indent=4)
    
    
    def _create_place_setting_box(self, name, parent_layout):
        layout = QHBoxLayout()
        
        label = QLabel(name)
        self.label_widgets[name] = label
        label.setFixedSize(200, 25)
        layout.addWidget(label)
        
        button = QPushButton("Edit")
        self.entry_widgets[name] = button
        button.pressed.connect(lambda: self.edit_setting(name))
        layout.addWidget(button)
        
        self.layouts[name] = layout
        
        parent_layout.addLayout(layout)
        
    
    def _set_setting_layout(self):
        self.layouts = {}
        self.label_widgets = {}
        self.entry_widgets = {}
        
        for setting_name in self.config["Settings"].keys():
            self._create_place_setting_box(setting_name, self.settings_layout)
        
        self.settings_layout.addStretch(1)
    
    
    def edit_setting(self, name):
        print(f"Editing: {name}")
        
        dialog = EditSettingDialog(name, self.config)
        
        if dialog.exec() == QDialog.Accepted:
            self.config = dialog.config
            
            with open(self.filepath, 'w') as file:
                json.dump(self.config, file, indent=4)
            
            if dialog.deleted:
                self.label_widgets[name].deleteLater()
                self.entry_widgets[name].deleteLater()
                self.settings_layout.removeItem(self.layouts[name])


class EditSettingDialog(QDialog):
    def __init__(self, setting_name:str, config:dict):
        super().__init__()
        
        self.setting_name = setting_name
        self.config = config
        
        self.entry_boxes = {}
        
        layout = QVBoxLayout()
        
        for setting_param in self.config["Settings"][self.setting_name].keys():
            self._create_place_info_setting(setting_param, layout)
        
        self.apply_button = QPushButton("Apply Settings")
        self.apply_button.pressed.connect(self.apply)
        layout.addWidget(self.apply_button)
        
        self.cancel_button = QPushButton("Cancel Edit")
        self.cancel_button.pressed.connect(self.cancel)
        layout.addWidget(self.cancel_button)
        
        self.delete_button = QPushButton("Delete Setting")
        self.delete_button.pressed.connect(self.delete)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)
    
    
    def delete(self):
        self.config["Settings"].pop(self.setting_name)
        
        self.deleted = True
        
        self.accept()
    
    
    def cancel(self):
        
        self.deleted = False
        
        self.accept()
    
    def apply(self):
        for setting_atr, entry in self.entry_boxes.items():
            self.config["Settings"][self.setting_name][setting_atr] = entry.text()
        
        self.deleted = False
        
        self.accept()
    
    
    def _create_place_info_setting(self, name:str, parent_layout):
        layout = QHBoxLayout()
        
        label = QLabel(name)
        label.setFixedSize(125, 25)
        layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setFixedSize(200, 25)
        self.entry_boxes[name] = entry
        entry.setText(str(self.config["Settings"][self.setting_name][name]))
        layout.addWidget(entry)
        
        parent_layout.addLayout(layout)


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

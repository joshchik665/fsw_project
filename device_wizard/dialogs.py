# dialogs.py

from PySide6.QtWidgets import (
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
    QFileDialog,
    QStackedWidget
)
import json
from pathlib import Path
from pyvisa import ResourceManager
import ast

from device_wizard.widgets import DictEdit, SettingEdit, SettingEditCombo, toggleList

class EntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        button_layout = QHBoxLayout()
        
        title = QLabel("Device Config Wizard")
        layout.addWidget(title)
        
        self.edit_device_button = QPushButton("Edit existing device config")
        self.edit_device_button.pressed.connect(self.edit_device)
        button_layout.addWidget(self.edit_device_button)
        
        self.create_device_button = QPushButton("Create new device")
        self.create_device_button.pressed.connect(self.create_device)
        button_layout.addWidget(self.create_device_button)
        
        layout.addLayout(button_layout)
    
    
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
        
        with open(r"device\configs\device_types\configs.json", "r") as file:
            self.device_configs = json.load(file)
        
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        
        for key in self.device_configs.keys():
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
            self.filepath = self.device_configs[device]
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
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, 
            "Create JSON file", 
            str(Path.home() / "fsw_project"  / "device" / "configs" / "settings"), 
            "JSON Files (*.json);;All Files (*)"
            )
        
        if filepath:
            
            with open(r"device\configs\device_types\configs.json", "r") as file:
                device_types = json.load(file)
            
            device_types[self.name_entry.text()] = filepath
            
            with open(r"device\configs\device_types\configs.json", "w") as file:
                json.dump(device_types, file, indent=4)
            
            default_data = {
                "Device Name": self.name_entry.text(),
                "Default Mode": "",
                "Modes SCPI Commands": self.mode_edit.get_value(),
                "IDN": self.idn_entry.text(),
                "Settings": {}
            }
            
            with open(filepath, 'w') as json_file:
                json.dump(default_data, json_file, indent=4)
        
        self.filepath = filepath
        
        self.accept()


class EditSettingDialog(QDialog):
    def __init__(self, setting_name:str = "", config:dict = {}):
        super().__init__()
        
        self.setting_name = setting_name
        self.global_config = config
        self.settings_config = config["Settings"]
        
        self.is_new = not bool(setting_name)
        
        if not self.is_new:
            self.config = self.settings_config[setting_name]
        else:
            self.config = {}
        
        self.mode_widgets = {}
        self.numerical_widgets = {}
        
        self.widget_layout = QGridLayout()
        layout = QVBoxLayout()
        layout1 = QVBoxLayout()
        self.widget_layout.addLayout(layout, 0, 1)
        self.widget_layout.addLayout(layout1, 0, 0)
        
        self.name_widget = SettingEdit("Setting Name", setting_name, True)
        layout.addWidget(self.name_widget)
        
        self.setting_types = {"numerical": 0, "mode": 1, "None": 2}
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_numerical_layout())
        self.stacked_widget.addWidget(self.create_mode_layout())
        self.stacked_widget.addWidget(self.create_none_layout())
        
        if self.exists("setting_type"):
            if self.config["setting_type"] == "numerical":
                setting_type_widget = SettingEditCombo("setting_type", "numerical", True, self.setting_types.keys())
                setting_type_widget.valueChanged.connect(self.create_setting)
                self.create_setting("numerical")
                layout.addWidget(setting_type_widget)
            else:
                setting_type_widget = SettingEditCombo("setting_type", "mode", True, self.setting_types.keys())
                setting_type_widget.valueChanged.connect(self.create_setting)
                self.create_setting("mode")
                layout.addWidget(setting_type_widget)
        else:
            setting_type_widget = SettingEditCombo("setting_type", "None", True, self.setting_types.keys())
            setting_type_widget.valueChanged.connect(self.create_setting)
            self.create_setting("None")
            layout.addWidget(setting_type_widget)
        
        self.mode_widgets["setting_type"] = setting_type_widget
        self.numerical_widgets["setting_type"] = setting_type_widget
        
        layout.addWidget(self.stacked_widget)
        
        layout1.addStretch(1)
        
        self.apply_button = QPushButton("Apply Settings")
        self.apply_button.pressed.connect(self.apply)
        layout1.addWidget(self.apply_button)
        
        self.cancel_button = QPushButton("Cancel Edit")
        self.cancel_button.pressed.connect(self.cancel)
        layout1.addWidget(self.cancel_button)
        
        self.delete_button = QPushButton("Delete Setting")
        self.delete_button.pressed.connect(self.delete)
        layout1.addWidget(self.delete_button)
        
        layout1.addStretch(1)
        
        self.setLayout(self.widget_layout)
    
    
    def create_setting(self, text):
        self.stacked_widget.setCurrentIndex(self.setting_types[text])
    
    
    def create_mode_layout(self):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        
        default_value = SettingEdit("default_value", self.config.get("default_value", ""), True)
        layout.addWidget(default_value)
        self.mode_widgets["default_value"] = default_value
        
        write_commands = DictEdit("write_commands", self.config.get("write_commands", {}))
        layout.addWidget(write_commands)
        self.mode_widgets["write_commands"] = write_commands
        
        query_command = SettingEdit("query_command", self.config.get("query_command", ""), True)
        layout.addWidget(query_command)
        self.mode_widgets["query_command"] = query_command
        
        applicable_modes_label = QLabel("Applicable Modes:")
        layout.addWidget(applicable_modes_label)
        
        applicable_modes = toggleList(self.global_config["Modes SCPI Commands"].keys(), self.config.get("applicable_modes", []))
        layout.addWidget(applicable_modes)
        self.mode_widgets["applicable_modes"] = applicable_modes
        
        alias = DictEdit("alias", self.config.get("alias", {}))
        layout.addWidget(alias)
        self.mode_widgets["alias"] = alias
        
        custom_modes = DictEdit("custom_modes", self.config.get("custom_modes", {}))
        layout.addWidget(custom_modes)
        self.mode_widgets["custom_modes"] = custom_modes
        
        return container
    
    
    def create_numerical_layout(self):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        
        default_value = SettingEdit("default_value", self.config.get("default_value", ""), True)
        layout.addWidget(default_value)
        self.numerical_widgets["default_value"] = default_value
        
        write_command = SettingEdit("write_command", self.config.get("write_command", ""), True)
        layout.addWidget(write_command)
        self.numerical_widgets["write_command"] = write_command
        
        query_command = SettingEdit("query_command", self.config.get("query_command", ""), True)
        layout.addWidget(query_command)
        self.numerical_widgets["query_command"] = query_command
        
        measure = SettingEdit("measure", self.config.get("measure", ""), True)
        layout.addWidget(measure)
        self.numerical_widgets["measure"] = measure
        
        applicable_modes_label = QLabel("Applicable Modes:")
        layout.addWidget(applicable_modes_label)
        
        applicable_modes = toggleList(self.global_config["Modes SCPI Commands"].keys(), self.config.get("applicable_modes", []))
        layout.addWidget(applicable_modes)
        self.numerical_widgets["applicable_modes"] = applicable_modes
        
        return container
    
    
    def create_none_layout(self):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        
        return container
    
    
    def exists(self, key:str) -> bool:
        try:
            value = self.config[key]
            return True
        except KeyError:
            return False
    
    
    def delete(self):
        self.global_config["Settings"].pop(self.setting_name)
        
        self.deleted = True
        
        self.accept()
    
    
    def cancel(self):
        
        self.deleted = False
        
        self.accept()
    
    
    def apply(self):
        current_index = self.stacked_widget.currentIndex()
        
        self.setting_name = self.name_widget.get_value()
        
        if current_index == 0:
            self.config = {name: widget.get_value() for name, widget in self.numerical_widgets.items() if widget.get_value()}
        elif current_index == 1:
            self.config = {name: widget.get_value() for name, widget in self.mode_widgets.items() if widget.get_value() and not name == "custom_modes"}
            
            dict = self.mode_widgets["custom_modes"].get_value()
            
            if dict:
                self.config["custom_modes"] = {}
                for key, text in dict.items():
                    try:
                        string_list = ast.literal_eval(text)
                        if isinstance(string_list, list) and all(isinstance(i, str) for i in string_list):
                            self.config["custom_modes"][key] = string_list
                    except (ValueError, SyntaxError):
                        print(f"Invalid input format. Please enter a valid list of strings.{text}")
        
        self.global_config["Settings"][self.setting_name] = self.config
        
        self.deleted = False
        
        self.accept()



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
    QFileDialog,
    QComboBox,
    QCheckBox,
    QStackedWidget,
    QMessageBox
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
import os
import sys
import json
from pathlib import Path
from pyvisa import ResourceManager
import shutil
import ast


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
        # folder_path = QFileDialog.getExistingDirectory(
        #     self, 
        #     "Select or Create Folder", 
        #     str(Path.home() / "fsw_project" / "configs" / "device_configs" / "settings"),
        #     QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        # )
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, 
            "Create JSON file", 
            str(Path.home() / "fsw_project" / "configs" / "device_configs" / "settings"), 
            "JSON Files (*.json);;All Files (*)"
            )
        
        if filepath:
            
            with open(r"configs\device_configs\device_types\configs.json", "r") as file:
                device_types = json.load(file)
            
            #device_types["Device IDNs"][self.idn_entry.text()] = self.name_entry.text()
            
            device_types[self.name_entry.text()] = filepath
            
            with open(r"configs\device_configs\device_types\configs.json", "w") as file:
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
            value_widget.setText(str(value))
            self.value_widgets[key] = value_widget
            layout.addWidget(value_widget)
            
            button = QPushButton("Delete")
            self.delete_buttons[key] = button
            self.delete_buttons[key].setObjectName("delete-button")
            self.delete_buttons[key].pressed.connect(lambda key=key: self.delete(key))
            layout.addWidget(self.delete_buttons[key])
            
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
        self.delete_buttons[key].pressed.connect(lambda: self.delete(key))
    
    
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


class SettingEditCombo(QWidget):
    
    valueChanged = Signal(str)
    
    def __init__(self, name:str, value:str, requried:bool, values:tuple):
        super().__init__()
        
        self.name = name
        self.values = values
        self.required = requried
        
        layout = QHBoxLayout()
        
        label = QLabel(name)
        label.setFixedSize(200, 25)
        layout.addWidget(label)
        
        self.entry = QComboBox()
        self.entry.setFixedSize(500, 25)
        
        self.entry.addItems(values)
        
        if self.required:
            self.entry.currentIndexChanged.connect(self.set_status)
        
        self.entry.setCurrentText(value)
        
        layout.addWidget(self.entry)
        
        self.setLayout(layout)
        
        self.set_status(0)
    
    
    def set_status(self, index):
        text = self.entry.currentText()
        
        self.valueChanged.emit(text)
        
        if self.entry.currentText() == "None":
            self.entry.setStyleSheet("QComboBox {border-radius: 5px; padding: 5px; border: 1px solid #8f8f91; background-color: #FDACB8;}")
        else:
            self.entry.setStyleSheet("QComboBox {border-radius: 5px; padding: 5px; border: 1px solid #8f8f91; background-color: white;}")
    
    
    def get_value(self):
        text = self.entry.currentText()
        if self.required and not text:
            print(f"Setting: {self.name} is required!")
        return text


class toggleList(QWidget):
    def __init__(self, options, checked_options = [], parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        self._checkboxes = []
        
        for option in options:
            checkbox = QCheckBox(str(option))
            layout.addWidget(checkbox)
            self._checkboxes.append(checkbox)
            if str(option) in checked_options:
                checkbox.setChecked(True)
        
        layout.addStretch(1)
        
        self.setLayout(layout)
    
    def get_value(self):
        """
        Returns a list of checked items
        
        Returns:
            list: List of checked item texts
        """
        return [
            checkbox.text() 
            for checkbox in self._checkboxes 
            if checkbox.isChecked()
        ]


class MainWindow(QMainWindow):
    def __init__(self, filepath):
        super().__init__()
        
        self.filepath = filepath
        self.json_filepath = r"configs\device_configs\device_types\configs.json"
        
        with open(filepath, "r") as file:
            self.config = json.load(file)
        
        with open(self.json_filepath, "r") as file:
            self.json_config = json.load(file)
        
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
        
        self.delete_device_button = QPushButton("Delete This Device")
        self.delete_device_button.pressed.connect(self.delete_device)
        self.info_layout.addWidget(self.delete_device_button)
        
        self.info_layout.addStretch(1)
    
    
    def delete_device(self):
        reply = QMessageBox.question(
            self, 
            'Confirm Deletion', 
            'Are you sure you want to delete the configuration?\n'
            'This action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                filepath = self.json_config.pop(self.config["Device Name"])
                
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                with open(self.json_filepath, 'w') as file:
                    json.dump(self.json_config, file, indent=4)
                
                QMessageBox.information(
                    self, 
                    'Deletion Successful', 
                    'Configuration has been deleted successfully.'
                )
                
                self.close()
                
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    'Deletion Error', 
                    f'An error occurred: {str(e)}'
                )
    
    
    def apply_info(self):
        filepath = self.json_config.pop(self.config["Device Name"])
        self.json_config[self.info_widgets["Device Name"].get_value()] = filepath
        
        for key, value in self.info_widgets.items():
            self.config[key] = value.get_value()
            
        with open(self.filepath, "w") as file:
            json.dump(self.config, file, indent=4)
    
    
    def _create_place_setting_box(self, name, parent_layout):
        parent_layout.addLayout(self._create_setting_box(name))
    
    
    def _create_setting_box(self, name):
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
        
        return layout
    
    
    def _set_setting_layout(self):
        self.layouts = {}
        self.label_widgets = {}
        self.entry_widgets = {}
        
        self.create_setting_button = QPushButton("Create new setting")
        self.create_setting_button.pressed.connect(self.create_new_setting)
        self.settings_layout.addWidget(self.create_setting_button)
        
        for setting_name in self.config["Settings"].keys():
            self._create_place_setting_box(setting_name, self.settings_layout)
        
        self.settings_layout.addStretch(1)
    
    
    def create_new_setting(self):
        dialog = EditSettingDialog("", self.config)
        
        if dialog.exec() == QDialog.Accepted:
            self.config = dialog.global_config
            
            with open(self.filepath, 'w') as file:
                json.dump(self.config, file, indent=4)
            
            layout = self._create_setting_box(dialog.setting_name)
            
            self.settings_layout.insertLayout(layout.count() - 1, layout)
    
    
    def edit_setting(self, name):
        print(f"Editing: {name}")
        
        dialog = EditSettingDialog(name, self.config)
        
        if dialog.exec() == QDialog.Accepted:
            self.config = dialog.global_config
            
            with open(self.filepath, 'w') as file:
                json.dump(self.config, file, indent=4)
            
            if dialog.deleted:
                self.label_widgets[name].deleteLater()
                self.entry_widgets[name].deleteLater()
                self.settings_layout.removeItem(self.layouts[name])


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

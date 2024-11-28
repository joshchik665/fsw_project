# main_window.py

from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QGridLayout,
    QPushButton, 
    QLineEdit, 
    QLabel, 
    QDialog,
    QMessageBox
)
import os
import json

from device_wizard.widgets import SettingEdit, DictEdit
from device_wizard.dialogs import EditSettingDialog

class MainWindow(QMainWindow):
    def __init__(self, filepath):
        """MainWindow for the device manager wizard"""
        super().__init__()
        
        self.filepath = filepath
        self.json_filepath = r"device\configs\device_types\configs.json"
        
        with open(self.filepath, "r") as file:
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
        """Creates and Places a text edit field"""
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
        """Places all the widgets for the device wide config"""
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
        """deletes this device"""
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
        """Apply all the info settings and writes them to the json file"""
        filepath = self.json_config.pop(self.config["Device Name"])
        self.json_config[self.info_widgets["Device Name"].get_value()] = filepath
        
        for key, value in self.info_widgets.items():
            self.config[key] = value.get_value()
            
        with open(self.filepath, "w") as file:
            json.dump(self.config, file, indent=4)
    
    
    def _create_place_setting_box(self, name, parent_layout):
        """Creates then places an entry in the list of settings"""
        parent_layout.addLayout(self._create_setting_box(name))
    
    
    def _create_setting_box(self, name):
        """Creates the setting entry object"""
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
        """Creates all the widgets for each of the settings in the config file"""
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
        """Creates a new empty setting and adds it to the layout"""
        dialog = EditSettingDialog("", self.config)
        
        if dialog.exec() == QDialog.Accepted:
            self.config = dialog.global_config
            
            with open(self.filepath, 'w') as file:
                json.dump(self.config, file, indent=4)
            
            layout = self._create_setting_box(dialog.setting_name)
            
            self.settings_layout.insertLayout(layout.count() - 1, layout)
    
    
    def edit_setting(self, name):
        """Edit a setting"""
        dialog = EditSettingDialog(name, self.config)
        
        if dialog.exec() == QDialog.Accepted:
            self.config = dialog.global_config
            
            with open(self.filepath, 'w') as file:
                json.dump(self.config, file, indent=4)
            
            if dialog.deleted:
                self.label_widgets[name].deleteLater()
                self.entry_widgets[name].deleteLater()
                self.settings_layout.removeItem(self.layouts[name])


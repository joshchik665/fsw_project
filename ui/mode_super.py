from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PySide6.QtGui import (
    QPixmap,
    QImage,
)
from PySide6.QtCore import (
    Qt,
    Slot,
)
from ui.common_widgets import SettingBox, SweepBox, DetectorBox
import common.utilities as util
import json


class ModeSuper(QWidget):
    def __init__(self, mode, device, parent):
        super().__init__(parent)
        
        self.tab_indicies = {
            "Spectrum": 0,
            "Real-Time Spectrum": 1,
            "Zero-Span": 2,
        }
        
        self.instrument = device
        self.tab_widget = self.parent()
        self.main_window = self.tab_widget.parent()
        self.mode = mode
        self.settings_widgets = {}
        
        self._set_layout()
        self._set_title()
        self._set_header()
        
        self.setLayout(self.window_layout)
    
    
    def _set_layout(self) -> None:
        self.window_layout = QVBoxLayout()
        
        self.title_layout = QHBoxLayout()
        self.header_layout = QHBoxLayout()
        self.content_layout = QVBoxLayout()
        
        self.window_layout.addLayout(self.title_layout)
        self.window_layout.addLayout(self.header_layout)
        self.window_layout.addStretch(1)
        self.window_layout.addLayout(self.content_layout)
    
    
    def _set_title(self) -> None:
        title = QLabel('Rhode & Schwarz FSW-43 GUI')
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title.setObjectName('title')
        
        img= QImage('images\\crc_icon.png')
        pixmap = QPixmap(img.scaledToWidth(100))
        crc_logo = QLabel(self)
        crc_logo.setPixmap(pixmap)
        crc_logo.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addWidget(crc_logo)
        
        self.title_layout.addLayout(layout)
    
    
    def _set_header(self) -> None:
        self.load_button = QPushButton('Load Config')
        self.load_button.pressed.connect(self.load)
        
        self.save_button = QPushButton('Save Config')
        self.save_button.pressed.connect(self.save)
        
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        
        layout = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(1)
        layout.addLayout(layout2)
        
        layout1.setAlignment(Qt.AlignLeft)
        layout2.setAlignment(Qt.AlignRight)
        
        layout1.addWidget(self.load_button)
        layout1.addWidget(self.save_button)
        
        self.header_layout.addLayout(layout)
    
    
    def set_mode(self) -> None:
        self.instrument.set_mode(self.mode)
    
    
    def create_setting_box_widget(self, setting_name:str) -> None:
        setting = self.instrument.get_setting_object(setting_name)
        
        widget = SettingBox(self.instrument,setting,self)
        widget.set_value(setting.current_value)
        
        self.settings_widgets[setting_name] = widget
    
    
    def create_place_setting_box_widget(self, setting_name:str, layout) -> None:
        self.create_setting_box_widget(setting_name)
        layout.addWidget(self.settings_widgets[setting_name])
    
    
    def verify_all_settings(self):
        setting_names = list(self.settings_widgets.keys())
        return self.instrument.verify_all_settings(setting_names)
    
    
    def apply_all_settings(self):
        setting_names_values = {key: setting.get_value() for key, setting in self.settings_widgets.items()}
        return self.instrument.set_all_settings(setting_names_values)
    
    
    def apply(self):
        all_set_results = self.apply_all_settings()
        all_verify_results = self.verify_all_settings()
        
        for name, (set_result, set_status) in all_set_results.items():
            widget = self.settings_widgets[name]
            current_value = self.instrument.settings[name].current_value
            
            (verify_result, verify_status) = all_verify_results[name]
            
            if set_result and verify_result:
                widget.set_status(True, "Set Correctly & Verified!")
            else:
                widget.set_status(False, f"Verify_status:{verify_status}, Set_status:{set_status}")
            
            widget.set_value(current_value)
    
    
    def verify(self):
        all_verify_results = self.verify_all_settings()
        
        for name, (result, status) in all_verify_results.items():
            widget = self.settings_widgets[name]
            current_value = self.instrument.settings[name].current_value
            
            if result:
                widget.set_status(True, "Set Correctly & Verified!")
            else:
                widget.set_status(False, f"Verify_status:{status}")
            
            widget.set_value(current_value)
    
    
    def load(self):
        filepath = util.open_file_dialog('Open JSON file', '.json', self)
        
        if filepath:
            with open(filepath, 'r') as file:
                config = json.load(file)
            
            self.load_settings(self, config)
    
    
    def load_settings(self, config):
            self.main_window.change_tab_programmatically(self.tab_indicies[config['mode']])
            
            self.instrument.set_all_settings(config['data'])
            
            self.tab_widget.widget(self.tab_indicies[config['mode']]).verify()
    
    
    def save(self):
        filepath = util.save_file_dialog('Save JSON file', '.json', self)
        
        if filepath:
            with open(filepath, 'w') as file:
                config = {
                    'ip_address': self.instrument.ip_address,
                    'mode': self.instrument.current_mode,
                }
                current_settings = {name: setting.get_value() for name, setting in self.settings_widgets.items()}
                config['data'] = current_settings
                
                json.dump(config, file, indent=4)








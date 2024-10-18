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


class ModeSuper(QWidget):
    def __init__(self, mode, device):
        super().__init__()
        
        self.instrument = device
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
        
        self.save_button = QPushButton('Save Config')
        
        visa_label = QLabel('Visa Timeout(ms):')
        
        self.visa_entry = QLineEdit()
        self.visa_entry.returnPressed.connect(self.set_visa_timeout)
        self.visa_entry.setPlaceholderText('3000')
        self.visa_entry.setFixedWidth(100)
        
        opc_label = QLabel('Opc Timeout(ms):')
        
        self.opc_entry = QLineEdit()
        self.opc_entry.returnPressed.connect(self.set_opc_timeout)
        self.opc_entry.setPlaceholderText('3000')
        self.opc_entry.setFixedWidth(100)
        
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
        
        layout2.addWidget(visa_label)
        layout2.addWidget(self.visa_entry)
        layout2.addWidget(opc_label)
        layout2.addWidget(self.opc_entry)
        
        self.header_layout.addLayout(layout)
    
    
    def set_mode(self) -> None:
        self.instrument.set_mode(self.mode)
    
    
    def create_place_sweep_box_widget(self, layout):
        self.sweep_box = SweepBox(self.instrument, self)
        layout.addWidget(self.sweep_box)
    
    
    def create_place_detector_box_widget(self, layout):
        self.detector_box = DetectorBox(self.instrument, self.mode, self)
        layout.addWidget(self.detector_box)
    
    
    def create_setting_box_widget(self, setting_name:str) -> None:
        setting = self.instrument.get_setting_object(setting_name)
        
        widget = SettingBox(setting,self)
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
    
    
    def set_visa_timeout(self):
        time = self.visa_entry.text()
        if util.is_number(time):
            self.instrument.visa_timeout = time
            self.visa_entry.setPlaceholderText(time)
        self.visa_entry.clear()
    
    
    def set_opc_timeout(self):
        time = self.opc_entry.text()
        if util.is_number(time):
            self.instrument.opc_timeout = time
            self.opc_entry.setPlaceholderText(time)
        self.opc_entry.clear()








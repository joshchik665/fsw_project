from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from ui.mode_super import ModeSuper
from ui.common_widgets import SettingBox

class ModeSpec(ModeSuper):
    def __init__(self,device, tab_widget):
        super().__init__('Spectrum',device, tab_widget)
        
        
        self.create_place_setting_box_widget("Center Frequency",self.content_layout)
        self.create_place_setting_box_widget("Reference Level",self.content_layout)
        self.create_place_setting_box_widget("Frequency Span",self.content_layout)
        self.create_place_setting_box_widget("Resolution Bandwidth",self.content_layout)
        self.create_place_setting_box_widget("Video Bandwidth",self.content_layout)
        self.create_place_setting_box_widget("Sweep Time",self.content_layout)
        self.create_place_setting_box_widget("Number of Points",self.content_layout)
        
        self.create_place_setting_box_widget("Detector",self.content_layout)
        self.create_place_setting_box_widget("Sweep", self.content_layout)
        
        self.apply_button = QPushButton("Apply All Settings")
        self.apply_button.pressed.connect(self.apply)
        self.content_layout.addWidget(self.apply_button)






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
    def __init__(self,device):
        super().__init__('Spectrum',device)
        
        self.create_place_setting_box_widget("Center Frequency")
        self.create_place_setting_box_widget("Reference Level")
        self.create_place_setting_box_widget("Frequency Span")
        self.create_place_setting_box_widget("Resolution Bandwidth")
        self.create_place_setting_box_widget("Video Bandwidth")
        self.create_place_setting_box_widget("Sweep Time")
        self.create_place_setting_box_widget("Number of Points")
        
        self.apply_button = QPushButton("Apply All Settings")
        self.apply_button.pressed.connect(self.apply)
        self.content_layout.addWidget(self.apply_button)
        
        





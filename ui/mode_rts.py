from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from ui.mode_super import ModeSuper

class ModeRts(ModeSuper):
    def __init__(self,device, parent=None):
        super().__init__('Real-Time Spectrum',device, parent)
        
        self.create_place_setting_box_widget("Center Frequency",self.content_layout)

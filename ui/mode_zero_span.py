from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from ui.mode_super import ModeSuper

class ModeZs(ModeSuper):
    def __init__(self, device, parent=None):
        super().__init__('Zero-Span',device, parent)
        
        self.create_place_setting_box_widget("Center Frequency",self.content_layout)

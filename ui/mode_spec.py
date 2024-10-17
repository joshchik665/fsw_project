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
        
        self.create_setting_widget("Center Frequency")
        self.content_layout.addWidget(self.settings_widgets["Center Frequency"])
        
        self.apply_button = QPushButton("Apply All Settings")
        self.apply_button.pressed.connect(self.apply)
        self.content_layout.addWidget(self.apply_button)
        
        





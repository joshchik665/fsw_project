from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLabel
)
from ui.common_gui.mode_super import ModeSuper

class ModeDefault(ModeSuper):
    def __init__(self, device, parent=None):
        super().__init__('Default', device, parent)
        
        layout = QVBoxLayout()
        
        for setting_name in self.instrument.settings.keys():
            self.create_place_setting_box_widget(setting_name, layout)
        
        self.content_layout.addLayout(layout, 1, 0)
        
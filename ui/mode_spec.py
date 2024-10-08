from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
#from fsw.device import RsFswInstrument
from ui.mode_super import ModeSuper
from ui.common_widgets import SettingBox


class ModeSpec(ModeSuper):
    def __init__(self):
        super().__init__()
        
        self.mode = 'Spectrum'
        
        self.set_widgets()
        
        self.setLayout(self.window_layout)
        
        self.configure()
    
    
    def set_widgets(self):
        self.test1_setting = SettingBox('Test1','frequency',self)
        self.content_layout.addWidget(self.test1_setting)
        
        self.test2_setting = SettingBox('Test2','frequency',self)
        self.content_layout.addWidget(self.test2_setting)



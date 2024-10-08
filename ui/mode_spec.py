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
    
    
    def set_widgets(self):
        self.test1_setting = SettingBox('Test1','10','Hz','frequency',self)
        self.content_layout.addWidget(self.test1_setting)
        
        self.test2_setting = SettingBox('Test2','10','GHz','frequency',self)
        self.content_layout.addWidget(self.test2_setting)
        
        self.test3_setting = SettingBox('Test3','10','kHz','frequency',self)
        self.content_layout.addWidget(self.test3_setting)


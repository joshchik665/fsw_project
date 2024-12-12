from PySide6.QtWidgets import (
    QVBoxLayout
)
from ui.common_gui.mode_super import ModeSuper
from ui.common_gui.trace_widget import SpectralWidget


class ModeSpec(ModeSuper):
    def __init__(self, device, parent=None):
        super().__init__('Spectrum', device, parent)
        
        self.setting_layout1 = QVBoxLayout()
        self.setting_layout2 = QVBoxLayout()
        
        self.create_place_setting_box_widget("Center Frequency", self.setting_layout1)
        self.create_place_setting_box_widget("Frequency Span", self.setting_layout1)
        self.create_place_setting_box_widget("Resolution Bandwidth", self.setting_layout1)
        self.create_place_setting_box_widget("Video Bandwidth", self.setting_layout1)
        self.create_place_setting_box_widget("Sweep Time", self.setting_layout1)
        self.create_place_setting_box_widget("Number of Points", self.setting_layout1)
        
        self.create_place_setting_box_widget("Sweep", self.setting_layout2)
        self.create_place_setting_box_widget("Detector", self.setting_layout2)
        
        self.setting_layout1.addStretch(1)
        self.setting_layout2.addStretch(1)
        
        self.content_layout.addLayout(self.setting_layout1, 1, 0)
        self.content_layout.addLayout(self.setting_layout2, 1, 1)
        
        
        self.graph_layout = QVBoxLayout()
        
        self.graph = SpectralWidget(self.instrument, self.mode)
        self.graph_layout.addWidget(self.graph)
        
        self.graph_layout.addStretch(1)
        
        self.content_layout.addLayout(self.graph_layout, 0, 2, 2, 1)
        

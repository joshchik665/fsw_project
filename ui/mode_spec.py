from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from ui.mode_super import ModeSuper
from ui.common_widgets import SettingBox, SpectralWidget

class ModeSpec(ModeSuper):
    def __init__(self, device, parent=None):
        super().__init__('Spectrum', device, parent)
        
        self.setting_layout = QVBoxLayout()
        
        self.create_place_setting_box_widget("Center Frequency", self.setting_layout)
        self.create_place_setting_box_widget("Reference Level", self.setting_layout)
        self.create_place_setting_box_widget("Frequency Span", self.setting_layout)
        self.create_place_setting_box_widget("Resolution Bandwidth", self.setting_layout)
        self.create_place_setting_box_widget("Video Bandwidth", self.setting_layout)
        self.create_place_setting_box_widget("Sweep Time", self.setting_layout)
        self.create_place_setting_box_widget("Number of Points", self.setting_layout)
        self.create_place_setting_box_widget("Attenuation", self.setting_layout)
        
        self.create_place_setting_box_widget("Detector", self.setting_layout)
        self.create_place_setting_box_widget("Sweep", self.setting_layout)
        self.create_place_setting_box_widget("Sweep Time Auto", self.setting_layout)
        self.create_place_setting_box_widget("Attenuation Auto", self.setting_layout)
        self.create_place_setting_box_widget("Pre-Amp Value", self.setting_layout)
        self.create_place_setting_box_widget("Pre-Amp Mode", self.setting_layout)
        
        self.apply_button = QPushButton("Apply All Settings")
        self.apply_button.pressed.connect(self.apply)
        self.setting_layout.addWidget(self.apply_button)
        
        self.content_layout.addLayout(self.setting_layout, 0, 0)
        
        
        self.graph_layout = QVBoxLayout()
        
        self.graph = SpectralWidget(self.instrument)
        self.graph_layout.addWidget(self.graph)
        
        self.abort_button = QPushButton("Abort")
        self.abort_button.pressed.connect(self.instrument.abort)
        self.graph_layout.addWidget(self.abort_button)
        
        self.sweep_button = QPushButton("Run Sweep")
        self.sweep_button.pressed.connect(self.instrument.sweep)
        self.graph_layout.addWidget(self.sweep_button)
        
        self.content_layout.addLayout(self.graph_layout, 0 ,1)






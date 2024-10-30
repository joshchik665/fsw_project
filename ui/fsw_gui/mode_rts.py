from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
)
from ui.common_gui.mode_super import ModeSuper
from ui.common_gui.common_widgets import SpectralWidget
from ui.common.utilities import save_file_dialog
from datetime import datetime
from pathlib import Path
from ui.common_gui.message_boxes import copy_error, copy_sucess

class ModeRts(ModeSuper):
    def __init__(self,device, parent=None):
        super().__init__('Real-Time Spectrum',device, parent)
        
        self.setting_layout1 = QVBoxLayout()
        self.setting_layout2 = QVBoxLayout()
        
        self.create_place_setting_box_widget("Center Frequency", self.setting_layout1)
        self.create_place_setting_box_widget("Dwell Time", self.setting_layout1)
        self.create_place_setting_box_widget("Memory Depth", self.setting_layout1)
        self.create_place_setting_box_widget("Reference Level", self.setting_layout1)
        self.create_place_setting_box_widget("Frequency Span", self.setting_layout1)
        self.create_place_setting_box_widget("Resolution Bandwidth", self.setting_layout1)
        self.create_place_setting_box_widget("Sweep Time", self.setting_layout1)
        self.create_place_setting_box_widget("Attenuation", self.setting_layout1)
        
        self.create_place_setting_box_widget("Detector", self.setting_layout2)
        self.create_place_setting_box_widget("Sweep", self.setting_layout2)
        self.create_place_setting_box_widget("Sweep Time Auto", self.setting_layout2)
        self.create_place_setting_box_widget("Attenuation Auto", self.setting_layout2)
        self.create_place_setting_box_widget("Pre-Amp Value", self.setting_layout2)
        self.create_place_setting_box_widget("Pre-Amp Mode", self.setting_layout2)
        
        self.setting_layout1.addStretch(1)
        self.setting_layout2.addStretch(1)
        
        self.content_layout.addLayout(self.setting_layout1, 1, 0)
        self.content_layout.addLayout(self.setting_layout2, 1, 1)
        
        
        self.graph_layout = QVBoxLayout()
        
        self.graph = SpectralWidget(self.instrument, self.mode)
        self.graph_layout.addWidget(self.graph)
        
        self.graph_layout.addStretch(1)
        
        self.content_layout.addLayout(self.graph_layout, 0, 2, 2, 1)
        
        
        self.func_layout = QVBoxLayout()
        
        self.abort_button = QPushButton("Abort")
        self.abort_button.setFixedSize(150, 30)
        self.abort_button.pressed.connect(self.instrument.abort)
        self.func_layout.addWidget(self.abort_button)
        
        self.sweep_button = QPushButton("Run Sweep")
        self.sweep_button.setFixedSize(150, 30)
        self.sweep_button.pressed.connect(self.instrument.sweep)
        self.func_layout.addWidget(self.sweep_button)
        
        self.clear_spec_button = QPushButton("Clear Spectrogram")
        self.clear_spec_button.setFixedSize(150, 30)
        self.clear_spec_button.pressed.connect(self.instrument.clear_spectrogram)
        self.func_layout.addWidget(self.clear_spec_button)
        
        self.save_spec_button = QPushButton("Save Spectrogram")
        self.save_spec_button.setFixedSize(150, 30)
        self.save_spec_button.pressed.connect(self.get_save_spectrogram)
        self.func_layout.addWidget(self.save_spec_button)
        
        self.func_layout.addStretch(1)
        
        self.content_layout.addLayout(self.func_layout, 0, 3, 2, 1)
    
    
    def get_save_spectrogram(self):
        self.instrument.save_spectrogram()
        
        default_filename = Path("spectrograms") / f"trace_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filename = save_file_dialog("Select location to save csv file", str(default_filename), ".csv", self)
        
        if self.instrument.copy_spectrogram(filename):
            copy_sucess()
        else:
            copy_error()
        

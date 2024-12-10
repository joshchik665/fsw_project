# mode_default.py

from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt

from ui.common_gui.mode_super import ModeSuper
from device.setting_classes.numerical_setting import NumericalSetting
from device.setting_classes.display_setting import DisplaySetting
from device.setting_classes.mode_setting import ModeSetting

class ModeDefault(ModeSuper):
    def __init__(self, device, parent=None):
        """Default window layout if none is specified for this mode"""
        super().__init__('Default', device, parent)
        
        # Creates all the Numerical Settings from the instrument's settings list
        layout1 = QVBoxLayout()
        for setting_name, setting_object in self.instrument.settings.items():
            if isinstance(setting_object, NumericalSetting):
                self.create_place_setting_box_widget(setting_name, layout1)
        layout1.addStretch(1)
        self.content_layout.addLayout(layout1, 1, 0)
        
        # Creates all the Mode Settings from the instrument's setting list
        layout2 = QVBoxLayout()
        for setting_name, setting_object in self.instrument.settings.items():
            if isinstance(setting_object, ModeSetting):
                self.create_place_setting_box_widget(setting_name, layout2)
        layout2.addStretch(1)
        self.content_layout.addLayout(layout2, 1, 1)
        
        # Adds a button to refresh all the values if a display settings is present
        if self.contains_class(self.instrument.settings, DisplaySetting):
            self.refresh_button = QPushButton("Refresh values")
            self.refresh_button.pressed.connect(self.verify_all_settings)
            self.content_layout.addWidget(self.refresh_button, 0, 2, alignment=Qt.AlignBottom)
        
        # Adds all the display settings from the instrument's setting list
        layout3 = QVBoxLayout()
        for setting_name, setting_object in self.instrument.settings.items():
            if isinstance(setting_object, DisplaySetting):
                self.create_place_setting_box_widget(setting_name, layout3)
        layout3.addStretch(1)
        self.content_layout.addLayout(layout3, 1, 2)
    
    
    def contains_class(self, dictionary, cls):
        """Dictionary contains at least one value of type cls"""
        for value in dictionary.values():
            if isinstance(value, cls):
                return True
        return False
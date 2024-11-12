# common_widgets.py

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QComboBox,
)
from PySide6.QtGui import QDoubleValidator
from fsw.setting_objects.numerical_setting import NumericalSetting
from fsw.setting_objects.mode_setting import ModeSetting
from fsw.device.settings_manager import SettingsManager
from ui.common.utilities import remove_trailing_zeros
from typing import Union


class NumericalSettingBox(QWidget):
    def __init__(self, instrument:SettingsManager, setting:Union[NumericalSetting,ModeSetting], parent=None):
        """Initializes the setting box widget

        Args:
            instrument (SettingManager): The instrument
            setting (Union[NumericalSetting,ModeSetting]): The setting object
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        self.setting = setting # Store the setting object
        
        # The layout for this widget
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        # Setting name widget
        label = QLabel(self.setting.name)
        label.setFixedWidth(150)
        self.layout.addWidget(label)
        
        self.instrument = instrument
        
        # Get the units for this setting based on the measure of the setting
        self.all_units = {
            'frequency': {
                'mHz': 1e-3,
                'Hz': 1,
                'kHz': 1e3,
                'MHz': 1e6,
                'GHz': 1e9,
                'THz': 1e12,
            },
            'power': {
                'dBm': 1,
            },
            'time': {
                'ms': 1e-3,
                's': 1,
            },
            'number': {
                'Units': 1
            },
        }
        self.units = self.all_units[self.setting.measure]
        
        # Create the value entry for this setting
        self.value_entry = QLineEdit(self.setting.current_value)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.value_entry.setValidator(validator)
        self.value_entry.setFixedSize(60, 30)
        self.value_entry.textChanged.connect(self.value_changed)
        self.layout.addWidget(self.value_entry)
        
        # Adds the widget to select the unit for the setting
        self.unit_entry = QComboBox()
        self.unit_entry.addItems(list(self.units.keys()))
        self.unit_entry.setFixedSize(50, 30)
        self.unit_entry.currentTextChanged.connect(self.value_changed)
        self.layout.addWidget(self.unit_entry)
        
        self.layout.addStretch(1)
        
        self.changed = False
    
    
    def value_changed(self) -> None:
        if self.value_entry.hasFocus() or self.unit_entry.hasFocus():
            self.value_entry.setStyleSheet("background-color: white")
            self.changed = True
    
    
    def get_value(self) -> str:
        """Gets the current value of this widget and returns if as a string

        Returns:
            str: String of the value of this widget
        """
        # get text and unit
        value = self.value_entry.text()
        unit = self.unit_entry.currentText()
        
        value = float(value)
        
        widget_value = value * self.units[unit] # converts to base unit
        
        return str(widget_value)
    
    
    def set_value(self,value:str) -> None:
        """Set the current value of the widget

        Args:
            value (str): The value to be set on this widget
        """
        value = float(value)
        
        # Get all the units that are less than or equal to the value
        eligible_units = {k: v for k, v in self.units.items() if v <= value}
        
        # gets the largest possible unit that is less that the value
        if not eligible_units:
            unit = max(self.units, key=self.units.get)
        else:
            unit = max(eligible_units, key=eligible_units.get)
        
        value = value / self.units[unit] # Convert the value to the correct unit
        
        # Create the text to write on the display
        text = f"{value:.5f}"
        text = remove_trailing_zeros(text)
        
        # Set the value on the widget
        self.value_entry.setText(text)
        self.unit_entry.setCurrentText(unit)
    
    
    def set_status(self, state:bool, message:str) -> None:
        """Show the status of the setting on the widget and set the tool tip message

        Args:
            state (bool): True if the setting is set correctly
            message (str): message to display to the user about the setting
        """
        widget = self.value_entry
        # Set the status of the setting by color and set tooltip message
        if state:
            widget.setStyleSheet("background-color: #9CEC7B")
            widget.setToolTip("All good")
            self.changed = False
        else:
            widget.setStyleSheet("background-color: #FFB94F")
            widget.setToolTip(message)
            self.changed = True


class ModeSettingBox(QWidget):
    def __init__(self, instrument:SettingsManager, setting:Union[NumericalSetting,ModeSetting], mode: str, parent=None):
        """Initializes the setting box widget

        Args:
            instrument (SettingManager): The instrument
            setting (Union[NumericalSetting,ModeSetting]): The setting object
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        self.setting = setting # Store the setting object
        
        # The layout for this widget
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        # Setting name widget
        label = QLabel(self.setting.name)
        label.setFixedWidth(150)
        self.layout.addWidget(label)
        
        self.instrument = instrument
        
        # Creates the widget to select the options
        self.option_box = QComboBox()
        if self.setting.alias is not None:
            if self.setting.custom_modes is not None:
                self.option_box.addItems(self.setting.custom_modes[mode])
            else:
                self.option_box.addItems(self.setting.alias.keys())
        else:
            if self.setting.custom_modes is not None:
                self.option_box.addItems(self.setting.custom_modes[mode])
            else:
                self.option_box.addItems(self.setting.write_commands.keys())
        self.option_box.setFixedSize(110, 30)
        self.option_box.currentTextChanged.connect(self.value_changed)
        self.layout.addWidget(self.option_box)
        
        self.layout.addStretch(1)
        
        self.changed = False
    
    
    def value_changed(self) -> None:
        if self.option_box.hasFocus():
            self.option_box.setStyleSheet("background-color: white")
            self.changed = True
    
    
    def get_value(self) -> str:
        """Gets the current value of this widget and returns if as a string

        Returns:
            str: String of the value of this widget
        """
        return self.option_box.currentText()
    
    
    def set_value(self,value:str) -> None:
        """Set the current value of the widget

        Args:
            value (str): The value to be set on this widget
        """
        self.option_box.setCurrentText(value) # Set the text on the display
    
    
    def set_status(self, state:bool, message:str) -> None:
        """Show the status of the setting on the widget and set the tool tip message

        Args:
            state (bool): True if the setting is set correctly
            message (str): message to display to the user about the setting
        """
        widget = self.option_box
        
        # Set the status of the setting by color and set tooltip message
        if state:
            widget.setStyleSheet("background-color: #9CEC7B")
            widget.setToolTip("All good")
            self.changed = False
        else:
            widget.setStyleSheet("background-color: #FFB94F")
            widget.setToolTip(message)
            self.changed = True


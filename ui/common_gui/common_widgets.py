# common_widgets.py

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QDoubleValidator, QIntValidator
from fsw.setting_objects.numerical_setting import NumericalSetting
from fsw.setting_objects.mode_setting import ModeSetting
from fsw.device.settings_manager import SettingsManager
from ui.common.utilities import remove_trailing_zeros
from ui.common_gui.csv_logger import TraceLogger
from typing import Union
from pathlib import Path
import pyqtgraph as pg
import numpy as np


class SettingBox(QWidget):
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
        
        # Checks to see what type of setting this is by checking the type of the setting object
        if isinstance(self.setting, NumericalSetting):
            self.setting_type = 'numerical'
            self._make_numerical_setting_widget()
        elif isinstance(self.setting, ModeSetting):
            self.setting_type = 'mode'
            self._make_mode_setting_widget()
        else:
            raise TypeError("Unsupported object type")
    
    
    def _make_mode_setting_widget(self) -> None:
        """Make the layout if the layout is for a mode setting
        """
        # Creates the widget to select the options
        self.option_box = QComboBox()
        self.option_box.addItems(self.setting.write_commands.keys())
        self.option_box.setFixedSize(110, 30)
        self.layout.addWidget(self.option_box)
        
        self.layout.addStretch(1)
    
    
    def _make_numerical_setting_widget(self) -> None:
        """Make the layout if the layout is for a numerical setting
        """
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
        self.layout.addWidget(self.value_entry)
        
        # Adds the widget to select the unit for the setting
        self.unit_entry = QComboBox()
        self.unit_entry.addItems(list(self.units.keys()))
        self.unit_entry.setFixedSize(50, 30)
        self.layout.addWidget(self.unit_entry)
        
        self.layout.addStretch(1)
    
    
    def get_value(self) -> str:
        """Gets the current value of this widget and returns if as a string

        Returns:
            str: String of the value of this widget
        """
        if self.setting_type == 'numerical': # if the setting is numerical
            # get text and unit
            value = self.value_entry.text()
            unit = self.unit_entry.currentText()
            
            value = float(value)
            
            widget_value = value * self.units[unit] # converts to base unit
            
            return str(widget_value)
        elif self.setting_type == 'mode': # if the setting is for a mode
            return self.option_box.currentText()
    
    
    def set_value(self,value:str) -> None:
        """Set the current value of the widget

        Args:
            value (str): The value to be set on this widget
        """
        if self.setting_type == 'numerical':
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
            text = f"{value:.7f}"
            text = remove_trailing_zeros(text)
            
            # Set the value on the widget
            self.value_entry.setText(text)
            self.unit_entry.setCurrentText(unit)
        elif self.setting_type == 'mode':
            self.option_box.setCurrentText(value) # Set the text on the display
    
    
    def set_status(self, state:bool, message:str) -> None:
        """Show the status of the setting on the widget and set the tool tip message

        Args:
            state (bool): True if the setting is set correctly
            message (str): message to display to the user about the setting
        """
        # Get the right widget to set the status
        if self.setting_type == 'numerical':
            widget = self.value_entry
        elif self.setting_type == 'mode':
            widget = self.option_box
        
        # Set the status of the setting by color and set tooltip message
        if state:
            widget.setStyleSheet("background-color: #9CEC7B")
            widget.setToolTip("All good")
        else:
            widget.setStyleSheet("background-color: #FFB94F")
            widget.setToolTip(message)


class SpectralWidget(QWidget):
    def __init__(self, device: SettingsManager, mode: str):
        super().__init__()
        
        self.device = device
        self.mode = mode
        
        self.trace_logger = TraceLogger(self)  # Pass self as parent
        
        self.do_updates = True
        default_update_period = 100
        
        # Connect signals
        self.trace_logger.logging_started.connect(self.on_logging_started)
        self.trace_logger.logging_stopped.connect(self.on_logging_stopped)
        self.trace_logger.trace_logged.connect(self.on_trace_logged)
        self.trace_logger.error_occurred.connect(self.on_logging_error)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        layout1 = QHBoxLayout()
        layout.addLayout(layout1)
        
        self.update_label = QLabel("Display Updates: ")
        layout1.addWidget(self.update_label)
        
        self.update_on_button = QPushButton("On")
        self.update_on_button.setDisabled(True)
        self.update_on_button.pressed.connect(self.start_update)
        layout1.addWidget(self.update_on_button)
        
        self.update_off_button = QPushButton("Off")
        self.update_off_button.pressed.connect(self.stop_update)
        layout1.addWidget(self.update_off_button)
        
        self.update_period_label = QLabel("Update Period (ms): ")
        layout1.addWidget(self.update_period_label)
        
        self.update_period_entry = QLineEdit()
        int_validator = QIntValidator()
        self.update_period_entry.setValidator(int_validator)
        self.update_period_entry.setPlaceholderText(str(default_update_period))
        self.update_period_entry.returnPressed.connect(self.set_update_timing)
        layout1.addWidget(self.update_period_entry)
        
        self.change_period_button = QPushButton("Apply")
        self.change_period_button.pressed.connect(self.set_update_timing)
        layout1.addWidget(self.change_period_button)
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setFixedSize(500,400)
        self.plot_widget.setYRange(-100, 10)
        layout.addWidget(self.plot_widget)
        
        self.plot_widget.setBackground('w')
        
        self.plot_line = self.plot_widget.plot(pen='b')
        
        if self.mode == "Zero-Span":
            self.plot_widget.setTitle("Zero-Span Trace (Power vs. Time)")
            self.plot_widget.setLabel('left', 'Power (dBm)')
            self.plot_widget.setLabel('bottom', 'Time (s)')
        else:
            self.plot_widget.setTitle("Spectral Trace (Power vs. Frequency)")
            self.plot_widget.setLabel('left', 'Power (dBm)')
            self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
        
        layout2 = QHBoxLayout()
        layout.addLayout(layout2)
        
        self.start_button = QPushButton("Start Logging")
        self.start_button.pressed.connect(self.start_logging_action)
        layout2.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Logging")
        self.stop_button.pressed.connect(self.stop_logging_action)
        self.stop_button.setDisabled(True)
        layout2.addWidget(self.stop_button)
        
        layout3 = QHBoxLayout()
        layout.addLayout(layout3)
        
        self.status_label = QLabel("Status: Logging Stopped ")
        layout3.addWidget(self.status_label)
        
        self.trace_count_label = QLabel()
        layout3.addWidget(self.trace_count_label)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(default_update_period)
    
    
    def update_plot(self):
        if self.do_updates:
            num_points = int(remove_trailing_zeros(self.device.settings['Number of Points'].current_value))
            
            if self.mode == "Zero-Span":
                sweep_time = float(self.device.settings['Sweep Time'].current_value)
                
                x = [i * (sweep_time / (num_points - 1)) for i in range(num_points)]
                
                self.plot_widget.setXRange(0,sweep_time)
            else:
                center_freq = float(self.device.settings['Center Frequency'].current_value)
                freq_span = float(self.device.settings['Frequency Span'].current_value)
                
                start_freq = center_freq - (freq_span / 2)
                end_freq = center_freq + (freq_span / 2)
                
                x = [start_freq + (i * (freq_span / (num_points - 1))) for i in range(num_points)]
                
                self.plot_widget.setXRange(start_freq,end_freq)
            
            y = self.device.get_trace()
            
            self.plot_line.setData(x, y)
            
            self.trace_logger.log_trace(np.array(x), np.array(y))
    
    
    def start_update(self) -> None:
        self.do_updates = True
        self.update_off_button.setDisabled(False)
        self.update_on_button.setDisabled(True)
    
    
    def stop_update(self) -> None:
        self.do_updates = False
        self.update_off_button.setDisabled(True)
        self.update_on_button.setDisabled(False)
    
    
    def set_update_timing(self) -> None:
        period = self.update_period_entry.text()
        self.update_period_entry.clear()
        self.update_period_entry.setPlaceholderText(period)
        self.timer.setInterval(int(period))
    
    
    def start_logging_action(self):
        """Called when user wants to start logging (e.g., from a button)"""
        if self.trace_logger.start_logging():
            self.start_button.setDisabled(True)
            self.stop_button.setDisabled(False)
    
    
    def stop_logging_action(self):
        self.trace_logger.stop_logging()
        self.start_button.setDisabled(False)
        self.stop_button.setDisabled(True)
        self.trace_count_label.clear()


    def on_logging_started(self, filepath: str):
        print(f"Started logging to: {filepath}")
        self.status_label.setText(f"Status: Logging to: {Path(filepath).name} ")


    def on_logging_stopped(self):
        print("Logging stopped")
        self.status_label.setText("Status: Logging stopped ")


    def on_trace_logged(self, count: int):
        print(f"Logged trace #{count}")
        self.trace_count_label.setText(f"Traces: {count}")


    def on_logging_error(self, error_message: str):
        print(f"Logging error: {error_message}")
        QMessageBox.warning(self, "Logging Error", error_message)




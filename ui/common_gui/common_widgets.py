# common_widgets.py

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QPushButton,
    QButtonGroup,
    QRadioButton,
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QDoubleValidator
from fsw.setting_objects.numerical_setting import NumericalSetting
from fsw.setting_objects.mode_setting import ModeSetting
from ui.common.utilities import remove_trailing_zeros
from typing import Union
import pyqtgraph as pg
from fsw.device.settings_manager import SettingsManager


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
            text = f"{value:.4f}"
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
    def __init__(self, device: SettingsManager):
        super().__init__()
        
        self.device = device
        self.mode = self.device.current_mode
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setFixedSize(500,400)
        self.plot_widget.setYRange(-100, 10)
        layout.addWidget(self.plot_widget)
        
        self.plot_widget.setBackground('w')
        
        self.plot_line = self.plot_widget.plot(pen='b')
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)
    
    
    def update_plot(self):
        num_points = int(remove_trailing_zeros(self.device.settings['Number of Points'].current_value))
        
        self.mode = self.device.current_mode
        
        if self.mode == "Zero-Span":
            sweep_time = float(self.device.settings['Sweep Time'].current_value)
            x = [i * (sweep_time / (num_points - 1)) for i in range(num_points)]
            
            self.plot_widget.setXRange(0,sweep_time)
            
            self.plot_widget.setTitle("Zero-Span Trace (Power vs. Time)")
            self.plot_widget.setLabel('left', 'Power (dBm)')
            self.plot_widget.setLabel('bottom', 'Time (s)')
        else:
            center_freq = float(self.device.settings['Center Frequency'].current_value)
            freq_span = float(self.device.settings['Frequency Span'].current_value)
            
            start_freq = center_freq - (freq_span / 2)
            end_freq = center_freq + (freq_span / 2)
            
            self.plot_widget.setXRange(start_freq,end_freq)
            
            x = [start_freq + (i * (freq_span / (num_points - 1))) for i in range(num_points)]
            
            self.plot_widget.setTitle("Spectral Trace (Power vs. Frequency)")
            self.plot_widget.setLabel('left', 'Power (dBm)')
            self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
        
        y = self.device.get_trace()
        
        self.plot_line.setData(x, y)


# class SweepBox(QWidget):
#     def __init__(self,instrument,parent=None):
#         super().__init__(parent)
        
#         self.instrument = instrument
        
#         layout = QHBoxLayout()
        
#         self.single_sweep_button = QPushButton('Single Sweep')
#         self.single_sweep_button.pressed.connect(self.single_sweep)
#         layout.addWidget(self.single_sweep_button)
        
#         self.cont_sweep_button = QPushButton('Continuous Sweep')
#         self.cont_sweep_button.pressed.connect(self.cont_sweep)
#         self.cont_sweep_button.setDisabled(True)
#         layout.addWidget(self.cont_sweep_button)
        
#         self.abort_sweep_button = QPushButton('Stop Sweep')
#         self.abort_sweep_button.pressed.connect(self.abort)
#         layout.addWidget(self.abort_sweep_button)
        
#         self.setLayout(layout)
    
    
#     def cont_sweep(self):
#         self.instrument.set_setting("Sweep", "Continuous")
#         self.cont_sweep_button.setDisabled(True)
#         self.single_sweep_button.setDisabled(False)
    
    
#     def single_sweep(self):
#         self.instrument.set_setting("Sweep", "Single")
#         self.cont_sweep_button.setDisabled(False)
#         self.single_sweep_button.setDisabled(True)
    
    
#     def abort(self):
#         self.instrument.set_setting("Sweep", 'Abort')


# class DetectorBox(QWidget):
#     def __init__(self, instrument, mode, parent=None):
#         super().__init__(parent)
        
#         self.instrument = instrument
#         self.mode = mode
        
#         self.all_detectors = {
#             'Spectrum': (
#                 'auto_peak',
#                 'positive_peak',
#                 'negative_peak',
#                 'rms',
#                 'average',
#                 'sample',
#             ),
#             'Real-Time Spectrum': (
#                 'positive_peak',
#                 'negative_peak',
#                 'average',
#                 'sample',
#             ),
#             'Zero-Span': (
#                 'auto_peak',
#                 'positive_peak',
#                 'negative_peak',
#                 'rms',
#                 'average',
#                 'sample',
#             ),
#         }
        
#         self.applicable_detectors = self.all_detectors[self.mode]
#         self.current_detector = self.applicable_detectors[0] # The first element is the default one
        
#         self.layout = QVBoxLayout()
        
#         self.title = QLabel('Detectors:')
#         self.layout.addWidget(self.title)
        
#         self.button_group = QButtonGroup()
        
#         for option in self.applicable_detectors:
#             radio_button = QRadioButton(option)
#             self.layout.addWidget(radio_button)
#             self.button_group.addButton(radio_button)
            
#             if option == self.current_detector:
#                 radio_button.setChecked(True)
        
#         self.set_detector_button = QPushButton('Set Detector')
#         self.set_detector_button.pressed.connect(self.set_detector)
#         self.layout.addWidget(self.set_detector_button)
        
#         self.status_label = QLabel(f"Current Detector: {self.current_detector}")
#         self.layout.addWidget(self.status_label)
        
#         self.setLayout(self.layout)
    
    
#     def set_detector(self):
#         selected_button = self.button_group.checkedButton().text()
        
#         if selected_button:
#             self.instrument.set_setting('Detector',selected_button)
#             self.current_detector = selected_button
#             self.status_label.setText(f"Current Detector: {self.current_detector}")
        













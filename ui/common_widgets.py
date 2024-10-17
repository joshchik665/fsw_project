from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QPushButton,
)
from PySide6.QtGui import QDoubleValidator
from fsw.setting import Setting
import common.utilities as util


class SettingBox(QWidget):
    def __init__(self, setting:Setting, parent=None):
        super().__init__(parent)
        
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
            }
        }
        
        self.units = self.all_units[setting.measure]
        
        layout = QHBoxLayout()
        
        label = QLabel(setting.name)
        label.setFixedWidth(150)
        layout.addWidget(label)
        
        self.value_entry = QLineEdit(setting.current_value)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        # Set the range (optional, adjust as needed)
        #validator.setRange(-999999.99, 999999.99, 2)  # 2 decimal places
        self.value_entry.setValidator(validator)
        
        self.value_entry.setFixedWidth(60)
        self.value_entry.setFixedHeight(30)
        layout.addWidget(self.value_entry)
        
        self.unit_entry = QComboBox()
        self.unit_entry.addItems(list(self.units.keys()))
        self.unit_entry.setFixedWidth(50)
        self.unit_entry.setFixedHeight(30)
        layout.addWidget(self.unit_entry)
        
        layout.addStretch(1)
        
        self.setLayout(layout)
    
    
    def get_value(self) -> str:
        value = self.value_entry.text()
        unit = self.unit_entry.currentText()
        
        value = float(value)
        
        widget_value = value * self.units[unit]
        
        return str(widget_value)
    
    
    def set_value(self,value:str):
        value = float(value)
        
        eligible_items = {k: v for k, v in self.units.items() if v <= value}
        
        if not eligible_items:
            unit = max(self.units, key=self.units.get)
        else:
            unit = max(eligible_items, key=eligible_items.get)
        
        value = value / self.units[unit]
        
        text = f"{value:.4f}"
        text = util.remove_trailing_zeros(text)
        
        self.value_entry.setText(text)
        
        self.unit_entry.setCurrentText(unit)
    
    
    def set_status(self, state:bool, message:str) -> None:
        if state:
            self.value_entry.setStyleSheet(f"background-color: #9CEC7B")
            self.value_entry.setToolTip("All good")
        else:
            self.value_entry.setStyleSheet(f"background-color: #F86A6B")
            self.value_entry.setToolTip(message)


class SweepBox(QWidget):
    def __init__(self,instrument,parent=None):
        super().__init__(parent)
        
        self.instrument = instrument
        
        layout = QHBoxLayout()
        
        self.single_sweep_button = QPushButton('Single Sweep')
        self.single_sweep_button.pressed.connect(self.single_sweep)
        layout.addWidget(self.single_sweep_button)
        
        self.cont_sweep_button = QPushButton('Continuous Sweep')
        self.cont_sweep_button.pressed.connect(self.cont_sweep)
        layout.addWidget(self.cont_sweep_button)
        
        self.abort_sweep_button = QPushButton('Stop Sweep')
        self.abort_sweep_button.pressed.connect(self.abort)
        layout.addWidget(self.abort_sweep_button)
        
        self.setLayout(layout)
    
    
    def cont_sweep(self):
        self.instrument.write_command("INIT:CONT ON")
    
    
    def single_sweep(self):
        self.instrument.write_command('INIT:CONT OFF')
        self.instrument.write_command('INIT:IMM;*WAI')
    
    
    def abort(self):
        self.instrument.write_command('ABOR')
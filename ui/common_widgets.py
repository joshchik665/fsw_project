from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QComboBox,
    QPushButton,
)


class SettingBox(QWidget):
    def __init__(self, setting_name:str, setting_measure:str, parent=None):
        super().__init__(parent)
        
        self.units = {
            'frequency': {
                'mHz': 1e-3,
                'Hz': 1,
                'kHz': 1e3,
                'MHz': 1e6,
                'GHz': 1e9,
                'THz': 1e12,
            },
            'power': {
                'dBm': 1
            }
        }
        
        layout = QHBoxLayout()
        
        self.label_button = QPushButton(setting_name)
        self.label_button.setFixedHeight(30)
        
        self.value_entry = QLineEdit()
        self.value_entry.setFixedWidth(60)
        self.value_entry.setFixedHeight(30)
        
        self.unit_entry = QComboBox()
        self.unit_entry.addItems(list(self.units[setting_measure].keys()))
        # index = self.unit_entry.findText(default_unit)
        # if index != -1:  # Check if the item exists
        #     self.unit_entry.setCurrentIndex(index)
        self.unit_entry.setFixedWidth(50)
        self.unit_entry.setFixedHeight(30)
        
        layout.addWidget(self.label_button)
        layout.addWidget(self.value_entry)
        layout.addWidget(self.unit_entry)
        layout.addStretch(1)
        
        self.setLayout(layout)
        
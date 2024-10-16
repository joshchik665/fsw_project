from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PySide6.QtGui import (
    QPixmap,
    QImage,
)
from PySide6.QtCore import (
    Qt,
    Slot,
)


class ModeSuper(QWidget):
    def __init__(self, mode, device):
        super().__init__()
        
        self.instrument = device
        self.mode = mode
        
        self._set_layout()
        self._set_title()
        self._set_header()
    
    
    def _set_layout(self):
        self.window_layout = QVBoxLayout()
        
        self.title_layout = QHBoxLayout()
        self.header_layout = QHBoxLayout()
        self.content_layout = QVBoxLayout()
        
        self.window_layout.addLayout(self.title_layout)
        self.window_layout.addLayout(self.header_layout)
        self.window_layout.addStretch(1)
        self.window_layout.addLayout(self.content_layout)
    
    
    def _set_title(self):
        title = QLabel('Rhode & Schwarz FSW-43 GUI')
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title.setObjectName('title')
        
        img= QImage('images\\crc_icon.png')
        pixmap = QPixmap(img.scaledToWidth(100))
        crc_logo = QLabel(self)
        crc_logo.setPixmap(pixmap)
        crc_logo.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addWidget(crc_logo)
        
        self.title_layout.addLayout(layout)
    
    
    def _set_header(self):
        self.load_button = QPushButton('Load Config')
        
        self.save_button = QPushButton('Save Config')
        
        visa_label = QLabel('Visa Timeout(ms):')
        
        self.visa_entry = QLineEdit()
        self.visa_entry.setPlaceholderText('3000')
        self.visa_entry.setFixedWidth(100)
        
        opc_label = QLabel('Opc Timeout(ms):')
        
        self.opc_entry = QLineEdit()
        self.opc_entry.setPlaceholderText('3000')
        self.opc_entry.setFixedWidth(100)
        
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        
        layout = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(1)
        layout.addLayout(layout2)
        
        layout1.setAlignment(Qt.AlignLeft)
        layout2.setAlignment(Qt.AlignRight)
        
        layout1.addWidget(self.load_button)
        layout1.addWidget(self.save_button)
        
        layout2.addWidget(visa_label)
        layout2.addWidget(self.visa_entry)
        layout2.addWidget(opc_label)
        layout2.addWidget(self.opc_entry)
        
        self.header_layout.addLayout(layout)
    
    
    # def _create_entry_widgets(self):
    #     self.setting_widgets = {}
    #     for name, setting in self.instrument.settings.items():
    #         if setting.is_applicable(self.mode):
    #             widget = SettingBox(setting)
    #             self.setting_widgets[name] = widget
    #     self.apply_button = QPushButton('Apply & Verify Settings')
    #     self.apply_button.pressed.connect(self._apply_entry_settings)
    
    
    # @Slot()
    # def _apply_entry_settings(self):
    #     values = {key: setting.get_value() for key, setting in self.setting_widgets.items()}
        
    #     self.instrument.set_settings(values)
        
    #     correct = self.instrument.verify_all_settings()
        
    #     self._display_current_values()
        
    #     self._update_colors(correct)
    
    
    # def _display_current_values(self):
        
    #     values = {key: setting.current_value for key, setting in self.instrument.settings.items()}
        
    #     for key, widget in self.setting_widgets.items():
    #         widget.set_value(values[key])
    #         widget.set_status('Unchecked')
    
    
    # def _update_colors(self, correct:dict):
    #     for key, widget in self.setting_widgets.items():
    #         widget.set_status(correct[key])
    
    
    def set_mode(self,previous_tab_index:int):
        
        mode_index = {
            '0': 'Spectrum',
            '1': 'Real-Time Spectrum',
            '2': 'Zero-Span'
        }
        
        mode_scpi_commands = {
            'Spectrum': "SANALYZER",
            'Real-Time Spectrum': "RTIM",
            'Zero-Span': 'SANALYZER',
        }
        
        command = f"INST:CRE:REPL '{mode_index[str(previous_tab_index)]}', {mode_scpi_commands[self.mode]}, '{self.mode}'"
        
        self.instrument.write_command(command)




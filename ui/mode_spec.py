from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from fsw.device import RsFswInstrument


class ModeSpec(QWidget):
    def __init__(self):
        super().__init__()
        
        self.window_layout = QVBoxLayout()
        
        self.title_layout = QHBoxLayout()
        self.header_layout = QHBoxLayout()
        self.content_layout = QHBoxLayout()
        
        self.window_layout.addLayout(self.title_layout)
        self.window_layout.addLayout(self.header_layout)
        self.window_layout.addLayout(self.content_layout)
        
        self.instrument = RsFswInstrument.get_instance()
        
        
        
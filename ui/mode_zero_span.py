from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from ui.mode_super import ModeSuper

class ModeZs(ModeSuper):
    def __init__(self,device):
        super().__init__('Zero-Span',device)

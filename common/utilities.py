from PySide6.QtWidgets import QFileDialog
import ui.message_boxes as mb

def open_file_dialog(parent = None):
        file_path, __ = QFileDialog.getOpenFileName(parent,'Open .json file','','JSON Files (*.json)')
        
        if not file_path:
            return 0
        if not file_path.endswith('.json'):
            mb.invalid_filetype()
            return 0
        else:
            return file_path
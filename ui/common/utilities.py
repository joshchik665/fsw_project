from PySide6.QtWidgets import QFileDialog
import ui.common_gui.message_boxes as mb


def open_file_dialog(prompt:str, filetype:str, parent = None) -> str:
    filetypes = {
        '.json': 'JSON Files (*.json)',
    }
    
    file_path, __ = QFileDialog.getOpenFileName(parent,prompt,r'configs\user_configs',filetypes[filetype])
    
    if not file_path:
        return ''
    elif not file_path.endswith(filetype):
        mb.invalid_filetype()
        return ''
    else:
        return file_path


def save_file_dialog(prompt:str, filetype:str, parent = None) -> str:
    filetypes = {
        '.json': 'JSON Files (*.json)',
    }
    
    file_path, __ = QFileDialog.getSaveFileName(parent,prompt,r'configs\user_configs',filetypes[filetype])
    
    return file_path


def remove_trailing_zeros(string:str) -> str:
    while string.endswith('0'):
        string = string[:-1]
    if string.endswith('.'):
        string = string[:-1]
    return string
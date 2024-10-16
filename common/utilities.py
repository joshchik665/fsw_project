from PySide6.QtWidgets import QFileDialog
import ui.message_boxes as mb
import math

def open_file_dialog(prompt:str, filetype:str, parent = None) -> str:
    filetypes = {
        '.json': 'JSON Files (*.json)',
    }
    
    file_path, __ = QFileDialog.getOpenFileName(parent,prompt,'',filetypes[filetype])
    
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
    
    file_path, __ = QFileDialog.getSaveFileName(parent,prompt,'',filetypes[filetype])
    
    return file_path
    
    # if not file_path:
    #     return ''
    # elif not file_path.endswith(filetype):
    #     mb.invalid_filetype()
    #     return ''
    # else:
    #     return file_path


def is_number(string:str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def compare_number_strings(str1:str, str2:str) -> bool:
    try:
        num1 = float(str1)
        num2 = float(str2)
        
        return math.isclose(num1,num2)
    except ValueError:
        # conversion failed
        return False
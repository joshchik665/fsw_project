# widgets.py

from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QLineEdit, 
    QLabel, 
    QComboBox,
    QCheckBox
)
from PySide6.QtCore import Signal



class DictEdit(QWidget):
    def __init__(self, name:str, dictionary:dict):
        """Creates a widget that allows editing of a dictionary containing str:str"""
        super().__init__()
        
        self.widget_layout = QVBoxLayout()
        
        self.dictionary = dictionary
        
        self.key_widgets = {}
        self.value_widgets = {}
        self.layouts = {}
        self.delete_buttons = {}
        
        layout1 = QHBoxLayout()
        
        self.name_label = QLabel(name)
        layout1.addWidget(self.name_label)
        
        layout1.addStretch(1)
        
        self.add_button = QPushButton("Add entry")
        self.add_button.pressed.connect(self.add_entry)
        layout1.addWidget(self.add_button)
        
        self.widget_layout.addLayout(layout1)
        
        for key, value in self.dictionary.items():
            layout = QHBoxLayout()
            self.layouts[key] = layout
            
            key_widget = QLineEdit()
            key_widget.setText(key)
            self.key_widgets[key] = key_widget
            layout.addWidget(key_widget)
            
            value_widget = QLineEdit()
            value_widget.setText(str(value))
            self.value_widgets[key] = value_widget
            layout.addWidget(value_widget)
            
            button = QPushButton("Delete")
            self.delete_buttons[key] = button
            self.delete_buttons[key].setObjectName("delete-button")
            self.delete_buttons[key].pressed.connect(lambda key=key: self.delete(key))
            layout.addWidget(self.delete_buttons[key])
            
            self.widget_layout.addLayout(layout)
        
        self.setLayout(self.widget_layout)
    
    
    def add_entry(self):
        """Add a new entry to the dictionary"""
        layout = QHBoxLayout()
        
        key_widget = QLineEdit()
        layout.addWidget(key_widget)
        
        value_widget = QLineEdit()
        layout.addWidget(value_widget)
        
        button = QPushButton(" Add ")
        button.pressed.connect(lambda: self.add(layout, key_widget, value_widget, button))
        layout.addWidget(button)
        
        self.widget_layout.addLayout(layout)

    
    def add(self, layout, key_widget, value_widget, button):
        """Add a line to the dictionary"""
        key = key_widget.text()
        self.layouts[key] = layout
        self.key_widgets[key] = key_widget
        self.value_widgets[key] = value_widget
        
        button.setObjectName("delete-button")
        button.style().polish(button)
        self.delete_buttons[key] = button
        self.delete_buttons[key].setText("Delete")
        self.delete_buttons[key].pressed.connect(lambda: self.delete(key))
    
    
    def delete(self, key:str):
        """Delete an entry from the dictionary"""
        self.key_widgets[key].deleteLater()
        self.value_widgets[key].deleteLater()
        self.delete_buttons[key].deleteLater()
        self.widget_layout.removeItem(self.layouts[key])
        
        self.key_widgets.pop(key)
        self.value_widgets.pop(key)
        self.delete_buttons.pop(key)
        self.layouts.pop(key)
    
    
    def get_value(self):
        """Return the dictionary"""
        dict = {}
        for key in self.key_widgets.keys():
            dict[self.key_widgets[key].text()] = self.value_widgets[key].text()
        return dict


class SettingEdit(QWidget):
    def __init__(self, name:str, value:str, requried:bool):
        """Creates a custom widget where the user can enter a string"""
        super().__init__()
        
        self.name = name
        self.required = requried
        
        layout = QHBoxLayout()
        
        label = QLabel(name)
        label.setFixedSize(200, 25)
        layout.addWidget(label)
        
        self.entry = QLineEdit()
        self.entry.setFixedSize(500, 25)
        if self.required:
            self.entry.textEdited.connect(self.set_status)
        self.entry.setText(value)
        layout.addWidget(self.entry)
        
        self.setLayout(layout)
        
        self.set_status()
    
    
    def set_status(self) -> None:
        """If the setting is required, it will highlight the field in red"""
        if not self.entry.text():
            self.entry.setStyleSheet("QLineEdit {border-radius: 5px; padding: 5px; border: 1px solid #8f8f91; background-color: #FDACB8;}")
        else:
            self.entry.setStyleSheet("QLineEdit {border-radius: 5px; padding: 5px; border: 1px solid #8f8f91; background-color: white;}")
    
    
    def get_value(self) -> str:
        """Returns the current falue as a string"""
        text = self.entry.text()
        if self.required and not text:
            print(f"Setting: {self.name} is required!")
        return text


class SettingEditCombo(QWidget):
    
    valueChanged = Signal(str)
    
    def __init__(self, name:str, value:str, requried:bool, values:tuple):
        """Custom widget that allows user to select between a list of entries"""
        super().__init__()
        
        self.name = name
        self.values = values
        self.required = requried
        
        layout = QHBoxLayout()
        
        label = QLabel(name)
        label.setFixedSize(200, 25)
        layout.addWidget(label)
        
        self.entry = QComboBox()
        self.entry.setFixedSize(500, 25)
        
        self.entry.addItems(values)
        
        if self.required:
            self.entry.currentIndexChanged.connect(self.set_status)
        
        self.entry.setCurrentText(value)
        
        layout.addWidget(self.entry)
        
        self.setLayout(layout)
        
        self.set_status(0)
    
    
    def set_status(self, index):
        """if the fiels is required and filed is none, highlights in red"""
        text = self.entry.currentText()
        
        self.valueChanged.emit(text)
        
        if self.entry.currentText() == "none":
            self.entry.setStyleSheet("QComboBox {border-radius: 5px; padding: 5px; border: 1px solid #8f8f91; background-color: #FDACB8;}")
        else:
            self.entry.setStyleSheet("QComboBox {border-radius: 5px; padding: 5px; border: 1px solid #8f8f91; background-color: white;}")
    
    
    def get_value(self):
        """Returns the current value"""
        text = self.entry.currentText()
        if self.required and not text:
            print(f"Setting: {self.name} is required!")
        return text


class toggleList(QWidget):
    def __init__(self, options, checked_options = [], parent=None):
        """Creates a field of checkboxes that the user can select"""
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        self._checkboxes = []
        
        for option in options:
            checkbox = QCheckBox(str(option))
            layout.addWidget(checkbox)
            self._checkboxes.append(checkbox)
            if str(option) in checked_options:
                checkbox.setChecked(True)
        
        layout.addStretch(1)
        
        self.setLayout(layout)
    
    
    def get_value(self):
        """
        Returns a list of checked items
        
        Returns:
            list: List of checked item texts
        """
        return [
            checkbox.text() 
            for checkbox in self._checkboxes 
            if checkbox.isChecked()
        ]


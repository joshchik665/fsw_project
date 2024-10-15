# settings_manager.py

from fsw.config import SETTINGS, MODES
from fsw.device import RsFswInstrument
import math

class SettingsManager:
    def __init__(self, instrument):
        self.settings = SETTINGS
        self.instrument = instrument
    
    
    def set_settings(self, settings:dict):
        for setting_name, setting_value in settings.items():
            self.set_setting(setting_name, setting_value)
    
    
    def set_setting(self, setting_name:str, value:str) -> bool:
        try:
            setting = self.settings[setting_name]
        except KeyError:
            print(f"Setting: {setting_name}, is not known!")
            return False
        
        if not setting.is_applicable(self.instrument.mode):
            print(f"Setting: {setting_name} is not applicable in mode: {self.instrument.mode}")
            return False
        
        if not self.is_number(value):
            print(f"Value: {value}, is not a numeric value!")
            return False
        
        command = setting.get_set_command()
        self.instrument.write_command(f"{command} {value}")
        setting.set_current_value(value)
        return True
    
    
    def verify_setting(self, setting_name:str) -> str:
        try:
            setting = self.settings[setting_name]
        except KeyError:
            print(f"Setting: {setting_name}, is not known!")
            return 'Error'
        
        if not setting.is_applicable(self.instrument.mode):
            print(f"Setting: {setting_name} is not applicable in mode: {self.instrument.mode}")
            return 'Invalid'
        
        command = setting.get_query_command()
        
        try:
            response = self.instrument.query_command(command)
            
            if self.compare_number_strings(setting.current_value, response):
                return 'Correct'
            else:
                setting.current_value = response
                return 'Incorrect'
        except Exception as e:
            print(f"Error querying {setting_name}: {str(e)}")
            return 'Error'
    
    
    def verify_all_settings(self) -> dict:
        return {name: self.verify_setting(name) for name in self.settings if self.settings[name].is_applicable(self.instrument.mode)}
    
    
    
    def compare_number_strings(self, str1:str, str2:str) -> bool:
        try:
            num1 = float(str1)
            num2 = float(str2)
            
            return math.isclose(num1,num2)
        except ValueError:
            # conversion failed
            return False
    
    
    def is_number(self, string:str) -> bool:
        try:
            float(string)
            return True
        except ValueError:
            return False
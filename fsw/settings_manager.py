# settings_manager.py

from fsw.device import RsFswInstrument
import common.utilities as util
from fsw.setting import Setting
import json

class SettingsManager(RsFswInstrument):
    def __init__(self, ip_address,default_config_filepath):
        super().__init__(ip_address)
        
        self.current_mode = 'Spectrum' # Default mode on startup
        
        with open(default_config_filepath, 'r') as file:
            config = json.load(file)
        
        self.settings = {name: Setting.from_dict(**setting) for name, setting in config.items()}
    
    
    def get_setting_object(self, setting_name:str) -> Setting:
        return self.settings[setting_name]
    
    
    def set_all_settings(self, settings:dict):
        return {name: self.set_setting(name, value) for name, value in settings.items()}
    
    
    def set_setting(self, setting_name:str, value:str) -> tuple[bool, str]:
        try:
            setting = self.settings[setting_name]
        except KeyError:
            print(f"Setting: {setting_name}, is not known!")
            return 'Setting unknown'
        
        if not setting.is_applicable(self.current_mode):
            print(f"Setting: {setting_name} is not applicable in mode: {self.current_mode}")
            return 'Setting is not applicable'
        
        if not setting.check_if_valid_value(value):
            print(f"Value: {value}, is not valid for this setting")
            return 'Value is not valid for this setting'
        
        command_list = setting.get_scpi_command(value)
        
        try:
            for command in command_list:
                self.write_command(command)
            setting.current_value = value
        except Exception as e:
            print(f"Error querying {setting_name}: {str(e)}")
            return f'Error writing setting: {str(e).split(',')[1]}'
        
        return 'Set Command Sucess'
    
    
    def verify_all_settings(self, settings:list) -> dict:
        return {name: self.verify_setting(name) for name in settings}
    
    
    def verify_setting(self, setting_name:str) -> tuple[bool, str]:
        try:
            setting = self.settings[setting_name]
        except KeyError:
            print(f"Setting: {setting_name}, is not known!")
            return (False, 'setting unknown')
        
        if not setting.is_applicable(self.current_mode):
            print(f"Setting: {setting_name} is not applicable in mode: {self.current_mode}")
            return (False, 'setting not applicable')
        
        command = f"{setting.scpi_command}?"
        
        try:
            response = self.query_command(command)
        except Exception as e:
            print(f"Error querying {setting_name}: {str(e).split(',')[1]}")
            return (False, f'error querying setting: {str(e).split(',')[1]}')
        
        if util.compare_number_strings(setting.current_value, response):
            return (True, 'verified')
        else:
            setting.current_value = response
            return (False, 'incorrect')
    
    
    def set_mode(self, mode:str) -> None:
        mode_scpi = {
            'Spectrum': "SANALYZER",
            'Real-Time Spectrum': "RTIM",
            'Zero-Span': 'SANALYZER',
        }
        
        command = f"INST:CRE:REPL '{self.current_mode}', {mode_scpi[mode]}, '{mode}'"
        
        self.write_command(command)
        
        self.current_mode = mode


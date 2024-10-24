# settings_manager.py

from fsw.device.device import RsFswInstrument
from fsw.common.common_functions import is_number, compare_number_strings
from typing import Union
from fsw.setting_objects.numerical_setting import NumericalSetting
from fsw.setting_objects.mode_setting import ModeSetting
import json

class SettingsManager(RsFswInstrument):
    def __init__(self, ip_address:str, default_config_filepath:str, visa_timeout:int, opc_timeout:int):
        super().__init__(ip_address, visa_timeout, opc_timeout)
        
        self.current_mode = 'Spectrum' # Default mode on startup
        
        with open(default_config_filepath, 'r') as file:
            config = json.load(file)
        
        self.numerical_settings = {name: NumericalSetting.from_dict(name,**setting) for name, setting in config["Numerical Settings"].items()}
        self.mode_settings = {name: ModeSetting.from_dict(name,**setting) for name, setting in config["Mode Settings"].items()}
        
        self.settings = self.mode_settings | self.numerical_settings
    
    
    def setting_known(self, setting_name:str):
        return setting_name in self.settings.keys()
    
    
    def get_setting_object(self, setting_name:str) -> Union[NumericalSetting, ModeSetting]:
        return self.settings[setting_name]
    
    
    def set_all_settings(self, settings:dict) -> dict:
        return {name: self.set_setting(name, value) for name, value in settings.items()}
    
    
    def set_setting(self, setting_name:str, value:str) -> tuple[bool, str]:
        if not self.setting_known(setting_name):
            return False, 'Setting Unknown'
        
        setting = self.settings[setting_name]
        
        if not setting.is_applicable(self.current_mode):
            return False, 'Setting is not applicable'
        
        if not setting.check_if_valid_value(value):
            return False, 'Value is not valid for this setting'
        
        command_list = setting.get_write_scpi_command(value).split(";")
        
        try:
            for command in command_list:
                self.write_command(command)
            
            setting.current_value = value
        except Exception as e:
            return False, f'Error writing setting: {str(e).split(',')[1]}'
        
        return True, 'Set sucessful'
    
    
    def verify_all_settings(self, settings:list) -> dict:
        return {name: self.verify_setting(name) for name in settings}
    
    
    def verify_setting(self, setting_name:str) -> tuple[bool, str]:
        if not self.setting_known(setting_name):
            return False, 'Setting Unknown'
        
        setting = self.settings[setting_name]
        
        if not setting.is_applicable(self.current_mode):
            return False, 'Setting is not applicable'
        
        command = setting.get_query_scpi_command()
        
        try:
            response = self.query_command(command)
        except Exception as e:
            return False, f'Error querying setting: {str(e).split(',')[1]}'
        
        if is_number(response) and compare_number_strings(setting.current_value, response):
            return True, 'Setting verified'
        elif setting.current_value == response:
            return True, 'Setting verified'
        else:
            setting.current_value = response
            return False, f'Setting set incorrect:{response}'
    
    
    def set_mode(self, mode:str) -> None:
        mode_scpi = {
            'Spectrum': "SANALYZER",
            'Real-Time Spectrum': "RTIM",
            'Zero-Span': 'SANALYZER',
        }
        
        command = f"INST:CRE:REPL '{self.current_mode}', {mode_scpi[mode]}, '{mode}'"
        
        self.write_command(command)
        
        self.current_mode = mode


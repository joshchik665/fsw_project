# settings_manager.py

from device.base_classes.device import Instrument
from device.setting_classes.numerical_setting import NumericalSetting
from device.setting_classes.mode_setting import ModeSetting

import json
import math
import os

class SettingsManager(Instrument):
    def __init__(self, ip_address:str, settings_config_filepath:str = None):
        """Initializes the Setting Manager instrument that controls all the settings on the instrument

        Args:
            ip_address (str): IP Address of the instrument
            default_config_filepath (str): String containing a file path to the setting config file
            visa_timeout (int): Visa timeout in milliseconds
            opc_timeout (int): OPC timeout in milliseconds
        """
        super().__init__(ip_address)
        
        if not settings_config_filepath:
            directory = r"device\configs\settings"
            
            for filename in os.listdir(directory):
                
                filepath = os.path.join(directory, filename)
                
                if filename.endswith('.json') and os.path.isfile(filepath):
                    with open(filepath, 'r') as file:
                        data = json.load(file)
                    
                    if data.get("IDN","") in self.idn:
                        config = data
                        self.device_type = data.get("Device Name")
        else:
            with open(settings_config_filepath, 'r') as file: # Opens file containing all the settings
                config = json.load(file)
        
        self.current_mode = config["Default Mode"] # Default mode on startup
        
        self.mode_scpi = config["Modes SCPI Commands"] # Scpi commands to change modes
        
        self.modes = self.mode_scpi.keys()
        
        # Initializes the Setting objects and puts them into dictionaries. The dictionaries are combined together into joint dictionary
        self.numerical_settings = {name: NumericalSetting.from_dict(name,**setting) for name, setting in config["Settings"].items() if setting["setting_type"] == "numerical"}
        self.mode_settings = {name: ModeSetting.from_dict(name,**setting) for name, setting in config["Settings"].items() if setting["setting_type"] == "mode"}
        self.settings = self.mode_settings | self.numerical_settings
    
    
    def setting_known(self, setting_name:str) -> bool:
        """Checks if the setting is in the settings dictionary

        Args:
            setting_name (str): The setting name to check

        Returns:
            bool: Result to check
        """
        return setting_name in self.settings.keys()
    
    
    def get_setting_object(self, setting_name:str) -> NumericalSetting | ModeSetting:
        """Returns the setting object from the settings dictionary

        Args:
            setting_name (str): Name of the setting to get

        Returns:
            Union[NumericalSetting, ModeSetting]: Returns the setting object
        """
        return self.settings[setting_name]
    
    
    def set_all_settings(self, settings:dict[str,str]) -> dict[str,tuple[bool, str]]:
        """Sets a whole dictionary of settings on the instrument

        Args:
            settings (dict): Input dictionary of settings to set. The dict has setting name as keys and setting values as values

        Returns:
            dict: returns a dictionary of results from the process of setting the settings. 
            Keys are the setting names, values are tuples containing a boolean for results and a status string
        """
        return {name: self.set_setting(name, value) for name, value in settings.items()}
    
    
    def set_setting(self, setting_name:str, value:str) -> tuple[bool, str]:
        """Sets a single setting

        Args:
            setting_name (str): Name of the setting to be set
            value (str): Value of the setting

        Returns:
            tuple[bool, str]: Results a tupple containing results, boolean for setting result and string for status
        """
        # Checks if the setting is known
        if not self.setting_known(setting_name):
            return False, 'Setting Unknown'
        
        setting = self.settings[setting_name] # Get setting object
        
        # Checks if the setting is applicable in the mode
        if not setting.is_applicable(self.current_mode):
            return False, 'Setting is not applicable'
        
        # Check if the value passed is a valid value for the setting
        if not setting.check_if_valid_value(value):
            return False, 'Value is not valid for this setting'
        
        # Get SCPI command. The command is stored as a list for settings that require multiple commands to set
        command_list = setting.get_write_scpi_command(value).split(";") 
        try:
            # Try writing the full command to thei instrument
            for command in command_list:
                self.write_command(command)
        except Exception as e:
            # Error writing setting
            return False, f'Error writing setting: {e}'
        
        setting.set_current_value(value) # Set the current value in the object
        
        return True, 'Set sucessful'
    
    
    def verify_all_settings(self, settings:list[str]) -> dict[str,tuple[bool, str]]:
        """Verify a list of settings

        Args:
            settings (list): A list of setting names to verify

        Returns:
            dict: Returns a dictionary with setting names a keys and verify result
        """
        return {name: self.verify_setting(name) for name in settings}
    
    
    def verify_setting(self, setting_name:str) -> tuple[bool, str]:
        """Verify a single setting on the instrument

        Args:
            setting_name (str): The name of the setting to verify

        Returns:
            tuple[bool, str]: Contains the result from the verifying of the setting
        """
        # Check if the setting is known
        if not self.setting_known(setting_name):
            return False, 'Setting Unknown'
        
        setting = self.settings[setting_name] # Get setting object
        
        # Check if the setting is applicable in the current mode
        if not setting.is_applicable(self.current_mode):
            return False, 'Setting is not applicable'
        
        command = setting.get_query_scpi_command() # Get query command
        
        try:
            # Try to get the value from the device
            response = self.query_command(command).split("\n")[0]
        except Exception as e:
            return False, f'Error querying setting: {e}'
        
        # Check to see if the value is set correctly
        if self.is_number(response) and self.compare_number_strings(setting.current_value, response):
            return True, 'Setting verified'
        elif setting.current_value == response:
            return True, 'Setting verified'
        else:
            setting.set_current_value(response)
            return False, f'Setting set incorrect:{response}'
    
    
    def set_mode(self, mode:str) -> None:
        """Set the instrument mode

        Args:
            mode (str): Mode to be set
        """
        command = f"INST:CRE:REPL '{self.current_mode}', {self.mode_scpi[mode]}, '{mode}'" # Command to change mode
        
        self.write_command(command)
        
        self.current_mode = mode # update the current mode
    
    
    def is_number(self, string:str) -> bool:
        """Checks if string passed could be a number

        Args:
            string (str): imput string

        Returns:
            bool: returns true if string represents a number
        """
        try:
            float(string)
            return True
        except ValueError:
            return False


    def compare_number_strings(self, str1:str, str2:str) -> bool:
        """ Compares two strings that contain numbers, returns true if the match

        Args:
            str1 (str): string 1
            str2 (str): string 2

        Returns:
            bool: Comparison result
        """
        try:
            num1 = float(str1)
            num2 = float(str2)
            
            return math.isclose(num1,num2)
        except ValueError:
            return False


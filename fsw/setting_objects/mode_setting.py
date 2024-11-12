# mode_setting.py

from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class ModeSetting:
    name: str
    default_value: str
    write_commands: Dict[str, str]
    query_command: str
    applicable_modes: set[str]
    setting_type: str
    current_value: Optional[Any] = None
    alias: Optional[Dict[str, str]] = None
    custom_modes: Optional[dict[str, set[str]]] = None
    
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.default_value
    
    
    @classmethod
    def from_dict(cls, name:str, **data):
        """Returns an instance of the Mode Setting from the dictionary. This is used because I want __post_init_ to be called

        Args:
            name (str): Name of the setting, will be become the name attribute of the class

        Returns:
            ModeSetting: An instane of this class
        """
        instance = cls(name=name,**data)
        instance.__post_init__()
        return instance
    
    
    def get_write_scpi_command(self, value:str) -> str:
        """Gets the SCPI command to set the value of the setting

        Args:
            value (str): Mode to be set on the instrument

        Returns:
            str: SCPI command to set that setting
        """
        if self.alias is not None:
            if value in self.alias:
                return self.write_commands[self.alias[value]]
        return self.write_commands[value]
    
    
    def get_query_scpi_command(self) -> str:
        """Gets the command to query the setting

        Returns:
            str: The query command
        """
        return self.query_command
    
    
    def is_applicable(self, mode: str) -> bool:
        """Checks if this setting is applicable in the mode

        Args:
            mode (str): Mode to check

        Returns:
            bool: True if the setting is applicable, false otherwise
        """
        return mode in self.applicable_modes
    
    
    def check_if_valid_value(self, value: str) -> bool:
        """Checks to see if the value is valid for this setting

        Args:
            value (str): value to set this setting to

        Returns:
            bool: True if that value is valid
        """
        if self.alias is not None:
            if value in self.alias:
                return True
        return value in self.write_commands
    
    
    def set_current_value(self, value: str) -> None:
        """Sets the current value, needed to convert from an alias

        Args:
            value (str): Value to set as current value
        """
        if self.alias is not None:
            if value in self.alias:
                self.current_value = self.alias[value]
                return
        self.current_value = value





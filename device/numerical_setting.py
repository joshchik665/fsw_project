# numerical_setting.py

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class NumericalSetting:
    name: str
    measure: str
    default_value: str
    write_command: str
    query_command: str
    setting_type: str
    applicable_modes: set[str]
    current_value: Optional[Any] = None
    
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.default_value
    
    
    @classmethod
    def from_dict(cls, name:str, **data):
        """Returns an instance of this class initialized with the values provided, used so that __post_init__ gets called

        Args:
            name (str): The name of the setting, will become the name attribute of this object

        Returns:
            NumericalSetting: An instance of this class
        """
        instance = cls(name=name,**data)
        instance.__post_init__()
        return instance
    
    
    def get_write_scpi_command(self, value:str) -> str:
        """Gets the SCPI command to write a value to the instrument

        Args:
            value (str): value to be set in the instrument

        Returns:
            str: SCPI command to set the value on the instrument
        """
        return f"{self.write_command} {value}"
    
    
    def get_query_scpi_command(self) -> str:
        """Get the command to query this setting on the instrument

        Returns:
            str: SCPI command to query this setting
        """
        return self.query_command
    
    
    def is_applicable(self, mode: str) -> bool:
        """Checks to see if this setting is applicable in mode

        Args:
            mode (str): Mode to be checked

        Returns:
            bool: The result from the check
        """
        return mode in self.applicable_modes
    
    
    def check_if_valid_value(self, value: str) -> bool:
        """Check to see if a value is valid to be set on ths instrument for this setting

        Args:
            value (str): value to be written to the setting

        Returns:
            bool: True if the value is valid for this setting (is a number)
        """
        return self.is_number(value)
    
    
    def set_current_value(self, value: str) -> None:
        """Set the current value

        Args:
            value (str): The value to set as the current value
        """
        self.current_value = value
    
    
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
# display_setting.py

from dataclasses import dataclass
from typing import Optional, Any, Dict

@dataclass
class DisplaySetting:
    name: str
    measure: str
    default_value: str
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
    

    def set_current_value(self, value: str) -> None:
        """Set the current value

        Args:
            value (str): The value to set as the current value
        """
        self.current_value = value
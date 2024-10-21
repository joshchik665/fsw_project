from dataclasses import dataclass
from typing import Optional, Any, List, Dict, Union
import common.utilities as util
from enum import Enum


@dataclass
class Setting:
    name: str
    measure: str
    applicable_modes: List[str]
    default_value: Optional[Any] = None
    options: Optional[Dict[str, str]] = None
    current_value: Optional[Any] = None
    
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.default_value
        if self.options is None:
            self.options = {}
    
    
    @classmethod
    def from_dict(cls, name:str, **data):
        instance = cls(name=name,**data)
        instance.__post_init__()
        return instance
    
    
    def get_write_scpi_command(self, value=None) -> list:
        if value in self.options:
            return self.options[value].split(";")
        else:
            return [f"{self.options["numerical"]} {value}"]
    
    
    def is_applicable(self, mode: str) -> bool:
        return mode in self.applicable_modes
    
    
    def check_if_valid_value(self, value: Any) -> bool:
        if value == "numerical": 
            return False
        
        if value in self.options:
            return True
        
        if util.is_number(value):
            return True
        
        return False




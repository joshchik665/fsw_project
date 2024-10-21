from dataclasses import dataclass
from typing import Optional, Any, Dict
import common.utilities as util


@dataclass
class Setting:
    name: str
    measure: str
    default_value: str
    applicable_modes: set[str]
    options: Dict[str, str]
    current_value: Optional[Any] = None
    
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.default_value
    
    
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
    
    
    def get_query_scpi_command(self) -> list:
        pass
    
    
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




from dataclasses import dataclass
from typing import Optional, Any, List, Dict, Union
import common.utilities as util

@dataclass
class Setting:
    name: str
    scpi_command: str
    measure: str
    applicable_modes: List[str]
    default_value: Optional[Any] = None
    current_value: Optional[Any] = None
    options: Optional[Dict] = None
    
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.default_value
    
    
    # here because __post_init__ is not called when init from dict
    @classmethod
    def from_dict(cls, **data):
        instance = cls(**data)
        instance.__post_init__()
        return instance
    
    
    def get_scpi_command(self) -> Union[str, dict]:
        if self.options is None:
            return self.scpi_command
        else:
            return self.options
    
    def is_applicable(self, mode: str) -> bool:
        return mode in self.applicable_modes
    
    
    def check_if_valid_value(self, value:str) -> bool:
        if not self.options:
            return util.is_number(value)
        else:
            return value in self.options.keys()
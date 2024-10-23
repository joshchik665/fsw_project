from dataclasses import dataclass
from typing import Optional, Any, Dict
import common.utilities as util


@dataclass
class ModeSetting:
    name: str
    default_value: str
    write_commands: Dict[str, str]
    query_command: str
    applicable_modes: set[str]
    current_value: Optional[Any] = None
    
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.default_value
    
    
    @classmethod
    def from_dict(cls, name:str, **data):
        instance = cls(name=name,**data)
        instance.__post_init__()
        return instance
    
    
    def get_write_scpi_command(self, value:str) -> str:
        return self.write_commands[value]
    
    
    def get_query_scpi_command(self) -> str:
        return self.query_command
    
    
    def is_applicable(self, mode: str) -> bool:
        return mode in self.applicable_modes
    
    
    def check_if_valid_value(self, value: str) -> bool:
        return value in self.write_commands





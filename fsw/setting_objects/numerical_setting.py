from dataclasses import dataclass
from typing import Optional, Any
from fsw.common.common_functions import is_number


@dataclass
class NumericalSetting:
    name: str
    measure: str
    default_value: str
    write_command: str
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
        return f"{self.write_command} {value}"
    
    
    def get_query_scpi_command(self) -> str:
        return self.query_command
    
    
    def is_applicable(self, mode: str) -> bool:
        return mode in self.applicable_modes
    
    
    def check_if_valid_value(self, value: Any) -> bool:
        return is_number(value)
from dataclasses import dataclass
from typing import Optional, Any, List
import common.utilities as util

@dataclass
class Setting:
    name: str
    scpi_command: str
    measure: str
    applicable_modes: List[str]
    default_value: Optional[Any] = None
    current_value: Optional[Any] = None
    options: Optional[List[str]] = None
    
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.default_value
    
    
    # here because __post_init__ is not called when init from dict
    @classmethod
    def from_dict(cls, **data):
        instance = cls(**data)
        instance.__post_init__()
        return instance
    
    
    def is_applicable(self, mode: str) -> bool:
        return mode in self.applicable_modes
    
    
    def check_if_valid_value(self, value:str) -> bool:
        if not self.options:
            return util.is_number(value)
        else:
            return value in self.options








# #from fsw.device import RsFswInstrument

# class RsFswSetting():
#     def __init__(self,device,setting_name,scpi_command,modes,measure):
        
#         self.setting_name = setting_name
#         self.scpi_command = scpi_command
#         self.modes = modes
#         self.measure = measure
        
#         self.instrument = device
        
#         self.value = '0'
        
#         self.status = False
        
#         self.check_status()
    
    
#     def check_status(self):
#         if self.instrument.mode in self.modes:
#             self.status = True
#         else:
#             self.value = '0'
#             self.status = False
    
    
#     def check_value(self,value):
#         self.get_value()
#         if value == self.value:
#             return True
#         else:
#             return False
    
    
#     def get_value(self):
#         if self.status:
#             self.value = self.intrument.query_str_with_opc(f"{self.scpi_command}?")
    
    
#     def set_value(self, value):
#         if self.status:
#             self.instrument.write_str_with_opc(f"{self.scpi_command} {value}")
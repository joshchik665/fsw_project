from dataclasses import dataclass
from typing import Optional, Any, List

@dataclass
class Setting:
    name: str
    scpi_command: str
    measure: str
    applicable_modes: List[str]
    default_value: Optional[Any] = None
    current_value: Optional[Any] = None
    
    
    def __post_init__(self):
        self.current_value = self.default_value
    
    
    def is_applicable(self, mode: str) -> bool:
        return mode in self.applicable_modes
    
    
    def set_current_value(self, value:str):
        self.current_value = value
    
    
    def get_query_command(self) -> str:
        return f"{self.scpi_command}?"
    
    
    def get_set_command(self) -> str:
        return self.scpi_command







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
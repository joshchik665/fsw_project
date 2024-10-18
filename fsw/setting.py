from dataclasses import dataclass
from typing import Optional, Any, List, Dict, Union
import common.utilities as util
from enum import Enum

NUMERICAL_VALUE_KEY = 'numerical'


class SettingType(Enum):
    MODE_ONLY = "mode_only"
    VALUE_ONLY = "value_only"
    BOTH = "both"

@dataclass
class Setting:
    name: str
    scpi_command: str
    measure: str
    applicable_modes: List[str]
    setting_type: SettingType
    default_value: Optional[Any] = None
    options: Optional[Dict[str, str]] = None
    current_value: Optional[Any] = None
    
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.default_value
        if self.options is None:
            self.options = {}
        if self.setting_type in [SettingType.VALUE_ONLY, SettingType.BOTH]:
            self.options[NUMERICAL_VALUE_KEY] = self.scpi_command
    
    
    # here because __post_init__ is not called when init from dict
    @classmethod
    def from_dict(cls, **data):
        # Convert setting_type string to enum
        # if 'setting_type' in data:
        #     data['setting_type'] = SettingType[data['setting_type']]
        
        if 'setting_type' in data:
            setting_type_str = data['setting_type']
            data['setting_type'] = next(
                (st for st in SettingType if st.value == setting_type_str),
                None
            )
            if data['setting_type'] is None:
                raise ValueError(f"Invalid setting_type: {setting_type_str}")
        
        instance = cls(**data)
        instance.__post_init__()
        return instance
    
    
    def get_scpi_command(self, value=None) -> str:
        if value in self.options:
            return self.options[value].split(";")
        if self.setting_type in [SettingType.VALUE_ONLY, SettingType.BOTH]:
            return [f"{self.options[NUMERICAL_VALUE_KEY]} {value}"]
        raise ValueError("Invalid setting value")
    
    
    def is_applicable(self, mode: str) -> bool:
        return mode in self.applicable_modes
    
    
    def check_if_valid_value(self, value: Any) -> bool:
        if self.setting_type == SettingType.MODE_ONLY:
            return value in self.options
        elif self.setting_type == SettingType.VALUE_ONLY:
            return util.is_number(value)
        else:  # BOTH
            return value in self.options or (value != NUMERICAL_VALUE_KEY and util.is_number(value))




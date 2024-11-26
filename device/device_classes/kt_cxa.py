# kt_cxa.py

from device.base_classes.settings_manager import SettingsManager
import json

class KtCxa(SettingsManager):
    def __init__(self, ip_address:str):
        with open(r"device\configs\device_types\configs.json") as file:
            config = json.load(file)
        
        self.device_type = "Keysight Technologies CXA N9000B"
        
        super().__init__(ip_address, config[self.device_type])
    
    
    def abort(self) -> None:
        """Aborts the current measurment
        """
        self.write_command("ABOR")
    
    
    def sweep(self) -> None:
        """Performs a single sweep
        """
        self.write_command("INIT:IMM;*WAI")
    
    
    def get_trace(self) -> list:
        """Gets the current trace from the instrument

        Returns:
            list: list of floats of the trace values
        """
        return self.instrument.query_ascii_values('FORM ASC;:TRAC:DATA? TRACE1')
from fsw.device import RsFswInstrument

class RsFswSetting():
    def __init__(self,setting_name,scpi_command,modes,measure):
        
        self.setting_name = setting_name
        self.scpi_command = scpi_command
        self.modes = modes
        self.measure = measure
        
        self.instrument = RsFswInstrument.get_instance()
        
        self.value = '0'
        
        self.status = False
        
        self.check_status()
    
    
    def check_status(self):
        if self.instrument.mode in self.modes:
            self.status = True
        else:
            self.value = '0'
            self.status = False
    
    
    def get_value(self):
        if self.status:
            self.value = self.intrument.query_str_with_opc(f"{self.scpi_command}?")
    
    
    def set_value(self, value):
        if self.status:
            self.instrument.write_str_with_opc(f"{self.scpi_command} {value}")
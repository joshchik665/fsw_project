from RsInstrument import RsInstrument


class RsFswInstrument(RsInstrument):
    _instance = None
    
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RsFswInstrument,cls).__new__(cls)
        return cls._instance
    
    
    def __init__(self,ip_address=None,**kwargs):
        if ip_address and not getattr(self, "initialized", False):
            self.connect_to_device(ip_address)
            
            self.json_data = kwargs
            
            self.mode = self.json_data['Mode']
            
            self.initialized = True
    
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise Exception("Instrument instance is not intialized")
        return cls._instance
    
    
    def connect_to_device(self,ip_address):
        try:
            # Adjust the VISA Resource string to fit your instrument
            super().__init__('TCPIP::' + ip_address + '::INSTR', True, False)
            self.visa_timeout = 3000  # Timeout for VISA Read Operations, default is 3s
            self.opc_timeout = 3000  # Timeout for opc-synchronised operations, default is 3s
            self.instrument_status_checking = True  # Error check after each command
            print('Hello I am: ' + self.query('*IDN?')) # Asks the FSW it's ID
        except Exception as ex:
            print('Error initializing the instrument session:\n' + ex.args[0])
            exit()
        
        self.write('*RST')
        
        self.ip_address = ip_address
    
    
    def write_command(self, command:str):
        self.write_str_with_opc(command)
    
    
    def query_command(self, command:str) -> str:
        return self.query_str_with_opc(command)
    
    
    def cont_sweep(self):
        self.write_str_with_opc("INIT:CONT ON")
    
    
    def single_sweep(self):
        self.write_str_with_opc('INIT:CONT OFF')
        self.write_str_with_opc('INIT:IMM;*WAI')
    
    
    def abort(self):
        self.write_str_with_opc('ABOR')
    
    
    
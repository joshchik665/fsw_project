from RsInstrument import RsInstrument

class RsFswInstrument(RsInstrument):
    def __init__(self, ip_address:str, visa_timeout:int, opc_timeout:int):
        try:
            # Adjust the VISA Resource string to fit your instrument
            super().__init__('TCPIP::' + ip_address + '::INSTR', True, False)
            self.visa_timeout = visa_timeout  # Timeout for VISA Read Operations, default is 3s
            self.opc_timeout = opc_timeout  # Timeout for opc-synchronised operations, default is 3s
            self.instrument_status_checking = True  # Error check after each command
            print('Hello I am: ' + self.query('*IDN?')) # Asks the FSW it's ID
        except Exception as ex:
            print('Error initializing the instrument session:\n' + ex.args[0])
            exit()
        
        self.write('*RST')
        
        self.ip_address = ip_address
    
    
    def write_command(self, command:str) -> None:
        self.write_str_with_opc(command)
    
    
    def query_command(self, command:str) -> str:
        return self.query_str_with_opc(command)
    
    
    def abort(self) -> None:
        self.write_command("ABOR")
    
    
    def sweep(self) -> None:
        self.write_command("INIT:IMM;*WAI")
    
    
    def get_trace(self) -> list:
        return self.query_bin_or_ascii_float_list('FORM ASC;:TRAC:DATA? TRACE1')

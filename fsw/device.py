from RsInstrument import RsInstrument

class RsFswInstrument(RsInstrument):
    def __init__(self,ip_address):
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
    
    

    
    
    
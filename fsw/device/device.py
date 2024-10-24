# device.py

from RsInstrument import RsInstrument

class RsFswInstrument(RsInstrument):
    def __init__(self, ip_address:str, visa_timeout:int, opc_timeout:int):
        """ Initialize the Instrument

        Args:
            ip_address (str): String with the IP address of the instrument
            visa_timeout (int): Visa timeout in milliseconds
            opc_timeout (int): OPC timeout in milliseconds
        """
        # Initializes the RsInstrument object
        try:
            # Adjust the VISA Resource string to fit your instrument
            super().__init__('TCPIP::' + ip_address + '::INSTR', True, False)
            self.visa_timeout = visa_timeout  # Timeout for VISA Read Operations, default is 3s
            self.opc_timeout = opc_timeout  # Timeout for opc-synchronised operations, default is 3s
            self.instrument_status_checking = True  # Error check after each command
            print('Hello I am: ' + self.query('*IDN?')) # Asks the FSW it's ID
        except Exception as ex:
            print('Error initializing the instrument session:\n' + ex.args[0]) # Error
            exit()
        
        self.write('*RST') # Reset the instrument
        
        self.ip_address = ip_address # Store the ip address
    
    
    def write_command(self, command:str) -> None:
        """Write a command to the instrument

        Args:
            command (str): The command to be written
        """
        self.write_str_with_opc(command)
    
    
    def query_command(self, command:str) -> str:
        """Send a Query to the instrument

        Args:
            command (str): The query command

        Returns:
            str: The value returned from the instrument
        """
        return self.query_str_with_opc(command)
    
    
    def abort(self) -> None:
        """Aborts the current measurment
        """
        self.write_command("ABOR")
    
    
    def sweep(self) -> None:
        """Performs a single sweep
        """
        self.write_command("INIT:IMM;*WAI")
    
    
    def get_trace(self) -> list[float]:
        """Gets the current trace from the instrument

        Returns:
            list: list of floats of the trace values
        """
        return self.query_bin_or_ascii_float_list('FORM ASC;:TRAC:DATA? TRACE1')

# device.py

from RsInstrument import RsInstrument
from pyvisa import ResourceManager

class RsFswInstrument():
    def __init__(self, ip_address:str, visa_timeout:int, opc_timeout:int):
        """ Initialize the Instrument

        Args:
            ip_address (str): String with the IP address of the instrument
            visa_timeout (int): Visa timeout in milliseconds
            opc_timeout (int): OPC timeout in milliseconds
        """
        self.rm = ResourceManager("@py")
        try:
            self.instrument = self.rm.open_resource(f"TCPIP::{ip_address}::hislip0")
        except Exception as ex:
            print('Error initializing the instrument session:\n' + ex.args[0]) # Error
            exit()
        
        self.visa_timeout = visa_timeout  # Timeout for VISA Read Operations
        self.opc_timeout = opc_timeout  # Timeout for opc-synchronised operations
        self.instrument_status_checking = True  # Error check after each command
        print('Hello I am: ' + self.instrument.query('*IDN?')) # Asks the FSW it's ID
        
        self.write_command('*RST') # Reset the instrument
        
        self.ip_address = ip_address # Store the ip address
    
    
    def write_command(self, command:str) -> None:
        """Write a command to the instrument

        Args:
            command (str): The command to be written
        """
        self.instrument.write(command)
    
    
    def query_command(self, command:str) -> str:
        """Send a Query to the instrument

        Args:
            command (str): The query command

        Returns:
            str: The value returned from the instrument
        """
        return self.instrument.query(command)
    
    
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
    
    
    def save_spectrogram(self) -> None:
        """ Saves the spectrogram to a file in the specified directory

        Args:
            file_path (str): file with path where spectrogram data is to be saved on the device
        """
        self.write_command('DISP:WIND2:SUBW:SEL')
        self.write_command('FORM:DEXP:DSEP POIN')
        self.write_command('FORM:DEXP:FORM CSV')
        self.write_command('FORM:DEXP:HEAD ON')
        self.write_command(r"MMEM:STOR2:SGR 'C:\Users\Instrument\Documents\lab_automation\test.CSV'")
    
    
    def clear_spectrogram(self) -> None:
        """Clears the spectrogram on the device"""
        self.write_command('CALC2:SGR:CLE:IMM')
    
    
    def copy_spectrogram(self, filename:str) -> bool:
        """Copy the spectrogram files from the instrument to the local computer

        Args:
            filename (str): Filename to save to on the local computer

        Returns:
            bool: Copied sucessfully
        """
        try:
            self.instrument.write(f'MMEM:DATA? "test.csv"')
            data = self.instrument.read_raw()  # Read binary data

            # Save to local file
            with open(filename, 'wb') as f:
                f.write(data)
            
            return True
        except:
            return False
    
    
    def close(self) -> None:
        """Closes the instrument session"""
        self.instrument.close()
    
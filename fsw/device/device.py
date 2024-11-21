# device.py

from pyvisa import ResourceManager

class Instrument():
    def __init__(self, ip_address:str):
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
            print(f'Error initializing the instrument session:\n{ex.args[0]}') # Error
            exit()
        
        self.idn = self.instrument.query('*IDN?')
        print(f'Hello I am: {self.idn}') # Asks the FSW it's ID
        
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
    
    
    def close(self) -> None:
        """Closes the instrument session"""
        self.instrument.close()
    
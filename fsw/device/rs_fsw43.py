# rs_fsw.py

from fsw.device.settings_manager import SettingsManager

class RsFsw43(SettingsManager):
    def __init__(self, ip_address:str):
        super().__init__(ip_address)
    
    
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
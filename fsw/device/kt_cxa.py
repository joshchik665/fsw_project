# kt_cxa.py

from fsw.device.settings_manager import SettingsManager

class KtCxa(SettingsManager):
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
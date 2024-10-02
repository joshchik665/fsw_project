from RsInstrument import RsInstrument

class RsFswInstrument(RsInstrument):
    def __init__(self,ip_address):
        
        self.scpi_commands = {
            'Center Frequency': 'FREQ:CENT',
            'Dwell Time': 'SENS:SWE:DTIM',
            'Reference Level': 'DISP:WIND:TRAC:Y:SCAL:RLEV',
            'Frequency Span': 'FREQ:SPAN',
            'Resolution Bandwidth': 'BAND',
            'Sweep Time': 'SENS:SWE:TIME',
            'Memory Depth': 'CALC2:SGR:HDEP',
            'Number of Points': 'SENS:SWE:WIND1:POIN',
            'Video Bandwidth': 'BAND:VID',
        }
        
        self.settings_for_mode = {
            'Spectrum': (
                'Center Frequency',
                'Reference Level',
                'Frequency Span',
                'Resolution Bandwidth',
                'Sweep Time',
                'Number of Points',
                'Video Bandwidth'
            ),
            'Real-Time Spectrum': (
                'Center Frequency',
                'Reference Level',
                'Frequency Span',
                'Resolution Bandwidth',
                'Sweep Time',
                'Memory Depth',
                'Video Bandwidth',
                'Dwell Time'
            ),
            'Zero span': (
                'Center Frequency',
                'Reference Level',
                'Resolution Bandwidth',
                'Sweep Time',
                'Number of Points',
                'Video Bandwidth'
            )
        }
        
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
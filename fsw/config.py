# config.py

from fsw.setting import Setting

MODES = ['Spectrum','Real-Time Spectrum','Zero Span']

SETTINGS = {
    'Center Frequency': Setting(
        name='Center Frequency',
        scpi_command='FREQ:CENT',
        applicable_modes=['Spectrum','Real-Time Spectrum','Zero Span'],
        measure='frequency',
        default_value='21500000000',
    ),
    'Dwell Time': Setting(
        name='Dwell Time',
        scpi_command='SENS:SWE:DTIM',
        applicable_modes=['Real-Time Spectrum'],
        measure='time',
        default_value='1',
    ),
    'Reference Level': Setting(
        name='Reference Level',
        scpi_command='DISP:WIND:TRAC:Y:SCAL:RLEV',
        applicable_modes=['Spectrum','Real-Time Spectrum','Zero Span'],
        measure='power',
        default_value='1',
    ),
    'Frequency Span': Setting(
        name='Frequency Span',
        scpi_command='FREQ:SPAN',
        applicable_modes=['Spectrum','Real-Time Spectrum'],
        measure='frequency',
        default_value='43000000000',
    ),
    'Resolution Bandwidth': Setting(
        name='Resolution Bandwidth',
        scpi_command='BAND',
        applicable_modes=['Spectrum','Real-Time Spectrum','Zero Span'],
        measure='frequency',
        default_value='3000000',
    ),
    'Sweep Time': Setting(
        name='Sweep Time',
        scpi_command='SENS:SWE:TIME',
        applicable_modes=['Spectrum','Real-Time Spectrum','Zero Span'],
        measure='time',
        default_value='0.1',
    ),
    'Memory Depth': Setting(
        name='Memory Depth',
        scpi_command='CALC2:SGR:HDEP',
        applicable_modes=['Real-Time Spectrum'],
        measure='number',
        default_value='3000',
    ),
    'Number of Points': Setting(
        name='Number of Points',
        scpi_command='SENS:SWE:WIND1:POIN',
        applicable_modes=['Spectrum','Zero Span'],
        measure='number',
        default_value='1001',
    ),
    'Video Bandwidth': Setting(
        name='Video Bandwidth',
        scpi_command='BAND:VID',
        applicable_modes=['Spectrum','Zero Span'],
        measure='frequency',
        default_value='3000000',
    ),
    
}
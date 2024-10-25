# main_window.py

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)
from ui.fsw_gui.mode_spec import ModeSpec
from ui.fsw_gui.mode_rts import ModeRts
from ui.fsw_gui.mode_zero_span import ModeZs
from fsw.device.settings_manager import SettingsManager


class MainWindow(QMainWindow):
    def __init__(self, config: dict, visa_timeout: int, opc_timeout: int):
        """Main window for the GUI

        Args:
            config (dict): Dictionary of config values passed on startup
            visa_timeout (int): Visa timeout in milliseconds for the instrument
            opc_timeout (int): OPC imeout in milliseconds for the instrument
        """
        super().__init__()
        
        # indicies for the tabs, will change later
        self.tab_indicies = {
            "Spectrum": 0,
            "Real-Time Spectrum": 1,
            "Zero-Span": 2,
        }
        self._programmatic_change = False # Flag to change the behavior of the tab change function
        
        self._set_title_and_window() # Set the window oand label for the main window
        
        # Creates instance of the SettingsManager class that controls the instrument
        self.instrument = SettingsManager(
            config['ip_address'],
            r"configs\fsw_settings\default.json", 
            visa_timeout, 
            opc_timeout
            )
        
        self._set_status_bar(config['ip_address']) # Set the status bar
        
        self._create_tabs() # Creates the tabs
        
        current_tab_widget = self.tab_widget.widget(self.current_tab_index)
        if config['data']:
            current_tab_widget.load_settings(config)
        else:
            current_tab_widget.verify()
    
    
    def _set_title_and_window(self) -> None:
        """Set the title and window
        """
        self.setWindowTitle('Rhode&Schwarz FSW-43 GUI')
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
    
    
    def _set_status_bar(self, ip_address:str) -> None:
        """Set the status bar of the Main window

        Args:
            ip_address (str): IP address of the instrument
        """
        status_bar = self.statusBar()
        status_bar.showMessage(
            f'Connected to Rhode&Schwarz FSW-43 @ {ip_address}', 
            timeout=0
            )
    
    
    def _create_tabs(self) -> None:
        """Creats the tab widget and initiates the individual tab widgets
        """
        # Create and set the tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        self.current_tab_index = 0
        
        # Creates the tab widgets and adds them to the main tab widget
        self.tab_widget.addTab(ModeSpec(self.instrument, self.tab_widget), "Spectrum Mode")
        self.tab_widget.addTab(ModeRts(self.instrument, self.tab_widget), "Real-Time Spectrume Mode")
        self.tab_widget.addTab(ModeZs(self.instrument, self.tab_widget), "Zero Span Mode")
        
        # When the tab changes, function called
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    
    def on_tab_changed(self, new_tab_index:int) -> None:
        """Run this when the tab is changed, changes the mode of the device and verify the values

        Args:
            new_tab_index (int): Index of the new tab
        """
        new_tab_widget = self.tab_widget.widget(new_tab_index)
        
        new_tab_widget.set_mode()
        
        if not self._programmatic_change:
            new_tab_widget.verify()
        
        self.current_tab_index = new_tab_index
    
    
    def change_tab_programmatically(self, index:int) -> None:
        """This function is called when a tab wants to change it tab. Used when new config is loaded

        Args:
            index (int): Index of the tab that to change to
        """
        self._programmatic_change = True
        self.tab_widget.setCurrentIndex(index)
        self._programmatic_change = False
    
    
    def close(self, *args):
        """This function shuts down the connection"""
        self.instrument.set_setting('Sweep', '0')
        self.instrument.close()
        print("Closed Session")
        return args
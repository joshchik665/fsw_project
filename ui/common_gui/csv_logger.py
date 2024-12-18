#csv_logger.py

from PySide6.QtCore import QObject, Signal, Slot

from pathlib import Path
import csv
from datetime import datetime
import numpy as np

from ui.common.utilities import save_file_dialog


class TraceLogger(QObject):
    """
    A class to handle logging of spectrum analyzer traces to CSV files
    with file selection capability.
    """
    logging_started = Signal(str)  # Emits filename when logging starts
    logging_stopped = Signal()
    trace_logged = Signal(int)
    error_occurred = Signal(str)  # For error handling


    def __init__(self, parent=None):
        super().__init__(parent)
        self.csv_file = None
        self.csv_writer = None
        self.trace_count = 0
        self.is_logging = False
        self.current_filepath = None


    def prompt_for_file(self) -> Path | None:
        """
        Opens a file dialog for the user to select a save location
        or create a new file.

        Returns:
            Path object if file was selected, None if cancelled
        """
        # Generate default filename with timestamp
        default_filename = Path("data") / "traces" / f"trace_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Open file dialog
        filepath = save_file_dialog("Save to CSV file: ", str(default_filename), '.csv', self.parent())
        
        return Path(filepath) if filepath else None


    def start_logging(self, filepath: Path | None = None) -> bool:
        """
        Start logging traces to a CSV file.
        
        Args:
            filepath: Optional Path object. If None, will prompt for file location.
        
        Returns:
            bool: True if logging started successfully, False otherwise
        """
        if self.is_logging:
            return False

        # If no filepath provided, prompt for one
        if filepath is None:
            filepath = self.prompt_for_file()
            if filepath is None:  # User cancelled
                return False

        try:
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Open file and initialize CSV writer
            self.csv_file = open(filepath, 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            
            # Write header row
            self.csv_writer.writerow(['Timestamp', 'Frequency', 'Amplitude'])
            
            self.is_logging = True
            self.trace_count = 0
            self.current_filepath = filepath
            
            self.logging_started.emit(str(filepath))
            return True

        except IOError as e:
            self.error_occurred.emit(f"Error starting logging: {str(e)}")
            self.cleanup()
            return False


    def stop_logging(self):
        """Stop the current logging session."""
        if not self.is_logging:
            return

        self.cleanup()
        self.logging_stopped.emit()


    def cleanup(self):
        """Clean up file handles and reset state."""
        try:
            if self.csv_file:
                self.csv_file.close()
            self.csv_file = None
            self.csv_writer = None
            self.is_logging = False
            self.current_filepath = None
        except IOError as e:
            self.error_occurred.emit(f"Error during cleanup: {str(e)}")


    @Slot(np.ndarray, np.ndarray)
    def log_trace(self, frequencies: np.ndarray, amplitudes: np.ndarray):
        """Log a single trace to the CSV file."""
        if not self.is_logging or not self.csv_writer:
            return

        try:
            timestamp = datetime.now().isoformat()
            for freq, amp in zip(frequencies, amplitudes):
                self.csv_writer.writerow([timestamp, freq, amp])
            
            self.trace_count += 1
            self.trace_logged.emit(self.trace_count)
            
            # Ensure data is written to disk
            self.csv_file.flush()
        except IOError as e:
            self.error_occurred.emit(f"Error logging trace: {str(e)}")
            self.stop_logging()



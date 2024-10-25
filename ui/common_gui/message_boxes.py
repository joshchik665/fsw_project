# message_boxes.py

from PySide6.QtWidgets import QMessageBox

class invalid_filetype(QMessageBox):
    def __init__(self):
        """Message box to tell the user that the filetype is invalid
        """
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setText("Invalid File Type!")
        self.setWindowTitle("Message")
        self.setStandardButtons(QMessageBox.Ok)
        self.exec()


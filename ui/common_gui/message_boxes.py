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


class logging_error(QMessageBox):
    def __init__(self):
        """Message box to tell the user that the filetype is invalid
        """
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setText("Logging Error!")
        self.setWindowTitle("Message")
        self.setStandardButtons(QMessageBox.Ok)
        self.exec()


class copy_error(QMessageBox):
    def __init__(self):
        """Message box to tell the user that the filetype is invalid
        """
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setText("Error occured copying file from device")
        self.setWindowTitle("Message")
        self.setStandardButtons(QMessageBox.Ok)
        self.exec()


class copy_sucess(QMessageBox):
    def __init__(self):
        """Message box to tell the user that the filetype is invalid
        """
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setText("File copied sucessfully!")
        self.setWindowTitle("Message")
        self.setStandardButtons(QMessageBox.Ok)
        self.exec()


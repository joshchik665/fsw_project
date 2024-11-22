from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SpectrogramWindow(QWidget):
    def __init__(self, spec_data, frequencies, times):
        super().__init__()
        self.setWindowTitle("Spectrogram View")
        self.setMinimumSize(600, 400)
        
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create matplotlib figure
        fig = Figure(figsize=(8, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        # Plot spectrogram
        im = ax.pcolormesh(times, frequencies, spec_data, shading='auto')
        fig.colorbar(im, ax=ax, label='Amplitude')
        ax.set_ylabel('Frequency [Hz]')
        ax.set_xlabel('Frame')
        ax.set_title('Spectrogram')
        
        # Add to layout
        layout.addWidget(canvas)
        self.setLayout(layout)
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import collections

class PlotWidget(QWidget):
    """Widget de plotagem em tempo real para corrente x tempo."""

    def __init__(self, max_points=200, parent=None):
        super().__init__(parent)
        self.max_points = max_points
        self.times = collections.deque(maxlen=max_points)
        self.currents = collections.deque(maxlen=max_points)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Current vs Time")
        self.ax.set_xlabel("Time (ms)")
        self.ax.set_ylabel("Current (mA)")
        self.ax.grid(True)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_plot(self, t_ms, current_mA):
        self.times.append(t_ms)
        self.currents.append(current_mA)

        self.ax.clear()
        self.ax.plot(self.times, self.currents, color="tab:blue")
        self.ax.set_xlabel("Time (ms)")
        self.ax.set_ylabel("Current (mA)")
        self.ax.grid(True)
        self.canvas.draw()

    def reset_plot(self):
        self.times.clear()
        self.currents.clear()
        self.ax.clear()
        self.ax.set_title("Current vs Time")
        self.ax.set_xlabel("Time (ms)")
        self.ax.set_ylabel("Current (mA)")
        self.ax.grid(True)
        self.canvas.draw()
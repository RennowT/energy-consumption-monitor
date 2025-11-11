from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt5.QtCore import QTimer
from src.core.app_controller import AppController
from src.ui.plot_widget import PlotWidget
from src.ui.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    """Janela principal do Energy Consumption Monitor."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Energy Consumption Monitor")
        self.controller = None
        self.running = False
        self.plot = PlotWidget(max_points=300)
        self.status_label = QLabel("Disconnected")

        # Botões
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_settings = QPushButton("Settings")
        self.btn_start.clicked.connect(self.start_acquisition)
        self.btn_stop.clicked.connect(self.stop_acquisition)
        self.btn_settings.clicked.connect(self.open_settings)

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_settings)
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_stop)

        layout = QVBoxLayout()
        layout.addWidget(self.plot)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer de atualização da UI
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(200)  # atualiza a cada 200ms

        self.port = "COM6"
        self.baudrate = 9600

    def open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec_():
            self.port, self.baudrate = dlg.get_settings()
            self.status_label.setText(f"Port: {self.port}, Baud: {self.baudrate}")

    def start_acquisition(self):
        if self.running:
            return
        try:
            self.controller = AppController(port=self.port, baudrate=self.baudrate)
            self.controller.start()
            self.running = True
            self.status_label.setText("Running...")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def stop_acquisition(self):
        if not self.running:
            return
        self.controller.stop()
        summary = self.controller.summarize()
        text = f"Avg: {summary['avg_mA']:.1f} mA | RMS: {summary['rms_mA']:.1f} mA | E: {summary['energy_Wh']:.6f} Wh"
        self.status_label.setText(f"Stopped. {text}")
        self.running = False

    def update_ui(self):
        if self.running and self.controller and self.controller.samples:
            t_ms = len(self.controller.samples) * (1000 / self.controller.sample_rate_hz)
            current = self.controller.samples[-1]
            self.plot.update_plot(t_ms, current)

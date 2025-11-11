from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QDialogButtonBox, QLabel
import serial.tools.list_ports

class SettingsDialog(QDialog):
    """Diálogo para seleção de porta serial e baudrate."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Serial Settings")
        self.port_combo = QComboBox()
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200"])

        for port in serial.tools.list_ports.comports():
            self.port_combo.addItem(port.device)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_combo)
        layout.addWidget(QLabel("Baudrate:"))
        layout.addWidget(self.baud_combo)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_settings(self):
        return self.port_combo.currentText(), int(self.baud_combo.currentText())

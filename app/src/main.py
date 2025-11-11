"""
Energy Consumption Monitor - Main Application
---------------------------------------------
Entry point for the Python desktop software.

Features:
 - Connects to Arduino Nano (ACS712 current sensor) via serial.
 - Displays real-time current graph using PyQt5 and Matplotlib.
 - Supports CSV logging and energy estimation.
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Main entry point for the Energy Consumption Monitor."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

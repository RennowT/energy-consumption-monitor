import csv
from datetime import datetime
from pathlib import Path

class DataLogger:
    """Gerencia gravação de dados em CSV para o Energy Monitor."""

    def __init__(self, output_dir="logs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.file = None
        self.writer = None

    def start(self, device_name="default"):
        """Inicia um novo arquivo CSV."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{device_name}_{timestamp}.csv"
        self.file = open(self.output_dir / filename, "w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["timestamp_ms", "current_mA"])
        print(f"[LOGGER] Recording to {filename}")

    def log(self, timestamp_ms: int, current_mA: float):
        """Registra uma linha CSV."""
        if self.writer:
            self.writer.writerow([timestamp_ms, f"{current_mA:.3f}"])
            self.file.flush()

    def stop(self):
        """Fecha o arquivo atual."""
        if self.file:
            print("[LOGGER] Recording stopped.")
            self.file.close()
            self.file = None
            self.writer = None

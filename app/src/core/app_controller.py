import time
from threading import Thread, Event
from src.drivers.serial_reader import SerialReader
from src.drivers.calibration import ACS712Calibrator
from src.core.data_logger import DataLogger
from src.core.analysis import DataAnalyzer

class AppController:
    """Coordena captura de dados, calibração, logging e análise."""

    def __init__(self, port="COM6", baudrate=9600, sample_rate_hz=50):
        self.port = port
        self.baudrate = baudrate
        self.sample_rate_hz = sample_rate_hz
        self.reader = SerialReader(port, baudrate)
        self.calibrator = ACS712Calibrator()
        self.logger = DataLogger()
        self.analyzer = DataAnalyzer()
        self._thread = None
        self._stop_event = Event()
        self.samples = []

    def start(self):
        """Inicia captura e gravação."""
        self.reader.connect()
        self.logger.start(device_name="energy_monitor")
        self._stop_event.clear()
        self._thread = Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("[CORE] Acquisition started.")

    def stop(self):
        """Interrompe a captura."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
        self.reader.disconnect()
        self.logger.stop()
        print("[CORE] Acquisition stopped.")

    def calibrate_zero(self, samples_n=100):
        """Coleta amostras em 0 A para calibrar offset."""
        print("[CORE] Calibrating zero-current offset...")
        samples = []
        self.reader.connect()
        for _ in range(samples_n):
            data = self.reader.read(block=True, timeout=1)
            if data:
                _, current_mA = data
                samples.append(current_mA)
        self.reader.disconnect()
        self.calibrator.calibrate_zero(samples)
        print(f"[CORE] Offset calibrated: {self.calibrator.offset_mA:.3f} mA")

    def _loop(self):
        """Loop de leitura e registro contínuo."""
        while not self._stop_event.is_set():
            data = self.reader.read()
            if not data:
                continue

            timestamp, current_mA = data
            current_corr = self.calibrator.apply(current_mA)
            self.logger.log(timestamp, current_corr)
            self.samples.append(current_corr)
            time.sleep(1 / self.sample_rate_hz)

    def summarize(self):
        """Retorna métricas básicas do registro atual."""
        if not self.samples:
            return {}
        avg = self.analyzer.average_current(self.samples)
        rms = self.analyzer.rms_current(self.samples)
        energy = self.analyzer.estimate_energy_wh(self.samples)
        return {"avg_mA": avg, "rms_mA": rms, "energy_Wh": energy}

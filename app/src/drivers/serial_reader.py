import serial
import threading
from queue import Queue, Empty
from .sensor_parser import parse_csv_line

class SerialReader:
    """Driver para leitura de dados via UART (Arduino Nano @9600bps)."""

    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._serial = None
        self._thread = None
        self._running = False
        self.queue = Queue()

    def connect(self):
        """Abre a conexão serial."""
        self._serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        self._running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def _read_loop(self):
        """Thread para leitura contínua da serial."""
        while self._running:
            try:
                line = self._serial.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    parsed = parse_csv_line(line)
                    if parsed:
                        self.queue.put(parsed)
            except serial.SerialException:
                break

    def read(self, block: bool = False, timeout: float = 0.1):
        """Lê o próximo item da fila de dados (ou None se vazio)."""
        try:
            return self.queue.get(block, timeout)
        except Empty:
            return None

    def disconnect(self):
        """Encerra a leitura e fecha a porta serial."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        if self._serial and self._serial.is_open:
            self._serial.close()

import time
from types import SimpleNamespace
from src.core.app_controller import AppController

class MockSerialReader:
    """Simula o SerialReader, gerando leituras fixas."""
    def __init__(self, *_, **__):
        self.connected = False
        self.counter = 0

    def connect(self): self.connected = True
    def disconnect(self): self.connected = False
    def read(self, block=False, timeout=None):
        if self.counter >= 5:
            return None
        self.counter += 1
        return (self.counter * 1000, 100.0 * self.counter)

class MockLogger:
    def __init__(self):
        self.logged = []
        self.started = False
        self.stopped = False

    def start(self, device_name="mock"): self.started = True
    def log(self, ts, val): self.logged.append((ts, val))
    def stop(self): self.stopped = True

def test_app_controller_loop(monkeypatch):
    """Testa ciclo completo com mocks."""
    monkeypatch.setattr("src.core.app_controller.SerialReader", MockSerialReader)
    monkeypatch.setattr("src.core.app_controller.DataLogger", MockLogger)

    app = AppController(port="COM_FAKE")
    app.start()
    time.sleep(0.3)   # deixa o loop rodar um pouco
    app.stop()

    assert app.logger.started
    assert app.logger.stopped
    assert len(app.logger.logged) > 0
    assert all(isinstance(v[1], float) for v in app.logger.logged)

def test_calibrate_zero(monkeypatch):
    """Testa calibração de zero usando mock de SerialReader."""
    monkeypatch.setattr("src.core.app_controller.SerialReader", MockSerialReader)

    app = AppController(port="COM_FAKE")
    app.calibrate_zero(samples_n=3)

    assert abs(app.calibrator.offset_mA) > 0

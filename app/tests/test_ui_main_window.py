import pytest
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

class MockController:
    def __init__(self, *_, **__):
        self.samples = [0.0, 10.0, 20.0]
        self.sample_rate_hz = 50
    def start(self): pass
    def stop(self): pass
    def summarize(self):
        return {"avg_mA": 10.0, "rms_mA": 12.0, "energy_Wh": 0.001}

@pytest.fixture(scope="module")
def app():
    return QApplication([])

def test_main_window_loads(app, monkeypatch):
    monkeypatch.setattr("src.ui.main_window.AppController", MockController)
    window = MainWindow()
    assert window is not None
    assert window.plot is not None
    assert window.btn_start.text() == "Start"

def test_start_and_stop_flow(app, monkeypatch):
    monkeypatch.setattr("src.ui.main_window.AppController", MockController)
    window = MainWindow()
    window.start_acquisition()
    assert window.running
    window.stop_acquisition()
    assert not window.running
    assert "Stopped" in window.status_label.text()

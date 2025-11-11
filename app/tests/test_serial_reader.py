import io
import time
import types
from src.drivers.serial_reader import SerialReader

class MockSerial:
    def __init__(self, data: str):
        self.data = io.StringIO(data)
        self.is_open = True

    def readline(self):
        return self.data.readline().encode()

    def close(self):
        self.is_open = False

def test_read_loop_with_mock(monkeypatch):
    mock = MockSerial("1000,250.0\n2000,500.0\n")
    monkeypatch.setattr("serial.Serial", lambda *a, **kw: mock)

    reader = SerialReader(port="COM_FAKE")
    reader.connect()
    time.sleep(0.1)  # deixa a thread rodar um pouco
    reader.disconnect()

    data1 = reader.read(block=True)
    data2 = reader.read(block=True)
    assert data1 == (1000, 250.0)
    assert data2 == (2000, 500.0)

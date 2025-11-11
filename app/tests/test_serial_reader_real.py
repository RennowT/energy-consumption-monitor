from src.drivers.serial_reader import SerialReader

def test_real_serial_read():
    reader = SerialReader(port="COM6", baudrate=9600)
    reader.connect()

    for _ in range(5):
        data = reader.read(block=True, timeout=2)
        if data:
            print("Received:", data)
    reader.disconnect()

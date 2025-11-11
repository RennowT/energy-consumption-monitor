import csv
from src.core.data_logger import DataLogger

def test_data_logger_creates_file(tmp_path):
    logger = DataLogger(output_dir=tmp_path)
    logger.start(device_name="test_device")
    logger.log(1000, 12.345)
    logger.stop()

    files = list(tmp_path.glob("*.csv"))
    assert len(files) == 1, "Logger should create one CSV file"

    with open(files[0], newline="") as f:
        rows = list(csv.reader(f))
        assert rows[0] == ["timestamp_ms", "current_mA"]
        assert rows[1][0] == "1000"
        assert abs(float(rows[1][1]) - 12.345) < 1e-3

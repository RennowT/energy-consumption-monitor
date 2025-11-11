from src.drivers.sensor_parser import parse_csv_line

def test_valid_line():
    line = "1234,56.7"
    ts, current = parse_csv_line(line)
    assert ts == 1234
    assert abs(current - 56.7) < 1e-6

def test_invalid_line_format():
    assert parse_csv_line("1234") is None
    assert parse_csv_line("a,b,c") is None

def test_invalid_numbers():
    assert parse_csv_line("abc,12") is None
    assert parse_csv_line("12,xyz") is None

from src.drivers.calibration import ACS712Calibrator

def test_zero_calibration():
    c = ACS712Calibrator()
    c.calibrate_zero([10, 12, 14, 16])
    assert abs(c.offset_mA - 13) < 0.1

def test_scale_calibration():
    c = ACS712Calibrator()
    c.calibrate_scale(measured_current_A=2.0, sensor_output_mA=1950)
    assert 1.02 < c.scale < 1.04  # próximo de 2.0/1.95

def test_apply_calibration():
    c = ACS712Calibrator()
    c.offset_mA = 10
    c.scale = 2.0
    result = c.apply(20)
    assert abs(result - 20.0) < 1e-6

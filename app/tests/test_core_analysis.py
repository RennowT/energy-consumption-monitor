from src.core.analysis import DataAnalyzer

def test_average_current():
    data = [100, 200, 300]
    assert DataAnalyzer.average_current(data) == 200.0

def test_rms_current():
    data = [0, 1000]
    rms = DataAnalyzer.rms_current(data)
    assert abs(rms - 707.1) < 0.5

def test_estimate_energy_wh():
    data = [1000, 1000, 1000, 1000]  # 1A por 4 amostras a 50Hz
    energy = DataAnalyzer.estimate_energy_wh(data, voltage_v=5.0, sample_rate_hz=50)
    # 1A * 5V * (4/50)s = 0.4J = 0.000111Wh
    assert 0.0001 < energy < 0.00012

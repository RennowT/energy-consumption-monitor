import numpy as np

class DataAnalyzer:
    """Funções para análise de corrente e energia."""

    @staticmethod
    def average_current(currents_mA):
        return float(np.mean(currents_mA)) if len(currents_mA) else 0.0

    @staticmethod
    def rms_current(currents_mA):
        arr = np.array(currents_mA)
        return float(np.sqrt(np.mean(np.square(arr)))) if len(arr) else 0.0

    @staticmethod
    def estimate_energy_wh(currents_mA, voltage_v=5.0, sample_rate_hz=50):
        """
        Estima energia consumida (Wh) a partir da corrente e tensão.
        E = (I_avg * V * t) / 3600
        """
        if not currents_mA:
            return 0.0
        i_avg_a = np.mean(currents_mA) / 1000.0
        duration_s = len(currents_mA) / sample_rate_hz
        return float((i_avg_a * voltage_v * duration_s) / 3600.0)

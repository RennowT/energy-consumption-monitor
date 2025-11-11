import numpy as np

class ACS712Calibrator:
    """Realiza calibração do sensor ACS712 para offset e ganho."""

    def __init__(self, nominal_sensitivity_mV_per_A: float = 185.0):
        self.nominal_sensitivity = nominal_sensitivity_mV_per_A
        self.offset_mA = 0.0
        self.scale = 1.0

    def calibrate_zero(self, samples):
        """Calcula o offset (corrente em 0 A)."""
        if len(samples) == 0:
            return
        self.offset_mA = float(np.mean(samples))

    def calibrate_scale(self, measured_current_A: float, sensor_output_mA: float):
        """
        Ajusta a escala comparando a leitura do sensor com corrente conhecida.
        Exemplo: 2 A reais → sensor indica 1950 mA ⇒ scale ≈ 2000/1950
        """
        if sensor_output_mA != 0:
            self.scale = (measured_current_A * 1000.0) / sensor_output_mA

    def apply(self, current_mA: float) -> float:
        """Aplica calibração ao valor lido."""
        return (current_mA - self.offset_mA) * self.scale

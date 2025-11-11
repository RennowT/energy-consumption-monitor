import pytest
from PyQt5.QtWidgets import QApplication
from src.ui.plot_widget import PlotWidget

@pytest.fixture(scope="module")
def app():
    """Instância única do QApplication para todos os testes."""
    return QApplication([])

def test_plot_widget_creation(app):
    plot = PlotWidget()
    assert plot.ax is not None
    assert plot.canvas is not None

def test_plot_update(app):
    plot = PlotWidget(max_points=5)
    for i in range(10):
        plot.update_plot(i * 100, i * 10)
    assert len(plot.times) <= 5
    assert len(plot.currents) <= 5

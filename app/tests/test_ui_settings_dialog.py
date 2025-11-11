import pytest
from PyQt5.QtWidgets import QApplication
from src.ui.settings_dialog import SettingsDialog

@pytest.fixture(scope="module")
def app():
    return QApplication([])

def test_settings_dialog_creation(app):
    dlg = SettingsDialog()
    assert dlg.port_combo is not None
    assert dlg.baud_combo.count() > 0

def test_get_settings(app):
    dlg = SettingsDialog()
    port, baud = dlg.get_settings()
    assert isinstance(port, str)
    assert isinstance(baud, int)

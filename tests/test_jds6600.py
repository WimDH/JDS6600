import pytest
from jds6600.core import JDS6600, WAVEFORMS


def test_waveforms_list():
    """Test if the order and the entries in WAVEFORM is the same."""
    assert WAVEFORMS == [
        "sine",  # 0
        "square",  # 1
        "pulse",  # 2
        "triangle",  # 3
        "parial_sine",  # 4
        "cmos",  # 5
        "dc",  # 6
        "half_wave",  # 7
        "full_wave",  # 8
        "pos_ladder",  # 9
        "neg-ladder",  # 10
        "noise",  # 11
        "exp-rise",  # 12
        "exp-decay",  # 13
        "multi-tone",  # 14
        "sinc",  # 15
        "lorenz",  # 16        
    ]

@pytest.fixture
def signal_generator():
    return JDS6600(port="/dev/fakeUSB") 


def test_jds6600_get_waveform_id(signal_generator):
    """Test of we can get the waveform id from a waveform name."""
    assert signal_generator._get_waveform_id("dc") == 6


def test_jds6600_get_waveform_name(signal_generator):
    """Test of we can get the waveform name from a waveform id."""
    assert signal_generator._get_waveform_name(6) == "dc"

def test_validate_channel(signal_generator):
    """Test the channel validation."""
    
    assert signal_generator._validate_channel(value=1) is None
    with pytest.raises(ValueError):
        assert signal_generator._validate_channel(value=3)

def test_validate_waveform(signal_generator):
    """Test the waveform validation."""
    assert signal_generator._validate_waveform_name(value="sine") is None    
    with pytest.raises(ValueError):
        assert signal_generator._validate_waveform_name(value="mexican wave")

def test_validate_amplitude(signal_generator):
    """Test the amplitude validation."""
    assert signal_generator._validate_amplitude(value=1) is None    
    with pytest.raises(ValueError):
        assert signal_generator._validate_amplitude(value=999)

def test_validate_offset(signal_generator):
    """Test the offset validation."""
    assert signal_generator._validate_offset(value=1) is None    
    with pytest.raises(ValueError):
        assert signal_generator._validate_offset(value=1000)

def test_validate_dutycycle(signal_generator):
    """Test the dutycycle validation."""
    assert signal_generator._validate_dutycycle(value=10) is None
    with pytest.raises(ValueError):
        assert signal_generator._validate_dutycycle(value=-50)

def test_parse_output(signal_generator):
    """Test if we can parse the output we get from the JDS6600."""
    assert signal_generator._parse_output(data=":ok") == 'ok'
    assert signal_generator._parse_output(data=":r20=12345.") == "12345"
    assert signal_generator._parse_output(data="") == ""
    assert signal_generator._parse_output(data="funky_data") == ""
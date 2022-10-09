from select import select
import serial
from typing import Union, Tuple


# Allowed waveforms and their mapping.
WAVEFORMS = [
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


class JDS6600:
    """
    Class to control the JDS6600 Signal Generator/Counter.
    """

    def __init__(self, port: str) -> None:
        self.port = port

    def __enter__(self) -> serial.Serial:
        self.connection = serial.Serial(
            port=self.port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            timeout=1,
        )
        return self

    def __exit__(self, *args, **kwargs) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()

    def connect(self):
        """Connect to the Signal Generator."""
        self.connection = serial.Serial(
            port=self.port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            timeout=1,
        )
        return self
    
    def close(self):
        if self.connection:
            self.connection.close()

    @staticmethod
    def _get_waveform_id(name: str) -> int:
        """Get the numeric value of the waveform."""
        return WAVEFORMS.index(name)

    @staticmethod
    def _get_waveform_name(id: int) -> str:
        """Get the numeric value of the waveform."""
        return WAVEFORMS[id]

    @staticmethod
    def _validate_channel(value: int) -> None:
        """
        Raise exception if the channel is not 1 or 2.
        """
        if value not in (1, 2):
            raise ValueError("Channel should be 1 or 2!")

    @staticmethod
    def _validate_waveform_name(value: str) -> None:
        """
        Raise exception if the waveform name is not in the predefined list.
        """
        if value not in WAVEFORMS:
            raise ValueError("Waveform is not one of {}".format(WAVEFORMS))

    @staticmethod
    def _validate_amplitude(value: float) -> None:
        """
        Raise exception if the amplitude is negative or more than 10v.
        """
        if value < 0.001 or value > 10:
            raise ValueError("The amplitude should be bewteen 1mV and 10V.")

    @staticmethod
    def _validate_offset(value: float) -> None:
        """
        Raise exception if the amplitude is negative or more than 10v.
        """
        if not (-10 < value < 10):
            raise ValueError("The offset should be bewteen -9.99V and 9.99V.")

    @staticmethod
    def _validate_dutycycle(value: float) -> None:
        """
        Raise exception if the amplitude is negative or more than 10v.
        """
        if value < 0 or value > 100:
            raise ValueError("The duty cycle should be bewteen 0% and 100%.")

    @staticmethod
    def __parse_output(data: str) -> str:
        """
        Return the value of the result:
        r20=1,1.
        returns 1,1
        """
        if data == ":ok":
            return "ok"
        elif len(data) > 3 and "=" in data:
            return data.split("=")[1][:-1]

        return ""

    def __send_command(self, command: str) -> str:
        """Send the command to the device and return the result."""
        self.connection.write(command.encode())
        result :str = self.connection.readline().strip().decode()
        return result

    def get_channels(self) -> Tuple:
        """
        Read the status of the channels, and return a Tuple.
        First entry is the status of channel 1, the second of channel 2.
        True means that the channel is enabled.
        """
        result: str = self.__parse_output(self.__send_command(command=":r20=0.\n"))
        return tuple(map(lambda x: x == "1", result.split(",")))
        
    def set_channels(self, channel1: bool, channel2: bool) -> str:
        """
        Enable or disable the channels.
        True enables a channel, False disables a channel.
        """
        if type(channel1) != bool or type(channel2) != bool:
            raise ValueError("Channel status should be either True or False!")
        status: str = "{},{}".format(
            (False, True).index(channel1), (False, True).index(channel2)
        )
        return self.__parse_output(self.__send_command(command=f":w20={status}.\n"))

    def get_waveform(self, channel: int) -> str:
        """
        Get the type of waveform which is currently configured on a given channel.
        """
        self._validate_channel(channel)
        waveform_id: int = int(
            self.__parse_output(self.__send_command(command=f":r{20 + channel}=0.\n"))
        )
        return self._get_waveform_name(waveform_id)

    def set_waveform(self, channel: int, value: str) -> str:
        """Set the waveform for a given channel."""
        self._validate_channel(channel)
        self._validate_waveform_name(value)
        waveform_id: int = self._get_waveform_id(value)
        return self.__parse_output(
            self.__send_command(command=f":w{20 + channel}={waveform_id}.\n")
        )

    def get_frequency(self, channel: int) -> float:
        """return the configured frequency for a give channel."""
        frequency: str
        magnitude_indicator: str
        self._validate_channel(channel)
        frequency, magnitude_indicator = self.__parse_output(
            self.__send_command(command=f":r{22 + channel}=0.\n")
        ).split(",")
        frequency_num: float = float(frequency)
        magnitude_indicator_num: int = int(magnitude_indicator)

        for i in range(magnitude_indicator_num):
            frequency_num = frequency_num / 1000

        return frequency_num / 100

    def set_frequency(self, channel: int, value: float) -> str:
        """
        Set the frequency for one of the given channels.
        Frequency in in Hz.
        TODO: allow frequencies < 0.01Hz.
        """
        self._validate_channel(channel)
        value = int(value * 100)
        return self.__parse_output(
            self.__send_command(command=f":w{22 + channel}={value},0.\n")
        )

    def get_amplitude(self, channel: int) -> float:
        """Get the amplitude of the signal for a given channel."""
        self._validate_channel(channel)
        return (
            float(
                self.__parse_output(self.__send_command(command=f":r{24 + channel}=0.\n"))
            )
            / 1000
        )

    def set_amplitude(self, channel: int, value: float) -> str:
        """
        Set the amplitude of the signal for a given channel.
        Amplitude is in Volt.
        """
        self._validate_channel(channel)
        self._validate_amplitude(value)

        return self.__parse_output(
            self.__send_command(command=f":w{24 + channel}={int(value*1000)}.\n")
        )

    def get_offset(self, channel: int) -> float:
        """
        Get the DC offset of the signal for a given channel.
        Returned values vs offset (V):
            1999 - 9.99
            1000 - 0
            1    - -9.99
        """
        self._validate_channel(channel)
        result = float(
            self.__parse_output(self.__send_command(command=f":r{26 + channel}=0.\n"))
        )
        return (result - 1000) / 100

    def set_offset(self, channel: int, value: float) -> str:
        """
        Set the offset of the signal for a given channel.
        """
        offset = round(value, 2)
        self._validate_channel(channel)
        self._validate_offset(offset)

        reg_val = int((offset * 100) + 1000)
        return self.__parse_output(
            self.__send_command(command=f":w{26 + channel}={reg_val}.\n")
        )

    def get_dutycycle(self, channel: int) -> float:
        """
        Get the duty cycle of the signal for a given channel.
        result is in percent.
        """
        self._validate_channel(channel)
        result = float(
            self.__parse_output(self.__send_command(command=f":r{28 + channel}=0.\n"))
        )
        return round(result / 10, 1)

    def set_dutycycle(self, channel: int, value: float) -> str:
        """
        Set the sudycycle of the signal for a given channel (in percent).
        """
        dutycycle: float = round(value, 1)
        self._validate_channel(channel)
        self._validate_dutycycle(dutycycle)

        reg_val: int = int((dutycycle * 10))
        return self.__parse_output(
            self.__send_command(command=f":w{28 + channel}={reg_val}.\n")
        )

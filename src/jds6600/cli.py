import argparse
import sys
from jds6600 import JDS6600
from typing import Callable


def f_channel(args: argparse.ArgumentParser) -> None:
    """Operations on the channels."""
    with JDS6600(port=args.port) as sg:
        if not hasattr(args, "value"):
            ch1, ch2 = sg.get_channels()
            print(f"channel1: {ch1}, channel2: {ch2}.")
        else:
            if not hasattr(args, "channel_id"):
                print("Setting the status of a channel requires the channel_id!")
            



def _add_common_args(subparser: argparse.ArgumentParser, target_function: Callable) -> None:
    subparser.add_argument("-p", "--port", help="USB port where the waveform generator is connected.")
    subparser.add_argument("-c", "--channel_id", type=int, help="The channel number (1 or 2).")
    subparser.set_defaults(func=target_function)


def cli_builder() -> argparse.ArgumentParser:
    """Build the CLI."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='options to set or read from the JDS6600 Signal Generator.')
    
    p_channel = subparsers.add_parser('channel', help='Read or set the channel status.')
    p_channel.add_argument("-v", "--value", type=int, help="The channel status (0=off, 1=on).")
    _add_common_args(p_channel, f_channel)
    
    return parser


if __name__ == "__main__":

    parser = cli_builder()

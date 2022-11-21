import argparse
from jds6600 import JDS6600
from typing import Callable, Optional, Set, Dict
import json


def f_channel(args: argparse.ArgumentParser) -> None:
    """Operations on the channels."""
    out_dict = {}
    channels = _define_channels(args.channel_id)

    with JDS6600(port=args.port) as sg:
        state = list(sg.get_channels())

        if args.value is not None:
            for channel in channels:
                state[channel - 1] = args.value == 1
            sg.set_channels(*state)

        for i, channel_state in enumerate(state):
            out_dict[i] = channel_state

        dump_output(args.print_json, out_dict)


def dump_output(print_json: bool, data: Dict) -> None:
    """Print the output."""
    if print_json:
        print(json.dumps(data))
    else:
        for ch, value in data.items():
            print(f"channel{ch}: {value}")


def _define_channels(channel_id: Optional[int]) -> Set:
    """Define the channels wet command applies to."""
    return set([1, 2]) if channel_id is None else set([channel_id])


def _add_common_args(
    subparser: argparse.ArgumentParser, target_function: Callable
) -> None:
    subparser.add_argument(
        "-p", "--port", help="USB port where the waveform generator is connected."
    )
    subparser.add_argument(
        "-c",
        "--channel_id",
        type=int,
        required=False,
        help="The channel number (1 or 2). If omitted, command applies to both channels.",
    )
    subparser.add_argument(
        "-j",
        "--json",
        action="store_true",
        dest="print_json",
        required=False,
        help="Print output in JSON (default is text.)",
    )
    subparser.set_defaults(func=target_function)


def cli_builder() -> argparse.ArgumentParser:
    """Build the CLI."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help="options to set or read from the JDS6600 Signal Generator."
    )

    p_channel = subparsers.add_parser("channel", help="Read or set the channel status.")
    p_channel.add_argument(
        "-v", "--value", type=int, help="The channel status (0=off, 1=on)."
    )
    _add_common_args(p_channel, f_channel)

    return parser


def main():
    """Main entry point."""
    parser = cli_builder()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

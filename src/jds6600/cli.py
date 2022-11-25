import argparse
from jds6600 import JDS6600, WAVEFORMS
from typing import Callable, Optional, Set, Dict
import json
import sys


def f_channel(args: argparse.Namespace) -> None:
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


def f_waveform(args: argparse.Namespace) -> None:
    """Operations on the waveform."""
    _generic_channel_operation(args, "waveform")


def f_frequency(args: argparse.Namespace) -> None:
    """Operations on the frequency."""
    _generic_channel_operation(args, "frequency")


def f_amplitude(args: argparse.Namespace) -> None:
    """Operations on the amplitude."""
    _generic_channel_operation(args, "amplitude")


def f_offset(args: argparse.Namespace) -> None:
    """Operations on the offset."""
    _generic_channel_operation(args, "offset")


def f_dutycycle(args: argparse.Namespace) -> None:
    """Operations on the offset."""
    _generic_channel_operation(args, "dutycycle")


def _generic_channel_operation(args: argparse.Namespace, option: str) -> None:
    """
    Wrapper for most channel operations. Only the channel status operations require
    a different way of handling.
    """
    out_dict = {}
    channels = _define_channels(args.channel_id)

    try:
        with JDS6600(port=args.port) as sg:
            setter = getattr(sg, "set_{}".format(option))
            getter = getattr(sg, "get_{}".format(option))

            for channel in channels:
                if args.value is not None:
                    if setter(channel, args.value) == "ok":
                        out_dict[channel] = args.value
                    else:
                        out_dict[channel] = "ERROR!"
                else:
                    out_dict[channel] = getter(channel)

        dump_output(args.print_json, out_dict)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)


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
    """Arguments that apply to every command. Also map the function to run to the command."""
    subparser.add_argument(
        "-p",
        "--port",
        required=True,
        help="USB port where the waveform generator is connected.",
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
    _add_common_args(p_channel, f_channel)
    p_channel.add_argument(
        "-v", "--value", type=int, help="The channel status (0=off, 1=on)."
    )

    p_waveform = subparsers.add_parser(
        "waveform", help="Read or set the waveform type."
    )
    _add_common_args(p_waveform, f_waveform)
    p_waveform.add_argument(
        "-v",
        "--value",
        type=str,
        help="The type of waveform ({}).".format(", ".join(WAVEFORMS)),
    )

    p_frequency = subparsers.add_parser(
        "frequency", help="Read or set the frequency (in Hz)."
    )
    _add_common_args(p_frequency, f_frequency)
    p_frequency.add_argument(
        "-v", "--value", type=float, help="The Frequency of the waveform in Hz."
    )

    p_amplitude = subparsers.add_parser(
        "amplitude", help="Read or set the amplitude (in Volt)."
    )
    _add_common_args(p_amplitude, f_amplitude)
    p_amplitude.add_argument(
        "-v", "--value", type=float, help="The amplitude of the waveform in Volt."
    )

    p_offset = subparsers.add_parser(
        "offset", help="Read or set the offset of the signal (in Volt)."
    )
    _add_common_args(p_offset, f_offset)
    p_offset.add_argument(
        "-v", "--value", type=float, help="The offset of the waveform in Volt."
    )

    p_dutycycle = subparsers.add_parser(
        "dutycycle", help="Read or set the duty cycle (in percent)."
    )
    _add_common_args(p_dutycycle, f_dutycycle)
    p_dutycycle.add_argument(
        "-v", "--value", type=float, help="The duty cycle of the waveform in percent."
    )

    return parser


def main():
    """Main entry point."""
    parser = cli_builder()

    if len(sys.argv) < 2:
        parser.parse_args(["-h"])
        sys.exit(2)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

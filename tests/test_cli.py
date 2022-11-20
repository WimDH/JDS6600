from jds6600.cli import cli_builder


def test_channel():
    """Test the channel command."""
    parser = cli_builder()
    args = parser.parse_args("channel -p /dev/ttyUSB3 -c 1 -v 2".split())

    assert args.port == '/dev/ttyUSB3'
    assert args.channel_id == 1
    assert args.value == 2


import sys
from argparse import ArgumentParser

class CmdLineInterface:
    """
    """

    def __init__(self, cli_args: list=None):
        if cli_args is None:
            cli_args = sys.argv[1:]

        self._parser = ArgumentParser(allow_abbrev=False)

        self._parser.add_argument(
            'Game', metavar='rom', type=str,
            help=(
                'Name of the game to run. '
                'See pychip8/roms for a list of available games.'
            )
        )

        self._parser.add_argument(
            '--scale', '-s', type=int, default=10,
            metavar='', dest='display_scale',
            help=(
                'Set a scale factor to resize the graphical display.',
                'The original Chip8 display was 64x32 pixels,'
                ' scaling by x10 to 640x320 is the default.'
            )
        )

        self.parsed_args = vars(self._parser.parse_args(cli_args))
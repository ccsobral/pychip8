import unittest

from pychip8.cli import CmdLineInterface 

class TestCLI(unittest.TestCase):
    def test_cli_args(self):
        test_args = ['test_rom', '-d', '64x32']
        expected_args = {
            'Game': 'test_rom', 'display_size': '64x32',
        }
        self.assertEqual(CmdLineInterface(test_args).parsed_args, expected_args)

    def test_optional_defaults(self):
        test_args = ['test_rom']
        expected_args = {
            'Game': 'test_rom', 'display_size': '640x320',
        }
        self.assertEqual(
            CmdLineInterface(test_args).parsed_args, expected_args
        )

if __name__ == '__main__':
    unittest.main()
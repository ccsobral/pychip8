from time import perf_counter, sleep

import numpy as np
import sdl2
import sdl2.ext

from pychip8 import cli, cpu, display, key_input

class Chip8:
    """
    """

    def __init__(self):
        self._cli = cli.CmdLineInterface()
        self._args = self._cli.parsed_args
        self._cpu = cpu.Cpu()
        self._display = display.Display(self._args['display_scale'])
        self._fps = 1.0 / 60.0
        self._key_input = key_input.KeyInput(self._cpu.key_presses)
        self._open_rom()

    def _open_rom(self):
        with open(self._args['Game'], 'rb') as f_rom:
            self._cpu.load_rom(f_rom.read())

    def run(self):
        """Runs the emulator loop.
        """

        self._exit = False
        while not self._exit:
            start_frame = perf_counter()
            delta_time = 0.0
            while delta_time < self._fps:
                self._key_input.process_events()
                self._cpu.run_cycle()
                if self._cpu.draw_flag:
                    np.copyto(self._cpu.draw_flag, False)
                    self._display.update_pixel_grid(self._cpu.pixel_buffer)
                sleep(self._fps/6)
                delta_time = perf_counter() - start_frame
            self._cpu.decrease_timers()
            self._exit = self._key_input.update_exit_status()

    def __repr__(self):
        params = [f'{param}: {value!r}' for param, value in self._args.items()]
        return 'Chip8({})'.format(', '.join(params))

if __name__ == '__main__':
    instance = Chip8()
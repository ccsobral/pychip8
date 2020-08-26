import numpy as np
import tkinter as tk

import sdl2
import sdl2.ext

class KeyInput():
    """Class handling keyboard input.

    The Chip8 has a 16-key input in a 4x4 grid.
    """

    _key_list = [
        sdl2.SDLK_1, sdl2.SDLK_2, sdl2.SDLK_3, sdl2.SDLK_4,
        sdl2.SDLK_q, sdl2.SDLK_w, sdl2.SDLK_e, sdl2.SDLK_r,
        sdl2.SDLK_a, sdl2.SDLK_s, sdl2.SDLK_d, sdl2.SDLK_f,
        sdl2.SDLK_z, sdl2.SDLK_x, sdl2.SDLK_c, sdl2.SDLK_v,
        ]

    def __init__(self, key_presses: np.array):
        self._key_array = key_presses
        self._exit_status = False

    def process_events(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                self._exit_status = True
            elif event.type in (sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP):
                key_sym = event.key.keysym.sym
                if key_sym in KeyInput._key_list:
                    idx = KeyInput._key_list.index(key_sym)
                    #if a key is pressed
                    if event.type == sdl2.SDL_KEYDOWN:
                        self._key_array[idx] = True
                    #if a key is released
                    elif event.type == sdl2.SDL_KEYUP:
                        self._key_array[idx] = False

    def update_exit_status(self):
        return self._exit_status

'''
class KeyInput():
    """Class handling keyboard input.

    The Chip8 has a 16-key input in a 4x4 grid.
    """

    _key_list = [
        '1', '2', '3', '4',
        'q', 'w', 'e', 'r',
        'a', 's', 'd', 'f',
        'z', 'x', 'c', 'v'
        ]

    def __init__(self, tk_manager: tk.Tk, key_presses: np.array):
        self._tk_manager = tk_manager
        self._tk_manager.bind('<Key>', self._on_press)
        self._tk_manager.bind('<KeyRelease>', self._on_release)
        self._key_array = key_presses
        self._exit_status = False

    def _on_press(self, key):
        key_str = key.keysym
        if key_str in KeyInput._key_list:
            idx = KeyInput._key_list.index(key_str)
            #This should suffice to update the key state
            self._key_array[idx] = True
            #print(key_str, idx, self._key_array)

    def _on_release(self, key):
        #Stop emulation if escape key is pressed
        key_str = key.keysym
        if key_str == 'Return':
            self._exit_status = True
        if key_str in KeyInput._key_list:
            idx = KeyInput._key_list.index(key_str)
            self._key_array[idx] = False

    def update_exit_status(self):
        return self._exit_status
'''
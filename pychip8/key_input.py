import tkinter as tk
import numpy as np

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
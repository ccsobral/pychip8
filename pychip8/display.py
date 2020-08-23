import tkinter as tk
from itertools import product

import numpy as np

class Display:
    """Manager class to handle graphical output.

    Args:
        tk_manager: The tkinter manager handling graphics and input.
        display_scale: Sets the scale factor of the graphics window.
    
    Attributes:
        pixel_buffer: Array of bools storing the current state of the pixel grid.
            (pixel_buffer[i][j] == True means that pixel is active/on)
    """

    _original_width, _original_height = 64, 32
    
    def __init__(self, tk_manager: tk.Tk, display_scale: int = 10):
        #self._check_integer_dimensions(display_size)
        #self._check_valid_dimensions()
        self._display_scale = display_scale
        self._width = self._display_scale * Display._original_width
        self._height = self._display_scale * Display._original_height
        self._pixel_width = self._display_scale
        self._pixel_height = self._display_scale

        self._pixel_ids = np.zeros(32*64, dtype=int)

        self.px_color_off = 'black'
        self.px_color_on = 'green'

        self._tk_manager = tk_manager
        self._tk_manager.geometry(f'{self._width}x{self._height}')
        self._tk_manager.resizable(width=False, height=False)

        self._display = tk.Canvas(
            tk_manager, width = self._width, height = self._height
        )
        self._display.pack()
        self._create_pixel_grid()
    
    #def _check_integer_dimensions(self, display_size: str):
    #    """Raises error if display_size can't be split into two integers.
    #    """

    #    try:
    #        self._width, self._height = map(int, display_size.split('x'))
    #    except ValueError:
    #        print(
    #            'Could not extract width and height from display size!',
    #            f'The input display size was {display_size!r}\n',
    #            sep='\n'
    #        )
    #        raise

    #def _check_valid_dimensions(self):
    #    """Raises error if the requested dimensions of the tkinter window
    #    are not multiple of 64x32.

    #    This may change later on, but I think the output looks distorted
    #    if the width and height of the window can take arbitrary values.

    #    Raises:
    #        ValueError: if width not multiple of 64 or height not multiple of 32.
    #    """

    #    self._is_width_multiple = (
    #        True if self._width % Display._original_width == 0 else False
    #    )
    #    self._is_height_multiple = (
    #        True if self._height % Display._original_height == 0 else False
    #    )
    #    if not self._is_width_multiple or not self._is_height_multiple:
    #        raise ValueError(
    #            'Display width should be a number multiple of 64'
    #            ' and height should be multiple of 32.'
    #        )

    def _create_pixel_grid(self):
        """Defines the virtual 64x32 Chip8 display.

        The Chip8 display is 64x32 pixels so in practice we define "virtual pixels",
        where each is actually `display_scale` pixels wide and tall.
        """
        
        pixel_grid = product(
            range(0, self._height, self._pixel_height),
            range(0, self._width, self._pixel_width)
        )

        for y_pos, x_pos in pixel_grid:
            pixel_id = self._display.create_rectangle(
                x_pos, y_pos, 
                x_pos + self._pixel_width, y_pos + self._pixel_height,
                fill=self.px_color_off, outline=self.px_color_off
            )
            self._pixel_ids[pixel_id-1] = pixel_id

        self._tk_manager.update()

    def update_pixel_grid(self, pixel_buffer: np.array):
        """Updates graphical output to show the current game state.
        """

        for pixel_id, is_pixel_on in zip(
                self._pixel_ids, pixel_buffer.reshape(-1)
        ):
            #print(pixel_id, is_pixel_on)
            if is_pixel_on:
                self._display.itemconfigure(pixel_id, fill=self.px_color_on)
            else:
                self._display.itemconfigure(pixel_id, fill=self.px_color_off)
        self._tk_manager.update()

    def __repr__(self):
        return f'Display({self._width!r}, {self._height!r})'
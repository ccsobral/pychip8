import ctypes
from itertools import product

import numpy as np
import sdl2

class Display:
    """Manager class to handle graphical output.

    Args:
        display_scale: Sets the scale factor of the graphics window.
    
    Attributes:
        pixel_buffer: Array of bools storing the current state of the pixel grid.
            (pixel_buffer[i][j] == True means that pixel is active/on)
    """

    _original_width, _original_height = 64, 32
    
    def __init__(self, display_scale: int = 10):
        self._display_scale = display_scale
        self._width = self._display_scale * Display._original_width
        self._height = self._display_scale * Display._original_height
        self._pixels = np.zeros(
            Display._original_width*Display._original_height,
            dtype = np.uint32
        )

        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
            raise sdl2.ext.SDLError()

        self._window = sdl2.SDL_CreateWindow(
            b'pychip8',
            sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED,
            self._width, self._height,
            sdl2.SDL_WINDOW_SHOWN
        )
        if not self._window:
            raise sdl2.ext.SDLError()

        self._renderer = sdl2.SDL_CreateRenderer(
            self._window, -1, sdl2.SDL_RENDERER_ACCELERATED
        )
        if not self._renderer:
            raise sdl2.ext.SDLError()

        self._texture = sdl2.SDL_CreateTexture(
            self._renderer,
            sdl2.SDL_PIXELFORMAT_ARGB8888,
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            Display._original_width, Display._original_height
        )
        if not self._texture:
            raise sdl2.ext.SDLError()

        sdl2.SDL_RenderClear(self._renderer)
        sdl2.SDL_RenderPresent(self._renderer)
    
    def update_pixel_grid(self, pixel_buffer: np.array):
        """Updates graphical output to show the current game state.
        """
        
        self._pixels[:] = pixel_buffer[:] * 0xFF00FF00
        sdl2.SDL_UpdateTexture(
            self._texture,
            None,
            self._pixels.ctypes.data_as(ctypes.c_void_p),
            ctypes.c_int(4*Display._original_width)
        )

        sdl2.SDL_RenderClear(self._renderer)
        sdl2.SDL_RenderCopy(self._renderer, self._texture, None, None)
        sdl2.SDL_RenderPresent(self._renderer)

    def __repr__(self):
        return f'Display({self._width!r}, {self._height!r})'
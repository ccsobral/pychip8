import ctypes
import numpy as np
import sdl2
import sdl2.ext
import array

width, height = 640, 320

if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
    raise sdl2.SDL_GetError()

window = sdl2.SDL_CreateWindow(
    b'pychip8', 
    sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED,
    width, height,
    sdl2.SDL_WINDOW_SHOWN
)
if not window:
    raise sdl2.SDL_GetError()

renderer = sdl2.SDL_CreateRenderer(
    window, -1, sdl2.SDL_RENDERER_ACCELERATED
)
if not renderer:
    raise sdl2.SDL_GetError()
#sdl2.SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
texture = sdl2.SDL_CreateTexture(
    renderer, 
    sdl2.SDL_PIXELFORMAT_ARGB8888, 
    sdl2.SDL_TEXTUREACCESS_STREAMING,
    64, 32
)
if not texture:
    raise sdl2.ext.SDLError()
sdl2.SDL_RenderClear(renderer)
sdl2.SDL_RenderPresent(renderer)


buf = np.zeros(64*32, dtype=np.uint32)
#buf[:] = 0xFFFF0000
#sdl2.SDL_UpdateTexture(
#    texture, 
#    None, 
#    buf.ctypes.data_as(ctypes.c_void_p),
#    ctypes.c_int(4*64)
#)
c_p = ctypes.POINTER(ctypes.c_void_p)
c_i = ctypes.POINTER(ctypes.c_int)
sdl2.SDL_LockTexture(
    texture, 
    None, 
    c_p(buf.ctypes.data_as(ctypes.c_void_p)), 
    c_i(ctypes.c_int(4*64))
)
buf[:] = 0xFFFF0000
sdl2.SDL_UnlockTexture(texture)
#print(buf)

sdl2.SDL_RenderClear(renderer)
sdl2.SDL_RenderCopy(renderer, texture, None, None)
sdl2.SDL_RenderPresent(renderer)

'''
#buf = np.ones(64*32)
#print(buf)
#sdl2.SDL_LockTexture(texture, None, buf.ctypes.data_as(ctypes.c_void_p), ctypes.c_int(64))
#print(buf)

rng = np.random.default_rng()
buf = 0xFF*rng.integers(2, size=64*32, dtype=np.uint8)
print(buf.reshape((32,64)))

sdl2.SDL_LockTexture(texture, None, buf.ctypes.data_as(ctypes.c_void_p), ctypes.c_int(64))
buf[:] = 0xFF*rng.integers(2, size=64*32, dtype=np.uint8)
print(buf.reshape((32,64)))
sdl2.SDL_UnlockTexture(texture)
#sdl2.SDL_UpdateTexture(texture, None, buf.__array_interface__['data'][0], ctypes.c_int(64))
#sdl2.SDL_UpdateTexture(texture, None, buf.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), ctypes.c_int(64))

#sdl2.SDL_RenderClear(renderer)
sdl2.SDL_RenderCopy(renderer, texture, None, None)
sdl2.SDL_RenderPresent(renderer)
'''
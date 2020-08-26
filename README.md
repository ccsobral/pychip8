# pychip8
CHIP-8 emulator implementation in Python.

From the top directory run as: `python -m pychip8 ./roms/ROMNAME`

## Setup
This emulator has very minimal requirements in terms of external packages: `numpy` and `pysdl2`.

Assuming you have `conda` installed, all* you need to do is `conda env create -f environment.yml`.
> \*On Linux, `pysdl2-dll` apparently has no effect, one has to install SDL2 via their distro's package manager (it might be install by default!).
The `Tk`-based branch runs well on Linux, so you may be able to avoid SDL if you so wish.
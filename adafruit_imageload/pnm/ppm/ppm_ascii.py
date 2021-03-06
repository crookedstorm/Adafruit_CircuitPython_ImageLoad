# The MIT License (MIT)
#
# Copyright (c) 2018 Scott Shawcroft for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_imageload.pnm.ppm.ppm_ascii`
====================================================

Load pixel values (indices or colors) into a bitmap and for an ascii ppm,
return None for pallet.

* Author(s):  Matt Land, Brooke Storm, Sam McGahan

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"

import struct


def load(file, width, height, max_colors, bitmap=None, palette=None):
    """Load an ascii ppm into the Bitmap object"""
    if bitmap:
        for y in range(height):
            offset = y * width
            for x in range(width):
                triplet = []
                color = bytearray()
                while True:
                    if len(triplet) == 3:
                        break
                    this_byte = file.read(1)
                    if this_byte.isdigit():
                        color += this_byte
                    else:
                        triplet.append(color)
                        color = bytearray()
                        continue
                pixel = bytearray(3)
                # This just became 8-bit only...
                struct.pack_into(
                    "BBB",
                    pixel,
                    0,
                    int("".join(["%c" % char for char in triplet[0]])),
                    int("".join(["%c" % char for char in triplet[1]])),
                    int("".join(["%c" % char for char in triplet[2]])),
                )
                bitmap[offset + x] = int.from_bytes(pixel, "little")

    return bitmap, palette

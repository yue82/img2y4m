#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PIL import Image
import numpy as np


def write_component(f, mat):
    f.write(mat.astype(np.uint8).tobytes())


def output_y4m(output_file, yuv_stream):
    with open(output_file, 'wb') as f:
        for yuv in yuv_stream:
            write_component(f, yuv[0])
            write_component(f, yuv[1])
            write_component(f, yuv[2])


def ex_fade_y(y, u, v, frames):
    return ([y * (0.9**i), u, v] for i in range(frames))


def yuv444p_main(rgb_image_file, output_file_prefix, make_stream_fun, frames):
    img = Image.open(rgb_image_file).convert('YCbCr')
    width, height = img.size
    y_t, u_t, v_t = np.array(img, dtype='float').T
    y, u, v = y_t.T, u_t.T, v_t.T

    output_y4m('{}.yuv'.format(output_file_prefix), make_stream_fun(y, u, v, frames))


if __name__ == '__main__':
    yuv444p_main('./image.jpg', './image', ex_fade_y, 20)

#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PIL import Image
import numpy as np


def trans_444_to_420(mat, width, height):
    return np.array([[np.sum(mat[row*2:row*2+2, col*2:col*2+2])/4
                     for col in range(int(width/2))]
                      for row in range(int(height/2))])


def write_stream_header(f, y4m_tags):
    f.write('YUV4MPEG2 {}\n'.format(
        ' '.join(['{}{}'.format(k, v) for k, v in y4m_tags.items()])).encode('utf-8'))


def write_frame_header(f, frame_tags):
    # frame tag 未対応
    f.write('FRAME\n'.encode('utf-8'))


def write_component(f, mat):
    f.write(mat.astype(np.uint8).tobytes())


def output_y4m(output_file, yuv_stream, y4m_tags):
    with open(output_file, 'wb') as f:
        write_stream_header(f, y4m_tags)
        for yuv in yuv_stream:
            write_frame_header(f, {})
            write_component(f, yuv[0])
            write_component(f, yuv[1])
            write_component(f, yuv[2])


def ex_fade_y(y, u, v, frames):
    return ([y * (0.9**i), u, v] for i in range(frames))


def yuv420p_main(rgb_image_file, output_file_prefix, y4m_tags, make_stream_fun, frames):
    img = Image.open(rgb_image_file).convert('YCbCr')
    width, height = img.size

    y_t, u_t, v_t = np.array(img, dtype='float').T
    y = y_t.T
    u_half = trans_444_to_420(u_t.T, width, height)
    v_half = trans_444_to_420(v_t.T, width, height)

    y4m_tags['C'] = '420mpeg2'            # yuv420
    y4m_tags['I'] = 'p'                   # プログレッシブ
    y4m_tags['W'], y4m_tags['H'] = width, height

    output_y4m('{}.y4m'.format(output_file_prefix), make_stream_fun(y, u_half, v_half, frames), y4m_tags)


if __name__ == '__main__':
    y4m_tags = {
        'F': '4:1',                     # フレームレート 4 fps
        'A': '1:1'                      # ピクセルアスペクト比 1:1
        }

    yuv420p_main('./image.jpg', './image', y4m_tags, ex_fade_y, 20)

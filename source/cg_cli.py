#!/usr/bin/env python
# -*- coding:utf-8 -*-

from cmath import log
import sys
import os
from turtle import width
import cg_algorithms as alg
import numpy as np
from PIL import Image


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    item_dict = {} # items container
    pen_color = np.zeros(3, np.uint8)
    width = 0
    height = 0

    with open(input_file, "r") as fp:
        line = fp.readline()
        while line:
            line = line.strip().split(' ')
            if line[0] == 'resetCanvas':
                width = int(line[1])
                height = int(line[2])
                item_dict = {} # clear existing items
            elif line[0] == 'saveCanvas':
                save_name = line[1]
                canvas = np.zeros([height, width, 3], np.uint8)
                canvas.fill(255)
                # render
                for item_type, p_list, algorithm, color in item_dict.values():
                    if item_type == 'line':
                        pass
                    elif item_type == 'polygon':
                        pass
                    elif item_type == 'ellipse':
                        pass
                    elif item_type == 'curve':
                        pass
                Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')
            elif line[0] == 'setColor':
                pass
            elif line[0] == 'drawLine':
                pass
            elif line[0] == 'drawPolygon':
                pass
            elif line[0] == 'drawEllipse':
                pass
            elif line[0] == 'drawCurve':
                pass
            elif line[0] == 'translate':
                pass
            elif line[0] == 'rotate':
                pass
            elif line[0] == 'scale':
                pass
            elif line[0] == 'clip':
                pass
            else:
                sys.stderr.write('Syntax error: Command not find.\n')
            line = fp.readline()


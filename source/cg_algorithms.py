#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
from unittest import result

def draw_line(p_list: list, algorithm: str) -> list :
    """Draw line

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) start and end coordinates
    :param algorithm: (string) Naive | DDA | Bresenham
    :return: (list of list of int: [[x0, y0], [x1, y1], ...]) list of pixels' coordinates
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append([x, int(y0 + k*(x - x0))])
    elif algorithm == 'DDA':
        # k = 0
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        # k = inf
        elif y0 == y1:
            for x in range(x0, x1 + 1):
                result.append([y0, x])
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            dx = x1 - x0
            dy = y1 - y0
            k = dy / dx
            delta = 0
            if k > -1 and k < 1:
                delta = k
                y = y0
                for x in range(x0, x1 + 1):
                    result.append([x, round(y)])
                    y = y + delta
            else:
                delta = abs(1 / k)
                x = x0
                ymax = (y1 + 1) if (dy > 0) else (y1 - 1)
                for y in range(y0, ymax):
                    result.append([round(x), y])
                    x = x + delta
    elif algorithm == 'Bresenham':
        pass
    return result
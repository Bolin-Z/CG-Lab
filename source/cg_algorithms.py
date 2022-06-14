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
    def draw_verticalLine(p_list: list) -> list :
        x0, y0 = p_list[0]
        y1 = p_list[1][1]
        result = []
        if y0 > y1:
            y0, y1 = y1, y0
        for y in range(y0, y1 + 1):
            result.append([x0, y])
        return result

    def draw_horizontalLine(p_list: list) -> list :
        x0, y0 = p_list[0]
        x1 = p_list[1][0]
        result = []
        if x0 > x1:
            x0, x1 = x1, x0
        for x in range(x0, x1 + 1):
            result.append([x, y0])
        return result

    def draw_diagonalLine(p_list: list) -> list :
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]
        result = []
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        d = 1 if (y1 > y0) else -1
        y = y0
        for x in range(x0, x1 + 1):
            result.append([x, y])
            y += d
        return result

    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    dx = x1 - x0
    dy = y1 - y0

    if x0 == x1:
        return draw_verticalLine(p_list)
    elif y0 == y1:
        return draw_horizontalLine(p_list)
    elif abs(dx) == abs(dy):
        return draw_diagonalLine(p_list)
    else:
        result = []
        k = dy / dx
        if algorithm == 'Naive':
            for x in range(x0, x1 + 1):
                result.append([x, int(y0 + k*(x - x0))])
        elif algorithm == 'DDA':
            delta = 0
            if abs(k) < 1:
                delta = k
                y = y0
                for x in range(x0, x1 + 1):
                    result.append([x, round(y)])
                    y = y + delta
            else:
                delta = abs(1 / k)
                x = x0
                ystep = 1 if (dy > 0) else - 1
                for y in range(y0, y1 + ystep, ystep):
                    result.append([round(x), y])
                    x = x + delta
        elif algorithm == 'Bresenham':
            absdx = abs(dx)
            absdy = abs(dy)
            if abs(k) < 1:
                ystep = 1 if k > 0 else -1
                p = 2*absdy - absdx
                result.append([x0, y0])
                y = y0
                for x in range(x0 + 1, x1 + 1):
                    if p >= 0:
                        y += ystep
                        p += 2*(absdy - absdx)
                    else:
                        p += 2*absdy
                    result.append([x, y])
            else:
                xstep = 1
                p = 2*absdx - absdy
                result.append([x0, y0])
                x = x0
                ystep = 1 if (dy > 0) else -1
                for y in range(y0 + ystep, y1 + ystep, ystep):
                    if p >= 0:
                        x += xstep
                        p += 2*(absdx - absdy)
                    else:
                        p += 2*absdx
                    result.append([x, y])
        return result
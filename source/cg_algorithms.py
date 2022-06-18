#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math

def draw_line(p_list: list, algorithm: str) -> list :
    """Draw line

    param p_list:    (list of list of int: [[x0, y0], [x1, y1]]) start and end points coordinates
    param algorithm: (string) valid algorithms Naive | DDA | Bresenham
    return:          (list of list of int: [[x0, y0], [x1, y1], ...]) list of pixels' coordinates
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

def draw_polygon(p_list : list, algorithm : str) -> list :
    """Draw polygon

    param p_list:    (list of list of int: [[x0, y0], [x1, y1], ... , [xk, yk]]) vertives coordinates of polygon
    param algorithm: (string) valid algorithms Naive | DDA | Bresenham
    return:          (list of list of int: [[x0, y0], [x1, y1], ... , [xn, yn]])
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result

def draw_ellipse(p_list: list) -> list:
    """Draw ellipse

    param p_list: (list of list of int: [[x0, y0], [x1, y1]]) the diagonal vertices coordinates
    return:       (list of list of int: [[x0, y0], [x1, y1], ... , [xn, yn]])
    """

    def mapping(src: list, center: list) -> list:
        result = []
        x, y = src
        xc, yc = center
        result.append([xc + x, yc + y])
        result.append([xc + x, yc - y])
        result.append([xc - x, yc - y])
        result.append([xc - x, yc + y])
        return result

    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    xc = round((x0 + x1) / 2)
    yc = round((y0 + y1) / 2)
    rx = round(abs(x0 - x1) / 2)
    ry = round(abs(y0 - y1) / 2)
    rx2 = rx * rx
    ry2 = ry * ry

    result = []
    x, y = 0, ry
    p = ry2 - rx2 * ry + 0.25 * rx2
    result += mapping([x, y], [xc, yc])
    
    while(ry2 * x < rx2 * y):
        if p < 0:
            p = p + 2*ry2*x + 3*ry2
            x += 1
        else:
            p = p + 2*ry2*x - 2*rx2*y + 2*rx2 + 3*ry2
            x += 1
            y -= 1
        result += mapping([x, y], [xc, yc])
    
    p = ry2*(x + 0.5)*(x + 0.5) + rx2*(y - 1)*(y - 1) - rx2 * ry2
    while y > 0:
        if p > 0:
            p = p - 2*rx2*y + 3*rx2
            y -= 1
        else:
            p = p + 2*ry2*x - 2*rx2*y + 2*ry2 + 3*rx2
            y -= 1
            x += 1
        result += mapping([x, y], [xc, yc])

    return result

def draw_curve(p_list: list, algorithm : str) -> list :
    """Draw curve

    param p_list:    (list of list of int: [[x0, y0], [x1, y1], ... , [xk, yk]]) control points
    param algorithm: (string) valid algorithms Bezier | B-spline
    return:          (list of list of int: [[x0, y0], [x1, y1], ... , [xn, yn]])
    """

    if len(p_list) <= 1:
        return p_list
    elif len(p_list) == 2:
        return draw_line(p_list, 'Bresenham')
    else:
        result = []
        
        if algorithm == 'Bezier':
            def getPointonCurve(p_list : list, u : float) -> list:
                """Get point on bezier curve given parameter u

                param p_list: (list of list of int: [[x0, y0], [x1, y1], ... , [xk, yk]]) control points
                param u:      (float) parameter
                return:       (list of int: [x, y]) the coordinate
                """
                p = []
                for i in range(0, len(p_list)):
                    p.append(p_list[i])
                for k in range(1, len(p_list)):
                    for s in range(0, len(p_list) - k):
                        p[s][0] = (1-u)*p[s][0] + u * p[s+1][0]
                        p[s][1] = (1-u)*p[s][1] + u * p[s+1][1]
                return [round(p[0][0]), round(p[0][1])]

            curvePoints = []
            u = 0.0
            step = 0.01
            while u <= 1.0:
                curvePoints.append(getPointonCurve(p_list, u))                
                u += step
            for i in range(1, len(curvePoints)):
                result += draw_line([curvePoints[i-1], curvePoints[i]], 'Bresenham')
        elif algorithm == 'B-spline':
            p = 3
            n = len(p_list) - 1
            m = n + p + 1
            # sample points number in each interval [u_{k}, u_{k+1})
            samplePointsNumber = 50
            knots = [ x * samplePointsNumber for x in range(0, m + 1)]
            points = []

            for k in range(p, m - p):
                for u in range(knots[k], knots[k+1]):
                    # u in [u_{k}, u_{k+1})
                    # deBoor-cox algorithm
                    s = 0 if (u != knots[k]) else 1
                    h = p - s
                    ctrlPoints = []
                    # ctrlPoints = {P_{k-p}, P_{k-p+1}, ..., P_{k-s-1}, P_{k-s}}
                    for affectedPoint in range(k - p, k - s + 1):
                        ctrlPoints.append(p_list[affectedPoint])
                    # calculate C(u)
                    for r in range(1, h + 1):
                        offset = k - p
                        # [P_{k-p+r}, P_{k-s}]
                        for i in range((k - s),(k - p + r) - 1,-1):
                            a = (u - knots[i]) / (knots[i+p-r+1] - knots[i])
                            ctrlPoints[i - offset] = [
                                (1 - a)*ctrlPoints[i-1-offset][0] + a*ctrlPoints[i-offset][0],
                                (1 - a)*ctrlPoints[i-1-offset][1] + a*ctrlPoints[i-offset][1]
                            ]
                    # P_{k-s, p-s} is the point C(u)
                    points.append( [round(ctrlPoints[-1][0]), round(ctrlPoints[-1][1])])
            # use line to connect points
            for i in range(0,len(points)-1):
                result += draw_line([points[i], points[i+1]], 'Bresenham')
        return result

def translate(p_list: list, dx: int, dy: int) -> None:
    """Traslation

    param p_list: (list of list of int: [[x0, y0], [x1, y1], ... , [xk, yk]]) control points
    param dx:     (int) horizontal offset
    param dy:     (int) vertical offset
    """

    for i in range(0,len(p_list)):
        p_list[i][0] += dx
        p_list[i][1] += dy

def rotate(p_list: list, xc:int, yc:int, r:int) -> None:
    """Rotation

    param p_list: (list of list of int: [[x0, y0], [x1, y1], ... , [xk, yk]]) control points
    param xc:     (int) x coordinate of rotate center
    param yc:     (int) y coordinate of rotate center
    param r:      (int) clockwise rotate degree
    """
    rad = r * math.pi / 180
    cos_r = math.cos(rad)
    sin_r = math.sin(rad)
    for i in range(0,len(p_list)):
        ox, oy = p_list[i]
        nx = xc + round((ox - xc)*cos_r - (oy - yc)*sin_r)
        ny = yc + round((oy - yc)*cos_r + (ox - xc)*sin_r)
        p_list[i] = [nx, ny]


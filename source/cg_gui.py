#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QWheelEvent
from PyQt5.QtCore import QRectF, Qt
from functools import partial


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        self.pen_color = [0, 0 , 0]
        self.item_cnt = 0
        self.last_transform_info = None

    def start_draw_line(self, algorithm):
        self.finish_draw()
        self.status = 'line'
        self.temp_algorithm = algorithm

    def start_draw_polygon(self, algorithm):
        self.finish_draw()
        self.status = 'polygon'
        self.temp_algorithm = algorithm
    
    def start_draw_ellipse(self):
        self.finish_draw()
        self.status = 'ellipse'
        self.temp_algorithm = ''
    
    def start_draw_curve(self, algorithm):
        self.finish_draw()
        self.status = 'curve'
        self.temp_algorithm = algorithm
    
    def start_translate(self):
        self.finish_draw()
        self.last_transform_info = None
        self.status = 'translate'
        self.temp_algorithm = ''
    
    def start_rotate(self):
        self.finish_draw()
        self.last_transform_info = None
        self.status = 'rotate'
        self.temp_algorithm = ''
    
    def start_scale(self):
        self.finish_draw()
        self.last_transform_info = None
        self.status = 'scale'
        self.temp_algorithm = ''
    
    def start_clip(self, algorithm):
        self.finish_draw()
        self.last_transform_info = None
        self.status = 'clip'
        self.temp_algorithm = algorithm

    def finish_draw(self):
        if self.temp_item != None:
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.temp_item = None
            self.temp_id = ''

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.status == 'rotate':
            if self.selected_id != '':
                if self.item_dict[self.selected_id].item_type != 'ellipse':
                    degree = 1 if event.angleDelta().y() > 0 else -1
                    fx, fy, fw, fh = self.item_dict[self.selected_id].boundingFrame
                    cx = round(fx + fw / 2)
                    cy = round(fy + fh / 2)
                    alg.rotate(self.item_dict[self.selected_id].p_list, cx, cy, degree)
                    self.item_dict[self.selected_id].calBoundingFrame()
        elif self.status == 'scale':
            if self.selected_id != '':
                s = 1.1 if event.angleDelta().y() > 0 else 0.9
                fx, fy, fw, fh = self.item_dict[self.selected_id].boundingFrame
                alg.scale(self.item_dict[self.selected_id].p_list, fx, fy, s)
                self.item_dict[self.selected_id].calBoundingFrame()
        self.updateScene([self.sceneRect()])
        super().wheelEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if event.buttons() == Qt.LeftButton:
            if self.status == 'line' or self.status == 'ellipse':
                if self.temp_item == None:
                    self.temp_id = str(self.item_cnt)
                    self.item_cnt += 1
                    self.temp_item = MyItem(self.temp_id, self.status, self.pen_color, [[x, y], [x, y]], self.temp_algorithm)
                    self.scene().addItem(self.temp_item)
                else:
                    self.temp_item.p_list[0] = self.temp_item.p_list[1]
                    self.temp_item.p_list[1] = [x, y]
                    self.temp_item.calBoundingFrame()
            elif self.status == 'polygon' or self.status == 'curve':
                if self.temp_item == None:
                    self.temp_id = str(self.item_cnt)
                    self.item_cnt += 1
                    self.temp_item = MyItem(self.temp_id, self.status, self.pen_color, [[x, y]], self.temp_algorithm)
                    self.scene().addItem(self.temp_item)
                else:
                    self.temp_item.p_list.append([x,y])
                    self.temp_item.calBoundingFrame()
            elif self.status == 'translate':
                if self.selected_id != '':
                    fx, fy, fw, fh = self.item_dict[self.selected_id].boundingFrame
                    cx = round(fx + fw / 2)
                    cy = round(fy + fh / 2)
                    self.last_transform_info = [cx, cy]
                    alg.translate(self.item_dict[self.selected_id].p_list, (x - cx), (y - cy))
                    self.item_dict[self.selected_id].calBoundingFrame()
            elif self.status == 'rotate':
                if self.selected_id != '':
                    if self.item_dict[self.selected_id].item_type != 'ellipse':
                        fx, fy, fw, fh = self.item_dict[self.selected_id].boundingFrame
                        cx = round(fx + fw / 2)
                        cy = round(fy + fh / 2)
                        alg.rotate(self.item_dict[self.selected_id].p_list, cx, cy, 1)
                        self.item_dict[self.selected_id].calBoundingFrame()
            elif self.status == 'scale':
                if self.selected_id != '':
                    s = 1.1
                    fx, fy, fw, fh = self.item_dict[self.selected_id].boundingFrame
                    alg.scale(self.item_dict[self.selected_id].p_list, fx, fy, s)
                    self.item_dict[self.selected_id].calBoundingFrame()
            elif self.status == 'clip':
                if self.selected_id != '':
                    if self.item_dict[self.selected_id].item_type == 'line':
                        if self.last_transform_info == None:
                            self.last_transform_info = {'last_line' : None, 'last_point' : [x, y]}
                        else:
                            if self.last_transform_info['last_point'] != None:
                                x0, y0 = self.last_transform_info['last_point']
                                x1, y1 = x, y
                                if len(self.item_dict[self.selected_id].p_list) == 2:
                                    xs, ys = self.item_dict[self.selected_id].p_list[0]
                                    xf, yf = self.item_dict[self.selected_id].p_list[1]
                                    self.last_transform_info['last_line'] = [[xs, ys],[xf, yf]]
                                    alg.clip(self.item_dict[self.selected_id].p_list, x0, y0, x1, y1, self.temp_algorithm)
                                    self.item_dict[self.selected_id].calBoundingFrame()
                                self.last_transform_info['last_point'] = None
                            else:
                                self.last_transform_info['last_point'] = [x, y]
        elif event.buttons() == Qt.RightButton:
            if self.status == 'line' or self.status == 'ellipse':
                if self.temp_item != None:
                    self.temp_item.p_list[1] = self.temp_item.p_list[0]
                    self.temp_item.calBoundingFrame()
            elif self.status == 'polygon' or self.status == 'curve':
                if self.temp_item != None:
                    if len(self.temp_item.p_list) > 1:
                        self.temp_item.p_list.pop()
                        self.temp_item.calBoundingFrame()
            elif self.status == 'translate':
                if self.selected_id != '' and self.last_transform_info != None:
                    fx, fy, fw, fh = self.item_dict[self.selected_id].boundingFrame
                    cx = round(fx + fw / 2)
                    cy = round(fy + fh / 2)
                    ox, oy = self.last_temp_pos
                    alg.translate(self.item_dict[self.selected_id].p_list, (ox - cx), (oy - cy))
                    self.item_dict[self.selected_id].calBoundingFrame()
                    self.last_transform_info = None
            elif self.status == 'rotate':
                if self.selected_id != '':
                    if self.item_dict[self.selected_id].item_type != 'ellipse':
                        fx, fy, fw, fh = self.item_dict[self.selected_id].boundingFrame
                        cx = round(fx + fw / 2)
                        cy = round(fy + fh / 2)
                        alg.rotate(self.item_dict[self.selected_id].p_list, cx, cy, -1)
                        self.item_dict[self.selected_id].calBoundingFrame()
            elif self.status == 'scale':
                if self.selected_id != '':
                    s = 0.9
                    fx, fy, fw, fh = self.item_dict[self.selected_id].boundingFrame
                    alg.scale(self.item_dict[self.selected_id].p_list, fx, fy, s)
                    self.item_dict[self.selected_id].calBoundingFrame()
            elif self.status == 'clip':
                if self.selected_id != '':
                    if self.item_dict[self.selected_id].item_type == 'line':
                        if self.last_transform_info != None:
                            if self.last_transform_info['last_line'] != None:
                                xs, ys = self.last_transform_info['last_line'][0]
                                xf, yf = self.last_transform_info['last_line'][1]
                                self.item_dict[self.selected_id].p_list = [[xs, ys],[xf, yf]]
                                self.item_dict[self.selected_id].calBoundingFrame()
                                self.last_transform_info['last_line'] = None
                                self.last_transform_info['last_point'] = None
        elif event.buttons() == Qt.MidButton:
            self.finish_draw()
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, pen_color: list, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        
        self.pen_color = pen_color  # 图元颜色, (R,G,B)
        self.boundingFrame = []     # 图元外方框 [ x, y, w, h]
        self.calBoundingFrame()
    
    def calBoundingFrame(self) -> None:
        if self.item_type == 'line' or self.item_type == 'ellipse':
            if len(self.p_list) == 0:
                self.boundingFrame = [0, 0, -2, -2]
            else:
                x0, y0 = self.p_list[0]
                x1, y1 = self.p_list[1]
                x = min(x0, x1)
                y = min(y0, y1)
                w = max(x0, x1) - x
                h = max(y0, y1) - y
                self.boundingFrame = [x , y, w, h]
        if self.item_type == 'polygon' or self.item_type == 'curve':
            if len(self.p_list) != 0:
                xmin, ymin = self.p_list[0]
                xmax, ymax = self.p_list[0]
                for item in self.p_list:
                    xmin = min(xmin, item[0])
                    xmax = max(xmax, item[0])
                    ymin = min(ymin, item[1])
                    ymax = max(ymax, item[1])
                self.boundingFrame = [xmin, ymin, xmax - xmin, ymax - ymin]
            else:
                self.boundingFrame = [0, 0, -2, -2]

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:        
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
        
        r, g, b = self.pen_color
        painter.setPen(QColor(r, g, b))
        for p in item_pixels:
            painter.drawPoint(*p)
        if self.selected:
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        x, y, w, h = self.boundingFrame
        return QRectF(x - 1, y - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(partial(self.line_action, 'Naive'))
        line_dda_act.triggered.connect(partial(self.line_action, 'DDA'))
        line_bresenham_act.triggered.connect(partial(self.line_action, 'Bresenham'))
        polygon_dda_act.triggered.connect(partial(self.polygon_action, 'DDA'))
        polygon_bresenham_act.triggered.connect(partial(self.polygon_action, 'Bresenham'))
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(partial(self.curve_action, 'Bezier'))
        curve_b_spline_act.triggered.connect(partial(self.curve_action, 'B-spline'))
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(partial(self.clip_action, 'Cohen-Sutherland'))
        clip_liang_barsky_act.triggered.connect(partial(self.clip_action, 'Liang-Barsky'))
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def line_action(self, algorithm):
        self.canvas_widget.start_draw_line(algorithm)
        self.statusBar().showMessage(algorithm + '算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def polygon_action(self, algorithm):
        self.canvas_widget.start_draw_polygon(algorithm)
        self.statusBar().showMessage(algorithm + '算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse()
        self.statusBar().showMessage('中点圆算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def curve_action(self, algorithm):
        self.canvas_widget.start_draw_curve(algorithm)
        self.statusBar().showMessage(algorithm + '算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()       
    
    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移图元')
    
    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转图元')
    
    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('缩放图元')
    
    def clip_action(self, algorithm):
        self.canvas_widget.start_clip(algorithm)
        self.statusBar().showMessage(algorithm + '算法裁剪线段')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

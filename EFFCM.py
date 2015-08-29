#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import xlrd
from enthought.traits.api import (HasTraits, File, HTML, List, Button)
from enthought.traits.ui.api import (View, VGroup, HGroup, Item, HTMLEditor)


def excel_table_byindex(f, colnameindex=0, by_index=0):
    data = xlrd.open_workbook(f)
    table = data.sheets()[by_index]
    coldata = table.col_values(2, start_rowx=4)
    return coldata
    # CSVGrapher.text = coldata
    # fw = open('768-9-4-313re.txt', 'w')
    # for line in coldata:
    #     temp = str(line)  # f.write只接受str类型的参数
    #     fw.write(temp)
    #     fw.write('\n')  # f.write不能自动添加换行符
    # fw.close()


# def save(f, data):  # 全部save
#     fw = open(f, 'w')

#     for line in data:

#         temp = str(line)  # f.write只接受str类型的参数
#         fw.write(temp)
#         fw.write('\n')  # f.write不能自动添加换行符

#     fw.close()


# def save(f, data):  # 分阶次save
#     fw = open(f, 'w')
#     index = 0
#     for line in data:  # 2-24 200-512阶
#         if index % 2048 >= 8 and index % 2048 <= 96 or index % 2048 >= 800 and index % 2048 <= 2047:
#             temp = str(line)  # f.write只接受str类型的参数
#             fw.write(temp)
#             fw.write('\n')  # f.write不能自动添加换行符
#         index += 1
#     fw.close()


# def add(f, data):  # 分阶次add
#     fw = open(f, 'a')
#     index = 0
#     for line in data:  # 2-24 200-512阶
#         if index % 2048 >= 8 and index % 2048 <= 96 or index % 2048 >= 800 and index % 2048 <= 2047:
#             temp = str(line)  # f.write只接受str类型的参数
#             fw.write(temp)
#             fw.write('\n')  # f.write不能自动添加换行符
#         index += 1
#     fw.close()

def add(f, data):  # 全阶次add
    fw = open(f, 'a')
    for line in data:
        temp = str(line)  # f.write只接受str类型的参数
        fw.write(temp)
        fw.write('\n')  # f.write不能自动添加换行符
    fw.close()


class Graph(HasTraits):
    """
    绘图组件，包括左边的数据选择控件和右边的绘图控件
    """
    name = Str  # 绘图名，显示在标签页标题和绘图标题中
    button = Button(u"画图")  # 快速清除Y轴的所有选择的数据
    data_source = Instance(DataSource)  # 保存数据的数据源
    figure = Instance(Figure)  # 控制绘图控件的Figure对象
    view = View(
        VGroup(
            Item("button"),  # 清除按钮
            # 右边绘图控件
            Item("figure", editor=MPLFigureEditor(), show_label=False, width=600)
        )
        )

    def _figure_default(self):
        """
        figure属性的缺省值，直接创建一个Figure对象
        """
        self.name = "xls"
        figure = Figure()
        figure.add_axes([0.1, 0.1, 0.85, 0.80])  # 添加绘图区域，四周留有边距
        return figure


class CSVGrapher(HasTraits):
    data = List
    csv_file_name = File(filter=[u"*.xls"])  # 文件选择
    save_name = File(filter=[u"*.txt"])
    add_data_button = Button(u"添加数据")  # 添加数据按钮
    mean_button = Button(u"计算均值")  # 添加计算均值
    draw_button = Button(u"画图")
    sample_text = ("""
<html><body><h1>Choose a xls file</h1>

""")

    my_html_trait = HTML(sample_text)
    # button = Button(u"画图")
    view = View(
        # 整个窗口分为上下两个部分
        VGroup(

            Item("csv_file_name", label="selcect xls file", width=400),
            Item("save_name", label="save file", width=400),
            HGroup(
                Item("add_data_button", show_label=False, width=100, height=400),  # 添加绘图按钮
                Item('my_html_trait', show_label=False, editor=HTMLEditor(format_text=True), width=100, height=400),
                Item("mean_button", show_label=False, width=100, height=400),
                Item("draw_button")
                )),
        resizable=True,
        buttons=['OK'],
        height=0.4,
        width=0.4,
        title="xls processor"
    )

    def update(self):
        self.my_html_trait = ("""
<html><body><h1>The convert is over!</h1>
<html><body><h1>Please enter the "添加数据"</h1>

""")

    def _csv_file_name_changed(self):
        self.data = excel_table_byindex(self.csv_file_name)
        self.my_html_trait = ("""
<html><body><h1>Choose save txt file</h1>

""")
        # excel_table_byindex(self.csv_file_name)
        # self.update()

        # self.text = "The Convert is over!"

    def _save_name_changed(self):
        # print self.save_name
        # save(self.save_name, self.data)
        self.update()

    def mean_button_changed(self):
        dataMat = np.mat(self.data)
        dataMat.reshape(-1, 2048)
        meanVals = np.mean(dataMat, axis=0)


    def draw_button_changed(self):
        dataMat = np.mat(self.data)


    def _add_data_button_changed(self):
        """
        添加数据按钮的事件处理
        """
        # f = open(self.save_name, 'r+')
        # if f is not None:  # 如果文件为空，则添加新数据，
        #     add(self.save_name, self.data)
        # else:
        #     save(self.save_name, self.data)
        try:
            add(self.save_name, self.data)
        except Exception, e:
            self.my_html_trait = ("""
<html><body><h1>Error, choose a excel</h1>

""")
            raise e
        else:
            self.my_html_trait = ("""
<html><body><h1>add complete, choose another excel or enter the "OK" to exit</h1>

""")


if __name__ == "__main__":
    csv_grapher = CSVGrapher()
    csv_grapher.configure_traits()
# raw_input()

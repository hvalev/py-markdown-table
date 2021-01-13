# -*- coding: utf-8 -*-
import math


class markdownTable():
    """
    A class used to generate padded tables in a markdown code block
    ...

    Args:
    data (list): List of dicts with uniform key : value pairs.
    The keys will be used for generating the header and values -- the rows.
    row_sep (str): A flag used to indicate how and where to insert row separators. Possible values are 'always'/'topbottom'/None where:
                   'always 'inserts separators between each individual data row
                   'topbottom' inserts separators above the header and below the last row
                   'None' omits the insertion of a row separator
    padding_width (int): Value used to indicate how much extra padding to insert to table cells.
    padding_weight (str): Flag used to indicate the strategy of applying the padding indicated through padding_width.
                   Possible values are 'left'/'right'/'centerleft'/'centerright' where:
                   'left' aligns items in cells to the end of the cell
                   'right' aligns items in cells to the beginning of the cell
                   'centerleft' centers items with the extra padding allocated to the beginning of the cell
                   'centerright' centers items with the extra padding allocated to the end of the cell
    padding_char (str): Custom character to fill extra and normal padding with. Default is a blank space.
    newline_char (str): Custom character to be used for indicating a newline

    Methods
    -------
    getHeader()
        gets unescaped table header
    getBody()
        gets unescaped table content
    getMarkdown()
        gets complete escaped markdown table
    """

    def __init__(self, data):
        self.data = data
        self.validate()
        self.row_sep = 'always'
        self.padding_width = 0
        self.padding_weight = 'centerleft'
        self.padding_char = ' '
        self.newline_char = '\n'
        return

    def setParams(self, row_sep='always', padding_width=0, padding_weight='centerleft', padding_char=' ', newline_char='\n'):
        self.row_sep = row_sep
        self.padding_width = padding_width
        self.padding_weight = padding_weight
        self.padding_char = padding_char
        self.newline_char = newline_char
        return self

    def validate(self):
        if len(self.data) < 1:
            raise Exception('Data variable is empty')
        keys = self.data[0].keys()
        for item in self.data:
            for key in keys:
                if key not in item:
                    raise Exception('Keys are not uniform')

    def getPadding(self):
        padding = dict()
        for item in self.data[0].keys():
            padding[item] = len(item)
        for item in self.data:
            for key in item.keys():
                if (padding[key]-self.padding_width) < len(str(item[key])):
                    padding[key] = len(str(item[key]))+self.padding_width
        return padding

    def getRowSepStr(self):
        row_sep_str = ''
        for value in self.getPadding().values():
            row_sep_str = row_sep_str + '+' + '-'*value
        row_sep_str = row_sep_str + '+'
        return row_sep_str

    def getRowSepLast(self):
        row_sep_str_last = '+'
        for value in self.getPadding().values():
            row_sep_str_last = row_sep_str_last + '-'*(value+1)
        row_sep_str_last = row_sep_str_last[:-1] + '+'
        return row_sep_str_last

    def getMargin(self, margin):
        if self.padding_weight == 'left':
            left = margin
        elif self.padding_weight == 'right':
            left = 0
        elif self.padding_weight == 'centerleft':
            left = math.ceil(margin/2)
        elif self.padding_weight == 'centerright':
            left = math.floor(margin/2)
        else:
            left = math.ceil(margin/2)
        right = margin - left
        return right

    def getMarkdown(self):
        return '```'+self.getHeader()+self.getBody()+'```'

    def getHeader(self):
        header = ''
        if self.row_sep == 'topbottom' or 'always':
            header = header + self.newline_char + self.getRowSepLast() + self.newline_char
        for key in self.data[0].keys():
            margin = self.getPadding()[key]-len(key)
            right = self.getMargin(margin)
            header += '|' + key.rjust(self.getPadding()[key]-right, self.padding_char).ljust(self.getPadding()[key], self.padding_char)
        header = header + '|' + self.newline_char
        if self.row_sep == 'always':
            header = header + self.getRowSepStr() + self.newline_char
        return header

    def getBody(self):
        rows = ''
        for ix, item in enumerate(self.data):
            for key in self.data[0].keys():
                margin = self.getPadding()[key]-len(str(item[key]))
                right = self.getMargin(margin)
                rows += '|' + str(item[key]).rjust(self.getPadding()[key]-right, self.padding_char).ljust(self.getPadding()[key], self.padding_char)
            rows += '|'
            if(ix < len(self.data)-1):
                rows = rows + self.newline_char
            if self.row_sep == 'always' and ix < len(self.data)-1:
                rows = rows + self.getRowSepStr() + self.newline_char
            if (self.row_sep == 'always' or self.row_sep == 'topbottom') and ix == len(self.data)-1:
                rows = rows + self.newline_char + self.getRowSepLast()
        return rows

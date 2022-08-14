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
    float_rounding (int): decimal place to round float values to. Default is 2, but can also be set to 'None' to show complete values

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
        self.float_rounding = 2
        self.multiline = False
        self.quote = True
        return

    def setParams(
            self,
            row_sep='always',
            padding_width=0,
            padding_weight='centerleft',
            padding_char=' ',
            newline_char='\n',
            float_rounding=2,
            multiline=False,
            quote=True):
        self.row_sep = row_sep
        self.padding_width = padding_width
        self.padding_weight = padding_weight
        self.padding_char = padding_char
        self.newline_char = newline_char
        self.float_rounding = float_rounding
        self.multiline = multiline
        self.quote = quote
        self.updateMetaParams()
        return self

    def updateMetaParams(self):
        self.var_padding = self.getPadding()
        self.var_row_sep = self.getRowSepStr()
        self.var_row_sep_last = self.getRowSepLast()

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
                if (type(item[key]) is float and self.float_rounding):
                    item[key] = round(item[key], self.float_rounding)
                if self.multiline:
                    multiline_data = item[key].split(" ")
                    multiline_min_width = max(multiline_data, key=len)
                    if (padding[key]+self.padding_width) < len(multiline_min_width) + self.padding_width:
                        padding[key] = len(multiline_min_width)+self.padding_width
                else:
                    if (padding[key]-self.padding_width) < len(str(item[key])):
                        padding[key] = len(str(item[key]))+self.padding_width
        return padding

    def getRowSepStr(self):
        row_sep_str = ''
        for value in self.var_padding.values():
            row_sep_str += '+' + '-'*value
        row_sep_str += '+'
        return row_sep_str

    def getRowSepLast(self):
        row_sep_str_last = '+'
        for value in self.var_padding.values():
            row_sep_str_last += '-'*(value+1)
        row_sep_str_last = row_sep_str_last[:-1] + '+'
        return row_sep_str_last

    def getMargin(self, margin):
        if self.padding_weight == 'left':
            right = 0
        elif self.padding_weight == 'right':
            right = margin
        elif self.padding_weight == 'centerleft':
            right = math.floor(margin/2)
        elif self.padding_weight == 'centerright':
            right = math.ceil(margin/2)
        else:
            right = math.floor(margin/2)
        return right

    def getHeader(self):
        header = ''
        if self.row_sep in ('topbottom', 'always'):
            header += self.newline_char + \
                      self.var_row_sep_last + \
                      self.newline_char
        for key in self.data[0].keys():
            margin = self.var_padding[key]-len(key)
            right = self.getMargin(margin)
            header += '|' + key.rjust(
                self.var_padding[key]-right,
                self.padding_char).ljust(
                    self.var_padding[key],
                    self.padding_char)
        header += '|' + self.newline_char
        if self.row_sep == 'always':
            header += self.var_row_sep + self.newline_char
        if self.row_sep == 'markdown':
            header += self.var_row_sep.replace('+', '|') + self.newline_char
        return header

    def getRow(self, item):
        if not self.multiline:
            return self.getNormalRow(item)
        # local check if element could be split in mulitple lines
        multiline = False
        for key in self.data[0].keys():
            if len(item[key]) > self.var_padding[key]:
                multiline = True
        if multiline:
            return self.getMultilineRow(item)
        return self.getNormalRow(item)

    def getNormalRow(self, item):
        row = ''
        for key in self.data[0].keys():
            margin = self.var_padding[key]-len(str(item[key]))
            right = self.getMargin(margin)
            row += '|' + str(item[key]).rjust(
                self.var_padding[key]-right,
                self.padding_char).ljust(
                    self.var_padding[key],
                    self.padding_char)
        row += '|'
        return row

    def getMultilineRow(self, item):
        multiline_items = {}
        for key in self.data[0].keys():
            items = item[key].split(" ")
            column_list = []
            multiline_row = ''
            for ix, sub_item in enumerate(items):
                multiline_row += sub_item
                if ix+1 < len(items) and len(multiline_row) + len(items[ix+1]) > self.var_padding[key]:
                    column_list.append(multiline_row)
                    multiline_row = ''
                else:
                    multiline_row += ' '
                if ix+1 == len(items):
                    column_list.append(sub_item)
            multiline_items[key] = column_list

        # get the max vertical length of the multiline row
        multiline_rows = 0
        for key, value in multiline_items.items():
            if len(value) > multiline_rows:
                multiline_rows = len(value)

        # fill in blank values
        for key, value in multiline_items.items():
            if len(value) < multiline_rows:
                for i in range(len(value), multiline_rows):
                    multiline_items[key].append(" ")

        rows = ''
        for ix in range(0, multiline_rows):
            row_dict = {}
            for key in self.data[0].keys():
                row_dict[key] = multiline_items[key][ix]
            rows += self.getNormalRow(row_dict)
            if ix < multiline_rows-1:
                rows += self.newline_char
        return rows

    def getBody(self):
        rows = ''
        for ix, item in enumerate(self.data):
            rows += self.getRow(item)
            if (ix < len(self.data)-1):
                rows += self.newline_char
            if self.row_sep == 'always' and ix < len(self.data)-1:
                rows += self.var_row_sep + self.newline_char
            if (self.row_sep == 'always' or self.row_sep == 'topbottom') and ix == len(self.data)-1:
                rows += self.newline_char + self.var_row_sep_last
        return rows

    def getMarkdown(self):
        self.updateMetaParams()
        data = self.getHeader()+self.getBody()
        if self.quote:
            return '```'+data+'```'
        else:
            return data

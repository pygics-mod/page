# -*- coding: utf-8 -*-
'''
Created on 2017. 11. 6.
@author: HyechurnJang
'''

from core import createVid
from W3 import Table, Thead, Tbody, Tr, Th, Td, Script

def setup(page):
    page.css('/page/static/datatables/datatables.min.css')
    page.js('/page/static/datatables/datatables.min.js')
    page.js('/page/static/datatables/page-datatables.js') 
    
class Style:
    
    Compact = {'class' : 'compact'}
    Border = {'class' : 'cell-border'}

class Flush(Table):
    
    def __init__(self, *cols, **attrs):
        Table.__init__(self, **attrs)
        Table.attr(self, Class='display')
        id = createVid()
        tr = Tr()
        self.tbody = Tbody()
        for col in cols: tr.html(Th().html(col))
        self['attrs']['id'] = id
        self['elems'].append(Thead().html(tr))
        self['elems'].append(self.tbody)
        self['elems'].append(Script().html('$(document).ready(function(){datatable_flush_draw("%s")});' % id))
        
    def html(self, *elems, **attrs):
        tr = Tr(**attrs)
        for elem in elems: tr.html(Td().html(elem))
        self.tbody.html(tr)
        return self

class Sync(Table):
    
    def __init__(self, *cols, **attrs):
        Table.__init__(self, **attrs)
        Table.attr(self, Class='display')
        id = createVid()
        tr = Tr()
        for col in cols: tr.html(Th().html(col))
        self['attrs']['id'] = id
        self['elems'].append(Thead().html(tr))
        self['elems'].append(Script().html('$(document).ready(function(){datatable_sync_draw("%s")});' % id))
    
    def attr(self, **attrs):
        if 'id' in attrs and 'url' in attrs:
            self['attrs']['page_url'] = attrs['url']
            return self
        else: return Table.attr(self, **attrs)

class Data(dict):
    
    def __init__(self):
        self._data = []
        dict.__init__(self, data=self._data)
    
    def record(self, *values):
        self._data.append(values)
        return self
    
    def __rshift__(self, values):
        if values:
            if isinstance(values, tuple) or isinstance(values, list): return self.record(*values)
            else: return self.record(values)
        return self
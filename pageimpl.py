# -*- coding: utf-8 -*-
'''
Created on 2017. 5. 30.
@author: HyechurnJang
'''

from tags import TAG, DIV, STRONG, ICON, INPUT, TABLE

import os
import types
import jzlib
import pygics
import jinja2

_page_registered = []

class PAGE(jzlib.LifeCycle):
    
    class TEMPLATE:
        
        SIMPLE = '/page/template/simple.html'
    
    class IndexHtml(types.FileType):
        def __init__(self):
            self.data = None
            self.path = 'index.html'
        
        @property
        def name(self): return self.path
        def read(self): return self.data
        def close(self): return None
    
    class CacheData(types.FileType):
        def __init__(self, path):
            self.fd = open(path, 'rb')
            self.data = self.fd.read()
            self.path = path
        
        @property
        def name(self): return self.path
        def read(self): return self.data
        def close(self): return None
    
    def __init__(self,
                 url='',
                 template=TEMPLATE.SIMPLE,
                 logo=None,
                 loading_bg='/page/resource/image/background.jpg',
                 loading_color='#777',
                 cache=True):
        # Get Template
        if '/page/template/' in template:
            template = template.replace('/page/template/', '/template/')
            with open(pwd() + template) as fd: self.template = jinja2.Template(fd.read())
        else:
            with open(template) as fd: self.template = jinja2.Template(fd.read())
        # Page Elements
        self.js_list = []
        self.css_list = []
        self.head_list = []
        self.logo = logo
        self.loading_bg = loading_bg
        self.loading_color = loading_color
        self.main = {'name' : 'Pygics-Page', 'url' : '/page/empty'}
        self.menu_category = {}
        self.menu_list = []
        self.views = {}
        self.mod_path, self.mod_name = pmd()
        self.cache = cache
        self.cache_data = {}
        if url == '': self.page_url = '/%s' % self.mod_name
        elif url[0] != '/': self.page_url = '/%s/%s' % (self.mod_name, url)
        else: self.page_url = '/%s%s' % (self.mod_name, url)
        _page_registered.append(self)
        self.index = PAGE.IndexHtml()
        
        @pygics.api('GET', self.page_url)
        def get(req, *argv, **kargs):
            path = '/'.join(argv)
            if path:
                file_path = '%s/%s' % (self.mod_path, path)
                if self.cache:
                    if file_path in self.cache_data: return self.cache_data[file_path]
                    else:
                        if not os.path.exists(file_path): raise Exception('could not find %s' % path)
                        cache_data = PAGE.CacheData(file_path)
                        self.cache_data[file_path] = cache_data
                        return cache_data
                else:
                    if not os.path.exists(file_path): raise Exception('could not find %s' % path)
                    return open(file_path, 'rb')
            else:
                if self.cache and not self.index.data: self.index.data = self.__render_index_page__()
                else: self.index.data = self.__render_index_page__()
                return self.index
        
    def __release__(self):
        if self in _page_registered: _page_registered.remove(self)
    
    def __render_index_page__(self):
        return self.template.render(**{'loading_bg' : self.loading_bg,
                                       'loading_color' : self.loading_color,
                                       'brand_logo' : self.logo,
                                       'main' : self.main,
                                       'menu_list' : self.menu_list,
                                       'customs' : self.__render_customs__(),
                                       'js_list' : self.js_list,
                                       'css_list' : self.css_list,
                                       'head_list' : self.head_list})
        
    def __render_customs__(self):
        return {}
    
    def __view_error__(self, name):
        return DIV(CLASS='view-error-box').html(
            ICON('exclamation-circle', CLASS='fa-3x'),
            DIV().html(STRONG().html('Could not find "%s"' % name))
        )
        
    def addJS(self, path):
        self.js_list.append(path)
        return self
    
    def addCSS(self, path):
        self.css_list.append(path)
        return self
    
    def addHead(self, text):
        self.head_list.append(text)
        return self
    
    def addCategory(self, name, icon=None):
        category = {'cat' : True, 'name' : name, 'icon' : icon, 'menu_list' : []}
        self.menu_category[name] = category
        self.menu_list.append(category)
        return self
    
    def patch(self, view, *argv):
        if '::' in view: view, sub_vid = view.split('::')
        else: sub_vid = ''
        if view not in self.views: return self.__view_error__(view)
        sub_url = '/' + '/'.join(argv)
        url = '%s%s' % (self.views[view]['url'], sub_url)
        vid = '%s%s' % (self.views[view]['id'], sub_vid)
        return DIV(ID=vid, VIEW=url).html('''<script>$(document).ready(function(){patchView("#%s");});</script>''' % vid)
    
    def refresh(self, view, *argv):
        if '::' in view: view, sub_vid = view.split('::')
        else: sub_vid = ''
        if view not in self.views: return self.__view_error__(view)
        vid = '%s%s' % (self.views[view]['id'], sub_vid)
        return '''<script>$(document).ready(function(){patchView("#%s");});</script>''' % vid
    
    def trigger(self, trig, view, *argv):
        return self.signal(trig, 'GET', view, *argv)
    
    def signal(self, trig, method, view, *argv):
        if '::' in view: view, sub_vid = view.split('::')
        else: sub_vid = ''
        if view not in self.views: return self.__view_error__(view)
        if not isinstance(trig, TAG): return self.__view_error__('%s is not tag object' % str(trig))
        if 'ID' not in trig['attrs']: trig['attrs']['ID'] = TAG.UUID()
        tid = trig['attrs']['ID']
        if 'CLASS' in trig['attrs']: trig['attrs']['CLASS'] += ' view-trigger'
        else: trig['attrs']['CLASS'] = 'view-trigger'
        sub_url = '/' + '/'.join(argv)
        url = '%s%s' % (self.views[view]['url'], sub_url)
        trig['attrs']['VIEW'] = url
        trig['attrs']['METHOD'] = method
        vid = '%s%s' % (self.views[view]['id'], sub_vid)
        return trig.html(
            '''<script>$(document).ready(function(){signalView("#%s","#%s");});</script>''' % (tid, vid)
        )
    
    def context(self, trig, view, *elems):
        if '::' in view: view, sub_vid = view.split('::')
        else: sub_vid = ''
        if view not in self.views: return self.__view_error__(view)
        _ctxt_uuid = TAG.UUID()
        if not isinstance(trig, TAG): return self.__view_error__('%s is not tag object' % str(trig))
        if 'ID' not in trig['attrs']: trig['attrs']['ID'] = TAG.UUID()
        tid = trig['attrs']['ID']
        if 'CLASS' in trig['attrs']: trig['attrs']['CLASS'] += ' view-trigger'
        else: trig['attrs']['CLASS'] = 'view-trigger'
        trig['attrs']['CONTEXT'] = '.' + _ctxt_uuid
        url = self.views[view]['url']
        trig['attrs']['VIEW'] = url
        vid = '%s%s' % (self.views[view]['id'], sub_vid)
        for elem in elems:
            if isinstance(elem, INPUT.__INPUT_SUBTYPE__):
                if 'CLASS' in elem['attrs']: elem['attrs']['CLASS'] += ' %s' % _ctxt_uuid
                else: elem['attrs']['CLASS'] = _ctxt_uuid
        return trig.html(
            '''<script>$(document).ready(function(){contextView("#%s","#%s");});</script>''' % (tid, vid)
        )
    
    def table(self, table, view, *argv):
        if view not in self.views: return self.__view_error__(view)
        if not isinstance(table, TABLE.SYNC) and not isinstance(table, TABLE.ASYNC):
            return self.__view_error__('%s is not datatable object' % str(table))
        if 'ID' not in table['attrs']: table['attrs']['ID'] = TAG.UUID()
        tid = table['attrs']['ID']
        sub_url = '/' + '/'.join(argv)
        url = '%s%s' % (self.views[view]['url'], sub_url)
        table['attrs']['VIEW'] = url
        return table.html(
            '''<script>$(document).ready(function(){tableView("#%s");});</script>''' % tid
        )
        
    @classmethod
    def MAIN(cls, page, name, logo=None):
        
        def wrapper(func):
            main_url = '%s/%s' % (page.page_url, func.__name__)
            page.logo = logo
            page.main = {'name' : name, 'url' : main_url}
            page.views[func.__name__] = {'url' : main_url, 'id' : 'page'}
            
            @pygics.api('GET', main_url)
            def worker_get(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            @pygics.api('POST', main_url)
            def worker_post(req, *argv, **kargs): return func(req, *argv, **kargs)
             
            @pygics.api('PUT', main_url)
            def worker_put(req, *argv, **kargs): return func(req, *argv, **kargs)
             
            @pygics.api('DELETE', main_url)
            def worker_delete(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            return worker_get
        
        return wrapper
    
    @classmethod
    def MENU(cls, page, name, icon=None):
        
        def wrapper(func):
            menu_url = '%s/%s' % (page.page_url, func.__name__)
            
            if '::' in name: category, sub_name = name.split('::')
            else: category = None
            if category != None and category in page.menu_category:
                category = page.menu_category[category]
                category['menu_list'].append({'cat' : False, 'name' : sub_name, 'url' : menu_url, 'icon' : icon})
            else:
                page.menu_list.append({'cat' : False, 'name' : name, 'url' : menu_url, 'icon' : icon})
            page.views[func.__name__] = {'url' : menu_url, 'id' : 'page'}
            
            @pygics.api('GET', menu_url)
            def worker_get(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            @pygics.api('POST', menu_url)
            def worker_post(req, *argv, **kargs): return func(req, *argv, **kargs)
             
            @pygics.api('PUT', menu_url)
            def worker_put(req, *argv, **kargs): return func(req, *argv, **kargs)
             
            @pygics.api('DELETE', menu_url)
            def worker_delete(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            return worker_get
        
        return wrapper
    
    @classmethod
    def VIEW(cls, page):
        
        def wrapper(func):
            view_id = TAG.UUID()
            view_url = '%s/%s' % (page.page_url, func.__name__)
            page.views[func.__name__] = {'url' : view_url, 'id' : view_id}
            
            @pygics.api('GET', view_url)
            def worker_get(req, *argv, **kargs):
                return DIV(ID=view_id).html(func(req, *argv, **kargs))
            
            @pygics.api('POST', view_url)
            def worker_post(req, *argv, **kargs):
                return DIV(ID=view_id).html(func(req, *argv, **kargs))
             
            @pygics.api('PUT', view_url)
            def worker_put(req, *argv, **kargs):
                return DIV(ID=view_id).html(func(req, *argv, **kargs))
             
            @pygics.api('DELETE', view_url)
            def worker_delete(req, *argv, **kargs):
                return DIV(ID=view_id).html(func(req, *argv, **kargs))
            
            return worker_get
        
        return wrapper
    
    @classmethod
    def TABLE(cls, page):
        
        def wrapper(func):
            view_id = TAG.UUID()
            view_url = '%s/%s' % (page.page_url, func.__name__)
            page.views[func.__name__] = {'url' : view_url, 'id' : view_id}
            
            @pygics.api('GET', view_url)
            def worker(req, *argv, **kargs):
                
                class SYNC_DESC(dict):
                    
                    def __init__(self):
                        dict.__init__(self, data=[])
                        
                    def record(self, *vals):
                        self['data'].append([str(val) for val in vals])
                        return self
                        
                    def render(self):
                        return self
                
                class ASYNC_DESC(dict):
                    
                    def __init__(self, query):
                        dict.__init__(self)
                        self['draw'] = query['draw']
                        self.start = int(query['start'])
                        self.length = int(query['length'])
                        if self.length >= 0:
                            self.end = self.start + self.length
                            self.page = self.start / self.length
                        else:
                            self.end = 0
                            self.page = 0
                        self.search = query['search[value]']
                        self.order_col = query['order[0][column]']
                        self.order_dir = query['order[0][dir]']
                        self.query = query
                        self['length'] = None
                        self['recordsFiltered'] = None
                        self['recordsTotal'] = None
                        self['data'] = []
                        
                    def record(self, *vals):
                        self['data'].append([str(val) for val in vals])
                        return self
                    
                    def total(self, count):
                        self['recordsTotal'] = count
                        return self
                    
                    def filtered(self, count):
                        self['recordsFiltered'] = count
                        return self
                    
                    def render(self):
                        ldata = len(self['data'])
                        if self['recordsTotal'] == None: self['recordsTotal'] = ldata
                        if self['recordsFiltered'] == None: self['recordsFiltered'] = self['recordsTotal']
                        return self
                
                if 'draw' in kargs: desc = ASYNC_DESC(kargs)
                else: desc = SYNC_DESC()
                func(desc, *argv)
                return desc.render()
            
            return worker
        
        return wrapper

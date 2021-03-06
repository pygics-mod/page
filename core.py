# -*- coding: utf-8 -*-
'''
Created on 2017. 10. 25.
@author: HyechurnJang
'''

import os
import uuid
import types
import jinja2
from pygics import Lock, ContentType, export, rest

def createVid(): return 'v-' + str(uuid.uuid4())

class Tag(dict):
    
    def __init__(self, tag, **attrs):
        dict.__init__(self, tag=tag, elems=[], attrs={})
        for key, val in attrs.items(): self['attrs'][key.lower()] = val
    
    def __len__(self, *args, **kwargs):
        return self['elems'].__len__()
    
    def __str__(self):
        ret = '<%s' % self['tag']
        for k, v in self['attrs'].items(): ret += ' %s="%s"' % (k, v)
        ret += '>'
        for elem in self['elems']: ret += unicode(elem)
        ret += '</%s>' % self['tag']
        return ret
    
    #===========================================================================
    # Attributes (a.k.a : event & links)
    #===========================================================================
    def attr(self, **attrs):
        own_attrs = self['attrs']
        for key, val in attrs.items():
            key_low = key.lower()
            own_attrs[key_low] = '%s %s' % (own_attrs[key_low], val) if key_low in own_attrs else val
        return self
    
    def __lshift__(self, opts):
        if opts: return self.attr(**opts)
        return self
    
    def baseattr(self, **attrs):
        own_attrs = self['attrs']
        for key, val in attrs.items():
            key_low = key.lower()
            own_attrs[key_low] = '%s %s' % (val, own_attrs[key_low]) if key_low in own_attrs else val
        return self
    #===========================================================================
    # Elements (a.k.a : children)
    #===========================================================================
    def html(self, *elems):
        for elem in elems: self['elems'].append(elem)
        return self
    
    def __rshift__(self, elems):
        if elems:
            if isinstance(elems, tuple) or isinstance(elems, list): return self.html(*elems)
            else: return self.html(*(elems,))
        return self

class Cache:
    
    _CACHE_DATA = {}
    
    @classmethod
    def getCache(cls, file_path):
        if file_path in Cache._CACHE_DATA:
            return Cache._CACHE_DATA[file_path]
        else:
            class CacheDescriptor(types.FileType):
                def __init__(self, file_path):
                    with open(file_path, 'rb') as fd: self.data = fd.read()
                    self.file_path = file_path
                @property
                def name(self): return self.file_path
                def read(self): return self.data
                def close(self): return None
            if not os.path.exists(file_path): raise Exception('could not find %s' % file_path)
            cache = CacheDescriptor(file_path)
            Cache._CACHE_DATA[file_path] = cache
            return cache

class Static:
    
    def __init__(self, url, static='static', cache=True):
        mod_path, mod_name = pmd()
        mod_name = mod_name.replace('.', '/')
        
        if not url: self.url = '/%s' % mod_name
        elif url[0] == '/': self.url = url
        else: self.url = '/%s/%s' % (mod_name, url)
        if not static: self.static = mod_path
        elif static[0] == '/': self.static = '%s%s' % (mod_path, static)
        else: self.static = '%s/%s' % (mod_path, static)
        self._static_cache = cache
        
        @export('GET', self.url)
        def send_static(req, *argv):
            path = '/'.join(argv)
            file_path = '%s/%s' % (self.static, path)
            if self._static_cache: return Cache.getCache(file_path)
            else:
                if not os.path.exists(file_path): raise Exception('could not find %s' % path)
                return open(file_path, 'rb')
    

class Page:
    
    def __init__(self,
                 url=None,
                 title='',
                 favicon='/page/static/image/favicon.ico',
                 static='static',
                 cache=True):
        mod_path, mod_name = pmd()
        mod_name = mod_name.replace('.', '/')
        
        if not url: self.url = '/%s' % mod_name
        elif url[0] == '/': self.url = url
        else: self.url = '/%s/%s' % (mod_name, url)
        
        if static[0] == '/': static = static[1:]
        if not static: self.static_path = mod_path
        else: self.static_path = '%s/%s' % (mod_path, static)
        
        if not static: self.static_url = '%s/static' % self.url
        elif self.url != '/': self.static_url = '%s/%s' % (self.url, static)
        else: self.static_url = '/%s' % static
        
        self._page_init = '/page/empty'
        self._page_view = {}
        
        self._page_title = title
        self._page_favicon = favicon
        self._page_meta_list = []
        self._page_css_list = []
        self._page_js_list = []
        self._page_head = ''
        self._page_header = ''
        self._page_footer = ''
        
        self._page_cache = cache
        self._page_cache_data = {}
        
        self._page_updated = True
        self._page_lock = Lock()
        self._page_rendered = None
        with open(pwd() + '/template.html') as fd: self._page_template = jinja2.Template(fd.read())
        
        @export('GET', self.url, content_type=ContentType.TextHtml)
        def send_template(req): return self.__render__()
        
        @export('GET', self.static_url)
        def send_static(req, *argv):
            path = '/'.join(argv)
            file_path = '%s/%s' % (self.static_path, path)
            if self._page_cache: return Cache.getCache(file_path)
            else:
                if not os.path.exists(file_path): raise Exception('could not find %s' % path)
                return open(file_path, 'rb')
        
    def __render__(self):
        if self._page_updated:
            self._page_lock.on()
            self._page_rendered = self._page_template.render({
                'init' : self._page_init,
                'title' : self._page_title,
                'favicon' : self._page_favicon,
                'meta_list' : self._page_meta_list,
                'css_list' : self._page_css_list,
                'js_list' : self._page_js_list,
                'head' : unicode(self._page_head),
                'header' : unicode(self._page_header),
                'footer' : unicode(self._page_footer)
            })
            self._page_rendered = self._page_rendered.encode('utf-8')
            self._page_updated = False
            self._page_lock.off()
            return self._page_rendered
        else:
            return self._page_rendered
    
    def meta(self, *meta_list):
        self._page_lock.on()
        for meta in meta_list:
            meta_str = ' '
            for key, val in meta.items(): meta_str += '%s="%s"' % (key, val)
            self._page_meta_list.append(meta_str)
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def css(self, *css_list):
        self._page_lock.on()
        for css in css_list: self._page_css_list.append(css)
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def js(self, *js_list):
        self._page_lock.on()
        for js in js_list: self._page_js_list.append(js)
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def head(self, html):
        self._page_lock.on()
        self._page_head = html
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def header(self, html):
        self._page_lock.on()
        self._page_header = html
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def footer(self, html):
        self._page_lock.on()
        self._page_footer = html
        self._page_updated = True
        self._page_lock.off()
        return self
    
    #===========================================================================
    # View Definition
    #===========================================================================
    def init(self, method='r', **opts):
        
        def wrapper(func):
            crud = method.lower()
            id = createVid()
            name = func.__name__
            url = '%s/%s' % (self.url if self.url != '/' else '', func.__name__)
            self._page_view[name] = {'id' : id, 'name' : name, 'url' : url}
            
            if 'r' in crud or '*' in crud:
                @rest('GET', url, **opts)
                def get(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            if 'c' in crud or '*' in crud:
                @rest('POST', url, **opts)
                def post(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            if 'u' in crud or '*' in crud:
                @rest('PUT', url, **opts)
                def put(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            if 'd' in crud or '*' in crud:
                @rest('DELETE', url, **opts)
                def delete(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            self._page_lock.on()
            self._page_init = url
            self._page_updated = True
            self._page_lock.off()
        
        return wrapper
    
    def view(self, method='r', **opts):
        
        def wrapper(func):
            crud = method.lower()
            id = createVid()
            name = func.__name__
            url = '%s/%s' % (self.url if self.url != '/' else '', name)
            self._page_view[name] = {'id' : id, 'name' : name, 'url' : url}
            
            if 'r' in crud or '*' in crud:
                @rest('GET', url, **opts)
                def get(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            if 'c' in crud or '*' in crud:
                @rest('POST', url, **opts)
                def post(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            if 'u' in crud or '*' in crud:
                @rest('PUT', url, **opts)
                def put(req, *argv, **kargs): return func(req, *argv, **kargs)
            
            if 'd' in crud or '*' in crud:
                @rest('DELETE', url, **opts)
                def delete(req, *argv, **kargs): return func(req, *argv, **kargs)
        
        return wrapper
    
    def getView(self, name, *path):
        view = self._page_view[name]
        return {'id' : view['id'], 'name' : name, 'url' : '%s/%s' % (view['url'], '/'.join(path)) if path else view['url']}
    
    #===========================================================================
    # View Functions
    #===========================================================================
    def patch(self, name, *argv):
        view = self._page_view[name]
        id = view['id']
        url = '%s/%s' % (view['url'], '/'.join(argv)) if argv else view['url']
        return Tag('script', Id=id, Page_Url=url).html(
            '$(document).ready(function(){page_patch("%s")});' % id
        )
    
    def __call__(self, name, *argv):
        return self.patch(name, *argv)
    
    def reload(self, *names):
        reload = []
        for name in names:
            reload.append(self._page_view[name]['id'])
        return {'reload' : reload}
    
    def __getitem__(self, names):
        if isinstance(names, tuple) or isinstance(names, list): return self.reload(*names)
        else: return self.reload(*(names,))
    
    #===========================================================================
    # Interactive Functions
    #===========================================================================
    
    class InteractiveTag(Tag):
        
        def __init__(self, view, *argv):
            Tag.__init__(self, 'script')
            self._view_id = view['id']
            self._view_url = '%s/%s' % (view['url'] + '/'.join(argv)) if argv else view['url']
            self._event_id = createVid()
            self._event_attr = {'class' : self._event_id, 'page_url' : self._view_url, 'page_view' : self._view_id}
        
        def event(self): return self._event_attr
    
    def get(self, name, *argv):
        
        class Get(Page.InteractiveTag):
            
            def __init__(self, view, *argv):
                Page.InteractiveTag.__init__(self, view, *argv)
                self.html('$(document).ready(function(){$(".%s").click(function(){page_get($(this));});});' % self._event_id)
        
        return Get(self._page_view[name], *argv)
    
    def post(self, name, *argv):
        
        class Post(Page.InteractiveTag):
              
            def __init__(self, view, *argv):
                Page.InteractiveTag.__init__(self, view, *argv)
                self._data_id = self._event_id + '-data'
                self._data_attr = {'class' : self._data_id}
                self._event_attr['page_data'] = self._data_id
                self.html('$(document).ready(function(){$(".%s").click(function(){page_post($(this));});});' % self._event_id)
            
            def data(self): return self._data_attr
        
        return Post(self._page_view[name], *argv)
    
    def put(self, name, *argv):
        
        class Put(Page.InteractiveTag):
              
            def __init__(self, view, *argv):
                Page.InteractiveTag.__init__(self, view, *argv)
                self._data_id = self._event_id + '-data'
                self._data_attr = {'class' : self._data_id}
                self._event_attr['page_data'] = self._data_id
                self.html('$(document).ready(function(){$(".%s").click(function(){page_put($(this));});});' % self._event_id)
            
            def data(self): return self._data_attr
            
        return Put(self._page_view[name], *argv)
    
    def delete(self, name, *argv):
        
        class Delete(Page.InteractiveTag):
            
            def __init__(self, view, *argv):
                Page.InteractiveTag.__init__(self, view, *argv)
                self.html('$(document).ready(function(){$(".%s").click(function(){page_delete($(this));});});' % self._event_id)
        
        return Delete(self._page_view[name], *argv)

#===============================================================================
# Page Statics
#===============================================================================
Page(url='/page', cache=True)

@export('GET', '/page/empty', content_type=ContentType.AppJson)
def empty_page(req): return {'error' : 'Page Empty'}

@export('GET', '/favicon.ico', content_type=ContentType.AppStream)
def default_favicon(req, *argv): return Cache.getCache(pwd() + '/static/image/favicon.ico')

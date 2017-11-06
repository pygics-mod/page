# -*- coding: utf-8 -*-
'''
Created on 2017. 10. 25.
@author: HyechurnJang
'''

import os
import uuid
import types
import jinja2
import inspect
from pygics import Lock, ContentType, Response, export, rest

def createId(): return 'id-' + str(uuid.uuid4())

class Tag(dict):
    
    @classmethod
    def attrs(cls, target, **inject):
        for key, val in inject.items():
            key_low = key.lower()
            target[key_low] = '%s %s' % (target[key_low], val) if key_low in target else val
        return target
    
    def __init__(self, tag, **attrs):
        dict.__init__(self, tag=tag, elems=[], attrs={})
        for key, val in attrs.items(): self['attrs'][key.lower()] = val
    
    def __len__(self, *args, **kwargs):
        return self['elems'].__len__()
    
    def __str__(self):
        ret = '<%s' % self['tag']
        for k, v in self['attrs'].items(): ret += ' %s="%s"' % (k, v)
        ret += '>'
        for elem in self['elems']: ret += str(elem)
        ret += '</%s>' % self['tag']
        return ret
    
    def opts(self, opts): return self.attr(**opts)
    
    def attr(self, **attrs):
        tag_attrs = self['attrs']
        for key, val in attrs.items():
            key_low = key.lower()
            tag_attrs[key_low] = '%s %s' % (tag_attrs[key_low], val) if key_low in tag_attrs else val
        return self
    
    def html(self, *elems):
        for elem in elems: self['elems'].append(elem)
        return self

class Page:
    
    _CACHE_DATA = {}
    
    @classmethod
    def getCache(cls, file_path):
        if file_path in Page._CACHE_DATA: return Page._CACHE_DATA[file_path]
        else:
            class Cache(types.FileType):
                def __init__(self, file_path):
                    with open(file_path, 'rb') as fd: self.data = fd.read()
                    self.file_path = file_path
                @property
                def name(self): return self.file_path
                def read(self): return self.data
                def close(self): return None
            if not os.path.exists(file_path): raise Exception('could not find %s' % file_path)
            cache = Cache(file_path)
            Page._CACHE_DATA[file_path] = cache
            return cache
    
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
        
        static = static.replace('/', '')
        self.static_path = '%s/%s' % (mod_path, static)
        if self.url != '/': self.static_url = '%s/%s' % (self.url, static)
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
        def send_template(req):
            return self.__render__()
        
        @export('GET', self.static_url)
        def send_static(req, *argv):
            path = '/'.join(argv)
            file_path = '%s/%s' % (self.static_path, path)
            if self._page_cache: return Page.getCache(file_path)
            else:
                if not os.path.exists(file_path): raise Exception('could not find %s' % path)
                return open(file_path, 'rb')
        
    def __render__(self):
        if self._page_updated:
            self._page_lock.on()
            self._page_rendered = self._page_template.render(**{
                'init' : self._page_init,
                'title' : self._page_title,
                'favicon' : self._page_favicon,
                'meta_list' : self._page_meta_list,
                'css_list' : self._page_css_list,
                'js_list' : self._page_js_list,
                'head' : str(self._page_head),
                'header' : str(self._page_header),
                'footer' : str(self._page_footer)
            })
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
    def init(self, func):
        self._page_lock.on()
        self._page_init = '%s/%s' % (self.url if self.url != '/' else '', func.__name__)
        
        @rest('GET', self._page_init)
        def get(req, *argv, **kargs): return func(req, *argv, **kargs)
        
        @rest('POST', self._page_init)
        def post(req, *argv, **kargs): return func(req, *argv, **kargs)
         
        @rest('PUT', self._page_init)
        def put(req, *argv, **kargs): return func(req, *argv, **kargs)
         
        @rest('DELETE', self._page_init)
        def delete(req, *argv, **kargs): return func(req, *argv, **kargs)
        
        self._page_updated = True
        self._page_lock.off()
    
    def view(self, func):
        id = createId()
        name = func.__name__
        url = '%s/%s' % (self.url if self.url != '/' else '', name)
        self._page_view[name] = {'id' : id, 'name' : name, 'url' : url}
        
        @rest('GET', url)
        def get(req, *argv, **kargs):
            return func(req, *argv, **kargs)
        
        @rest('POST', url)
        def post(req, *argv, **kargs): return func(req, *argv, **kargs)
         
        @rest('PUT', url)
        def put(req, *argv, **kargs): return func(req, *argv, **kargs)
         
        @rest('DELETE', url)
        def delete(req, *argv, **kargs): return func(req, *argv, **kargs)
    
    #===========================================================================
    # Action Functions
    #===========================================================================
    def patch(self, name, *argv):
        view = self._page_view[name]
        id = view['id']
        url = '%s/%s' % (view['url'] + '/'.join(argv)) if argv else view['url']
        return Tag('script', Id=id, Page_Url=url).html(
            '$(document).ready(function(){page_patch("%s")});' % id
        )
    
    def reload(self, *names):
        reload = []
        for name in names:
            reload.append(self._page_view[name]['id'])
        return {'reload' : reload}
    
    def get(self, name, *argv):
        
        class Get(Tag):
            
            def __init__(self, view, *argv):
                Tag.__init__(self, 'script')
                self._view_id = view['id']
                self._view_url = '%s/%s' % (view['url'] + '/'.join(argv)) if argv else view['url']
                self._send_id = self._view_id + '-get'
                self.html('$(document).ready(function(){$(".%s").click(function(){page_get($(this));});});' % self._send_id)
                self.Send = {'class' : self._send_id, 'page_url' : self._view_url, 'page_view' : self._view_id}
        
        return Get(self._page_view[name], *argv)
    
    def post(self, name, *argv):
        
        class Post(Tag):
              
            def __init__(self, view, *argv):
                Tag.__init__(self, 'script')
                self._view = view
                self._view_id = view['id']
                self._view_url = '%s/%s' % (view['url'] + '/'.join(argv)) if argv else view['url']
                self._data_id = createId()
                self._send_id = createId()
                self.html('$(document).ready(function(){$(".%s").click(function(){page_post($(this));});});' % self._send_id)
                self.Data = {'class' : self._data_id}
                self.Send = {'class' : self._send_id, 'page_url' : self._view_url, 'page_view' : self._view_id, 'page_data' : self._data_id}
        
        return Post(self._page_view[name], *argv)
    
    def put(self, name, *argv):
        
        class Put(Tag):
              
            def __init__(self, view, *argv):
                Tag.__init__(self, 'script')
                self._view = view
                self._view_id = view['id']
                self._view_url = '%s/%s' % (view['url'] + '/'.join(argv)) if argv else view['url']
                self._data_id = createId()
                self._send_id = createId()
                self.html('$(document).ready(function(){$(".%s").click(function(){page_put($(this));});});' % self._send_id)
                self.Data = {'class' : self._data_id}
                self.Send = {'class' : self._send_id, 'page_url' : self._view_url, 'page_view' : self._view_id, 'page_data' : self._data_id}
        
        return Put(self._page_view[name], *argv)
    
    def delete(self, name, *argv):
        
        class Delete(Tag):
            
            def __init__(self, view, *argv):
                Tag.__init__(self, 'script')
                self._view_id = view['id']
                self._view_url = '%s/%s' % (view['url'] + '/'.join(argv)) if argv else view['url']
                self._send_id = self._view_id + '-del'
                self.html('$(document).ready(function(){$(".%s").click(function(){page_delete($(this));});});' % self._send_id)
                self.Send = {'class' : self._send_id, 'page_url' : self._view_url, 'page_view' : self._view_id}
        
        return Delete(self._page_view[name], *argv)

#===============================================================================
# Page Statics
#===============================================================================
Page(url='/page', cache=False)

@export('GET', '/page/empty', content_type=ContentType.AppJson)
def empty_page(req): return {'error' : 'Page Empty'}

@export('GET', '/favicon.ico', content_type=ContentType.AppStream)
def default_favicon(req, *argv): return Page.getCache(pwd() + '/static/image/favicon.ico')

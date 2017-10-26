# -*- coding: utf-8 -*-
'''
Created on 2017. 10. 25.
@author: HyechurnJang
'''

import os
import types
import jinja2
from pygics import Lock, ContentType, api

@api('GET', '/page/empty_page')
def empty_page(req): return 'Empty Page'

class Page:
    
    _JS_JQUERY = '/page/static/js/jquery-3.2.1.min.js'
    _JS_PAGE_CORE = '/page/static/js/page-core.js'
    _JS_PAGE_INIT = '/page/static/js/page-init.js'
    
    class _CacheData_(types.FileType):
        def __init__(self, path):
            with open(path, 'rb') as fd: self.data = fd.read()
            self.path = path
        
        @property
        def name(self): return self.path
        def read(self): return self.data
        def close(self): return None
    
    def __init__(self,
                 url=None,
                 title='',
                 static='static',
                 favicon='/page/static/image/favicon.ico',
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
        
        self._page_main = '/page/empty_page'
        
        self._page_title = title
        self._page_favicon = favicon
        self._page_meta_list = []
        self._page_css_list = []
        self._page_js_list = [Page._JS_JQUERY, Page._JS_PAGE_CORE, Page._JS_PAGE_INIT]
        self._page_head_list = []
        self._page_hbody_list = []
        self._page_fbody_list = []
        
        self._page_cache = cache
        self._page_cache_data = {}
        
        self._page_updated = True
        self._page_lock = Lock()
        self._page_rendered = None
        with open(pwd() + '/template.html') as fd: self._page_template = jinja2.Template(fd.read())
        
        @api('GET', self.url, content_type=ContentType.TextHtml)
        def send_template(req):
            return self.__render__()
        
        @api('GET', self.static_url)
        def send_static(req, *argv):
            path = '/'.join(argv)
            file_path = '%s/%s' % (self.static_path, path)
            if self._page_cache:
                if file_path in self._page_cache_data:
                    return self._page_cache_data[file_path]
                else:
                    if not os.path.exists(file_path): raise Exception('could not find %s' % path)
                    cache_data = Page._CacheData_(file_path)
                    self._page_cache_data[file_path] = cache_data
                    return cache_data
            else:
                if not os.path.exists(file_path): raise Exception('could not find %s' % path)
                return open(file_path, 'rb')
        
    def __render__(self):
        if self._page_updated:
            self._page_lock.on()
            self._page_rendered = self._page_template.render(**{
                'main' : self._page_main,
                'title' : self._page_title,
                'favicon' : self._page_favicon,
                'meta_list' : self._page_meta_list,
                'css_list' : self._page_css_list,
                'head_list' : self._page_head_list,
                'js_list' : self._page_js_list,
                'hbody_list' : self._page_hbody_list,
                'fbody_list' : self._page_fbody_list
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
        for css in css_list: self._page_css_list.append('%s/%s' % (self.url if self.url != '/' else '', css))
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def js(self, *js_list):
        self._page_lock.on()
        for js in js_list: self._page_js_list.append('%s/%s' % (self.url if self.url != '/' else '', js))
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def head(self, *head_list):
        self._page_lock.on()
        for head in head_list: self._page_head_list.append(head)
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def hbody(self, *hbody_list):
        self._page_lock.on()
        for hbody in hbody_list: self._page_hbody_list.append(hbody)
        self._page_updated = True
        self._page_lock.off()
        return self
    
    def fbody(self, *fbody_list):
        self._page_lock.on()
        for fbody in fbody_list: self._page_fbody_list.append(fbody)
        self._page_updated = True
        self._page_lock.off()
        return self

def main(page):
    
    def wrapper(func):
        page._page_lock.on()
        page._page_main = '%s/%s' % (page.url if page.url != '/' else '', func.__name__)
        
        @api('GET', page._page_main, content_type=ContentType.AppJson)
        def get(req, *argv, **kargs): return func(req, *argv, **kargs)
        
        @api('POST', page._page_main, content_type=ContentType.AppJson)
        def post(req, *argv, **kargs): return func(req, *argv, **kargs)
         
        @api('PUT', page._page_main, content_type=ContentType.AppJson)
        def put(req, *argv, **kargs): return func(req, *argv, **kargs)
         
        @api('DELETE', page._page_main, content_type=ContentType.AppJson)
        def delete(req, *argv, **kargs): return func(req, *argv, **kargs)
        
        page._page_updated = True
        page._page_lock.off()
        
    return wrapper
    
    

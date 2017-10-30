# -*- coding: utf-8 -*-
'''
Created on 2017. 10. 31.
@author: HyechurnJang
'''

import uuid

class Tag(dict):
    
    @classmethod
    def attr(cls, attrs, **sets):
        for k in sets: attrs[k] = '%s %s' % (sets[k], attrs[k]) if k in attrs else sets[k]
        return attrs
    
    @classmethod
    def uuid(cls):
        return 'V' + str(uuid.uuid4()).replace('-', '')
    
    def __init__(self, tag, **attrs):
        dict.__init__(self, tag=tag, elems=[], attrs={})
        for k, v in attrs.items(): self['attrs'][k.lower()] = v
    
    def __len__(self, *args, **kwargs):
        return self['elems'].__len__()
    
    def __str__(self):
        ret = '<%s' % self['tag']
        for k, v in self['attrs'].items(): ret += ' %s="%s"' % (k, v)
        ret += '>'
        for elem in self['elems']: ret += str(elem)
        ret += '</%s>' % self['tag']
        return ret
    
    def html(self, *elems):
        for elem in elems: self['elems'].append(elem)
        return self
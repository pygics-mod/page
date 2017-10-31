# -*- coding: utf-8 -*-
'''
Created on 2017. 5. 30.
@author: HyechurnJang
'''

from pygics import ContentType, export
from core import Page
from tags import Tag

import W3 

Page(cache=False)

@export('GET', '/page/empty_page', content_type=ContentType.AppJson)
def empty_page(req): return {'error' : 'Empty Page'}

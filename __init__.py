# -*- coding: utf-8 -*-
'''
Created on 2017. 5. 30.
@author: HyechurnJang
'''

# from tags import TAG
# from tags import DIV, SPAN, ROW, COL, IFRAME, NAV, SCRIPT
# from tags import HEAD, PARA, ANCH, LABEL, STRONG, SMALL
# from tags import IMG, ICON
# from tags import THEAD, TBODY, TH, TR, TD, TABLE
# from tags import UL, LI
# from tags import FORM, INPUT, BUTTON

from pygics import ContentType, export
from core import Page
from tags import Tag

Page(cache=False)

@export('GET', '/page/empty_page', content_type=ContentType.AppJson)
def empty_page(req): return {'error' : 'Empty Page'}

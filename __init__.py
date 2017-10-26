# -*- coding: utf-8 -*-
'''
Created on 2017. 5. 30.
@author: HyechurnJang
'''

from tags import TAG
from tags import DIV, SPAN, ROW, COL, IFRAME, NAV, SCRIPT
from tags import HEAD, PARA, ANCH, LABEL, STRONG, SMALL
from tags import IMG, ICON
from tags import THEAD, TBODY, TH, TR, TD, TABLE
from tags import UL, LI
from tags import FORM, INPUT, BUTTON

# import pygics
# from pageimpl import PAGE

from core import Page, main

Page(cache=False)

# @pygics.api('GET', 'empty')
# def get_empty_page(req):
#     return DIV(ID='page-empty').html(
#         DIV().html(IMG('/page/resource/image/pygics_logo_144.png')),
#         HEAD(1).html('Now Preparing')
#     )
#     
# root = PAGE(template='/page/template/pageroot.html')
# 
# @PAGE.MAIN(root, 'Page')
# def root_page_main(req):
#     
#     page_list = DIV(ID='thumbnail-list')
#      
#     for reg in pageimpl._page_registered[1:]:
#         page_list.html(
#             DIV(CLASS='thumbnail-container', TITLE=reg.main['name'], TARGET=reg.page_url).html(
#                 DIV(CLASS='thumbnail-control').html(
#                     DIV(CLASS='thumbnail-control-title').html(reg.main['name']),
#                     DIV(CLASS='thumbnail-control-star-container').html(
#                         ICON('star-o', CLASS='fa-2x thumbnail-control-star', TITLE=reg.main['name'], TARGET=reg.page_url)
#                     )
#                 ),
#                 DIV(CLASS='thumbnail').html(
#                     IFRAME(reg.page_url)
#                 ),
#             )
#         )
#         
#     return DIV().html(
#         HEAD(2, ID='page-list-title').html("Page List"),
#         DIV(ID='add-page-container').html(
#             SPAN(ID='add-page-title').html('Add Page'),
#             LABEL().html('Name : '),
#             INPUT(ID='add-page-name', CLASS='add-page-input', TYPE='text'),
#             LABEL().html('Url : '),
#             INPUT(ID='add-page-url', CLASS='add-page-input', TYPE='text'),
#             BUTTON(ID='add-page-submit').html('Submit')
#         ),
#         page_list,
#         SCRIPT(SRC='/page/resource/js/pagerootmain.js')
#     )

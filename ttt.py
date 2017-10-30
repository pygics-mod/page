# -*- coding: utf-8 -*-

import uuid

#===============================================================================
# Abstract
#===============================================================================
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

#===============================================================================
# Layout
#===============================================================================
class Div(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'div', **attrs)

class Span(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'span', **attrs)

class ROW(Div):
    def __init__(self, **attrs): Div.__init__(self, **Tag.attr(attrs, CLASS='row'))

class COL(Div):
    def __init__(self, size, scr='sm', **attrs): Div.__init__(self, **Tag.attr(attrs, CLASS='col-%s-%d' % (scr, size)))

class IFRAME(Tag):
    def __init__(self, src, **attrs): Tag.__init__(self, 'iframe', **Tag.attr(attrs, SRC=src))

class NAV(Div):
    
    class TAB(Div):
        
        def __init__(self, label, **attrs):
            Div.__init__(self, **attrs)
            self.label = label
     
    def __init__(self, **attrs):
        Div.__init__(self, **attrs)
        self.uuid = Tag.uuid()
        self.tab_cnt = 0
        self.tab_first = True
        self.tab_header = UL(CLASS='nav nav-tabs', ROLE='tablist')
        self.tab_content = Div(CLASS='tab-content page-tab-content')
        self['elems'].append(self.tab_header)
        self['elems'].append(self.tab_content)
    
    def html(self, *elems):
        for elem in elems:
            if isinstance(elem, NAV.TAB):
                tab_id = '%s-%d' % (self.uuid, self.tab_cnt)
                self.tab_cnt += 1
                if self.tab_first:
                    lst_attr = {'CLASS':'active', 'ROLE':'presentation'}
                    div_attr = {'ID':tab_id, 'CLASS':'tab-pane fade in active', 'ROLE':'tabpanel'}
                    self.tab_first = False
                else:
                    lst_attr = {'ROLE':'presentation'}
                    div_attr = {'ID':tab_id, 'CLASS':'tab-pane fade', 'ROLE':'tabpanel'}
                self.tab_header.html(
                    LI(**lst_attr).html(
                        ANCH(**{'href':'#%s' % tab_id, 'aria-controls':tab_id, 'role':'tab', 'data-toggle':'tab'}).html(elem.label)
                    )
                )
                self.tab_content.html(Div(**div_attr).html(elem))
        return self

#===============================================================================
# Text
#===============================================================================
class SCRIPT(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'script', **attrs)

class HEAD(Tag):
    def __init__(self, level, **attrs): Tag.__init__(self, 'h' + str(level), **attrs)

class PARA(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'p', **Tag.attr(attrs, CLASS='para'))

class ANCH(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'a', **attrs)

class LABEL(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'label', **attrs)

class STRONG(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'strong', **attrs)

class SMALL(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'small', **attrs)
        
class IMG(Tag):
    def __init__(self, src, **attrs): Tag.__init__(self, 'img', **Tag.attr(attrs, SRC=src))
    
class ICON(Tag):
    def __init__(self, icon, **attrs): Tag.__init__(self, 'i', **Tag.attr(attrs, CLASS='fa fa-%s' % icon))

#===============================================================================
# Table
#===============================================================================
class THEAD(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'thead', **attrs)
        
class TBODY(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'tbody', **attrs)
        
class TH(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'th', **attrs)
        
class TR(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'tr', **attrs)

class TD(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'td', **attrs)

class TABLE(Tag):
    
    class SYNC(Tag):
        def __init__(self, *heads, **attrs):
            Tag.__init__(self, 'table', **Tag.attr(attrs, CLASS='table table-bordered table-hover', WIDTH='100%', PROC='sync'))
            tr = TR()
            for head in heads: tr.html(TH().html(head))
            self.html(THEAD().html(tr))
    
    class ASYNC(Tag):
        def __init__(self, *heads, **attrs):
            Tag.__init__(self, 'table', **Tag.attr(attrs, CLASS='table table-bordered table-hover', WIDTH='100%', PROC='async'))
            tr = TR()
            for head in heads: tr.html(TH().html(head))
            self.html(THEAD().html(tr))
    
    def __init__(self, **attrs): Tag.__init__(self, 'table', **attrs)

#===============================================================================
# List
#===============================================================================
class LI(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'li', **attrs)
    
class UL(Tag):
    
    class GROUP(Tag):
        def __init__(self, **attrs):
            UL.__init__(self, **Tag.attr(attrs, CLASS='list-group'))
        
        def html(self, *elems):
            for elem in elems: self['elems'].append(LI(CLASS='list-group-item').html(elem))
            return self
    
    def __init__(self, **attrs): Tag.__init__(self, 'ul', **attrs)

#===============================================================================
# Interactive
#===============================================================================
class FORM(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'form', **attrs)

class INPUT(Tag):
    
    class __INPUT_SUBTYPE__: pass
    
    class GROUP(__INPUT_SUBTYPE__, Div):
        def __init__(self, **attrs):
            Div.__init__(self, **Tag.attr(attrs, CLASS='input-group page-input-group'))
    
    class LABEL_TOP(LABEL):
        def __init__(self, label, **attrs):
            LABEL.__init__(self, **attrs)
            self.html(label)
    
    class LABEL_LEFT(Span):
        def __init__(self, label, **attrs):
            Span.__init__(self, **Tag.attr(attrs, CLASS='input-group-addon'))
            self.html(label)
    
    class DISPLAY(Div):
        def __init__(self, **attrs):
            Div.__init__(self, **Tag.attr(attrs, CLASS='form-control form-display-box'))
    
    class HIDDEN(__INPUT_SUBTYPE__, Tag):
        def __init__(self, name, placeholder='', **attrs):
            Tag.__init__(self, 'input', **Tag.attr(attrs, TYPE='hidden', NAME=name, PLACEHOLDER=placeholder))
    
    class TEXT(__INPUT_SUBTYPE__, Tag):
        def __init__(self, name, placeholder='', **attrs):
            Tag.__init__(self, 'input', **Tag.attr(attrs, CLASS='form-control', TYPE='text', NAME=name, PLACEHOLDER=placeholder))
    
    class PASSWORD(__INPUT_SUBTYPE__, Tag):
        def __init__(self, name='password', **attrs):
            Tag.__init__(self, 'input', **Tag.attr(attrs, CLASS='form-control', TYPE='password', NAME=name))
    
    class SELECT(__INPUT_SUBTYPE__, Tag):
        
        class OPTION(Tag):
            def __init__(self, **attrs): Tag.__init__(self, 'option', **attrs)
        
        def __init__(self, name, *elems, **attrs):
            Tag.__init__(self, 'select', **Tag.attr(attrs, CLASS='form-control', NAME=name))
            for elem in elems: self.html(INPUT.SELECT.OPTION().html(elem))
    
    def __init__(self, **attrs): Tag.__init__(self, 'input', **attrs)

class BUTTON(Tag):
    
    class GROUP(Div):
        def __init__(self, **attrs):
            Div.__init__(self, **Tag.attr(attrs, CLASS='btn-group page-btn-group'))
    
    def __init__(self, **attrs): Tag.__init__(self, 'button', **Tag.attr(attrs, CLASS='btn page-btn', TYPE='button'))

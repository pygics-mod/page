# -*- coding: utf-8 -*-

import uuid

#===============================================================================
# Abstract
#===============================================================================
class TAG(dict):
    
    @classmethod
    def ATTR(cls, attrs, **sets):
        for k in sets: attrs[k] = '%s %s' % (sets[k], attrs[k]) if k in attrs else sets[k]
        return attrs
    
    @classmethod
    def UUID(cls):
        return 'V' + str(uuid.uuid4()).replace('-', '')
    
    def __init__(self, tag, **attrs):
        dict.__init__(self, tag=tag, elems=[], attrs={})
        for k, v in attrs.items(): self['attrs'][k.upper()] = v
    
    def __len__(self, *args, **kwargs):
        return self['elems'].__len__()
    
    def __str__(self):
        return self.render()
    
    def render(self):
        ret = '<%s' % self['tag']
        for k, v in self['attrs'].items(): ret += ' %s="%s"' % (k, v)
        ret += '>'
        for elem in self['elems']:
            if isinstance(elem, TAG): ret += elem.render()
            else: ret += str(elem)
        ret += '</%s>' % self['tag']
        return ret
                
    def isEmpty(self):
        return not self['elems'].__len__()
    
    def html(self, *elems):
        for elem in elems: self['elems'].append(elem)
        return self

#===============================================================================
# Layout
#===============================================================================
class DIV(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'div', **attrs)

class SPAN(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'span', **attrs)

class ROW(DIV):
    def __init__(self, **attrs): DIV.__init__(self, **TAG.ATTR(attrs, CLASS='row'))

class COL(DIV):
    def __init__(self, size, scr='sm', **attrs): DIV.__init__(self, **TAG.ATTR(attrs, CLASS='col-%s-%d' % (scr, size)))

class IFRAME(TAG):
    def __init__(self, src, **attrs): TAG.__init__(self, 'iframe', **TAG.ATTR(attrs, SRC=src))

class NAV(DIV):
    
    class TAB(DIV):
        
        def __init__(self, label, **attrs):
            DIV.__init__(self, **attrs)
            self.label = label
     
    def __init__(self, **attrs):
        DIV.__init__(self, **attrs)
        self.uuid = TAG.UUID()
        self.tab_cnt = 0
        self.tab_first = True
        self.tab_header = UL(CLASS='nav nav-tabs', ROLE='tablist')
        self.tab_content = DIV(CLASS='tab-content page-tab-content')
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
                self.tab_content.html(DIV(**div_attr).html(elem))
        return self

#===============================================================================
# Text
#===============================================================================
class SCRIPT(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'script', **attrs)

class HEAD(TAG):
    def __init__(self, level, **attrs): TAG.__init__(self, 'h' + str(level), **attrs)

class PARA(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'p', **TAG.ATTR(attrs, CLASS='para'))

class ANCH(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'a', **attrs)

class LABEL(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'label', **attrs)

class STRONG(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'strong', **attrs)

class SMALL(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'small', **attrs)
        
class IMG(TAG):
    def __init__(self, src, **attrs): TAG.__init__(self, 'img', **TAG.ATTR(attrs, SRC=src))
    
class ICON(TAG):
    def __init__(self, icon, **attrs): TAG.__init__(self, 'i', **TAG.ATTR(attrs, CLASS='fa fa-%s' % icon))

#===============================================================================
# Table
#===============================================================================
class THEAD(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'thead', **attrs)
        
class TBODY(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'tbody', **attrs)
        
class TH(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'th', **attrs)
        
class TR(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'tr', **attrs)

class TD(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'td', **attrs)

class TABLE(TAG):
    
    class SYNC(TAG):
        def __init__(self, *heads, **attrs):
            TAG.__init__(self, 'table', **TAG.ATTR(attrs, CLASS='table table-bordered table-hover', WIDTH='100%', PROC='sync'))
            tr = TR()
            for head in heads: tr.html(TH().html(head))
            self.html(THEAD().html(tr))
    
    class ASYNC(TAG):
        def __init__(self, *heads, **attrs):
            TAG.__init__(self, 'table', **TAG.ATTR(attrs, CLASS='table table-bordered table-hover', WIDTH='100%', PROC='async'))
            tr = TR()
            for head in heads: tr.html(TH().html(head))
            self.html(THEAD().html(tr))
    
    def __init__(self, **attrs): TAG.__init__(self, 'table', **attrs)

#===============================================================================
# List
#===============================================================================
class LI(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'li', **attrs)
    
class UL(TAG):
    
    class GROUP(TAG):
        def __init__(self, **attrs):
            UL.__init__(self, **TAG.ATTR(attrs, CLASS='list-group'))
        
        def html(self, *elems):
            for elem in elems: self['elems'].append(LI(CLASS='list-group-item').html(elem))
            return self
    
    def __init__(self, **attrs): TAG.__init__(self, 'ul', **attrs)

#===============================================================================
# Interactive
#===============================================================================
class FORM(TAG):
    def __init__(self, **attrs): TAG.__init__(self, 'form', **attrs)

class INPUT(TAG):
    
    class __INPUT_SUBTYPE__: pass
    
    class GROUP(__INPUT_SUBTYPE__, DIV):
        def __init__(self, **attrs):
            DIV.__init__(self, **TAG.ATTR(attrs, CLASS='input-group page-input-group'))
    
    class LABEL_TOP(LABEL):
        def __init__(self, label, **attrs):
            LABEL.__init__(self, **attrs)
            self.html(label)
    
    class LABEL_LEFT(SPAN):
        def __init__(self, label, **attrs):
            SPAN.__init__(self, **TAG.ATTR(attrs, CLASS='input-group-addon'))
            self.html(label)
    
    class DISPLAY(DIV):
        def __init__(self, **attrs):
            DIV.__init__(self, **TAG.ATTR(attrs, CLASS='form-control form-display-box'))
    
    class HIDDEN(__INPUT_SUBTYPE__, TAG):
        def __init__(self, name, placeholder='', **attrs):
            TAG.__init__(self, 'input', **TAG.ATTR(attrs, TYPE='hidden', NAME=name, PLACEHOLDER=placeholder))
    
    class TEXT(__INPUT_SUBTYPE__, TAG):
        def __init__(self, name, placeholder='', **attrs):
            TAG.__init__(self, 'input', **TAG.ATTR(attrs, CLASS='form-control', TYPE='text', NAME=name, PLACEHOLDER=placeholder))
    
    class PASSWORD(__INPUT_SUBTYPE__, TAG):
        def __init__(self, name='password', **attrs):
            TAG.__init__(self, 'input', **TAG.ATTR(attrs, CLASS='form-control', TYPE='password', NAME=name))
    
    class SELECT(__INPUT_SUBTYPE__, TAG):
        
        class OPTION(TAG):
            def __init__(self, **attrs): TAG.__init__(self, 'option', **attrs)
        
        def __init__(self, name, *elems, **attrs):
            TAG.__init__(self, 'select', **TAG.ATTR(attrs, CLASS='form-control', NAME=name))
            for elem in elems: self.html(INPUT.SELECT.OPTION().html(elem))
    
    def __init__(self, **attrs): TAG.__init__(self, 'input', **attrs)

class BUTTON(TAG):
    
    class GROUP(DIV):
        def __init__(self, **attrs):
            DIV.__init__(self, **TAG.ATTR(attrs, CLASS='btn-group page-btn-group'))
    
    def __init__(self, **attrs): TAG.__init__(self, 'button', **TAG.ATTR(attrs, CLASS='btn page-btn', TYPE='button'))

# -*- coding: utf-8 -*-
'''
Created on 2017. 10. 31.
@author: HyechurnJang
'''

from core import Tag

# <a>
class A(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'a', **attrs)

# <abbr>
class Abbr(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'abbr', **attrs)

# <address>
class Address(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'address', **attrs)

# <area>
class Area(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'area', **attrs)

# <article> HTML5
class Article(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'article', **attrs)

# <aside> HTML5
class Aside(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'aside', **attrs)

# <audio> HTML5
class Audio(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'audio', **attrs)

# <b>
class B(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'b', **attrs)

# <base>
class Base(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'base', **attrs)

# <bdi> HTML5
class Bdi(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'bdi', **attrs)

# <bdo>
class Bdo(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'bdo', **attrs)

# <blockquote>
class BlockQuote(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'blockquote', **attrs)

# <body>
class Body(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'body', **attrs)

# <br>
class Br(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'br', **attrs)

# <button>
class Button(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'button', **attrs)

# <canvas> HTML5
class Canvas(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'canvas', **attrs)

# <caption>
class Caption(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'caption', **attrs)

# <cite>
class Cite(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'cite', **attrs)

# <code>
class Code(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'code', **attrs)

# <col>
class Col(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'col', **attrs)

# <colgroup>
class ColGroup(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'colgroup', **attrs)

# <datalist> HTML5
class DataList(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'datalist', **attrs)

# <dd>
class Dd(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'dd', **attrs)

# <del>
class Del(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'del', **attrs)

# <details> HTML5
class Details(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'details', **attrs)

# <dfn>
class Dfn(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'dfn', **attrs)

# <dialog> HTML5
class Dialog(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'dialog', **attrs)

# <div>
class Div(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'div', **attrs)

# <dl>
class Dl(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'dl', **attrs)

# <dt>
class Dt(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'dt', **attrs)

# <em>
class Em(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'em', **attrs)

# <embed> HTML5
class Embed(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'embed', **attrs)

# <fieldset>
class FieldSet(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'fieldset', **attrs)

# <figcaption> HTML5
class FigCaption(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'figcaption', **attrs)

# <figure> HTML5
class Figure(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'figure', **attrs)

# <footer> HTML5
class Footer(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'footer', **attrs)

# <form>
class Form(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'form', **attrs)

# <h1> ~ <h6>
class H(Tag):
    def __init__(self, level, **attrs): Tag.__init__(self, 'h' + str(level), **attrs)

# <head>
class Head(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'head', **attrs)

# <header> HTML5
class Header(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'header', **attrs)

# <hr>
class Hr(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'hr', **attrs)

# <html>
class Html(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'html', **attrs)

# <i>
class I(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'i', **attrs)

# <iframe>
class Iframe(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'iframe', **attrs)

# <img>
class Img(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'img', **attrs)

# <input>
class Input(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'input', **attrs)

# <ins>
class Ins(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'ins', **attrs)

# <kbd>
class Kbd(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'kbd', **attrs)

# <label>
class Label(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'label', **attrs)

# <legend>
class Legend(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'legend', **attrs)

# <li>
class Li(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'li', **attrs)

# <link>
class Link(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'link', **attrs)

# <main> HTML5
class Main(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'main', **attrs)

# <map>
class Map(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'map', **attrs)

# <mark> HTML5
class Mark(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'mark', **attrs)

# <menu>
class Menu(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'menu', **attrs)

# <menuitem> HTML5
class MenuItem(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'menuitem', **attrs)

# <meta>
class Meta(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'meta', **attrs)

# <meter> HTML5
class Meter(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'meter', **attrs)

# <nav> HTML5
class Nav(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'nav', **attrs)

# <noscript>
class NoScript(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'noscript', **attrs)

# <object>
class Object(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'object', **attrs)

# <ol>
class Ol(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'ol', **attrs)

# <optgroup>
class OptGroup(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'optgroup', **attrs)

# <option>
class Option(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'option', **attrs)

# <output> HTML5
class Output(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'output', **attrs)

# <p>
class P(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'p', **attrs)

# <param>
class Param(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'param', **attrs)

# <picture> HTML5
class Picture(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'picture', **attrs)

# <pre>
class Pre(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'pre', **attrs)

# <progress> HTML5
class Progress(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'progress', **attrs)

# <q>
class Q(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'q', **attrs)

# <rp> HTML5
class Rp(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'rp', **attrs)

# <rt> HTML5
class Rt(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'rt', **attrs)

# <ruby> HTML5
class Ruby(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'ruby', **attrs)

# <s>
class S(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 's', **attrs)

# <samp>
class Samp(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'samp', **attrs)

# <script>
class Script(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'script', **attrs)

# <section> HTML5
class Section(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'section', **attrs)

# <select>
class Select(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'select', **attrs)

# <small>
class Small(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'small', **attrs)

# <source> HTML5
class Source(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'source', **attrs)

# <span>
class Span(Tag): 
    def __init__(self, **attrs): Tag.__init__(self, 'span', **attrs)

# <strong>
class Strong(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'strong', **attrs)

# <style>
class Style(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'style', **attrs)

# <sub>
class Sub(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'sub', **attrs)

# <summary> HTML5
class Summary(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'summary', **attrs)

# <sup>
class Sup(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'sup', **attrs)

# <table>
class Table(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'table', **attrs)

# <tbody>
class Tbody(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'tbody', **attrs)

# <td>
class Td(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'td', **attrs)

# <textarea>
class TextArea(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'textarea', **attrs)

# <tfoot>
class Tfoot(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'tfoot', **attrs)

# <th>
class Th(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'th', **attrs)

# <thead>
class Thead(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'thead', **attrs)

# <time> HTML5
class Time(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'time', **attrs)

# <title>
class Title(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'title', **attrs)

# <tr>        
class Tr(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'tr', **attrs)

# <track> HTML5
class Track(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'track', **attrs)

# <u>
class U(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'u', **attrs)

# <ul>
class Ul(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'ul', **attrs)

# <var>
class Var(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'var', **attrs)

# <video> HTML5
class Video(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'video', **attrs)

# <wbr> HTML5
class Wbr(Tag):
    def __init__(self, **attrs): Tag.__init__(self, 'wbr', **attrs)

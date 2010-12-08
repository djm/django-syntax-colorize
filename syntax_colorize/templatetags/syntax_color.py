from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from lxml import html
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer, ClassNotFound

register = template.Library()

def generate_pygments_css(path=None):
    if path is None:
        import os
        path = os.path.join(os.getcwd(), 'pygments.css')
    f = open(path,'w')
    f.write(HtmlFormatter().get_style_defs('.highlight'))
    f.close()


def get_lexer(value, arg):
    if arg is None:
        return guess_lexer(value)
    return get_lexer_by_name(arg)

@register.filter(name='colorize')
@stringfilter
def colorize(value, arg=None):
    try:
        return mark_safe(highlight(value, get_lexer(value, arg), HtmlFormatter()))
    except ClassNotFound:
        return value

@register.filter(name='colorize_pre')
@stringfilter
def colorize_pre(value, arg=None):
    """
    Given a chunk of rendered html/text, will find all 
    `<pre>` tags and render them with the html formatter.
    The lexer used will be based on the lang attrib
    given to the `<pre>` tag. e.g `<pre lang="python">`
    """
    try:
        html_node = html.fragment_fromstring(value, create_parent='div')
        new_html_node = html_node
        for code_node in html_node.findall('pre'):
            lang = code_node.attrib.get('lang')
            if not code_node.text or not lang:
                continue
            lexer = get_lexer_by_name(lang, stripall=True)
            new_code_node = html.fragment_fromstring(highlight(code_node.text, 
                                                               lexer, 
                                                               HtmlFormatter()))
            new_html_node.replace(code_node, new_code_node)
        return html.tostring(new_html_node, encoding=unicode, method='xml')[5:-6]
    except ClassNotFound:
        return value

@register.filter(name='colorize_table')
@stringfilter
def colorize_table(value, arg=None):
    try:
        return mark_safe(highlight(value, get_lexer(value, arg), HtmlFormatter(linenos='table')))
    except ClassNotFound:
        return value

from django import template

from myapp.views import STOCKS_PER_PAGE

register = template.Library()


@register.simple_tag()
def cal_index(counter, page_num, elem_per_page):
    if elem_per_page:
        parsed_num = int(elem_per_page[elem_per_page.index('=') + 1:])
    else:
        parsed_num = STOCKS_PER_PAGE
    return (page_num - 1) * parsed_num + counter

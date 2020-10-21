from django import template

register = template.Library()


@register.simple_tag()
def cal_index(counter, page_num, elem_per_page):
    return (page_num - 1) * elem_per_page + counter

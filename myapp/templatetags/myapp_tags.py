# from django import template
#
# from myapp.views import STOCKS_PER_PAGE
#
# register = template.Library()
#
#
# @register.filter
# def cal_index(counter, page_num, stocks_per_page_query):
#     return (page_num-1) * int(stocks_per_page_query[stocks_per_page_query.index('=')+1:] or STOCKS_PER_PAGE) + counter

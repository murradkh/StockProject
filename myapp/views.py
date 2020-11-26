from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from myrails.settings import THREAD_INTERVAL

from myapp import stock_api
from myapp.models import Portfolio
from myapp.models import Stock, WatchedStock, Profile, Notification, SoldStock, BoughtStock
from myapp.sub_models.notification_rules_models import ChangeStatusRule, ChangeThresholdRule, PriceThresholdRule, \
    RecommendationAnalystRule

from myapp.forms import CustomRegistrationFrom, CustomChangePasswordForm, ChangeStatusRuleForm, get_rule_from_str
from django.http import JsonResponse, HttpResponse

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

from .exceptions.stock_service import StockServerUnReachable, StockSymbolNotFound, InvalidTimeRange, \
    InvalidSellQuantityValue, InAdequateBudgetLeft, InvalidQuantityValue, InvalidBuyID

from django.db.models import F

STOCKS_PER_PAGE = 10


def index(request):
    if request.method == "GET":
        kwargs = request.GET
        stocks_per_page_query = {}
        search_query = {}

        if "searchText" in kwargs:
            text = kwargs['searchText']
            if "," in text:
                text = text[:text.index(',')]
            search_query = {"searchText": text}
            response = stock_api.list_stocks_names(text)
            stocks = []
            for stock in response:
                stocks.append(Stock(symbol=stock['symbol'],
                                    name=stock['companyName'],
                                    price=stock['latestPrice'],
                                    change=stock['change'],
                                    change_percent=stock['c'
                                                         'hangePercent'],
                                    market_cap=stock['marketCap'],
                                    primary_exchange=stock['primaryExchange']))
        else:
            stocks = Stock.objects.all().order_by('top_rank')

        if "stocks_per_page" in kwargs and kwargs.get("stocks_per_page").isdecimal() \
                and int(kwargs.get("stocks_per_page")) > 0:
            paginator = Paginator(stocks, int(kwargs.get("stocks_per_page")))
            stocks_per_page_query.update({"stocks_per_page": kwargs['stocks_per_page']})
        else:
            paginator = Paginator(stocks, STOCKS_PER_PAGE)

        if "page" in kwargs:
            page_number = kwargs.get('page')
        else:
            page_number = 1
        page_obj = paginator.get_page(page_number)

        profile = None
        if request.user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=request.user)

        context = {
            'page_obj': page_obj,
            "pages_indices": range(1, paginator.num_pages + 1),
            # "search_form": SearchForm,
            "search_query": urlencode(search_query),
            "stocks_per_page_query": urlencode(stocks_per_page_query),
            'page_title': 'Main',
            'profile': profile,
            'Interval': (THREAD_INTERVAL * 1000)
        }

        return render(request, 'index.html', context)
    return redirect(reverse("index"))


# View for the single stock page
# symbol is the requested stock's symbol ('AAPL' for Apple)
def single_stock(request, symbol):
    context = {}
    profile = None
    status_code = 200
    template = 'single_stock.html'
    try:
        # budget
        if request.user.is_authenticated:
            profile, create = Profile.objects.get_or_create(user=request.user)
            budget = profile.portfolio.budget
        else:
            budget = 0
        data = stock_api.get_stock_info(symbol)
        stock = Stock.objects.filter(symbol=symbol)[:1]
        if request.user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=request.user)
    except StockSymbolNotFound as e:
        status_code = 404  # stock symbol not found!
        context = {'error_message': e.message, "status_code": status_code}
        template = "exception.html"
    except StockServerUnReachable as e:
        status_code = 503  # Service Unavailable code
        context = {'error_message': e.message, "status_code": status_code}
        template = "exception.html"
    except Exception as e:
        status_code = 520  # Unknown Error
        context = {'error_message': "Unknown Error occurred: {}".format(", ".join(e.args)), "status_code": status_code}
        template = "exception.html"
    else:
        context = {'page_title': 'Stock Page - %s' % symbol, 'data': data, 'stock': stock, 'profile': profile,
                   'budget': budget}
    finally:
        response = render(request, template, context)
        response.status_code = status_code
        return response


def register(request):
    form = CustomRegistrationFrom(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.info(request, 'Your account was successfully created!')
        return redirect('index')
    return render(request, 'register.html', {'page_title': 'Register', 'form': form})


@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'page_title': 'My account', 'profile': profile})


@login_required(login_url='login')
def watchlist_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'watchlist.html', {'page_title': 'My watchlist', 'profile': profile, 'Interval': (
            THREAD_INTERVAL * 1000)})


@require_http_methods(['POST'])
@login_required(login_url='login')
def watchlist_add_view(request, symbol):
    status_code = 200
    profile, created = Profile.objects.get_or_create(user=request.user)
    stock_in_db = Stock.objects.filter(symbol=symbol)[:1]
    if stock_in_db.exists():
        Stock.add_to_watchlist(profile, symbol)
        response = HttpResponse('OK')
    else:
        try:
            data = stock_api.get_stock_info(symbol)
            Stock.add_to_db(data)
            Stock.add_to_watchlist(profile, symbol)
            response = HttpResponse('OK')
        except StockSymbolNotFound as e:
            status_code = 404
            response = HttpResponse('Symbol Not Found')
        except StockServerUnReachable as e:
            status_code = 503
            response = HttpResponse('Service Unavailable')
        except Exception as e:
            status_code = 520
            response = HttpResponse('Unknown Error')
    response.status_code = status_code
    return response


@require_http_methods(['POST'])
@login_required(login_url='login')
def watchlist_remove_view(request, symbol):
    status_code = 200
    profile, created = Profile.objects.get_or_create(user=request.user)
    stock_in_db = Stock.objects.filter(symbol=symbol)[:1]
    if stock_in_db.exists():
        Stock.remove_from_watchlist(profile, symbol)
        response = HttpResponse('OK')
    else:
        status_code = 404
        response = HttpResponse('Symbol Not in DB')
    response.status_code = status_code
    return response


@require_http_methods(['POST'])
@login_required(login_url='login')
def sell_stock_view(request, buy_id):
    status_code = 200
    profile, created = Profile.objects.get_or_create(user=request.user)
    try:
        q = request.POST.get("quantity")
        portfolio, created = Portfolio.objects.get_or_create(profile=profile)
        if created:
            profile.save()
        if q is None:
            portfolio.sell_stock(buy_id, 1)
        else:
            portfolio.sell_stock(buy_id, int(q))
        response = HttpResponse('OK')
    except InvalidSellQuantityValue as e:
        status_code = 404
        response = HttpResponse(e.message)
    except InvalidBuyID as e:
        status_code = 404
        response = HttpResponse(e.message)
    except StockSymbolNotFound as e:
        status_code = 404
        response = HttpResponse('Symbol Not Found')
    except StockServerUnReachable as e:
        status_code = 503
        response = HttpResponse('Service Unavailable')
    except Exception as e:
        status_code = 520
        response = HttpResponse('Unknown Error')
    response.status_code = status_code
    return response


@require_http_methods(['POST'])
@login_required(login_url='login')
def buy_stock_view(request, symbol):
    status_code = 200
    profile, created = Profile.objects.get_or_create(user=request.user)
    try:
        q = request.POST.get("quantity")
        threshold = request.POST['threshold']
        price = float(request.POST['staticPrice'])
        print('staticPrice', price)

        portfolio, created = Portfolio.objects.get_or_create(profile=profile)
        if created:
            profile.save()
        if q is None:
            portfolio.buy_stock(symbol, 1)
        elif threshold is not None and len(threshold.strip()) > 0:
            profile.portfolio.buy_stock(symbol, price, int(q), int(threshold))
        else:
            profile.portfolio.buy_stock(symbol, price, int(q))
        response = HttpResponse('OK')
    except InvalidQuantityValue as e:
        status_code = 404
        response = HttpResponse(e.message)
    except InAdequateBudgetLeft as e:
        status_code = 404
        response = HttpResponse(e.message)
    except StockSymbolNotFound as e:
        status_code = 404
        response = HttpResponse('Symbol Not Found')
    except StockServerUnReachable as e:
        status_code = 503
        response = HttpResponse('Service Unavailable')
    except Exception as e:
        status_code = 520
        response = HttpResponse('Unknown Error')
    response.status_code = status_code
    return response


@login_required(login_url='login')
def password_change_view(request):
    form = CustomChangePasswordForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.info(request, 'Your password was successfully updated!')
        return redirect('index')
    else:
        messages.warning(request, 'Please enter the correct data below')
    return render(request, 'password_change.html', {'page_title': 'Change password', 'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


# API for a stock's price over time
# symbol is the requested stock's symbol ('AAPL' for Apple)
# The response is JSON data of an array composed of "snapshot" objects (date + stock info + ...), usually one per day
def single_stock_historic(request, symbols, time_range='1m'):
    context = None
    status_code = 200

    try:
        data = stock_api.get_stock_historic_prices(symbols, time_range=time_range)
        context = {'data': data}
    except StockSymbolNotFound as e:
        context = {"error_message": e.message}
        status_code = 404
    except InvalidTimeRange as e:
        context = {"error_message": e.message}
        status_code = 400
    except StockServerUnReachable as e:
        context = {"error_message": e.message}
        status_code = 503
    except Exception as e:
        context = {"error_message": "Unknown Error occurred: {}".format(", ".join(e.args))}
        status_code = 520
    finally:
        response = JsonResponse(context)
        response.status_code = status_code
        return response


@require_http_methods(['GET'])
def list_stocks_names_view(request, search_text):
    context = None
    status_code = 200
    try:
        stocks_names = stock_api.list_stocks_names(search_text, filter=("symbol", "companyName"))
        context = {"stocks_names": stocks_names}
    except StockServerUnReachable as e:
        context = {"error_message": e.message}
        status_code = 503
    except Exception as e:
        context = {"error_message": "Unknown Error occurred: {}".format(", ".join(e.args))}
        status_code = 520
    finally:
        response = JsonResponse(context)
        response.status_code = status_code
        return response


@login_required(login_url='login')
def portfolio_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {'page_title': 'My Portfolio', 'profile': profile,
               'bought_stocks': BoughtStock.objects.filter(portfolio=profile.portfolio,
                                                           quantity__gt=F('sold_quantity')),
               'sold_stocks': SoldStock.objects.filter(portfolio=profile.portfolio),
               'Interval': (THREAD_INTERVAL * 1000)}
    return render(request, 'portfolio.html', context)


def list_notifications_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return JsonResponse(profile.get_notifications())


@login_required(login_url='login')
def notification_unread_count_view(request, pk=""):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return JsonResponse({'unread_count': Notification.objects.filter(is_read=False, user=profile).count()})


@require_http_methods(['POST'])
@login_required(login_url='login')
def notification_remove_view(request, pk=""):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if pk:
        Notification.objects.filter(pk=pk, user=profile).delete()
    else:
        Notification.objects.filter(user=profile).delete()
    return HttpResponse('OK')


@require_http_methods(['POST'])
@login_required(login_url='login')
def notifications_mark_read_view(request, pk=""):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if pk:
        Notification.objects.filter(pk=pk, user=profile).update(is_read=True)
    else:
        Notification.objects.filter(user=profile).update(is_read=True)
    return HttpResponse('OK')


@login_required(login_url='login')
def add_rule_view(request, rule_type, symbol):
    form, rule_name, rule = get_rule_from_str(request, rule_type)
    if form == None:
        context = {'error_message': 'Invalid notification rule type'}
        response = render(request, 'exception.html', context)
        response.status_code = 400
        return response

    profile, created = Profile.objects.get_or_create(user=request.user)
    watched_stock = WatchedStock.objects.filter(stock__symbol=symbol, profile=profile)
    if watched_stock.exists():
        form.fields['watched_stock'].initial = watched_stock[0]
        if form.is_valid():
            form.save()
            messages.info(request, f'Notification rule for {watched_stock[0].stock.name} successfully added')
            return redirect('single_stock', symbol=symbol)
        context = {'page_title': f'New {rule_name} Rule',
                   'rule_type': rule_type,
                   'form': form,
                   'stock': watched_stock[0].stock}
        response = render(request, 'add_rule.html', context)
        return response
    else:
        messages.warning(request, 'This Stock could not be found in your watchlist')
        return redirect('single_stock', symbol=symbol)


@login_required(login_url='login')
def edit_rule_view(request, rule_type, pk):
    form, rule_name, rule = get_rule_from_str(request, rule_type, pk)
    if form == None:
        context = {'error_message': 'Invalid notification rule type'}
        response = render(request, 'exception.html', context)
        response.status_code = 400
        return response
    if rule:
        profile, created = Profile.objects.get_or_create(user=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Notification rule successfully updated')
            return redirect('index')
        context = {'page_title': f'Edit {rule_name} Rule',
                   'rule_name': rule_name, 'rule_type': rule_type,
                   'pk': pk, 'form': form}
        response = render(request, 'edit_rule.html', context)
        return response
    else:
        context = {'error_message': 'Notification rule not found'}
        response = render(request, 'exception.html', context)
        response.status_code = 404
        return response


@require_http_methods(['POST'])
@login_required(login_url='login')
def delete_rule_view(request, rule_type, pk):
    form, rule_name, rule = get_rule_from_str(request, rule_type, pk)
    rule.delete()
    return HttpResponse('OK')


@login_required(login_url='login')
def rules_list_view(request, symbol):
    profile, created = Profile.objects.get_or_create(user=request.user)
    resposne_dict = {'change_status': ChangeStatusRule.get_rules_dict(profile, symbol),
                     'change_threshold': ChangeThresholdRule.get_rules_dict(profile, symbol),
                     'price_threshold': PriceThresholdRule.get_rules_dict(profile, symbol),
                     'recommendation_analyst': RecommendationAnalystRule.get_rules_dict(profile, symbol)}
    return JsonResponse(resposne_dict)


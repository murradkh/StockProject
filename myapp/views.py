from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from myapp import stock_api
from myapp.models import Stock, Profile
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .exceptions.stock_service import StockServerUnReachable, StockSymbolNotFound


STOCKS_PER_PAGE = 10


def index(request):
    if request.method == "GET":
        kwargs = request.GET
        stocks_per_page_query = {}
        search_query = {}

        if "search_title" in kwargs:
            stocks = Stock.objects.filter(title__contains=kwargs['search_title']).order_by('-created_on')
            search_query = {"search_title": kwargs['search_title']}
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
            'profile': profile
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
        context = {'page_title': 'Stock Page - %s' % symbol, 'data': data, 'stock': stock, 'profile': profile}
    finally:
        response = render(request, template, context)
        response.status_code = status_code
        return response


def register(request):
    # If post -> register the user and redirect to main page
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        newuser = User.objects.create_user(username=email, email=email, password=password)
        newuser.first_name = firstname
        newuser.last_name = lastname
        newuser.save()
        login(request, newuser)
        return redirect('index')
    else:
        # If not post (regular request) -> render register page
        return render(request, 'register.html', {'page_title': 'Register'})


@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'page_title': 'My account', 'profile': profile})


@login_required(login_url='login')
def watchlist_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'watchlist.html', {'page_title': 'My watchlist', 'profile': profile})


@require_http_methods(['POST'])
@login_required(login_url='login')
def watchlist_add_view(request, symbol):
    profile, created = Profile.objects.get_or_create(user=request.user)
    stock = Stock.objects.filter(symbol=symbol)[:1]
    if not stock.exists():
        context = {'error_message': 'Stock symbol not found', 'status_code': 404}
        response = render(request, 'exception.html', context)
        response.status_code = 404
    else:
        Stock.add_to_watchlist(profile, symbol)
        response = HttpResponse('OK')
    return response


@require_http_methods(['POST'])
@login_required(login_url='login')
def watchlist_remove_view(request, symbol):
    profile, created = Profile.objects.get_or_create(user=request.user)
    stock = Stock.objects.filter(symbol=symbol)[:1]
    if not stock.exists():
        context = {'error_message': 'Stock symbol not found', 'status_code': 404}
        response = render(request, 'exception.html', context)
        response.status_code = 404
    else:
        Stock.remove_from_watchlist(profile, symbol)
        response = HttpResponse('OK')
    return response


@login_required(login_url='login')
def password_change_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)
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
def single_stock_historic(request, symbol):
    context = None
    status_code = 200
    try:
        data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
        context = {'data': data}
    except StockSymbolNotFound as e:
        context = {"error_message": e.message}
        status_code = 404
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

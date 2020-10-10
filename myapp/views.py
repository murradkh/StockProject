from django.shortcuts import render, redirect
from myapp import stock_api
from myapp.models import Stock, Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


# View for the home page - a list of 20 of the most active stocks
def index(request):
	# Query the stock table, filter for top ranked stocks and order by their rank.
	data = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
	profile = None
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=request.user)
	return render(request, 'index.html', {'page_title': 'Main', 'data': data, 'profile': profile})


# View for the single stock page
# symbol is the requested stock's symbol ('AAPL' for Apple)
def single_stock(request, symbol):
	data = stock_api.get_stock_info(symbol)
	stock = Stock.objects.get(symbol=symbol)
	profile = None
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=request.user)
	return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data, 'stock': stock, 'profile': profile})


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
	profile = Profile.objects.get(user=request.user)
	return render(request, 'profile.html', {'page_title': 'My account', 'profile': profile})


@login_required(login_url='login')
def watchlist_view(request):
	profile = Profile.objects.get(user=request.user)
	return render(request, 'watchlist.html', {'page_title': 'My watchlist', 'profile': profile})


@require_http_methods(['POST'])
@login_required(login_url='login')
def watchlist_add_view(request, symbol):
	profile = Profile.objects.get(user=request.user)
	stock = Stock.objects.filter(symbol=symbol)
	if not stock.exists():
		return Response(status=status.HTTP_404_NOT_FOUND)
	else:
		Stock.add_to_watchlist(profile, symbol)
		next = request.POST.get('next', '/')
		return redirect(next)


@require_http_methods(['POST'])
@login_required(login_url='login')
def watchlist_remove_view(request, symbol):
	profile = Profile.objects.get(user=request.user)
	stock = Stock.objects.filter(symbol=symbol)
	if not stock.exists():
		return Response(status=status.HTTP_404_NOT_FOUND)
	else:
		Stock.remove_from_watchlist(profile, symbol)
		next = request.POST.get('next', '/')
		return redirect(next)


def logout_view(request):
	logout(request)
	return redirect('index')


# API for a stock's price over time
# symbol is the requested stock's symbol ('AAPL' for Apple)
# The response is JSON data of an array composed of "snapshot" objects (date + stock info + ...), usually one per day
def single_stock_historic(request, symbol):
	data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
	return JsonResponse({'data': data})

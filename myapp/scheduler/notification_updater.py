from myapp.models import Stock, ChangeStatusRule, Notification
from myapp import stock_api
from django.db import transaction

CHANGE_STATUS_RULE_THREAD_INTERVAL = 1 * 60 * 60 * 24  # one day interval


def change_status_rule():
    rules = ChangeStatusRule.get_rules()
    for rule in rules:
        num_of_days = rule.num_of_days
        if num_of_days < 5:
            time_range = '5d'
        elif num_of_days < 20:
            time_range = '1m'
        elif num_of_days < 60:
            time_range = '3m'
        elif num_of_days < 120:
            time_range = '6m'
        elif num_of_days < 240:
            time_range = '1y'
        else:
            time_range = '2y'
        days = stock_api.get_stock_historic_prices(symbols=rule.watched_stock.stock.symbol, time_range=time_range,
                                                   chart_interval=1, filter=("changePercent", "date"))
        if num_of_days < len(days):
            for day in days[:-num_of_days - 1:-1]:
                if rule.status == 'N':
                    if day['changePercent'] > 0:
                        break  # indicating no sequential negative change value through <num_of_days> days
                if rule.status == 'P':
                    if day['changePercent'] < 0:
                        break  # indicating no sequential positive change value through <num_of_days> days
            else:
                # indicating there is sequential change through <num_of_days> days,
                # here we need to insert a notification to user in DB
                title = f"Sequential {'Positive' if rule.status == 'P' else 'Negative'} Change"
                description = f"sequential positive change in the past {num_of_days} days for {rule.watched_stock.stock.name}"
                Notification.objects.create(user=rule.watched_stock.profile, title=title, description=description)

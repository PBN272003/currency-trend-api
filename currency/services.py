import requests
from datetime import date
from django.conf import settings
from datetime import datetime, timedelta
from django.core.cache import cache
import hashlib
import json
from django.core.mail import send_mail
# BASE_API_URL = "https://api.exchangeratesapi.io/v1"

# def fetch_exchange_rate_data(base_currency, target_currency, start_date=None, end_date=None):
#     if start_date and end_date:
#         # Historical data via timeseries endpoint
#         API_KEY= settings.EXCHANGE_RATE_API_KEY
#         url = f"{BASE_API_URL}/timeseries"
#         params = {
#             "base": base_currency,
#             "symbols": target_currency,
#             "start_date": start_date,
#             "end_date": end_date,
#             "access_key": API_KEY
#         }
#     else:
#         # Current exchange rate via latest endpoint
#         API_KEY = settings.EXCHANGE_RATE_API_KEY
#         url = f"{BASE_API_URL}/latest"
#         params = {
#             "base": base_currency,
#             "symbols": target_currency,
#             "access_key": API_KEY
#         }
        
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         if 'error' in data:
#             raise ValueError(f"API Error: {data['error']['info']}")
#         return data
#     else:
#         raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")
BASE_API_URL = "https://openexchangerates.org/api"

def send_currency_alert_email(user, base, target, current_rate, avg_rate, percent_change):
    subject = f"📈 Alert: {base} → {target} Rate Changed by {percent_change}%"
    message = (
        f"Hi {user.username},\n\n"
        f"The currency rate for {base} to {target} has changed significantly.\n\n"
        f"🔸 Average Historical Rate: {avg_rate:.4f}\n"
        f"🔸 Current Rate: {current_rate:.4f}\n"
        f"🔸 Change: {percent_change:.2f}%\n\n"
        f"Thanks,\nCurrency Trends Team"
    )
    send_mail(
        subject,
        message,
        'priyank.naik2003@gmail.com',  
        [user.email],
        fail_silently=False,
    )

def should_notify_user(historical_rates: dict, current_rate: float, threshold=3.0):
    avg_historical_rate = sum(historical_rates.values()) / len(historical_rates)
    percent_change = ((current_rate - avg_historical_rate) / avg_historical_rate) * 100
    return abs(percent_change) >= threshold, round(percent_change, 2)

def get_cache_key(base,target, start, end):
    key_string = f"{base}_{target}_{start}_{end}"
    return hashlib.md5(key_string.encode()).hexdigest()
    
def fetch_exchange_rate_data(base_currency, target_currency, start_date=None, end_date=None):
    app_id = settings.OPENEXCHANGE_APP_ID

    if base_currency != "USD":
        raise ValueError("Base currency switching requires a paid plan. Only 'USD' is supported.")
    
    cache_key = get_cache_key(base_currency, target_currency, start_date, end_date)
    cached_data = cache.get(cache_key)
    if cached_data:
        print("✅ Data loaded from cache for:", cache_key)
        print("Cached data:", cached_data)
        return json.loads(cached_data)
    
    print("⚠️ Cache miss for:", cache_key)
    if start_date and end_date:
        # Historical range handling
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        results = {}

        while start <= end:
            date_str = start.strftime("%Y-%m-%d")
            url = f"{BASE_API_URL}/historical/{date_str}.json"

            params = {
                "app_id": app_id,
                "symbols": target_currency,
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                results[date_str] = data["rates"].get(target_currency)
            else:
                raise ValueError(f"Failed on {date_str}: {response.status_code} - {response.text}")

            start += timedelta(days=1)

        final_data= {
            "base": base_currency,
            "target": target_currency,
            "rates": results
        }
        cache.set(cache_key, json.dumps(final_data), 60*60*24) # cache for 24 hours
        return final_data

    else:
        # Latest data
        url = f"{BASE_API_URL}/latest.json"
        params = {
            "app_id": app_id,
            "symbols": target_currency
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            final_data= {
                "base": base_currency,
                "target": target_currency,
                "rate": data["rates"].get(target_currency),
                "date": data["timestamp"]
            }
            cache.set(cache_key, json.dumps(final_data), 60*60*24) # cache for 24 hours
            return final_data
        else:
            raise ValueError(f"Failed to fetch latest: {response.status_code} - {response.text}")
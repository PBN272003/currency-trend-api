# 💱 Currency Trend Monitoring API (Django + DRF)
This project allows users to monitor currency exchange rate trends and get alerts via email if there's a significant change. Features are JWT authentication, rate limiting, caching, Swagger docs, Admin Dashboad for visualizing the API usage, Watchlist for getting readily available currency pair.

# 🚀 Features

✅ JWT Authentication for secure login & registration

📈 Fetch Real-Time & Historical Exchange Rates

🧠 Caching using Django’s cache framework for faster repeated data retrieval

🛡️ Rate Limiting to prevent API abuse (e.g., max 4 requests/minute)

📬 Email Alerts triggered by significant currency fluctuations

📊 Swagger/OpenAPI API Documentation for interactive exploration

📘 Admin Dashboard with visual charts for top currency pair usage

💼 User Watchlist for tracking selected currency pairs


# 📁 Folder Structure

currency_trend_project/
├── currency/ # App for exchange rate logic and watchlist
├── user/ # Custom user logic
├── static/ # Static files (JS, CSS)
├── templates/ # (Optional) Templates folder
├── manage.py
└── README.md

# ⚙️ Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/your-username/currency-trend-api.git
cd currency-trend-api
```

2. Create a virtual environment:

python -m venv env
source env/bin/activate     # Windows: env\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt


4. Add your settings in settings.py:

✅ Exchange Rate API Key:

OPENEXCHANGE_APP_ID = "your_openexchangerates_app_id"

✅ Email SMTP Config:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

Use Gmail App Passwords if you have 2FA enabled.


5. Run migrations:

python manage.py makemigrations
python manage.py migrate


6. Create a superuser:

python manage.py createsuperuser


7. Start the server:

python manage.py runserver


# Registration

POST /api/register/ – Register user


# 🔐 Authentication

POST /api/token/ – Get JWT token

POST /api/token/refresh/ – Refresh token


# 📬 Sample API Requests

➕ Add to Watchlist

POST /api/currency/watchlist/
Authorization: Bearer <token>
{
  "base_currency": "USD",
  "target_currency": "INR"
}


Get Watchlist

GET /api/currency/watchlist/
Authorization: Bearer <token>


📈 Get Trends + Alert

1. for Latest Data

GET /api/currency/trends
Authorization: Bearer <token>


2. for Historical data(range)

GET /api/currency/trends/?base=USD&target=INR&start=2024-05-01&end=2024-05-03
Authorization: Bearer <token>


# 🔍 API Documentation (Swagger)

Once server is running, open:

Swagger UI → http://127.0.0.1:8000/swagger/

Redoc UI → http://127.0.0.1:8000/redoc/


# 🧪 Testing Emails

For development:

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

To send real email, use SMTP config mentioned earlier.


# 🧠 Tech Stack

Django 

Django REST Framework

drf-yasg (Swagger Docs)

SQLite (default DB)

OpenExchangeRates API

Gmail SMTP for alerts

# 📬 Sample API Requests & Responses

✅ Admin Dashboard

Charts visible under /admin/ for tracking the API usage and User activities.(project url)

🔐 User Registration

1. POST /api/register/

Request:
{
  "username": "roman",
  "email": "roman@example.com",
  "password": "strongpassword123"
}

Response:
{
  "id": 3,
  "username": "roman",
  "email": "roman@example.com"
}


🔑 JWT Token (Login)

1. POST /api/token/

Request:
{
  "username": "roman",
  "password": "strongpassword123"
}

Response:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJI..."
}

📈 Get Currency Trend (Current Rate Only)

1. GET /api/currency/trend/?base=USD&target=INR

Response:
{
  "base": "USD",
  "target": "INR",
  "rate": 83.4203,
  "date": 1750612525
}


📊 Get Historical + Current Rate (Triggers Email if Significant Change)

1. GET /api/currency/trend/?base=USD&target=INR&start=2024-05-01&end=2024-05-02

Response:
{
  "base": "USD",
  "target": "INR",
  "rates": {
    "2024-05-01": 83.406638,
    "2024-05-02": 83.40446
  },
  "current_rate": 86.601602
}
✅ If the percent change from historical average to current rate exceeds 3%, an email alert is sent to the user.


🧾 Watchlist (Add Currency Pair)

1. POST /api/watchlist/

Request:
{
  "base_currency": "USD",
  "target_currency": "JPY"
}

Response:
{
  "id": 5,
  "user": 3,
  "base_currency": "USD",
  "target_currency": "JPY"
}


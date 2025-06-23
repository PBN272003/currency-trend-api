from .models import WatchList
from django.urls import path
from .views import WatchlistView, ExchangeTrendView

urlpatterns = [
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', WatchlistView.as_view(), name='watchlist_delete'),
    path('trend/', ExchangeTrendView.as_view(), name='currency_trend'),
]
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import WatchList
from .serializers import WatchListSerializer
from .services import fetch_exchange_rate_data,should_notify_user,send_currency_alert_email
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class WatchlistView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get the authenticated user's watchlist.",
        responses={200: WatchListSerializer(many=True)}
    )    
    def get(self, request):
        watchlist = WatchList.objects.filter(user=request.user)
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=WatchListSerializer,
        operation_description="Add a new currency pair to the user's watchlist.",
        responses={201: WatchListSerializer()}
    )
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            if WatchList.objects.filter(
                user=request.user,
                base_currency=serializer.validated_data['base_currency'],
                target_currency=serializer.validated_data['target_currency']
            ).exists():
                return Response({"detail": "This currency pair is already in your watchlist."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_description="Delete a currency pair from the user's watchlist using the pair ID.",
        responses={204: "Deleted successfully", 404: "Item not found"}
    )    
    def delete(self, request, pk=None):
        try:
            watch = WatchList.objects.get(id=pk, user=request.user)
            watch.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WatchList.DoesNotExist:
            return Response({"detail": "Watchlist item not found."}, status=status.HTTP_404_NOT_FOUND)
        

class ExchangeTrendView(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='4/m', block=True))  
    @swagger_auto_schema(
        operation_description="Returns historical and/or current exchange rate trend between two currencies. If a significant change is detected, the user will receive an email notification.",
        manual_parameters=[
            openapi.Parameter('base', openapi.IN_QUERY, description="Base currency (e.g., USD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('target', openapi.IN_QUERY, description="Target currency (e.g., INR)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('start', openapi.IN_QUERY, description="Start date (optional, YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end', openapi.IN_QUERY, description="End date (optional, YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response(description="Exchange rate data returned.")}
    )    
    def get(self, request):
        if getattr(request, 'limited', False):
            return Response({'error': 'Rate limit exceeded.'}, status=429)
        base = request.query_params.get("base")
        symbols = request.query_params.get("target")
        # Optional parameters for historical data
        start = request.query_params.get("start")  
        end = request.query_params.get("end")      

        if not base or not symbols:
            return Response({"error": "base and target currencies are required."}, status=400)

        # data = fetch_exchange_rate_data(base, symbols, start, end)
        # print("Fetched data:",data)
        # rate = data.get("rate")
        # print("Rate data:", rate)

        # return Response(data)
        current_data = fetch_exchange_rate_data(base, symbols)
        current_rate = current_data.get("rate")

    # 🔹 Step 2: If historical params provided
        if start and end:
           historical_data = fetch_exchange_rate_data(base, symbols, start, end)
           historical_rates = historical_data.get("rates")
        
           if historical_rates and current_rate:
               should_notify, percent_change = should_notify_user(historical_rates, current_rate)
               if should_notify:
                     send_currency_alert_email(
                        request.user,
                        base,
                        symbols,
                        current_rate,
                        sum(historical_rates.values()) / len(historical_rates),
                        percent_change
                        )
           historical_data["current_rate"] = current_rate    
           return Response(historical_data)
        else:
           return Response(current_data)

        
from rest_framework import serializers
from .models import WatchList

class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ('id', 'base_currency', 'target_currency', 'created_at')
        read_only_fields = ('id', 'created_at')

  
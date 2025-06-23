from django.db import models
from django.conf import settings
# Create your models here.
class WatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    base_currency = models.CharField(max_length=10)
    target_currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'base_currency', 'target_currency')

    def __str__(self):
        return f"{self.user.username} - {self.base_currency}/{self.target_currency}"
    
    @property
    def currency_pair(self):
        return f"{self.base_currency}→{self.target_currency}"
    
class APILog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.PositiveIntegerField(default=200)
    success = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user if self.user else 'Anonymous'} - {self.endpoint} - {self.timestamp}"
    
    
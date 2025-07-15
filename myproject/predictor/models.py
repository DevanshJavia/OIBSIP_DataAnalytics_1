from django.db import models
from django.contrib.auth.models import User

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    predicted_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Input features for record-keeping
    area = models.FloatField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    stories = models.IntegerField(null=True, blank=True)
    parking = models.IntegerField(null=True, blank=True)
    mainroad = models.CharField(max_length=3, null=True, blank=True)
    guestroom = models.CharField(max_length=3, null=True, blank=True)
    basement = models.CharField(max_length=3, null=True, blank=True)
    hotwaterheating = models.CharField(max_length=3, null=True, blank=True)
    airconditioning = models.CharField(max_length=3, null=True, blank=True)
    prefarea = models.CharField(max_length=3, null=True, blank=True)
    furnishingstatus = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.predicted_price} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

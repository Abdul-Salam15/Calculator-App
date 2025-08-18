from django.db import models
from django.contrib.auth.models import User

class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    expression = models.CharField(max_length=255)  # e.g. "5 + 3"
    result = models.CharField(max_length=50)       # e.g. "8"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expression} = {self.result}"

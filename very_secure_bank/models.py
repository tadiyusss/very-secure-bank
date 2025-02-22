from django.db import models
from django.contrib.auth.models import User

class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    balance = models.FloatField(default=0.00)
    wallet_address = models.CharField(max_length=64, null=False)

    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Transactions(models.Model):
    sender = models.ForeignKey(UserInformation, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserInformation, on_delete=models.CASCADE, related_name='receiver')
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.user.username} -> {self.receiver.user.username}'
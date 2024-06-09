from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

class Payer(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.balance < Decimal('0.00'):
            raise ValidationError('Initial balance cannot be negative')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    from_payer = models.ForeignKey(Payer, related_name='outgoing_transactions', on_delete=models.CASCADE)
    to_payer = models.ForeignKey(Payer, related_name='incoming_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
from django.db import models

class Payer(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    from_payer = models.ForeignKey(Payer, related_name='outgoing_transactions', on_delete=models.CASCADE)
    to_payer = models.ForeignKey(Payer, related_name='incoming_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
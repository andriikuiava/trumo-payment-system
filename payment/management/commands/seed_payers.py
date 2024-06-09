from django.core.management.base import BaseCommand
from payment.models import Payer
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Creates 3 payers with random balances if there are less than 3 payers in the database'

    def handle(self, *args, **options):
        num_payers = Payer.objects.count()
        num_payers_to_create = 3 - num_payers

        for _ in range(num_payers_to_create):
            Payer.objects.create(
                name=f'Payer {num_payers + 1}',
                balance=Decimal(random.uniform(1, 1000))
            )
            num_payers += 1
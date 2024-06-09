import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from payment.models import Payer, Transaction


@pytest.mark.django_db
def test_create_payer():
    payer = Payer.objects.create(name='Test Payer', balance=Decimal('100.00'))
    assert payer.name == 'Test Payer'
    assert payer.balance == Decimal('100.00')

@pytest.mark.django_db
def test_create_payer_with_negative_balance():
    with pytest.raises(ValidationError):
        Payer.objects.create(name='Invalid Payer', balance=Decimal('-50.00'))

@pytest.mark.django_db
def test_create_transaction():
    from_payer = Payer.objects.create(name='From Payer', balance=Decimal('200.00'))
    to_payer = Payer.objects.create(name='To Payer', balance=Decimal('50.00'))
    transaction = Transaction.objects.create(from_payer=from_payer, to_payer=to_payer, amount=Decimal('100.00'))
    from_payer.balance -= transaction.amount
    to_payer.balance += transaction.amount
    from_payer.save()
    to_payer.save()
    from_payer.refresh_from_db()
    to_payer.refresh_from_db()

    assert from_payer.balance == Decimal('100.00')
    assert to_payer.balance == Decimal('150.00')
    assert transaction.amount == Decimal('100.00')
    assert transaction.from_payer == from_payer
    assert transaction.to_payer == to_payer

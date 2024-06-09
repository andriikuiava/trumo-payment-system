import pytest
from rest_framework.test import APIClient
from decimal import Decimal
from payment.models import Payer

@pytest.mark.django_db
def test_create_payer_api():
    client = APIClient()
    response = client.post('/api/payers/create_payer/', {'name': 'API Payer', 'balance': '100.00'}, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'API Payer'
    assert Decimal(response.data['balance']) == Decimal('100.00')

@pytest.mark.django_db
def test_create_payer_api_invalid_balance():
    client = APIClient()
    response = client.post('/api/payers/create_payer/', {'name': 'Invalid API Payer', 'balance': '-50.00'}, format='json')
    assert response.status_code == 400
    assert 'Initial balance cannot be negative' in str(response.data)

@pytest.mark.django_db
def test_transfer_api():
    client = APIClient()
    from_payer = Payer.objects.create(name='From API Payer', balance=Decimal('200.00'))
    to_payer = Payer.objects.create(name='To API Payer', balance=Decimal('50.00'))
    print(from_payer.balance)
    print(to_payer.balance)

    response = client.post('/api/payment/transfer/', {'from_payer': from_payer.id, 'to_payer': to_payer.id, 'amount': '100.00'}, format='json')
    assert response.status_code == 201

    from_payer.refresh_from_db()
    to_payer.refresh_from_db()

    assert from_payer.balance == Decimal('100.00')
    assert to_payer.balance == Decimal('150.00')

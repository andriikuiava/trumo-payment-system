from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from .models import Payer, Transaction
from .serializers import PayerSerializer, TransactionSerializer
from django.db import transaction as db_transaction
from decimal import Decimal

class PayerViewSet(viewsets.ModelViewSet):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer

    @action(detail=False, methods=['post'])
    def create_payer(self, request):
        name = request.data.get('name')
        balance = request.data.get('balance')

        if not name or balance is None:
            return Response({'error': 'Name and balance are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            balance = Decimal(balance)
            if balance < 0:
                return Response({'error': 'Initial balance cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, Decimal.InvalidOperation):
            return Response({'error': 'Invalid balance amount'}, status=status.HTTP_400_BAD_REQUEST)

        payer = Payer.objects.create(name=name, balance=balance)
        cache.delete('payers')
        return Response(PayerSerializer(payer).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def list_balances(self, request):
        payers = cache.get('payers')
        if not payers:
            payers = list(Payer.objects.all())
            cache.set('payers', payers)
        serializer = self.get_serializer(payers, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def transfer(self, request):
        from_payer_id = request.data.get('from_payer')
        print(from_payer_id)
        to_payer_id = request.data.get('to_payer')
        print(to_payer_id)
        amount = request.data.get('amount')

        if from_payer_id == to_payer_id:
            return Response({'error': 'Cannot transfer to the same payer'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
            if amount <= 0:
                return Response({'error': 'Transfer amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, Decimal.InvalidOperation):
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        with db_transaction.atomic():
            try:
                from_payer = Payer.objects.select_for_update().get(pk=from_payer_id)
                to_payer = Payer.objects.select_for_update().get(pk=to_payer_id)
            except Payer.DoesNotExist:
                return Response({'error': 'Payer not found'}, status=status.HTTP_404_NOT_FOUND)

            if from_payer.balance < amount:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

            from_payer.balance -= amount
            to_payer.balance += amount
            from_payer.save()
            to_payer.save()

            transaction = Transaction.objects.create(from_payer=from_payer, to_payer=to_payer, amount=amount)

        cache.delete('payers')

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        payer_id = self.request.query_params.get('payer_id')
        if payer_id:
            return Transaction.objects.filter(from_payer_id=payer_id) | Transaction.objects.filter(to_payer_id=payer_id)
        return super().get_queryset()

def index(request):
    payers = Payer.objects.all()
    transactions = Transaction.objects.all()
    return render(request, 'index.html', {'payers': payers, 'transactions': transactions})

def create_payer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        balance = request.POST.get('balance')

        try:
            balance = Decimal(balance)
            if balance < 0:
                return render(request, 'create_payer.html', {'error': 'Initial balance cannot be negative'})
        except (ValueError, Decimal.InvalidOperation):
            return render(request, 'create_payer.html', {'error': 'Invalid balance amount'})

        Payer.objects.create(name=name, balance=balance)
        cache.delete('payers')
        return redirect('index')

    return render(request, 'create_payer.html')

def transfer(request):
    if request.method == 'POST':
        from_payer_id = request.POST.get('from_payer')
        to_payer_id = request.POST.get('to_payer')
        amount = request.POST.get('amount')

        if from_payer_id == to_payer_id:
            return render(request, 'transfer.html', {'error': 'Cannot transfer to the same payer'})

        try:
            amount = Decimal(amount)
            if amount <= 0:
                return render(request, 'transfer.html', {'error': 'Transfer amount must be positive'})
        except (ValueError, Decimal.InvalidOperation):
            return render(request, 'transfer.html', {'error': 'Invalid amount'})

        with db_transaction.atomic():
            try:
                from_payer = Payer.objects.select_for_update().get(pk=from_payer_id)
                to_payer = Payer.objects.select_for_update().get(pk=to_payer_id)
            except Payer.DoesNotExist:
                return render(request, 'transfer.html', {'error': 'Payer not found'})

            if from_payer.balance < amount:
                return render(request, 'transfer.html', {'error': 'Insufficient funds'})

            from_payer.balance -= amount
            to_payer.balance += amount
            from_payer.save()
            to_payer.save()

            Transaction.objects.create(from_payer=from_payer, to_payer=to_payer, amount=amount)

        cache.delete('payers')
        return redirect('index')

    return render(request, 'transfer.html')

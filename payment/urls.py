from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayerViewSet, PaymentViewSet, TransactionViewSet, index, create_payer, transfer

router = DefaultRouter()
router.register(r'payers', PayerViewSet)
router.register(r'payment', PaymentViewSet, basename='payment')
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('create_payer/', create_payer, name='create_payer'),
    path('transfer/', transfer, name='transfer'),
    path('api/', include(router.urls)),
]

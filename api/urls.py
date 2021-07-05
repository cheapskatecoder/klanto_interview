from django.urls import path
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()

urlpatterns = [
    path('info', views.GetInfo.as_view(), name='info'),
    path('create-link-token', views.CreateLinkToken.as_view(), name='create-link-token'),
    path('set-access-token', views.SetAccessToken.as_view(), name='set-access-token'),
    path('accounts', views.GetAccounts.as_view(), name='accounts'),
    path('auth', views.Auth.as_view(), name='auth'),
    path('transactions', views.Transactions.as_view(), name='transactions'),
    path('balance', views.GetBalance.as_view(), name='get-balance'),
    path('investment-transactions', views.GetInvestementTransaction.as_view(), name='invtestment-transaction'),
    path('buy-item', views.BuyItem.as_view(), name='buy-item'),
    path('plaid-transactions-webhook', views.PlaidTransactionWebhook.as_view(), name='plaid-transactions-webhook'),
]

urlpatterns += router.urls

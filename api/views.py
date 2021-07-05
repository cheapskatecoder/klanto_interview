# Native Imports
import datetime
import logging

# Framework Imports
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import AllowAny

# Third Party Imports
import plaid

# Custom Imports
from utils.utils import GET_PLAID_REDIRECT_URI, GET_CLIENT, format_error, GET_ACCESS_TOKEN
from portal.models import AccessToken, PlaidWebhooksData

access_token = None
payment_id = None

item_id = None
client = GET_CLIENT()
logger = logging.getLogger(__name__)


class GetInfo(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        global access_token
        global item_id
        response = {
            'item_id': item_id,
            'access_token': access_token,
            'products': settings.PLAID_PRODUCTS
        }
        return JsonResponse(response)


class CreateLinkToken(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        try:
            response = client.LinkToken.create(
                {
                    'user': {
                        'client_user_id': 'sahilshukla50'
                    },
                    'client_name': 'Klanto Interview',
                    'products': settings.PLAID_PRODUCTS,
                    'country_codes': settings.PLAID_COUNTRY_CODES,
                    'language': 'en',
                    'redirect_uri': GET_PLAID_REDIRECT_URI(),
                    'webhook': 'https://klantointerview.herokuapp.com/api/v1/plaid-transactions-webhook',
                }
            )
            return JsonResponse(response)
        except plaid.errors.PlaidError as e:
            return JsonResponse(format_error(e))


class SetAccessToken(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        global access_token
        global item_id
        public_token = request.data.get('public_token')

        try:
            exchange_response = client.Item.public_token.exchange(public_token)
        except plaid.errors.PlaidError as e:
            return JsonResponse(format_error(e))

        access_token = exchange_response.get('access_token')
        AccessToken.objects.create(access_token=access_token)
        item_id = exchange_response.get('item_id')
        return JsonResponse(exchange_response)


class GetAccounts(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request):
        try:
            accounts_response = client.Accounts.get(access_token)
            return JsonResponse(accounts_response)
        except plaid.errors.PlaidError as e:
            return JsonResponse(format_error(e))


class Auth(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request):
        try:
            auth_response = client.Auth.get(access_token)
            return JsonResponse(auth_response)
        except plaid.errors.PlaidError as e:
            return JsonResponse(format_error(e))


class Transactions(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request):
        access_token = GET_ACCESS_TOKEN()
        print(access_token)
        start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())

        try:
            transaction_respose = client.Transactions.get(access_token, "2019-07-01", "2021-07-01")
            return JsonResponse(transaction_respose)
        except plaid.errors.PlaidError as e:
            return JsonResponse(format_error(e))



class GetBalance(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        access_token = GET_ACCESS_TOKEN()
        try:
            balance_response = client.Accounts.balance.get(access_token)
            return JsonResponse(balance_response)
        except plaid.errors.PlaidError as e:
            return JsonResponse(format_error(e))


class GetInvestementTransaction(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        access_token = GET_ACCESS_TOKEN()
        start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
        end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
        try:
            investment_transactions_response = client.InvestmentTransactions.get(access_token,
                                                                         start_date,
                                                                         end_date)
            return JsonResponse(investment_transactions_response)
        except plaid.errors.PlaidError as e:
            return JsonResponse(format_error(e))


class BuyItem(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        access_token = GET_ACCESS_TOKEN()
        price = request.data.get('price')
        subtype = request.data.get('subtype')

        try:
            balance_response = client.Accounts.balance.get(access_token)
            for balance in balance_response.get('accounts'):
                print(balance)
                if balance.get('subtype') == subtype:
                    available_balance = balance.get('balances').get('available')
                    if int(available_balance) >= int(price):
                        status = 'can'
                    else:
                        status = 'cant'
                    return JsonResponse({'success': f'You {status} buy this product your {subtype} available balance is {available_balance}', 'balance_response': balance_response})
            return JsonResponse(balance_response)
        except plaid.errors.PlaidError as e:
            return JsonResponse(format_error(e))


class PlaidTransactionWebhook(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        logger.info('\n\n\n\n{}\n\n\n\n'.format(request.data))
        print('\n\n\n\n{}\n\n\n\n'.format(request.data))
        # PlaidWebhooksData.objects.create(json_dump=)
        return JsonResponse({'success': 'success'})


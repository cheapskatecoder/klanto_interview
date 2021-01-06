import datetime
import pickle
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import AllowAny
import plaid
from utils.utils import GET_PLAID_REDIRECT_URI, GET_CLIENT, format_error, GET_ACCESS_TOKEN

# We store the access_token in memory - in production, store it in a secure
# persistent data store.
access_token = None
# The payment_id is only relevant for the UK Payment Initiation product.
# We store the payment_id in memory - in production, store it in a secure
# persistent data store.
payment_id = None

item_id = None
client = GET_CLIENT()


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
                        'client_user_id': 'sahilshukla50@gmail.com' 
                    },
                    'client_name': 'Klanto Interview', 
                    'products': settings.PLAID_PRODUCTS,
                    'country_codes': settings.PLAID_COUNTRY_CODES,
                    'language': 'en',
                    'redirect_uri': GET_PLAID_REDIRECT_URI()
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
        pickle.dump(access_token, open('pickled_file.pkl', 'wb'))
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
            transaction_respose = client.Transactions.get(access_token, start_date, end_date)
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
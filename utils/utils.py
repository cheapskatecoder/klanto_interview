import os
import pickle
from django.conf import settings
import plaid

def GET_PLAID_REDIRECT_URI():
    redirect_uri = os.environ.get('PLAID_REDIRECT_URI')
    if redirect_uri:
        return redirect_uri
    else:
        return None


def GET_CLIENT():
    client = plaid.Client(client_id=settings.PLAID_CLIENT_ID,
                            secret=settings.PLAID_SECRET,
                            environment=settings.PLAID_ENV,
                            api_version='2019-05-29')
    return client 


def GET_ACCESS_TOKEN():
    return pickle.load(open('pickled_file.pkl', 'rb'))

def format_error(e):
  return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type, 'error_message': e.message } }
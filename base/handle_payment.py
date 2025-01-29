import mercadopago
import mercadopago.config
import random
import string
import datetime
import time

import config

sdk = mercadopago.SDK(config.MP_SDK_TOKEN)

def generate_random_string(length = 10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_payment(value):
    unique_key = generate_random_string()
    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': f'{unique_key}'
    }

    expire = datetime.datetime.now() + datetime.timedelta(days=1)
    expire = expire.strftime("%Y-%m-%dT%H:%M:%S.000-03:00").replace("T0", "T")


    payment_data = {
        "transaction_amount": float(value),
        "payment_method_id": 'pix',
        "installments": 1,
        "description": 'Descrição',
        "date_of_expiration": f"{expire}",
        "payer": {
            "email": 'rafaelrossanopo@gmail.com'
        }
    }

    result = sdk.payment().create(payment_data)
    return result, result["response"]


def check_payment(payment_response):
    for _ in range(60):
        id = payment_response['id']
        payer_id = payment_response['payer']['id']
        #status = payment_response['status']

        request = sdk.payment().get(id)
        if request['response']['status'] == 'approved':
            return True

        time.sleep(5)

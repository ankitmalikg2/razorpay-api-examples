import requests
import uuid
from datetime import datetime, timedelta
import json
import constants



def get_time_in_sec_after_mins(mins:int):
    current_time = datetime.now()
    future_time = current_time + timedelta(minutes=mins)
    future_time_seconds = int(future_time.timestamp())
    return future_time_seconds


def create_payment_link(amount:int):

    redirect_url = constants.api_url_payment_create
    ref_id = "jc_"+str(uuid.uuid4())
    url = constants.api_url_payment_fetch_payments
    expire_time = get_time_in_sec_after_mins(constants.payment_url_expire_time) 

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+constants.token_key
    }
    data = {
        "amount": amount * 100,
        "currency": "INR",
        "accept_partial": False,
        "first_min_partial_amount": 0,
        "expire_by": expire_time,
        "reference_id": ref_id,
        "description": "Payment for policy no #6",
        "notes": {
            "policy_name": "policy for Rs "+str(amount)
        },
        "callback_url": redirect_url,
        "callback_method": "get"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to create payment link"


def get_payment_link(payment_link_id):
    url = constants.api_url_payment_fetch_payments + "/" +payment_link_id
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+constants.token_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to get payment link with payment_id"
    
def fetch_all_payment_links():
    url = constants.api_url_payment_fetch_payments
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+constants.token_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to fetch payment link"
    
def cancel_payment_id(payment_link_id):
    url = constants.api_url_payment_fetch_payments +"/"+ payment_link_id + "/cancel"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+constants.token_key
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to cancel payment link"

# Call the method to create the payment link
result = create_payment_link(100)
print( json.dumps(result))
payment_id = result["id"]
print("payment_id - ", payment_id)
print("payment_url - ", result["short_url"])
print()

# # Call the method to cancel the payment link
# cancel_payment_result = cancel_payment_id(payment_id)
# print(json.dumps(cancel_payment_result))
# print()

# # payment_link = "plink_Ob0BhsI5wLsCzk"
# get_payment_link_result = get_payment_link(payment_id)
# print(json.dumps(get_payment_link_result))
# print()

# Call the method to get the payment link
# result = fetch_all_payment_links()
# json_data = json.dumps(result)
# print(json_data)


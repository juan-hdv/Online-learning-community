'''
 ** UTILS
 	Contains general use functions 
 	and Paymemnts functions
'''
import base64
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings

# Converts a python string to Base64 encoding
def str2Base64str (message):
	# Decode/encode converts string2bytes/bytes2string
	# Converts a Python string to Bytes (8 bits groups)
	message_bytes = message.encode('ascii')
	# Converts Bytes (8 bits groups) to base64 bits (6 bits groups)
	base64_bytes = base64.b64encode(message_bytes)
	# Converts base64 bits (6 bits groups) to Base64 String
	base64_message = base64_bytes.decode('ascii')
	return base64_message

# Converts a Base64 encoding to a python string 
def base64str2str (base64_message):
	# Decode/encode converts string2bytes/bytes2string
	# Converts base64 message to base64 bits (6 bits groups)
	base64_bytes = base64_message.encode('ascii')
	# Converts base64 bits (6 bits groups) to Bytes (8 bits groups)
	message_bytes = base64.b64decode(base64_bytes)
	# Converts Bytes (8 bits groups) to Python String
	message = message_bytes.decode('ascii')
	return message


# Paypal Transactions

'''
 paypal_getToken - Request paypal token based on credentials

@Headers = {
	"accept":"" application/json",
	"accept-Language": "en_US",
	"autorization": BASIC base64(client_id:secret)
@data "grant_type=client_credentials"
---------
@returns 
response { 
	"status_code": "<status>" 
	"text" : {
		"scope": "<scope>",
		"access_token": "<Access-Token>",
		"token_type": "Bearer",
		"app_id": "APP-80W284485P519543T",
		"expires_in": 31349,
		"nonce": "<nonce>"
}
'''
def paypal_getToken (url):
	payload = "grant_type=client_credentials"
	autorization = f"{settings.PAYPAL_CLIENTID}:{settings.PAYPAL_SECRET}"
	headers = {
			'content-type': "application/x-www-form-urlencoded",
			'accept': "application/json",
			'accept-language': "en_US",
			'authorization': f"basic {str2Base64str(autorization)}"
			}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response 

'''
 paypal_createOrder - Request paypal create order passing token
 According to: https://www.paypal.com/apex/product-profile/ordersv2/createOrder

@Headers = {
	"accept":"" application/json",
	"accept-Language": "en_US",
	"autorization": "Bearer <token>
@data {
	{ "intent": "CAPTURE",	=> Get the funds inmediatly, not place funds on hold
		"purchase_units": [
			{
				"reference_id": "<REFERENCE-ID>",
				"amount": {
					"currency_code": "<CURRENCY CODE>",
					"value": "<AMMOUNT>"
				}
			}
		],
		"application_context": {
			"return_url": "<return_url>",
			"cancel_url": "<cancel_url>"
      "user_action": PAY_NOW
		}
	}
}
----------
@ returns
response { 
{
	"id": "2FK32148CW025621B",
	"status": "CREATED",
	"links": [
		{
			"href": "https://api.sandbox.paypal.com/v2/checkout/orders/2FK32148CW025621B",
			"rel": "self",
			"method": "GET"
		},
		{
			"href": "https://www.sandbox.paypal.com/checkoutnow?token=2FK32148CW025621B",
			"rel": "approve",
			"method": "GET"
		},
		{
			"href": "https://api.sandbox.paypal.com/v2/checkout/orders/2FK32148CW025621B",
			"rel": "update",
			"method": "PATCH"
		},
		{
			"href": "https://api.sandbox.paypal.com/v2/checkout/orders/2FK32148CW025621B/capture",
			"rel": "capture",
			"method": "POST"
		}
	]
}	
}
'''
def paypal_createOrder (url, token, order):
	payload = """{
		\"intent\": \"CAPTURE\",
		\"purchase_units\": [
			{
				\"reference_id\": \"<REFERENCECODE>\",
				\"amount\": {
					\"currency_code\": \"<CURRENCY>\",
					\"value\": \"<TOTALAMOUNT>\"
				}
			}
		],
		\"application_context\": {
			\"return_url\": \"<URLRETURN>\",
			\"cancel_url\": \"<URLCANCEL>\",
		  \"user_action\": \"PAY_NOW\"
    }
	}"""
	payload = payload.replace('<CURRENCY>','USD')
	payload = payload.replace('<REFERENCECODE>',order["referencecode"])
	payload = payload.replace('<TOTALAMOUNT>',order["totalamount"])
	payload = payload.replace('<URLRETURN>',"https://www.paypal.com/checkoutnow/error") # Deprecated
	payload = payload.replace('<URLCANCEL>',"https://www.paypal.com/checkoutnow/error") # Deprecated

	headers = {
			'accept': "application/json",
			'content-type': "application/json",
			'accept-language': "en_US",
			'authorization': f"Bearer {token}"
			}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response

'''
paypal_captureOrder
Acoording to: https://www.paypal.com/apex/product-profile/ordersv2/capturePayment

@headers = {
		'content-type': "application/json",
		'authorization': "Bearer <token>"
		}
----------
@ return
{
	"id": "7BG24496EL109023T",
	"status": "COMPLETED",
	"purchase_units": [
		{
			"reference_id": "PUHF",
			"shipping": {
				"name": {
					"full_name": "Jhon Buy"
				},
				"address": {
					"address_line_1": "Wall Street",
					...
				}
			},
			"payments": {
				"captures": [
					{
						"id": "78L07006DG807322X",
						"status": "COMPLETED",
						"amount": {
							"currency_code": "USD",
							"value": "200.00"
						},
						"final_capture": true,
						"seller_protection": {
							"status": "ELIGIBLE",
							"dispute_categories": [
								"ITEM_NOT_RECEIVED",
								"UNAUTHORIZED_TRANSACTION"
							]
						},
						"seller_receivable_breakdown": {
							"gross_amount": {
								"currency_code": "USD",
								"value": "200.00"
							},
							"paypal_fee": {
								"currency_code": "USD",
								"value": "11.10"
							},
							"net_amount": {
								"currency_code": "USD",
								"value": "188.90"
							}
						},
						"links": [
							{
								"href": "https://api.sandbox.paypal.com/v2/payments/captures/78L07006DG807322X",
								"rel": "self",
								"method": "GET"
							},
							{
								"href": "https://api.sandbox.paypal.com/v2/payments/captures/78L07006DG807322X/refund",
								"rel": "refund",
								"method": "POST"
							},
							{
								"href": "https://api.sandbox.paypal.com/v2/checkout/orders/7BG24496EL109023T",
								"rel": "up",
								"method": "GET"
							}
						],
						"create_time": "2020-08-13T00:01:33Z",
						"update_time": "2020-08-13T00:01:33Z"
					}
				]
			}
		}
	],
	"payer": {
		"name": {
			"given_name": "Jhon",
			"surname": "Buy"
		},
		"email_address": "juanhdv@gmail.com",
		"payer_id": "MRWGJRXX3S6TL",
		"address": {
			"country_code": "US"
		}
	},
	"links": [
		{
			"href": "https://api.sandbox.paypal.com/v2/checkout/orders/7BG24496EL109023T",
			"rel": "self",
			"method": "GET"
		}
	]
}
'''
def paypal_captureOrder (url, token):
	headers = {
			'content-type': "application/json",
			'authorization': f"Bearer {token}",
			}
	response = requests.request("POST", url, headers=headers)
	return response


'''
paypal_showDetailsOrder
@headers = {
	'content-type': "application/json",
	'authorization': "Bearer <token>
	}
---------
@return
{
	"id": "7BG24496EL109023T",
	"intent": "CAPTURE",
	"status": "COMPLETED",
	"purchase_units": [
		{
			"reference_id": "PUHF",
			"amount": {
				"currency_code": "USD",
				"value": "200.00",
				"breakdown": {
					"item_total": {
						"currency_code": "USD",
						"value": "180.00"
					},
					"shipping": {
						"currency_code": "USD",
						"value": "20.00"
					}
				}
			},
			"payee": {
				"email_address": "sb-h18c02863411@business.example.com",
				"merchant_id": "CBECU7AF2H4DA"
			},
			"soft_descriptor": "PAYPAL *JOHNDOESTES",
			"shipping": {
				"name": {
					"full_name": "Jhon Buy"
				},
				"address": {
					"address_line_1": "Wall Street",
					"address_line_2": "1,2,3",
					"admin_area_2": "New York",
					"admin_area_1": "NY",
					"postal_code": "03521",
					"country_code": "US"
				}
			},
			"payments": {
				"captures": [
					{
						"id": "78L07006DG807322X",
						"status": "COMPLETED",
						"amount": {
							"currency_code": "USD",
							"value": "200.00"
						},
						"final_capture": true,
						"seller_protection": {
							"status": "ELIGIBLE",
							"dispute_categories": [
								"ITEM_NOT_RECEIVED",
								"UNAUTHORIZED_TRANSACTION"
							]
						},
						"seller_receivable_breakdown": {
							"gross_amount": {
								"currency_code": "USD",
								"value": "200.00"
							},
							"paypal_fee": {
								"currency_code": "USD",
								"value": "11.10"
							},
							"net_amount": {
								"currency_code": "USD",
								"value": "188.90"
							}
						},
						"links": [
							{
								"href": "https://api.sandbox.paypal.com/v2/payments/captures/78L07006DG807322X",
								"rel": "self",
								"method": "GET"
							},
							{
								"href": "https://api.sandbox.paypal.com/v2/payments/captures/78L07006DG807322X/refund",
								"rel": "refund",
								"method": "POST"
							},
							{
								"href": "https://api.sandbox.paypal.com/v2/checkout/orders/7BG24496EL109023T",
								"rel": "up",
								"method": "GET"
							}
						],
						"create_time": "2020-08-13T00:01:33Z",
						"update_time": "2020-08-13T00:01:33Z"
					}
				]
			}
		}
	],
	"payer": {
		"name": {
			"given_name": "Jhon",
			"surname": "Buy"
		},
		"email_address": "juanhdv@gmail.com",
		"payer_id": "MRWGJRXX3S6TL",
		"address": {
			"country_code": "US"
		}
	},
	"create_time": "2020-08-12T23:47:11Z",
	"update_time": "2020-08-13T00:01:33Z",
	"links": [
		{
			"href": "https://api.sandbox.paypal.com/v2/checkout/orders/7BG24496EL109023T",
			"rel": "self",
			"method": "GET"
		}
	]
}
'''
def paypal_showDetailsOrder (url, token):
	headers = {
		'content-type': "application/json",
		'authorization': f"Bearer {token}",
			}
	response = requests.request("GET", url, headers=headers)
	return response

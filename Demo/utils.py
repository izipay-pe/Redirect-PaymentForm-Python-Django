import hashlib
import time
import hmac
import base64
from Keys.keys import keys
from datetime import datetime

def dataForm(parameters):
    newParams = {
        "vads_action_mode": "INTERACTIVE",
        "vads_amount": str(int(float(parameters["amount"]) * 100)),  # Monto * 100
        "vads_ctx_mode": "TEST",  # TEST o PRODUCTION
        "vads_currency": "604" if parameters["currency"] == "PEN" else "840",  # Código ISO 4217
        "vads_cust_address": parameters["address"],
        "vads_cust_city": parameters["city"],
        "vads_cust_country": parameters["country"],
        "vads_cust_email": parameters["email"],
        "vads_cust_first_name": parameters["firstName"],
        "vads_cust_last_name": parameters["lastName"],
        "vads_cust_national_id": parameters["identityCode"],
        "vads_cust_phone": parameters["phoneNumber"],
        "vads_cust_state": parameters["state"],
        "vads_cust_zip": parameters["zipCode"],
        "vads_order_id": parameters["orderId"],
        "vads_page_action": "PAYMENT",
        "vads_payment_config": "SINGLE",
        "vads_redirect_success_timeout": "5",
        "vads_return_mode": "POST",
        "vads_site_id": keys["SHOP_ID"],
        "vads_trans_date": datetime.utcnow().strftime('%Y%m%d%H%M%S'),  # Fecha en formato UTC
        "vads_trans_id": str(int(time.time()) % 1000000),  # ID de transacción único
        "vads_url_return": 'http://localhost:8000/result',  # URL de retorno
        "vads_version": "V2"
    }
    
    #Calcular la firma
    newParams["signature"] = calculateSignature(newParams, keys["KEY"])
    return newParams

def calculateSignature(parameters, key):
    content_signature = ""
    #Ordenar los campos alfabéticamente
    sorted_params = sorted(parameters.items(), key=lambda x: x[0])
    for name, value in sorted_params:
        if name.startswith('vads_'):
            content_signature += value + "+"
    #Añadir la clave al final del string
    content_signature += key
    hash_object = hmac.new(key.encode('utf-8'), content_signature.encode('utf-8'), hashlib.sha256)
    #Codificación base64 del string cifrada con el algoritmo HMAC-SHA-256
    signature = base64.b64encode(hash_object.digest()).decode('utf-8')
    return signature

def checkSignature(parameters):
    signature = parameters["signature"]
    return signature == calculateSignature(parameters, keys["KEY"])
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import base64
import time
from django.http import HttpResponse
import hashlib
import hmac
from Demo.configKey import SHOP_ID, MODE, KEY, URL_IZIPAY


def get_signature(params, keys):
    content_signature = ""
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    for name, value in sorted_params:
        if name.startswith('vads_'):
            content_signature += value + "+"
    content_signature += keys
    hash_object = hmac.new(keys.encode('utf-8'), content_signature.encode('utf-8'), hashlib.sha256)
    signature = base64.b64encode(hash_object.digest()).decode('utf-8')
    return signature


def home(request):
    order = datetime.now().strftime("Order-%Y%m%d%H%M%S")
    return render(request,'home.html', {"order": order})


def redirect(request):

    data = {
        "vads_action_mode": "INTERACTIVE",
        "vads_amount": str(int(request.POST.get('amount')) * 100),
        "vads_ctx_mode": MODE,
        "vads_currency": "604",  # Moneda PEN
        "vads_cust_email": request.POST.get('email'),
        "vads_page_action": "PAYMENT",
        "vads_payment_config": "SINGLE",
        "vads_site_id": SHOP_ID,
        "vads_url_success": "http://127.0.0.1:8000/result",
        "vads_return_mode": "POST",
        "vads_trans_date": datetime.utcnow().strftime('%Y%m%d%H%M%S'),
        "vads_trans_id": str(int(time.time()) % 1000000),
        "vads_version": "V2",
        "vads_order_id": request.POST.get('order'),
        "vads_redirect_success_timeout": str(5)
    }

    return render(request, 'Demo/redirect.html', {"redirect": data, "url_izipay": URL_IZIPAY, "signature": get_signature(data, KEY)})


@csrf_exempt
def paidResult(request):

    vadsResult = request.POST.get("vads_result")
    vadsTransStatus = request.POST.get("vads_trans_status")
    vadsAmount = request.POST.get("vads_amount")
    vadsOrder = request.POST.get("vads_order_id")

    return render(request, "Demo/result.html", {'result': vadsResult, 'status': vadsTransStatus, 'monto': int(vadsAmount)/100, 'order': vadsOrder})

@csrf_exempt
def ipn(request):
    signature = request.POST.get("signature")

    print("IPN")
    print(request.POST)
    print("Signature: " + signature)

    if signature == get_signature(request.POST, KEY):
        return HttpResponse('Correcto', status=200)
    else:
        return HttpResponse('Acceso denegado', status=500)
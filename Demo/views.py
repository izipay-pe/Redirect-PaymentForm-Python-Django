from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import hmac
from django.http import HttpResponse
from .utils import dataForm, checkSignature 

def index(request):
    return render(request,'Demo/index.html')

def checkout(request):
    parameters = dataForm(request.POST)
    return render(request, 'Demo/checkout.html', {'parameters': parameters, "amount": request.POST["amount"], "currency": request.POST["currency"]})

@csrf_exempt
def result(request):
    if not request.POST: 
        raise Exception("No post data received!")

    #Validación de firma
    if not checkSignature(request.POST):
        raise Exception("Invalid signature")

    #Mostrar datos de pago
    answer = request.POST
    vads_amount = round(float(answer["vads_amount"]) / 100, 2)
    vads_currency = "PEN" if answer["vads_currency"] == "604" else "USD"
    postData = json.dumps(request.POST, indent=4)

    return render(request, 'Demo/result.html', {'answer': answer, 'vads_amount': vads_amount, 'vads_currency': vads_currency, 'postData': postData})

@csrf_exempt
def ipn(request):
    if not request.POST: 
        raise Exception("No post data received!")

    #Validación de firma en IPN
    if not checkSignature(request.POST) : 
        raise Exception("Invalid signature")

    #Verificar orderStatus: AUTHORISED
    orderStatus = request.POST["vads_trans_status"]
    orderId = request.POST["vads_order_id"]
    transactionUuid = request.POST["vads_trans_uuid"]

    return HttpResponse(status=200, content=f"OK! OrderStatus is {orderStatus} ")

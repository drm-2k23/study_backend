from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import hashlib
import hmac
import time
from django.views.decorators.http import require_POST
import requests
import json
from django.middleware.common import CommonMiddleware
from django.utils.decorators import decorator_from_middleware
from corsheaders.middleware import CorsMiddleware


class WebhookView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        secret_token = hmac.new(b'YOUR_SECRET_TOKEN', request.GET['msg'].encode(
            'utf-8'), hashlib.sha256).hexdigest().lower()
        response = JsonResponse({
            'secret_token': secret_token
        })
        return (response)

    def post(self, request, *args, **kwargs):
        return HttpResponse("Successful Webhook Delivery", status=200)
    
    def put(self, request, *args, **kwargs):
        delivery_id = request.POST.get("delivery_id", None)
        authorization_token = request.META.get("HTTP_AUTHORIZATION")
        payload = {'delivery_id': delivery_id}
        headers = {
        'Authorization': authorization_token,
        }
        url = "https://app.dev.drchrono.com/pub_api/update_delivery_status/"
        response = requests.request("POST", url, headers=headers, data=payload, timeout=(5,120), verify=False)
        print(response.json())

        return json.render({"detail": "Unable to update delivery data"}, status=400)

class WebhookViewTwentySec(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        secret_token = hmac.new(b'YOUR_SECRET_TOKEN', request.GET['msg'].encode(
            'utf-8'), hashlib.sha256).hexdigest().lower()
        response = JsonResponse({
            'secret_token': secret_token
        })
        return (response)

    def post(self, request, *args, **kwargs):
        time.sleep(20)
        return HttpResponse("Successful Webhook Delivery", status=200)
    

class WebhookViewTensec(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        secret_token = hmac.new(b'YOUR_SECRET_TOKEN', request.GET['msg'].encode(
            'utf-8'), hashlib.sha256).hexdigest().lower()
        response = JsonResponse({
            'secret_token': secret_token
        })
        return (response)

    def post(self, request, *args, **kwargs):
        time.sleep(10)
        return HttpResponse("Successful Webhook Delivery", status=200)
    

class WebhookViewThirtySec(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        secret_token = hmac.new(b'YOUR_SECRET_TOKEN', request.GET['msg'].encode(
            'utf-8'), hashlib.sha256).hexdigest().lower()
        response = JsonResponse({
            'secret_token': secret_token
        })
        return (response)

    def post(self, request, *args, **kwargs):
        time.sleep(35)
        return HttpResponse("Successful Webhook Delivery", status=200)
    



def home(request):
    return HttpResponse('Webhook Home Page')

@decorator_from_middleware(CorsMiddleware)
@decorator_from_middleware(CommonMiddleware)
@csrf_exempt
@require_POST
def webhook_api_test(request):
    delivery_id = request.POST.get("delivery_id", None)
    authorization_token = request.META.get("HTTP_AUTHORIZATION")
    payload = {'delivery_id': delivery_id}
    headers = {
    'Authorization': authorization_token,
    }
    url =  "https://app.dev.drchrono.com/pub_api/update_delivery_status/"
    response = requests.request("POST", url, headers=headers, data=payload, timeout=(5,120), verify=False)
    print(response.json())

    return  JsonResponse({
            'detail': "successfull"
        }, success=200)
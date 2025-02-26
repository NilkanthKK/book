# Django Imports
import base64
import hashlib
import hmac
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings

# Django REST Framework Imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Third-Party Libraries
import json
import xmltodict
from dicttoxml import dicttoxml


from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from django.utils.html import strip_tags
from rest_framework.decorators import api_view
from email.utils import formataddr


# Create your views here.

@api_view(['POST'])
def xml_to_json(request):
    try:
        xml_data = request.body.decode('utf-8') 
        json_data = xmltodict.parse(xml_data) 

        return JsonResponse({'status': 'success', 'message': 'Data converted successfully', 'data': json_data}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@api_view(['POST'])
def json_to_xml(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))  

        xml_data = dicttoxml(json_data, attr_type=False)
        xml_str = xml_data.decode('utf-8')  

        return HttpResponse(xml_str, content_type='application/xml')  
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

@api_view(['POST'])
def send_notificationn(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    recipient_email = request.data.get('email')

    if not subject or not message or not recipient_email:
        return JsonResponse({'status': 'error', 'message': 'Subject, message, and recipient email are required.'}, status=400)

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient_email],
            fail_silently=False
        )
        return JsonResponse({'status': 'success', 'message': 'Email sent successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)
    


from email.utils import formataddr
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse
from django.utils.html import strip_tags

@api_view(['POST'])
def send_notification(request):
    subject = 'Verify Code for Email Verification'
    otp = request.data.get('otp')  
    recipient_email = request.data.get('email')

    if not otp or not recipient_email:
        return JsonResponse({'status': 'error', 'message': 'OTP and recipient email are required.'}, status=400)

    # HTML content
    html_content = """
        <html>
        <head></head>
        <body>
            <p>Dear User,</p>
            <p>Your OTP for Email Verification is: {otp}</p>
            <p>Please make sure to keep it confidential.</p>
            <p>This is an automated message. Please do not reply to this email, as replies are not monitored.</p>
            <p>If you have any questions, please contact our support team via our official website.</p>
            <p>Best regards,<br>TCPL</p>
        </body>
        </html>
    """.format(otp=otp)

    text_content = strip_tags(html_content)

    try:
        # Use a display name with a no-reply email address
        sender_email = formataddr(('No Reply', 'noreply@yourdomain.com'))

        # Create the email object
        email_message = EmailMultiAlternatives(
            subject, 
            text_content, 
            sender_email,  
            [recipient_email]
        )
        # Attach the HTML version of the email
        email_message.attach_alternative(html_content, "text/html")
        email_message.extra_headers = {
            'Auto-Submitted': 'auto-generated',
            'Precedence': 'bulk',
        }
        email_message.send(fail_silently=False)

        return JsonResponse({'status': 'success', 'message': 'Email sent successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)



 #==================================================BBPS===========================================================  

# Django REST Framework Imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Standard Library Imports
import xml.etree.ElementTree as ET

# Third-Party Libraries
import requests


api_key = ''  
merchant_id = ''
biller_id = ''
    

def dict_to_xml(tag, d):
    element = ET.Element(tag)
    for key, val in d.items():
        child = ET.SubElement(element, key)
        child.text = str(val)
    return ET.tostring(element, encoding='utf-8', method='xml')

# Biller MDM Request
@api_view(['POST'])
def biller_mdm_request(request):
    merchant_id = request.data.get('merchant_id')
    biller_id = request.data.get('biller_id')

    if not merchant_id or not biller_id:
        return Response({'status': 'failed', 'message': 'Merchant ID and Biller ID are required.'}, status=400)

    url = "https://api.billavenue.com/billpay/extMdmCntrl/mdmRequestNew/xml"

    headers = {
        'Content-Type': 'application/xml',
        'API-Key': api_key
    }

    mdm_data = {
        'merchantId': merchant_id,
        'billerId': biller_id,
        'type': 'MDM'
    }

    xml_data = dict_to_xml('Request', mdm_data)

    try:
        response = requests.post(url, headers=headers, data=xml_data)

        if response.status_code == 200:
            return Response({'status': 'success','message': 'MDM data fetched successfully.','data': response.text}, status=200)
        else:
            return Response({'status': 'failed','message': 'Failed to fetch MDM data from the server.','data': response.text}, status=response.status_code)

    except Exception as e:
        return Response({'status': 'failed','message': 'An error occurred while making the request.','error': str(e)}, status=500)

# Bill Fetch Request
@api_view(['POST'])
def bill_fetch_request(request):
    customer_id = request.data.get('customer_id')

    if not customer_id:
        return response({'status': 'failed', 'message':  'Customer ID is required.'}, status=400)
    
    url = "https://api.billavenue.com/billpay/extBillCntrl/billFetchRequest/xml"

    bill_fetch_data = {
        'merchantId': merchant_id,
        'billerId': biller_id,
        'customerId': customer_id
    }

    xml_data = dict_to_xml('BillFetchRequest', bill_fetch_data)

    headers = {
        'Content-Type': 'application/xml',
        'API-Key': api_key
    }

    try:
        response = requests.post(url, headers=headers, data=xml_data)

        if response.status_code == 200:
            return response({'status': 'success', 'message': 'Bill fetched successfully.', 'data': response.text}, status=200)
        else:
            return response({'status': 'failed', 'message': 'Failed to fetch bill from the server.', 'data': response.text}, status=response.status_code)
        
    except Exception as e:
        return response({'status': 'failed', 'message':  str(e)}, status=500)
    
# Bill Payment Request
@api_view(['POST'])
def bill_payment_request(request):
    customer_id = request.data.get('customer_id')
    amount = request.data.get('amount')
    payment_mode = request.data.get('payment_mode')

    if not customer_id or not amount or not payment_mode:
        return response({'status': 'failed', 'message': 'Customer ID, Amount, and Payment Mode are required.'}, status=400)

    url = "https://api.billavenue.com/billpay/extBillPayCntrl/billPayRequest/xml"

    headers = {
        'Content-Type': 'application/xml',
        'API-Key': api_key
    }

    payment_data = {
        'merchantId': merchant_id,
        'billerId': biller_id,
        'customerId': customer_id,
        'amount': amount,
        'paymentMode': payment_mode
    }

    xml_data = dict_to_xml('BillPaymentRequest', payment_data)

    try:
        response = requests.post(url, headers=headers, data=xml_data)

        if response.status_code == 200:
            return response({'status': 'success', 'message': 'Bill payment request sent successfully.', 'data': response.text}, status=200)
        else:
            return response({'status': 'failed', 'message': 'Failed to send bill payment request.', 'data': response.text}, status=response.status_code)
        
    except Exception as e:
        return response({'status': 'failed', 'message': str(e)}, status=500)
    

# Complaint Registration Request
@api_view(['POST'])
def complaint_registration_request(request):
    customer_id = request.data.get('customer_id')
    complaint_description = request.data.get('complaint_description')

    if not customer_id or not complaint_description:
        return response({'status': 'failed', 'message': 'Customer ID and Complaint Description are required.'}, status=400)

    url = "https://api.billavenue.com/billpay/extComplaints/register/xml"

    headers = {
        'Content-Type': 'application/xml',
        'API-Key': api_key
    }

    complaint_data = {
        'merchantId': merchant_id,
        'billerId': biller_id,
        'customerId': customer_id,
        'complaintDescription': complaint_description
    }

    xml_data = dict_to_xml('ComplaintRegisterRequest', complaint_data)

    try:
        response = requests.post(url, headers=headers, data=xml_data)

        if response.status_code == 200:
            return response({'status': 'success', 'message': 'Complaint registration request sent successfully.', 'data': response.text}, status=200)
        else:
            return response({'status': 'failed', 'message': 'Failed to send complaint registration request.', 'data': response.text}, status=response.status_code)
        
    except Exception as e:
        return response({'status': 'failed', 'message': str(e)}, status=500)


# Complaint Tracking Request
@api_view(['POST'])
def complaint_tracking_request(request):
    complaint_id = request.data.get('complaint_id')

    if not complaint_id:
        return response({'status': 'failed', 'message': 'Complaint ID is required.'}, status=400)

    url = "https://api.billavenue.com/billpay/extComplaints/track/xml"

    headers = {
        'Content-Type': 'application/xml',
        'API-Key': api_key
    }

    tracking_data = {
        'merchantId': merchant_id,
        'billerId': biller_id,
        'complaintId': complaint_id
    }

    xml_data = dict_to_xml('ComplaintTrackingRequest', tracking_data)

    try:
        response = requests.post(url, headers=headers, data=xml_data)

        if response.status_code == 200:
            return response({'status': 'success', 'message': 'Complaint tracking request sent successfully.', 'data': response.text}, status=200)
        else:
            return response({'status': 'failed', 'message': 'Failed to send complaint tracking request.', 'data': response.text}, status=response.status_code)
        
    except Exception as e:
        return response({'status': 'failed', 'message': str(e)}, status=500)
    

# Transaction Status Request
@api_view(['POST'])
def transaction_status_request(request):
    transaction_id = request.data.get('transaction_id')

    if not transaction_id:
        return response({'status': 'failed', 'message': 'Transaction ID is required.'}, status=400)

    url = "https://api.billavenue.com/billpay/transactionStatus/fetchInfo/xml"

    headers = {
        'Content-Type': 'application/xml',
        'API-Key': api_key
    }

    status_data = {
        'merchantId': merchant_id,
        'transactionId': transaction_id
    }

    xml_data = dict_to_xml('TransactionStatusRequest', status_data)

    try:
        response = requests.post(url, headers=headers, data=xml_data)

        if response.status_code == 200:
            return response({'status': 'success', 'message': 'Transaction status request sent successfully.', 'data': response.text}, status=200)
        else:
            return response({'status': 'failed', 'message': 'Failed to send transaction status request.', 'data': response.text}, status=response.status_code)
        
    except Exception as e:
        return response({'status': 'failed', 'message': str(e)}, status=500)
    
    
# Deposit Enquiry Request
@api_view(['POST'])
def deposit_enquiry_request(request):
    url = "https://api.billavenue.com/billpay/enquireDeposit/fetchDetails/xml"
    headers = {
        'Content-Type': 'application/xml',
        'API-Key': api_key
    }
    data = {
        'merchantId': merchant_id
    }
    xml_data = dict_to_xml('DepositEnquiryRequest', data)
    try:
        response = requests.post(url, headers=headers, data=xml_data)
        if response.status_code == 200:
            return response({'status': 'success', 'message': 'Deposit Enquiry request sent successfully.', 'data': response.text}, status=200)
        else:
            return response({'status': 'failed', 'message': 'Failed to send Deposit Enquiry request.', 'data': response.text}, status=response.status_code)
    except Exception as e:
        return response({'status': 'failed', 'message': str(e)}, status=500)


# Bill Validation Request
@api_view(['POST'])
def bill_validation_request(request):
    customer_id = request.data.get('customer_id')
    bill_id = request.data.get('bill_id')

    if not customer_id or not bill_id:
        return response({'status': 'failed', 'message': 'Customer ID and Bill ID are required.'}, status=400)

    url = "https://api.billavenue.com/billpay/extBillValCntrl/billValidationRequest/xml"
    
    headers = {
        'Content-Type': 'application/xml',
        'API-Key': api_key
    }
    data = {
        'merchantId': merchant_id,
        'billerId': biller_id,
        'customerId': customer_id,
        'billId': bill_id
    }
    xml_data = dict_to_xml('BillValidationRequest', data)

    try:
        response = requests.post(url, headers=headers, data=xml_data)

        if response.status_code == 200:
            return response({'status': 'success', 'message': 'Bill Validation request sent successfully.', 'data': response.text}, status=200)
        else:
            return response({'status': 'failed', 'message': 'Failed to send Bill Validation request.', 'data': response.text}, status=response.status_code)
    except Exception as e:
        return response({'status': 'failed', 'message': str(e)}, status=500)

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

x_client_id = "TEST379597698355e9f49312abcff4795973"
x_client_secret = "TESTa85244521ed3349dcf149da1a167e666eab9ce93"

@api_view(['GET'])
def get_webhook_status(request):
    transfer_id = request.data.get('transfer_id')  
    url = f"https://test.cashfree.com/api/v1/payouts/status/{transfer_id}"

    headers = {
        "x-client-id": x_client_id, 
        "x-client-secret": x_client_secret  
    }

    try:
        response = requests.get(url, headers=headers)
        print(response.text)
        data = response.json()
        
        if response.status_code == 200:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unable to fetch status"}, status=response.status_code)
    
    except Exception as e:  
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get(self, request, transfer_id):
    url = f"https://test.cashfree.com/api/v1/payouts/status/{transfer_id}"
    headers = {
        "x-client-id": self.x_client_id,
        "x-client-secret": self.x_client_secret
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unable to fetch status"}, status=response.status_code)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Webhooks(APIView):

    def post(self, request):
        action = request.data.get('action')

        if action == 'TRANSFER_SUCCESS':
            return self.transfer_success(request)
        else:
            return Response({"error": "Invalid action specified"}, status=status.HTTP_400_BAD_REQUEST)

    def transfer_success(self, request):
        payload = {
            "event": request.data.get('event'),
            "amount": request.data.get('amount'),
            "vAccountId": request.data.get('vAccountId'),
            "referenceId": request.data.get('referenceId'),
            "paymentTime": request.data.get('paymentTime'),
            "remitterName": request.data.get('remitterName'),
            "remitterVpa": request.data.get('remitterVpa'),
            "received_signature": request.data.get('signature', '')
        }

     
        if not self.verify_signature(request):
            return Response({"error": "Signature verification failed"}, status=status.HTTP_400_BAD_REQUEST)

      
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-api-version': '2023-08-01',
            'x-client-id': 'CF10200215CQOS9TNPU07S7391HH9G',
            'x-client-secret': 'cfsk_ma_test_b68698459f24796a6d655dd514e9b1b1_5180673a',
        }
        url = "https://payout-gamma.cashfree.com/payout/v1.2/transfer_success"

        try:
            response = requests.get(url, json=payload,headers=headers)

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response(response.json(), status=response.status_code)

        except requests.RequestException as e:
            return Response(
                {"error": f"Error while calling Cashfree API: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def verify_signature(self, request):
     
        raw_body = request.body  
        timestamp = request.headers.get('x-webhook-timestamp')


        payload = raw_body.decode('utf-8')

   
        signature_data = f"{timestamp}{payload}"
        message = bytes(signature_data, 'utf-8')

        
        secret_key = bytes("Secret_Key", 'utf-8')  

       
        computed_signature = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        computed_signature_str = computed_signature.decode('utf-8')


        received_signature = request.headers.get('x-webhook-signature', '')

       
        return hmac.compare_digest(computed_signature_str, received_signature)
    




#=================================================================================

import requests
import xml.etree.ElementTree as ET

BILLER_INFO_URL = "https://stgapi.billavenue.com/billpay/extMdmCntrl/mdmRequestNew/"
BILL_FETCH_URL = "https://stgapi.billavenue.com/billpay/extBillCntrl/billFetchRequest/xml"
BILL_PAYMENT_URL = "https://stgapi.billavenue.com/billpay/extBillPayCntrl/billPayRequest/xml"
TRANSACTION_STATUS_URL = "https://stgapi.billavenue.com/billpay/transactionStatus/fetchInfo/xml"
COMPLAINT_REGISTRATION_URL = "https://stgapi.billavenue.com/billpay/extComplaints/register/xml"
COMPLAINT_TRACKING_URL = "https://stgapi.billavenue.com/billpay/extComplaints/track/xml"
VALIDATION_URL = "https://stgapi.billavenue.com/billpay/extBillValCntrl/billValidationRequest/xml"
BALANCE_CHECK_URL = "https://stgapi.billavenue.com/billpay/enquireDeposit/fetchDetails/xml"

headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
}

def create_sample_xml_request(data):
    root = ET.Element('Request')
    for key, value in data.items():
        element = ET.SubElement(root, key)
        element.text = str(value)
    return ET.tostring(root, encoding='utf-8')

def bill_fetch_requestt(biller_id, customer_id):
    data = {
        'BillerId': biller_id,
        'CustomerId': customer_id
    }
    xml_data = create_sample_xml_request(data)
    response = requests.post(BILL_FETCH_URL, data=xml_data, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return {'error': 'API call failed', 'status_code': response.status_code}

def transaction_status_requestt(transaction_id):
    data = {
        'TransactionId': transaction_id
    }
    xml_data = create_sample_xml_request(data)
    response = requests.post(TRANSACTION_STATUS_URL, data=xml_data, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return {'error': 'API call failed', 'status_code': response.status_code}




@api_view(['GET'])
def fetch_bill_view(request):
    biller_id = request.data.get('biller_id')
    customer_id = request.data.get('customer_id')

    if biller_id and customer_id:
        response = bill_fetch_requestt(biller_id, customer_id)
        return JsonResponse({'status': 'success','message': 'Bill fetched successfully','response': response}, status=200)
    else:
        return JsonResponse({'status': 'failed','message': 'Missing required parameters'}, status=400)

@api_view(['GET'])
def transaction_status_view(request):
    transaction_id = request.data.get('transaction_id')

    if transaction_id:
        response = transaction_status_requestt(transaction_id)
        return JsonResponse({'status': 'success','message': 'Transaction status fetched successfully','response': response})
    else:
        return JsonResponse({'status': 'failed','message': 'Missing transaction_id'}, status=400)


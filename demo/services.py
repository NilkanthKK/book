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

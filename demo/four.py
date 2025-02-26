# from cashfree_sdk import Cashfree

# app_id = 'YOUR_APP_ID'  # Replace with your app ID
# secret_key = 'YOUR_SECRET_KEY'  # Replace with your secret key

# Cashfree.init(app_id, secret_key)

# # Webhook data
# webhook_data = '{"cashgramId": "5b8283182e0711eaa4c531df6a4f439b-28", "event": "CASHGRAM_EXPIRED", "eventTime": "2020-01-03 15:01:06", "reason": "OTP_ATTEMPTS_EXCEEDED", "signature": "TBpM+4nr1DsWsov7QiHSTfRJP4Z9BD8XrDgEhBlf9ss="}'

# # Verify the webhook
# try:
#     verification_result = Cashfree.verification.verify_webhook(webhook_data, 'JSON')
#     print(verification_result)
# except Exception as e:
#     print(f"Error verifying webhook: {e}")
# Cashfree Credentials KEYS
x_client_id = "TEST379597698355e9f49312abcff4795973"
x_client_secret = "TESTa85244521ed3349dcf149da1a167e666eab9ce93"

import hmac
import hashlib
import base64
import json

class PayoutWebhookEvent:
    def __init__(self, event_type, raw_body, obj):
        self.type = event_type
        self.raw = raw_body
        self.object = obj

class Cashfree:
    X_CLIENT_SECRET = x_client_secret  
    X_API_VERSION = "2024-01-01"

    @staticmethod
    def payout_verify_webhook_signature(signature, raw_body, timestamp):
        body = timestamp + raw_body
        secret_key = Cashfree.X_CLIENT_SECRET
        generated_signature = base64.b64encode(
            hmac.new(secret_key.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
        ).decode('utf-8')
        print(generated_signature)
        print(signature)
        if generated_signature == signature:
            json_object = json.loads(raw_body)
            return PayoutWebhookEvent(json_object['type'], raw_body, json_object)
        
        raise ValueError("Generated signature and received signature did not match.")

# Example usage:
# Replace these placeholders with actual values received from the webhook
received_signature = "HLxP9rjjFLIfuRPWFac2ayNVzhK/zRh0a6q5TGTCoCc="
raw_body = '{"type":"payment","data":{"amount":100}}'  # Example raw body (JSON string)
received_timestamp = "1690000000"  # Example timestamp as a string

try:
    event = Cashfree.payout_verify_webhook_signature(received_signature, raw_body, received_timestamp)
    print("Webhook verified successfully:", event.type, event.raw)
except ValueError as e:
    print("Error verifying webhook:", e)

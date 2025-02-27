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
 
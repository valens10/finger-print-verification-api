from django.urls import path
from .views import *

urlpatterns = [
    path('enroll_finger_print', enroll_fingerprint, name='enroll_finger_print'),
    path('verify_finger_print', verify_fingerprint, name='verify_finger_print'),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('enroll_user_fingerprint', enroll_user_fingerprint, name='enroll_user_fingerprint'),
    path('verify_user_fingerprint', verify_user_fingerprint, name='verify_user_fingerprint'),
    
    path('enroll_client_fingerprint', enroll_client_fingerprint, name='enroll_client_fingerprint'),
    path('verify_client_fingerprint', verify_client_fingerprint, name='verify_client_fingerprint'),
    
    path('get_client_fingerprint_data/<slug:client_id>', get_client_fingerprint_data, name='get_client_fingerprint_data'),
    path('get_user_fingerprint_data/<slug:user_id>', get_user_fingerprint_data, name='get_user_fingerprint_data'),
]

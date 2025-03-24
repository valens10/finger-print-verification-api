from django.db import models
from django.contrib.auth.models import User
import uuid

class Fingerprint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID as primary key
    user_id = models.CharField(max_length=50, null=True, unique=True, blank=True)  # Link to a quantum user
    template = models.BinaryField(null=True, blank=True)  # Store fingerprint data as binary
    created_at = models.DateTimeField(auto_now_add=True)
    is_client = models.BooleanField(default=False)
    client_id = models.CharField(max_length=40, blank=True, null=True)
    created_by = models.CharField(max_length=50, null=True, blank=True) # TODO current user login
    

    def __str__(self):
        return f"Fingerprint for {self.id}"
    
    class Meta:
        db_table = 'tb_finger_print'
        default_permissions = ()

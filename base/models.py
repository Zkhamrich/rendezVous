from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Appointment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="appointments")
    title = models.CharField(max_length=225)
    description = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending')
    def __str__(self):
        return f"Appointment for {self.user.username} - {self.title}"
    
    class Meta:
        ordering = ['start_time']
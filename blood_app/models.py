from django.db import models
from django.conf import settings

#  ===============Blood Request Section================
class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Accepted','Accepted'),
    ]
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests_created')
    message = models.TextField()
    blood_group_needed = models.CharField(
        max_length=5,
        choices=[
            ('A+','A+'),('A-','A-'),
            ('B+','B+'),('B-','B-'),
            ('AB+','AB+'),('AB-','AB-'),
            ('O+','O+'),('O-','O-'),
        ]
    )
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                    on_delete=models.CASCADE, null=True, related_name='requests_accepted'
                                    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blood_group_added} request by {self.created_by.email}"

# ===============Donation Section==================
class DonationHistory(models.Model):
    STATUS_CHOICES = [
        ('Successful','Successful'),
        ('Failed','Failed'),
        ('Pending','Pending'),
    ]
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, related_name='donation_given' )
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,related_name='donation_received')
    event = models.ForeignKey(
        BloodRequest, on_delete=models.CASCADE,
        related_name='donation_history'
    )
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    def __str__(self):
        return f"Donation: {self.donor} → {self.receiver}({self.status})"

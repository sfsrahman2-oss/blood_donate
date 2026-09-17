from django.conf import settings
from django.db import models
from django.urls import reverse


BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

AVAILABILITY_CHOICES = [
    ('available', 'Available'),
    ('not_available', 'Not Available'),
]

REQUEST_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('fulfilled', 'Fulfilled'),
    ('cancelled', 'Cancelled'),
]


class UserProfile(models.Model):
    """Extra info attached to Django's built-in User model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class DonorProfile(models.Model):
    """A user's donor listing: whether/how they can donate blood."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donor_profile'
    )
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    last_donation_date = models.DateField(blank=True, null=True)
    availability = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default='available'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

    def get_absolute_url(self):
        return reverse('donor_detail', kwargs={'pk': self.pk})


class BloodRequest(models.Model):
    """A request for blood posted by a logged-in user."""

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blood_requests'
    )
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    hospital_name = models.CharField(max_length=150)
    hospital_location = models.CharField(max_length=150)
    required_date = models.DateField()
    bags_required = models.PositiveIntegerField(default=1)
    contact_number = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=REQUEST_STATUS_CHOICES, default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient_name} needs {self.blood_group}"

    def get_absolute_url(self):
        return reverse('request_detail', kwargs={'pk': self.pk})

import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BloodRequest, DonorProfile, UserProfile

PHONE_REGEX = re.compile(r'^[0-9+\-\s]{7,20}$')


class SignUpForm(UserCreationForm):
    """Registration form: creates a User plus its UserProfile."""

    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150, required=True, label='Full Name')
    phone_number = forms.CharField(max_length=20, required=False)
    blood_group = forms.ChoiceField(
        choices=[('', '---------')] + UserProfile._meta.get_field('blood_group').choices,
        required=False,
    )
    location = forms.CharField(max_length=100, required=False)
    date_of_birth = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')
        if phone and not PHONE_REGEX.match(phone):
            raise forms.ValidationError('Enter a valid phone number.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=commit)
        full_name = self.cleaned_data['full_name'].strip()
        parts = full_name.split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone_number': self.cleaned_data.get('phone_number', ''),
                    'blood_group': self.cleaned_data.get('blood_group', ''),
                    'location': self.cleaned_data.get('location', ''),
                    'date_of_birth': self.cleaned_data.get('date_of_birth'),
                    'profile_picture': self.cleaned_data.get('profile_picture'),
                },
            )
        return user


class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, required=True, label='Full Name')
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'blood_group', 'location', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['full_name'].initial = self.user.get_full_name() or self.user.username
            self.fields['email'].initial = self.user.email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')
        if phone and not PHONE_REGEX.match(phone):
            raise forms.ValidationError('Enter a valid phone number.')
        return phone

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            full_name = self.cleaned_data['full_name'].strip()
            parts = full_name.split(' ', 1)
            self.user.first_name = parts[0]
            self.user.last_name = parts[1] if len(parts) > 1 else ''
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile


class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = [
            'name', 'blood_group', 'phone_number', 'location',
            'last_donation_date', 'availability', 'description',
        ]
        widgets = {
            'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')
        if not PHONE_REGEX.match(phone):
            raise forms.ValidationError('Enter a valid phone number.')
        return phone

    def clean_last_donation_date(self):
        date = self.cleaned_data.get('last_donation_date')
        if date and date > datetime.date.today():
            raise forms.ValidationError('Last donation date cannot be in the future.')
        return date


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'patient_name', 'blood_group', 'hospital_name', 'hospital_location',
            'required_date', 'bags_required', 'contact_number', 'description', 'status',
        ]
        widgets = {
            'required_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_contact_number(self):
        phone = self.cleaned_data.get('contact_number', '')
        if not PHONE_REGEX.match(phone):
            raise forms.ValidationError('Enter a valid contact number.')
        return phone

    def clean_bags_required(self):
        bags = self.cleaned_data.get('bags_required')
        if bags is None or bags <= 0:
            raise forms.ValidationError('Number of bags must be a positive number.')
        return bags

    def clean_required_date(self):
        date = self.cleaned_data.get('required_date')
        if date and date < datetime.date.today():
            raise forms.ValidationError('Required date cannot be in the past.')
        return date


class DonorSearchForm(forms.Form):
    blood_group = forms.ChoiceField(
        choices=[('', 'Any Blood Group')] + DonorProfile._meta.get_field('blood_group').choices,
        required=False,
    )
    location = forms.CharField(max_length=100, required=False)
    availability = forms.ChoiceField(
        choices=[('', 'Any')] + DonorProfile._meta.get_field('availability').choices,
        required=False,
    )


class RequestFilterForm(forms.Form):
    blood_group = forms.ChoiceField(
        choices=[('', 'Any Blood Group')] + BloodRequest._meta.get_field('blood_group').choices,
        required=False,
    )
    location = forms.CharField(max_length=100, required=False)
    status = forms.ChoiceField(
        choices=[('', 'Any Status')] + BloodRequest._meta.get_field('status').choices,
        required=False,
    )

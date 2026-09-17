from django.contrib import admin

from .models import BloodRequest, DonorProfile, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'blood_group', 'location')
    search_fields = ('user__username', 'user__email', 'location')


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'location', 'availability', 'updated_at')
    list_filter = ('blood_group', 'availability', 'location')
    search_fields = ('name', 'location', 'phone_number')


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name', 'blood_group', 'hospital_name', 'hospital_location',
        'required_date', 'status', 'created_at',
    )
    list_filter = ('blood_group', 'status', 'hospital_location')
    search_fields = ('patient_name', 'hospital_name', 'hospital_location')

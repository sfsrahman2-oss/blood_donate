from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import (
    BloodRequestForm,
    DonorProfileForm,
    DonorSearchForm,
    RequestFilterForm,
    SignUpForm,
    UserProfileForm,
)
from .models import BloodRequest, DonorProfile, UserProfile


def home(request):
    donor_count = DonorProfile.objects.filter(availability='available').count()
    pending_requests = BloodRequest.objects.filter(status='pending').count()
    latest_requests = BloodRequest.objects.filter(status='pending')[:5]
    context = {
        'donor_count': donor_count,
        'pending_requests': pending_requests,
        'latest_requests': latest_requests,
    }
    return render(request, 'donors/home.html', context)


# ---------- Authentication ----------

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Welcome! Your account has been created.')
        return response


class BloodLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully.')
        return super().form_valid(form)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'donors/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    return render(request, 'donors/profile_form.html', {'form': form})


# ---------- Donor Profile CRUD ----------

def donor_list(request):
    form = DonorSearchForm(request.GET or None)
    donors = DonorProfile.objects.all()

    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        location = form.cleaned_data.get('location')
        availability = form.cleaned_data.get('availability')
        if blood_group:
            donors = donors.filter(blood_group=blood_group)
        if location:
            donors = donors.filter(location__icontains=location)
        if availability:
            donors = donors.filter(availability=availability)

    paginator = Paginator(donors, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'donors/donor_list.html', {'form': form, 'page_obj': page_obj})


def donor_detail(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk)
    return render(request, 'donors/donor_detail.html', {'donor': donor})


@login_required
def donor_create(request):
    if hasattr(request.user, 'donor_profile'):
        messages.info(request, 'You already have a donor profile. You can edit it below.')
        return redirect('donor_edit')
    if request.method == 'POST':
        form = DonorProfileForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, 'Donor profile created. Thank you for registering!')
            return redirect('donor_detail', pk=donor.pk)
    else:
        form = DonorProfileForm(initial={
            'name': request.user.get_full_name() or request.user.username,
        })
    return render(request, 'donors/donor_form.html', {'form': form, 'title': 'Become a Donor'})


@login_required
def donor_edit(request):
    donor = get_object_or_404(DonorProfile, user=request.user)
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor profile updated.')
            return redirect('donor_detail', pk=donor.pk)
    else:
        form = DonorProfileForm(instance=donor)
    return render(request, 'donors/donor_form.html', {'form': form, 'title': 'Update Donor Profile'})


@login_required
def donor_delete(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        donor.delete()
        messages.success(request, 'Donor profile deleted.')
        return redirect('donor_list')
    return render(request, 'donors/donor_confirm_delete.html', {'donor': donor})


# ---------- Blood Request CRUD ----------

def request_list(request):
    form = RequestFilterForm(request.GET or None)
    requests_qs = BloodRequest.objects.all()

    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        location = form.cleaned_data.get('location')
        status = form.cleaned_data.get('status')
        if blood_group:
            requests_qs = requests_qs.filter(blood_group=blood_group)
        if location:
            requests_qs = requests_qs.filter(
                Q(hospital_location__icontains=location)
            )
        if status:
            requests_qs = requests_qs.filter(status=status)

    paginator = Paginator(requests_qs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'donors/request_list.html', {'form': form, 'page_obj': page_obj})


def request_detail(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    return render(request, 'donors/request_detail.html', {'req': blood_request})


@login_required
def request_create(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            messages.success(request, 'Blood request created successfully.')
            return redirect('request_detail', pk=blood_request.pk)
    else:
        form = BloodRequestForm(initial={'status': 'pending'})
    return render(request, 'donors/request_form.html', {'form': form, 'title': 'Create Blood Request'})


@login_required
def request_edit(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk, requester=request.user)
    if request.method == 'POST':
        form = BloodRequestForm(request.POST, instance=blood_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood request updated.')
            return redirect('request_detail', pk=blood_request.pk)
    else:
        form = BloodRequestForm(instance=blood_request)
    return render(request, 'donors/request_form.html', {'form': form, 'title': 'Edit Blood Request'})


@login_required
def request_delete(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk, requester=request.user)
    if request.method == 'POST':
        blood_request.delete()
        messages.success(request, 'Blood request deleted.')
        return redirect('my_requests')
    return render(request, 'donors/request_confirm_delete.html', {'req': blood_request})


@login_required
def my_requests(request):
    requests_qs = BloodRequest.objects.filter(requester=request.user)
    return render(request, 'donors/my_requests.html', {'requests': requests_qs})

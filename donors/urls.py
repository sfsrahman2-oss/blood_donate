from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.BloodLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Donors
    path('donors/', views.donor_list, name='donor_list'),
    path('donors/<int:pk>/', views.donor_detail, name='donor_detail'),
    path('donors/become/', views.donor_create, name='donor_create'),
    path('donors/edit/', views.donor_edit, name='donor_edit'),
    path('donors/<int:pk>/delete/', views.donor_delete, name='donor_delete'),

    # Blood requests
    path('requests/', views.request_list, name='request_list'),
    path('requests/mine/', views.my_requests, name='my_requests'),
    path('requests/create/', views.request_create, name='request_create'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/<int:pk>/edit/', views.request_edit, name='request_edit'),
    path('requests/<int:pk>/delete/', views.request_delete, name='request_delete'),
]

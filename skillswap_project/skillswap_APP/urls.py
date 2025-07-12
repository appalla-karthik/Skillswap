from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls'), name='login'),
    path('swap_requests/', views.swap_requests, name='swap_requests'),
    path('skills/', views.skill_search, name='skill'),
    path('messages/', views.notifications_view, name='messages'),  # ✅ updated
    path('profile/', views.profile_view, name='profile'),  
    path('profile/save/', views.save_profile, name='save_profile'),

    path('request/<int:receiver_id>/', views.send_swap_request, name='send_swap_request'),
    path('swap_requests/accept/<int:request_id>/', views.accept_swap_request, name='accept_swap_request'),
    path('swap_requests/reject/<int:request_id>/', views.reject_swap_request, name='reject_swap_request'),


]

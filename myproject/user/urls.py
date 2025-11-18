from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('redirect/',role_redirect,name='role_redirect'),
    path('admin-dashboard',admin_dashboard,name='admin_dashboard'),
    path('restaurant-dashbord',restaurant_dashboard,name='restaurant_dashboard'),
    path('customer-dashboard',customer_dashboard,name='customer_dashboard'),
    path('signup',signup,name='signup'),
    path('login',login_page,name='login_page'),
    path('profile_page',profile_page,name='profile_page'),
    path('edite_profile',edite_profile,name='edite_profile'),
    path('logout',logout_page,name='logout_page'),
    path('edit_booking/<int:booking_id>',edit_booking,name='edit_booking'),
    path('delete_booking/<int:booking_id>',delete_booking,name='delete_booking')

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
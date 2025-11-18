from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('home',home,name='home_page'),
    path('all_restaurant',allstaurants,name='all_restaurants'),
    path('add_restro',add_restaurant,name='add_restaurant'),
    path('restaurant/<int:res_id>',restaurant_detail,name='restaurant_detail'),
    path('add_table',add_table,name='add_table'),
    path('add_menu',add_menu,name='add_menu'),
    path('table_booking/<int:res_id>/',table_booking,name='table_booking'),
    path('booking_success/<int:booking_id>',booking_success,name='booking_success'),
    path('search',search,name='search'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
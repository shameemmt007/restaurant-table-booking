from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import SignupForm,ProfileForm
from .models import UserProfile,User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from datetime import date,time
from django.conf import settings
from django.contrib.auth import get_user_model

from RestroBook .models import Booking,Restaurant,Table
from RestroBook .views import home

@login_required
def role_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.user.role == 'admin':
        return render(request, 'admin_dashboard.html')
    elif request.user.role == 'restaurant':
        return render(request, 'restaurant_dashboard.html')
    else:
        return redirect(home)
    
@login_required
def admin_dashboard(request):
    restaurants = Restaurant.objects.all()
    User = get_user_model()
    customers = User.objects.filter(role='customer')
    owner = User.objects.filter(role='restaurants')
    return render(request,'admin_dashboard.html',{
        'restaurants':restaurants,
        'customers':customers,
        'owners':owner})

@login_required
def restaurant_dashboard(request):
    restaurant = Restaurant.objects.get(user=request.user)
    bookings = Booking.objects.filter(table__restaurant=restaurant)

    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        booking = Booking.objects.get(id=booking_id,table__restaurant=restaurant)
        booking.status=new_status
        booking.save()
        return redirect('restaurant_dashboard')
    total_bookings = bookings.count()
    available_tables = Table.objects.filter(restaurant=restaurant,is_available=True).count()
    todays_reservations = bookings.filter(date=date.today()).count
    cancelled_bookings = bookings.filter(status='Cancelled').count()

    context = {
        'restaurant':restaurant,
        'bookings':bookings,
        'total_bookings':total_bookings,
        'available_tables':available_tables,
        'todays_reservations':todays_reservations,
        'cancelled_bookings':cancelled_bookings
    }
    return render(request,'restaurant_dashboard.html',context)
@login_required
def customer_dashboard(request):
    return redirect(home)
    





from django.shortcuts import render, redirect
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'restaurants':
                return redirect('restaurant_dashboard')
            else:
                return redirect('')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request,username=usern,password=passw)
        if user:
            login(request,user)
            messages.success(request,'login success')
            if user.role == 'admin':
                return redirect(admin_dashboard)
            elif user.role == 'restaurants':
                return redirect(restaurant_dashboard)
            elif user.role == 'customer':
                return redirect(customer_dashboard)
            else:
                messages.error(request,'invalid username or password')
    return render(request,'login.html')

def profile_page(request):
    profile = UserProfile.objects.get(user=request.user)
    booking = Booking.objects.filter(user=request.user).select_related('table','table__restaurant')

    return render(request,'profile.html',{'profile':profile,'bookings':booking})

def edite_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=profile)
    return render(request,'edite_profile.html',{'form':form})

def logout_page(request):
    logout(request)
    messages.success(request,'user has been logout')
    return redirect(login_page)


def edit_booking(request,booking_id):
    booking = Booking.objects.get(id=booking_id)

    if booking.table.restaurant.user != request.user:
        messages.error(request,'you are not authorized to edit this booking')
        return redirect('restaurant_dashboard')
    
    if request.method == 'POST':
        booking.date = request.POST.get('date')
        booking.time = request.POST.get('time')
        booking.guests = request.POST.get('guests')
        booking.status = request.POST.get('status')
        booking.save()
        messages.success(request, f"booking #{booking.id} updated successfully.")
        return redirect('restaurant_dashboard')
        
    return render(request,'edit_booking.html',{'booking':booking})

def delete_booking(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    
    if booking.table.restaurant.user != request.user:
        messages.error(request,'you are not authorized user to delete this booking')

    if request.method == 'POST':
        booking.delete()
        messages.success(request,f"booking{booking_id} deleted successfully")
        return redirect('restaurant_dashboard')
        
    return render(request,'delete_booking.html',{'booking':booking})




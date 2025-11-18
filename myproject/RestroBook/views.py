from django.shortcuts import render,redirect
from .models import Restaurant,Table,Booking,Menu,Review
from datetime import date
from django.contrib import messages

from django.db.models import Q
# Create your views here.

def home(request):
    return render(request,'home.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        Restaurant.objects.create(
            user = request.user,
            name = name,
            description = description,
            location = location,
            img = image
        )
    return render(request,'restaurant_dashboard.html')

def add_table(request):
    if request.method == 'POST':
        restaurant = Restaurant.objects.get(user = request.user)
        table_num = request.POST.get('table_num')
        seats = request.POST.get('seats')

        Table.objects.create(
            restaurant = restaurant,
            table_num = table_num,
            seats = seats
        )
    return redirect(add_restaurant)

def add_menu(request):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        messages.error(request,"you dont have a restaurant yet")
        return redirect(add_restaurant)
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            Menu.objects.create(restaurant=restaurant,image=image)
            messages.success(request,'image added successfully')
        else:
            messages.warning(request,'please sellect an image to upload')
    return redirect(add_table)


def allstaurants(request):
    restaurant = Restaurant.objects.all()
    return render(request,'restaurant.html',{'restaurant':restaurant})

def restaurant_detail(request,res_id):
    from user.views import login_page
    restaurant = Restaurant.objects.get(id=res_id)
    menu = Menu.objects.filter(restaurant=restaurant)
    reviews = restaurant.reviews.order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request,"please log in to leave a review")
            return redirect(login_page)
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        Review.objects.create(
            restaurant=restaurant,
            user=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request,"your review has been added successfully")
    return render(request,'resto_detail.html',{
        'restaurant':restaurant,
        'menus':menu,
        'reviews':reviews
        })

def table_booking(request,res_id):
    restaurant = Restaurant.objects.get(id=res_id)
    available_table = Table.objects.filter(restaurant=restaurant,is_available=True)

    today = date.today().isoformat()

    if request.method == 'POST':
        table_id = request.POST['table']
        guests = request.POST['guests']
        datee = request.POST['date']
        time = request.POST['time']

        table = Table.objects.get(id=table_id)
        booking = Booking.objects.create(
            user=request.user,
            table=table,
            guests=guests,
            date=datee,
            time=time,
        )
        table.is_available = False
        table.save()

        return redirect('booking_success',booking_id=booking.id)
        
    return render(request,'table_booking.html',{
        'restaurant': restaurant,
        'tables':available_table,
        'today':today
        })
def booking_success(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request,'booking_success.html',{'booking':booking})


def search(request):
    query = request.GET.get('keyword')
    if query:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        restaurants = Restaurant.objects.all()
    context = {'restaurants':restaurants,'query':query}
    return render(request,'search.html',context)





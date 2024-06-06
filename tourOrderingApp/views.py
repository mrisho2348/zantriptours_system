import json
from django.contrib.auth import logout,login
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from tourOrderingApp.emailBackEnd import EmailBackend
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from tourOrderingApp.forms import ContactRequestForm, FeedbackForm
from tourOrderingApp.models import About, ContactRequest, Country, Feedback, Hotel, HotelBooking, Transport, TransportBooking
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


def ShowLogin(request):  
  return render(request,'login.html')

def about(request):  
  about_info= About.objects.get(pk=1)
  return render(request,'about.html',{"about_info":about_info})

def booking(request):  
  return render(request,'booking.html')

def index(request):  
  hotels = Hotel.objects.all()[:4]
  about_info= About.objects.get(pk=1)
  feedbacks = Feedback.objects.all() 
  return render(request,'index.html',{"hotels":hotels,"about_info":about_info,"feedbacks":feedbacks})

def packages(request):  
  hotels = Hotel.objects.all()[:6]
  return render(request,'pakages.html',{"hotels":hotels})

def client(request): 
  feedbacks = Feedback.objects.all() 
  return render(request,'client.html',{"feedbacks":feedbacks})

def book_transport(request, transport_id):
    transport_service = get_object_or_404(Transport, id=transport_id)
    # Add your booking logic here
    countries = Country.objects.all()
    return render(request, 'book_transport.html', {'transport_service': transport_service,"countries":countries})

def all_transport(request):
    transport_services = Transport.objects.all()
    return render(request, 'all_transport.html', {'transport_services': transport_services})

def blog(request):  
  transport_services = Transport.objects.filter(active=True)
  return render(request,'blog.html',{'transport_services': transport_services})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    return render(request, 'hotel_detail.html', {'hotel': hotel})
  
def book_hotel(request, pk):
    # Retrieve the hotel object corresponding to the provided pk
    hotel = get_object_or_404(Hotel, pk=pk)
    countries = Country.objects.all()
    # Pass the hotel object to the template
    context = {
        'hotel': hotel,
        'countries': countries
    }

    # Render the template and return it as an HTTP response
    return render(request, 'book_hotel.html', context)  
  
  

@csrf_exempt
def contact_ajax_view(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            words = request.POST.get('words')
            
            contact = ContactRequest(name=name, email=email, phone_number=phone_number, message=words)
            contact.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'error': str(e)})
    return JsonResponse({'status': 'fail', 'error': 'Invalid request method'})


def submit_booking(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    countries = Country.objects.all()
    context = {
      "countries":countries,
      "hotel":hotel,
    }
    if request.method == 'POST':
        try:
            # Extract data from the request
            customer_name = request.POST.get('name')
            customer_email = request.POST.get('email')
            nationality_id = request.POST.get('nationality')
            phone_number = request.POST.get('phone')
            passport_number = request.POST.get('passport')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact')
            gender = request.POST.get('gender')
            check_in_date = request.POST.get('check_in')
            check_out_date = request.POST.get('check_out')
            
            # Ensure each email is unique
            if HotelBooking.objects.filter(customer_email=customer_email).exists():
                messages.error(request, "Email already exists")
                return render(request, 'book_hotel.html',context)
            
            # Ensure each customer name is unique
            if HotelBooking.objects.filter(customer_name=customer_name).exists():
                messages.error(request, "Customer name already exists")
                return render(request, 'book_hotel.html',context)

            # Ensure each passport number is unique
            if passport_number and HotelBooking.objects.filter(passport_number=passport_number).exists():
                messages.error(request, "Passport number already exists")
                return render(request, 'book_hotel.html',context)

            # Ensure check-in is less than check-out date
            if check_in_date >= check_out_date:
                messages.error(request, "Check-in date must be before check-out date")
                return render(request, 'book_hotel.html',context)

            # Create HotelBooking object
            booking = HotelBooking.objects.create(
                hotel=hotel,
                customer_name=customer_name,
                customer_email=customer_email,
                nationality_id=nationality_id,
                phone_number=phone_number,
                passport_number=passport_number,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_number=emergency_contact_number,
                gender=gender,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            )
            
            # Redirect to home page upon success with success message
            messages.success(request, 'Booking submitted successfully!')
            return redirect('home')
        except Exception as e:
            # Add error message and return to booking page
            messages.error(request, str(e))
            return render(request, 'book_hotel.html', context)
    else:
        # Return error response for invalid request method
        messages.error(request, 'Invalid request method')
        return render(request, 'book_hotel.html', context)
    
    
def contact_view(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page') 
    else:
        form = ContactRequestForm()

    return render(request, 'contact.html', {'form': form})
  
def customers_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Check if the email exists in HotelBooking or TransportBooking
            customer_email = form.cleaned_data.get('email')
            if HotelBooking.objects.filter(customer_email=customer_email).exists() or TransportBooking.objects.filter(customer_email=customer_email).exists():
                form.save()
                messages.success(request, 'Feedback submitted successfully.')
                return redirect('thank_you_page')  # Redirect to a thank you page after submitting feedback
            else:
                form.add_error('email', 'No booking found for this email.')
                messages.error(request, 'Failed to submit feedback. No booking found for this email. so you cant sent feedback')
    else:
        form = FeedbackForm()
    return render(request, 'customers_feedback.html', {'form': form})

def thank_you_page(request):
    return render(request, 'thank_you_page.html')

def success_view(request):
    return render(request, 'success.html')      
      
def submit_transport_booking(request, transport_id):
    transport_service = get_object_or_404(Transport, id=transport_id)
    countries = Country.objects.all()
    context = {
        "countries": countries,
        "transport_service": transport_service,
    }

    if request.method == 'POST':
        try:
            # Extract data from the request
            customer_name = request.POST.get('name')
            customer_email = request.POST.get('email')
            nationality_id = request.POST.get('nationality')
            phone_number = request.POST.get('phone')
            passport_number = request.POST.get('passport')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact')
            gender = request.POST.get('gender')
            check_in_date = request.POST.get('check_in')
            check_out_date = request.POST.get('check_out')

            # Parse dates and current date
            check_in_date = timezone.datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = timezone.datetime.strptime(check_out_date, '%Y-%m-%d').date()
            current_date = timezone.now().date()

            # Ensure both dates are greater than the current date
            if check_in_date <= current_date or check_out_date <= current_date:
                messages.error(request, "Check-in and check-out dates must be greater than the current date")
                return render(request, 'book_transport.html', context)

            # Ensure check-in is less than check-out date
            if check_in_date >= check_out_date:
                messages.error(request, "Check-in date must be before check-out date")
                return render(request, 'book_transport.html', context)

            # Ensure each email is unique
            if TransportBooking.objects.filter(customer_email=customer_email).exists():
                messages.error(request, "Email already exists")
                return render(request, 'book_transport.html', context)

            # Ensure each customer name is unique
            if TransportBooking.objects.filter(customer_name=customer_name).exists():
                messages.error(request, "Customer name already exists")
                return render(request, 'book_transport.html', context)

            # Ensure each passport number is unique
            if passport_number and TransportBooking.objects.filter(passport_number=passport_number).exists():
                messages.error(request, "Passport number already exists")
                return render(request, 'book_transport.html', context)

            # Create TransportBooking object
            booking = TransportBooking.objects.create(
                transport_service=transport_service,
                customer_name=customer_name,
                customer_email=customer_email,
                nationality_id=nationality_id,
                phone_number=phone_number,
                passport_number=passport_number,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_number=emergency_contact_number,
                gender=gender,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            )

            # Redirect to home page upon success with success message
            messages.success(request, 'Booking submitted successfully!')
            return redirect('home')
        except Exception as e:
            # Add error message and return to booking page
            messages.error(request, str(e))
            return render(request, 'book_transport.html', context)
    else:
        # Return error response for invalid request method
        messages.error(request, 'Invalid request method')
        return render(request, 'book_transport.html', context)
  
  
def all_hotels(request):
    # Retrieve all hotels from the database
    hotels = Hotel.objects.all()
    
    # Pass the list of hotels to the template
    context = {
        'hotels': hotels
    }

    # Render the template and return it as an HTTP response
    return render(request, 'all_hotels.html', context)  

def DoLogin(request):
  if request.method!="POST":
    return HttpResponse("<h2>Method Not allowed")
  
  else:
    user = EmailBackend.authenticate(request,request.POST.get("email"),request.POST.get("password"))
    if user!=None:    
      login(request,user)  
      if user.user_type=="1":      
        return HttpResponseRedirect(reverse("admin_dashboard"))
      
      elif user.user_type == "2":
        return HttpResponseRedirect(reverse("tourist_dashboard"))    
   
    else:
      messages.error(request,"Invalid Login Details")
      return HttpResponseRedirect(reverse("login"))
    
    
def GetUserDetails(request):
  user = request.user
  if user.is_authenticated:
    return HttpResponse("User : "+user.email+" usertype : " + user.usertype)
  else:
    return HttpResponse("Please login first")   
  
  
def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse("home"))
    
    
        
 
  
  
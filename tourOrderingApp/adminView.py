import json
from django.urls import reverse
from datetime import datetime
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
from django.templatetags.static import static
import os
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.db import IntegrityError, DatabaseError
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseBadRequest
from PIL import Image
from django.db.models import Count
from tourOrderingApp.forms import AboutForm
from tourOrderingApp.models import About,  ContactRequest, Country, CustomUser, Feedback, Hotel, HotelBooking, Transport, TransportBooking, Transportation
from django.db.models.functions import TruncMonth

def admin_dashboard(request):
    current_year = datetime.now().year

    hotel_bookings_count = HotelBooking.objects.filter(booking_date__year=current_year,is_active=True).count()
    transport_bookings_count = TransportBooking.objects.filter(booking_date__year=current_year,is_active=True).count()
    transport_count = Transport.objects.all().count()
    hotel_count = Hotel.objects.all().count()

    context = {
        'transport_count': transport_count,
        'hotel_count': hotel_count,
        'hotel_bookings_count': hotel_bookings_count,
        'transport_bookings_count': transport_bookings_count,
    }
    return render(request, "admin_template/home_content.html", context)



def bookings_per_month(request):
    current_year = datetime.now().year
    bookings = (HotelBooking.objects
                .filter(booking_date__year=current_year)
                .annotate(month=TruncMonth('booking_date'))
                .values('month')
                .annotate(count=Count('id'))
                .order_by('month'))
                
    data = {
        'months': [booking['month'].strftime('%B') for booking in bookings],
        'counts': [booking['count'] for booking in bookings]
    }
    return JsonResponse(data)

def transport_bookings_per_month(request):
    current_year = datetime.now().year
    bookings = (TransportBooking.objects
                .filter(booking_date__year=current_year)
                .annotate(month=TruncMonth('booking_date'))
                .values('month')
                .annotate(count=Count('id'))
                .order_by('month'))
                
    data = {
        'months': [booking['month'].strftime('%B') for booking in bookings],
        'counts': [booking['count'] for booking in bookings]
    }
    return JsonResponse(data)

    
    
def update_tourist_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the staff object or return a 404 response if not found
            staff = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                staff.is_active = False
            elif is_active == '0':
                staff.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('tourist_list')  # Make sure 'manage_staffs' is the name of your staff list URL

            staff.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the staff list page
    return redirect('tourist_list')  # Make sure 'manage_staffs' is the name of your staff list URL

@login_required
def manage_country(request):
    countries=Country.objects.all() 
    return render(request,"admin_template/manage_country.html", {"countries":countries})   





    
def transportation_list(request):
    # Retrieve all Transportation objects
    transportations = Transportation.objects.all()
    # Pass the transportations to the template
    return render(request, 'admin_template/transportation_list.html', {'transportations': transportations})      

@csrf_exempt
def save_transportation(request):
    if request.method == 'POST':
        # Extract data from the request
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        type = request.POST.get('type')
        transportation_id = request.POST.get('transportation_id')
        image = request.FILES.get('image')
        
        # Validate image file
        accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']
        max_file_size = 5 * 1024 * 1024
        image_url = None
        
        if image:
            if image.content_type not in accepted_image_formats or image.size > max_file_size:
                return JsonResponse({'status': False, 'message': 'File must be PNG, JPEG, or JPG and should not exceed 5MB.'})
            fs = FileSystemStorage()
            image_name = fs.save('transportation_images/' + image.name, image)
            image_url = fs.url(image_name)
        
        try:
            if transportation_id:
                # Editing an existing Transportation record
                transportation = Transportation.objects.get(pk=transportation_id)
                transportation.name = name
                transportation.capacity = capacity
                transportation.type = type
                if image:
                    transportation.image = image_url
                transportation.save()
                return JsonResponse({'status': True, 'message': 'Transportation record updated successfully.'})
            else:
                # Adding a new Transportation record
                Transportation.objects.create(
                    name=name,
                    capacity=capacity,
                    type=type,
                    image=image_url
                )
                return JsonResponse({'status': True, 'message': 'Transportation record saved successfully.'})
        except Exception as e:
            # Return error response if an exception occurs
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    else:
        # Return error response for invalid request method
        return JsonResponse({'status': False, 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def delete_transportation(request):
    if request.method == 'POST':
        # Extract category ID from the request data
        transportation_id = request.POST.get('transportation_id')        
        try:
            # Retrieve the tour category object
            transportation_id = Transportation.objects.get(pk=transportation_id)
            # Delete the tour category
            transportation_id.delete()
            # Return success response
            return JsonResponse({'status': True, 'message': 'Tour transportation deleted successfully.'})
        except Transportation.DoesNotExist:
            # Return error response if category does not exist
            return JsonResponse({'status': False, 'message': 'Tour transportation does not exist.'}, status=404)
        except Exception as e:
            # Return error response for any other exceptions
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    else:
        # Return error response for invalid request method
        return JsonResponse({'status': False, 'message': 'Invalid request method.'}, status=400)  
    
 

@login_required 
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'admin_template/hotel_list.html', {'hotels': hotels})   

def contact_list_view(request):
    contacts = ContactRequest.objects.all()
    return render(request, 'admin_template/contact_list.html', {'contacts': contacts})



def add_about_record(request):
    try:
        # Get the About instance if it exists, or create it if it doesn't
        about_instance, created = About.objects.get_or_create(pk=1)

        if request.method == 'POST':
            form = AboutForm(request.POST, instance=about_instance)
            if form.is_valid():
                form.save()
                return redirect('about_page')  # Redirect to the about page after saving
        else:
            form = AboutForm(instance=about_instance)
    except About.MultipleObjectsReturned:
        # Handle case where multiple records exist (shouldn't happen)
        About.objects.filter(pk=1).delete()
        about_instance = About.objects.create(pk=1)
        form = AboutForm(instance=about_instance)
    except Exception as e:
        # Handle other exceptions gracefully
        return render(request, 'admin_template/about.html', {'error_message': str(e)})
    return render(request, 'admin_template/about.html', {'form': form})
  
@login_required 
def transport_list(request):
    transports = Transport.objects.all()
    return render(request, 'admin_template/transport_list.html', {'transports': transports})     

def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_template/feedback_list.html', {'feedbacks': feedbacks})

def booking_list(request):
    bookings = HotelBooking.objects.all()
    countries = Country.objects.all()
    return render(request, 'admin_template/booking_list.html', {'bookings': bookings, 'countries': countries})

@csrf_exempt
def update_booking(request):
    if request.method == 'POST':
        try:
            booking_id = request.POST.get('booking_id')
            booking = HotelBooking.objects.get(id=booking_id)
            
            # Fetching form data
            customer_name = request.POST.get('customer_name')
            customer_email = request.POST.get('customer_email')
            nationality_id = request.POST.get('nationality')
            phone_number = request.POST.get('phone_number')
            passport_number = request.POST.get('passport_number')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            gender = request.POST.get('gender')
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            booking_date = request.POST.get('booking_date')
            
            # Validate check-in and check-out dates
            if check_in_date >= check_out_date:
                return JsonResponse({'status': False, 'message': 'Check-in date must be before check-out date.'})

            # Ensure the edited details do not match an existing record
            if HotelBooking.objects.exclude(id=booking_id).filter(
                customer_name=customer_name,
                customer_email=customer_email,
                hotel=booking.hotel,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            ).exists():
                return JsonResponse({'status': False, 'message': 'Booking with these details already exists.'})

            # Update booking details
            booking.customer_name = customer_name
            booking.customer_email = customer_email
            if nationality_id:
                booking.nationality = Country.objects.get(id=nationality_id)
            booking.phone_number = phone_number
            booking.passport_number = passport_number
            booking.emergency_contact_name = emergency_contact_name
            booking.emergency_contact_number = emergency_contact_number
            booking.gender = gender
            booking.check_in_date = check_in_date
            booking.check_out_date = check_out_date
            booking.booking_date = booking_date

            booking.save()
            return JsonResponse({'status': True, 'message': 'Booking updated successfully.'})
        
        except HotelBooking.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Booking not found.'})
        except Country.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Invalid nationality selected.'})
        except ValidationError as e:
            return JsonResponse({'status': False, 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'An error occurred: ' + str(e)})

    return JsonResponse({'status': False, 'message': 'Invalid request method.'})

@csrf_exempt
def delete_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = HotelBooking.objects.get(id=booking_id)
            booking.delete()
            return JsonResponse({'status': True})
        except HotelBooking.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Booking does not exist'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False})

@csrf_exempt
def update_transport_booking(request):
    if request.method == 'POST':
        try:
            booking_id = request.POST.get('booking_id')
            booking = TransportBooking.objects.get(id=booking_id)
            
            # Fetching form data
            customer_name = request.POST.get('customer_name')
            customer_email = request.POST.get('customer_email')
            nationality_id = request.POST.get('nationality')
            phone_number = request.POST.get('phone_number')
            passport_number = request.POST.get('passport_number')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            gender = request.POST.get('gender')
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            booking_date = request.POST.get('booking_date')
            
            # Validate check-in and check-out dates
            if check_in_date >= check_out_date:
                return JsonResponse({'status': False, 'message': 'Check-in date must be before check-out date.'})

            # Ensure the edited details do not match an existing record
            if TransportBooking.objects.exclude(id=booking_id).filter(
                customer_name=customer_name,
                customer_email=customer_email,
                transport_service=booking.transport_service,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            ).exists():
                return JsonResponse({'status': False, 'message': 'Booking with these details already exists.'})

            # Update booking details
            booking.customer_name = customer_name
            booking.customer_email = customer_email
            if nationality_id:
                booking.nationality = Country.objects.get(id=nationality_id)
            booking.phone_number = phone_number
            booking.passport_number = passport_number
            booking.emergency_contact_name = emergency_contact_name
            booking.emergency_contact_number = emergency_contact_number
            booking.gender = gender
            booking.check_in_date = check_in_date
            booking.check_out_date = check_out_date
            booking.booking_date = booking_date

            booking.save()
            return JsonResponse({'status': True, 'message': 'Booking updated successfully.'})
        
        except TransportBooking.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Booking not found.'})
        except Country.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Invalid nationality selected.'})
        except ValidationError as e:
            return JsonResponse({'status': False, 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'An error occurred: ' + str(e)})

    return JsonResponse({'status': False, 'message': 'Invalid request method.'})

def fetch_transport_booking_total(request):
    # Get the start of today in the current timezone
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)

    # Count all transport bookings made today
    total_bookings = TransportBooking.objects.filter(booking_date__gte=today_start, booking_date__lt=today_end).count()
    
    return JsonResponse({'total_bookings': total_bookings})

def fetch_hotel_booking_total(request):
    # Get the start of today in the current timezone
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)

    # Count all hotel bookings made today
    total_bookings = HotelBooking.objects.filter(booking_date__gte=today_start, booking_date__lt=today_end).count()
    
    return JsonResponse({'total_bookings': total_bookings})

def update_hotel_booking_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            booking_id = request.POST.get('booking_id')
            is_active = request.POST.get('is_active')

            # Retrieve the staff object or return a 404 response if not found
            staff = get_object_or_404(HotelBooking, id=booking_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                staff.is_active = False
            elif is_active == '0':
                staff.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('booking_list')  # Make sure 'manage_staffs' is the name of your staff list URL

            staff.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    # Redirect back to the staff list page
    return redirect('booking_list')  # Make sure 'manage_staffs' is the name of your staff list URL

def update_transport_booking_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            booking_id = request.POST.get('booking_id')
            is_active = request.POST.get('is_active')

            # Retrieve the staff object or return a 404 response if not found
            staff = get_object_or_404(TransportBooking, id=booking_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                staff.is_active = False
            elif is_active == '0':
                staff.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('transport_booking_list')  # Make sure 'manage_staffs' is the name of your staff list URL

            staff.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    # Redirect back to the staff list page
    return redirect('transport_booking_list')  # Make sure 'manage_staffs' is the name of your staff list URL

@csrf_exempt
def delete_transport_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = TransportBooking.objects.get(id=booking_id)
            booking.delete()
            return JsonResponse({'status': True})
        except TransportBooking.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Booking does not exist'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False})

def transport_booking_list(request):
    bookings = TransportBooking.objects.all()
    countries = Country.objects.all()
    return render(request, 'admin_template/transport_booking_list.html', {'bookings': bookings,'countries':countries})

@csrf_exempt
def add_hotel(request):
    if request.method == 'POST':
        try:
            hotel_id = request.POST.get('hotel_id')
            name = request.POST.get('name')
            location = request.POST.get('location')
            print(location)
            price = request.POST.get('price')
            description = request.POST.get('description')
            active = request.POST.get('active') == 'true'
            
            image = request.FILES.get('image')
            
            # Check for uniqueness of the hotel name
            if hotel_id:
                hotel = get_object_or_404(Hotel, id=hotel_id)
                # Exclude the current hotel being edited from the uniqueness check
                if Hotel.objects.filter(name=name).exclude(id=hotel_id).exists():
                    return JsonResponse({'status': False, 'message': 'Hotel name must be unique.'})
                hotel.name = name
                hotel.location = location
                hotel.price = price
                hotel.description = description
                hotel.active = active
                if image:
                    hotel.image = image
                message = 'Hotel updated successfully!'
            else:
                # Check if a hotel with the same name already exists
                if Hotel.objects.filter(name=name).exists():
                    return JsonResponse({'status': False, 'message': 'Hotel name must be unique.'})
                hotel = Hotel(
                    name=name,
                    location=location,
                    price=price,
                    description=description,
                    active=active,
                )
                if image:
                    hotel.image = image
                message = 'Hotel added successfully!'
            
            hotel.save()
            
            return JsonResponse({'status': True, 'message': message})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Invalid request method'})


@csrf_exempt
def add_transport(request):
    if request.method == 'POST':
        try:
            transport_id = request.POST.get('transport_id')
            name = request.POST.get('name')
            location = request.POST.get('location')         
            price = request.POST.get('price')
            description = request.POST.get('description')
            active = request.POST.get('active') == 'true'
            
            image = request.FILES.get('image')
            
            # Check for uniqueness of the transport name
            if transport_id:
                transport = get_object_or_404(Transport, id=transport_id)
                # Exclude the current transport being edited from the uniqueness check
                if Transport.objects.filter(name=name).exclude(id=transport_id).exists():
                    return JsonResponse({'status': False, 'message': 'Transport name must be unique.'})
                transport.name = name
                transport.location = location
                transport.price = price
                transport.description = description
                transport.active = active
                if image:
                    transport.image = image
                message = 'Transport updated successfully!'
            else:
                # Check if a transport with the same name already exists
                if Transport.objects.filter(name=name).exists():
                    return JsonResponse({'status': False, 'message': 'Transport name must be unique.'})
                transport = Transport(
                    name=name,
                    location=location,
                    price=price,
                    description=description,
                    active=active,
                )
                if image:
                    transport.image = image
                message = 'Transport added successfully!'
            
            transport.save()
            
            return JsonResponse({'status': True, 'message': message})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Invalid request method'})

    
def delete_hotel(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            hotel.delete()
            return JsonResponse({'status': True})
        except Hotel.DoesNotExist:
            return JsonResponse({'status': False, 'error': 'Hotel not found'})
    return JsonResponse({'status': False, 'error': 'Invalid request method'})    

@csrf_exempt  # Consider using CSRF tokens for better security in production
def delete_transport(request):
    if request.method == 'POST':
        transport_id = request.POST.get('transport_id')
        try:
            transport = Transport.objects.get(id=transport_id)
            transport.delete()
            return JsonResponse({'status': True, 'message': 'Transport deleted successfully'})
        except Transport.DoesNotExist:
            return JsonResponse({'status': False, 'error': 'Transport not found'})
    return JsonResponse({'status': False, 'error': 'Invalid request method'})
    


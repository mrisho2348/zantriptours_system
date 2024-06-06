
from django.urls import path
from tourOrderingApp import adminView, imports

urlpatterns = [
     
        path('admin_dashboard',adminView.admin_dashboard, name="admin_dashboard"),
        path('save_transportation/',adminView.save_transportation, name="save_transportation"),
        path('delete_transportation/',adminView.delete_transportation, name="delete_transportation"),     
        path('update_tourist_status/',adminView.update_tourist_status, name="update_tourist_status"),
        path('manage_country/',adminView.manage_country, name="manage_country"),      
        path('transportations/', adminView.transportation_list, name='transportation_list'),
        path('hotels/', adminView.hotel_list, name='hotel_list'),      
        path('transport/', adminView.transport_list, name='transport_list'),      
        path('contacts/', adminView.contact_list_view, name='contact_list'),     
        path('add_about/',adminView.add_about_record, name='about_page'),
        path('feedbacks/', adminView.feedback_list, name='feedback_list'),
        path('edit_about/<int:about_id>/', adminView.add_about_record, name='edit_about'),
        path('add_hotel/', adminView.add_hotel, name='add_hotel'),  
        path('bookings/', adminView.booking_list, name='booking_list'),   
        path('transport_booking_list/', adminView.transport_booking_list, name='transport_booking_list'),   
        path('add_transport/', adminView.add_transport, name='add_transport'),
        path('delete_transport/', adminView.delete_transport, name='delete_transport'), 
        path('bookings_per_month/', adminView.bookings_per_month, name='bookings_per_month'),
        path('transport_bookings_per_month/', adminView.transport_bookings_per_month, name='transport_bookings_per_month'),
        path('delete_hotel/', adminView.delete_hotel, name='delete_hotel'),
        path('import_country_records/',imports.import_country_records, name="import_country_records"),
        path('import_transportation_record/',imports.import_transportation_record, name="import_transportation_record"),
       
]


from django.urls import  include, path
from . import views

urlpatterns = [
        path('about',views.about, name="about"),      
        path('booking',views.booking, name="booking"),     
        path('',views.index, name="home"),      
        path('packages',views.packages, name="packages"),      
        path('client',views.client, name="client"),  
        path('contact/', views.contact_view, name='contact'),
        path('success/', views.success_view, name='success_page'), 
        path('feedback/', views.customers_feedback, name='feedback'),
        path('all_transport',views.all_transport, name="all_transport"), 
        path('thank-you/', views.thank_you_page, name='thank_you_page'), 
        path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'), 
        path('book_hotel/<int:pk>/', views.book_hotel, name='book_hotel'),  
        path('contact/ajax/', views.contact_ajax_view, name='contact_ajax'), 
        path('all-hotels/', views.all_hotels, name='all_hotels'),
        path('submit_booking/<int:hotel_id>/', views.submit_booking, name='submit_booking'),
        path('book_transport/<int:transport_id>/', views.book_transport, name='book_transport'),
        path('submit_transport_booking/<int:transport_id>/', views.submit_transport_booking, name='submit_transport_booking'),
        path('blog',views.blog, name="blog"),     
        path('login',views.ShowLogin, name="login"),      
        path('dologin',views.DoLogin, name="DoLogin"),    
        path('logout_user', views.logout_user, name='logout_user'), 
        
    
]
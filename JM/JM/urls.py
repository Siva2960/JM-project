"""
URL configuration for JM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from JMate import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login/', views.login, name='login'),  # ✅ Fixed URL
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('Signup', views.Signup, name="Signup"),
    path('UserLogin', views.UserLogin, name="UserLogin"),
    path('save/', views.save_support_info, name='save_support_info'),
    path('pas/', views.save_pas_info, name='save_pas_info'),
    path('find_passengers_for_driver/', views.find_passengers_for_driver, name='find_passengers_for_driver'),
    path('find_passengers/', views.find_passengers),
    path('earn/', views.top_destinations, name='top_destinations'),
    path('find_passengers/', views.find_passengers, name='find_passengers'),
    path('accept-passenger/<int:passenger_id>/',views.AR, name='accept_passenger'),
    path('start_ride_page/<int:passenger_id>/', views.start_ride_page, name='start_ride_page'),

# In urls.py
    path('send-request/<int:driver_id>/<int:passenger_id>/', views.send_request_to_driver, name='send_request_to_driver'),
    path('pickup-page/<int:passenger_id>/', views.pickup_page, name='pickup_page'),
    path('pickup-another/', views.pickup_another, name='pickup_another'),
    path('finish_ride/<int:passenger_id>/', views.finish_ride, name='finish_ride'),
    path('home/', views.home, name='home'),
    path('accepted_driver/', views.accepted_driver_view, name='accepted_driver_view'),
path('p_start_ride/', views.p_start_ride, name='p_start_ride'),
path('passenger_ride/', views.passenger_ride_view, name='passenger_ride'),
path('finish_ride/', views.finish_ride_view, name='finish_ride'),
path('ride/<int:passenger_id>/', views.ride_tracking_view, name='ride_tracking'),




]





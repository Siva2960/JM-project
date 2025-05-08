
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.
from django.templatetags.static import static

def home(request):
    return render(request, 'home.html')

def login(requast):
    return render(requast, 'login.html')

def signin(requast):
    return render(requast, 'signin.html')


def passenger_list_view(request):
    # Make sure the user is authenticated and has a number
    print("User info:", request.user)  # Debug
    print("User number:", getattr(request.user, 'number', None))  # Debug

    return render(request, 'passenger_list.html', {
        'passengers': passengers,
        # No need to pass number manually if request.user.number is valid
    })


from django.shortcuts import render, redirect
from geopy.distance import geodesic  # make sure you have geopy installed
from .models import pas_Entry
from django.shortcuts import render, redirect
from geopy.distance import geodesic
from math import radians, sin, cos, sqrt, atan2
from django.shortcuts import render, redirect, get_object_or_404
from .models import pas_Entry


def checkUser(number):
    flag = False
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '123456', database = 'JM',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("SELECT number FROM jmate_signin WHERE number=%s", (number,))
        rows = cur.fetchall()
        for row in rows:
            flag = True
            break
    return flag


# this is for signin view

def Signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        user_type = request.POST.get('type')
        password = request.POST.get('password')

        if not all([name, number, user_type, password]):
            return render(request, 'signin.html', {'data': 'All fields are required'})

        print(f"checkUser result: {checkUser(number)}")

        if not checkUser(number):  # safer boolean check
            try:
                db_connection = pymysql.connect(
                    host='127.0.0.1',
                    port=3306,
                    user='root',
                    password='123456',
                    database='JM',
                    charset='utf8'
                )
                with db_connection.cursor() as cursor:
                    query = "INSERT INTO jmate_signin (name, number, user_type, password) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (name, number, user_type, password))
                    db_connection.commit()

                    if cursor.rowcount == 1:
                        return render(request, 'home.html', {'data': 'Signup Process Completed'})
                    else:
                        return render(request, 'signin.html', {'data': 'Error in signup process'})

            except Exception as e:
                print("Signup error:", e)
                return render(request, 'signin.html', {'data': 'Database error during signup'})

            finally:
                db_connection.close()

        else:
            return render(request, 'signin.html', {'data': 'Given username already exists'})

    return render(request, 'signin.html', {'data': 'Invalid request method'})







from django.shortcuts import render, redirect
import pymysql
def UserLogin(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        password = request.POST.get('password')

        con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='JM',
            charset='utf8'
        )

        try:
            with con.cursor() as cur:
                sql = "SELECT name, user_type FROM jmate_signin WHERE number=%s AND password=%s"
                cur.execute(sql, (number, password))
                result = cur.fetchone()

                if result:
                    name, user_type = result  # Fetch both name and user_type

                    request.session['number'] = number  # Store number in session
                    request.session['name'] = name  # Store name in session

                    if user_type == 'driver':
                        return render(request, 'driverscreen.html', {
                            'data': f'Welcome {name}',  # Show name instead of number
                            'name': name,
                            'number': number
                        })
                    elif user_type == 'passenger':
                        return render(request, 'passangerscreen.html', {
                            'data': f'Welcome {name}',  # Show name instead of number
                            'name': name,
                            'number': number
                        })
                    else:
                        return render(request, 'login.html', {'data': 'Unknown user type'})
                else:
                    return render(request, 'login.html', {'data': 'Invalid login details'})

        finally:
            con.close()

    return render(request, 'login.html')






from geopy.geocoders import Nominatim
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.utils import timezone
from datetime import timedelta
from .models import SupportEntry

geolocator = Nominatim(user_agent="jm_project")

def reverse_geocode(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        if location and location.raw.get("address"):
            address = location.raw["address"]
            area = address.get("suburb") or address.get("neighbourhood") or address.get("village") or address.get("town") or address.get("city", "")
            pincode = address.get("postcode", "")
            return area, pincode
    except:
        pass
    return None, None

def forward_geocode(area_name):
    try:
        location = geolocator.geocode(area_name, timeout=10)
        if location:
            return location.latitude, location.longitude
    except:
        pass
    return None, None

def extract_location_details(input_value):
    try:
        # Check if input is coordinates
        if "," in input_value:
            lat, lon = map(float, input_value.split(","))
        else:
            lat, lon = forward_geocode(input_value)
            if lat is None or lon is None:
                return None, None, None, None
        area, pincode = reverse_geocode(lat, lon)
        return lat, lon, area, pincode
    except:
        return None, None, None, None

def get_name_from_number(number):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM jmate_signin WHERE number = %s LIMIT 1", [number])
        row = cursor.fetchone()
        return row[0] if row else None

def get_user_type_from_number(number):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_type FROM jmate_signin WHERE number = %s LIMIT 1", [number])
        row = cursor.fetchone()
        return row[0] if row else None

def save_support_info(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        vehicle_type = request.POST.get('vehicle_type')
        support_input = request.POST.get('support_info')
        to_input = request.POST.get('to_location')

        # Get details for support location
        support_lat, support_lon, support_area, support_pin = extract_location_details(support_input)
        to_lat, to_lon, to_area, to_pin = extract_location_details(to_input)

        if not all([support_area, support_pin, to_area, to_pin]):
            return HttpResponse("Invalid location input", status=400)

        name = get_name_from_number(number)
        user_type = get_user_type_from_number(number)

        if not name or not user_type:
            return HttpResponse("User not found", status=404)

        time_threshold = timezone.now() - timedelta(minutes=10)
        existing_entry = SupportEntry.objects.filter(
            number=number,
            area_name=support_area,
            pincode=support_pin,
            to_area=to_area,
            to_pincode=to_pin,
            submitted_at__gte=time_threshold
        ).first()

        if existing_entry:
            existing_entry.name = name
            existing_entry.user_type = user_type
            existing_entry.vehicle_type = vehicle_type
            existing_entry.support_info = support_input
            existing_entry.latitude = support_lat
            existing_entry.longitude = support_lon
            existing_entry.area_name = support_area
            existing_entry.pincode = support_pin
            existing_entry.to_location = to_input
            existing_entry.to_latitude = to_lat
            existing_entry.to_longitude = to_lon
            existing_entry.to_area = to_area
            existing_entry.to_pincode = to_pin
            existing_entry.submitted_at = timezone.now()
            existing_entry.save()
        else:
            SupportEntry.objects.create(
                name=name,
                number=number,
                user_type=user_type,
                vehicle_type=vehicle_type,
                support_info=support_input,
                latitude=support_lat,
                longitude=support_lon,
                area_name=support_area,
                pincode=support_pin,
                to_location=to_input,
                to_latitude=to_lat,
                to_longitude=to_lon,
                to_area=to_area,
                to_pincode=to_pin
            )
        from JMate.models import RideRequest, pas_Entry  # make sure this import is present

        # Match to passenger
        passenger = pas_Entry.objects.filter(number=number).last()
        if passenger:
            ride_request, created = RideRequest.objects.get_or_create(
                passenger=passenger,
                driver=driver,
                defaults={'status': 'accepted'}
            )
            if not created:
                ride_request.status = 'accepted'
                ride_request.save()

            # Update passenger status
            passenger.status = 'picked'
            passenger.assigned_driver = driver.number
            passenger.save()

        return redirect('find_passengers')  # Update with correct URL name

    else:
        number = request.session.get("number")
        name = get_name_from_number(number) or "Guest"
        return render(request, 'driverscreen.html', {
            'data': f'Welcome {name}',
            'number': number
        })

def find_passengers(request):
    try:
        # Get the latest driver
        driver = SupportEntry.objects.filter(user_type="driver").latest('id')
    except SupportEntry.DoesNotExist:
        return render(request, 'passenger_list.html', {'passengers': []})

    driver_from_coords = (driver.latitude, driver.longitude)
    driver_to_pincode = driver.to_pincode
    driver_vehicle_type = driver.vehicle_type.lower()

    # Get IDs of passengers already accepted by any driver
    accepted_passenger_ids = RideRequest.objects.filter(
        status='accepted'
    ).values_list('passenger_id', flat=True)

    # Filter unaccepted passengers by pincode and vehicle type
    passengers = pas_Entry.objects.filter(
        to_pincode=driver_to_pincode,
        vehicle_type=driver_vehicle_type,
        status='pending'  # Only unaccepted passengers
    ).exclude(id__in=accepted_passenger_ids)

    matched_passengers = []
    for passenger in passengers:
        # Ensure passenger has coordinates
        if passenger.latitude is None or passenger.longitude is None:
            continue

        passenger_from_coords = (passenger.latitude, passenger.longitude)

        try:
            # Calculate distance between driver and passenger
            distance_km = geodesic(driver_from_coords, passenger_from_coords).km
            print(f"Driver: {driver_from_coords}, Passenger: {passenger_from_coords}, Distance: {distance_km} km")  # Debugging output

            if distance_km <= 3:
                passenger.distance = round(distance_km, 2)
                matched_passengers.append(passenger)
        except Exception as e:
            print(f"Error calculating distance for passenger {passenger.id}: {e}")
            continue

    print(f"Matched passengers count: {len(matched_passengers)}")
    return render(request, 'passenger_list.html', {'passengers': matched_passengers})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import pas_Entry
def AR(request, passenger_id):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Only POST allowed'})

        data = json.loads(request.body)
        driver_id = data.get('driver_id')

        passenger = pas_Entry.objects.get(id=passenger_id)

        if passenger.status != 'pending':
            return JsonResponse({'success': False, 'error': 'Already accepted by someone'})

        passenger.status = 'picked'
        passenger.assigned_driver = driver_id
        passenger.save()

        return JsonResponse({'success': True})
    except Exception as e:
        print("ERROR IN AR:", str(e))  # This will show in your terminal
        return JsonResponse({'success': False, 'error': str(e)})



from django.shortcuts import render, get_object_or_404
from .models import pas_Entry  # Replace with the correct model for passenger

def pickup_page(request, passenger_id):
    passenger = get_object_or_404(pas_Entry, id=passenger_id)

    context = {
        'passenger': passenger,
        'passenger_lat': passenger.latitude,
        'passenger_lon': passenger.longitude,
    }
    return render(request, 'pickup_page.html', context)

def get_driver_info(passenger):
    # Assuming assigned_driver contains phone number
    driver_number = passenger.assigned_driver
    try:
        driver = SupportEntry.objects.get(number=driver_number)  # Find by the phone number
        return driver
    except SupportEntry.DoesNotExist:
        return None

# Haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(R * c, 2)  # Distance in km


from .models import pas_Entry, SupportEntry
from django.http import HttpResponse
def start_ride_page(request, passenger_id):
    try:
        # Fetch the passenger using their ID
        passenger = pas_Entry.objects.get(id=passenger_id)

        # Send the passenger details to the template
        context = {
            'passenger': passenger,  # <-- Add this line
            'passenger_name': passenger.name,
            'passenger_number': passenger.number,
            'from_lat': passenger.latitude,
            'from_lon': passenger.longitude,
            'to_lat': passenger.to_latitude,
            'to_lon': passenger.to_longitude
        }
        return render(request, 'start_ride.html', context)
    except pas_Entry.DoesNotExist:
        return HttpResponse("Passenger not found", status=404)
def pickup_another(request):
    return redirect('find_passengers')

from django.shortcuts import render, redirect, get_object_or_404
from geopy.distance import geodesic
from .models import pas_Entry
def finish_ride(request, passenger_id):
    try:
        passenger = pas_Entry.objects.get(id=passenger_id)
    except pas_Entry.DoesNotExist:
        return HttpResponse("Passenger not found", status=404)

    rate_per_km = 9
    start = (passenger.latitude, passenger.longitude)
    end = (passenger.to_latitude, passenger.to_longitude)

    distance = round(geodesic(start, end).km, 2)
    total_amount = round(distance * rate_per_km, 2)

    if request.method == 'POST':
        passenger.status = 'completed'
        passenger.save()

        # After completion, render the results on the same finish_ride.html
        context = {
            'passenger': passenger,
            'rate_per_km': rate_per_km,
            'distance': distance,
            'total_amount': total_amount,
            'message': 'Ride marked as completed ✅'
        }
        return render(request, 'finish_ride.html', context)

    # If GET request, show confirmation page
    context = {
        'passenger': passenger,
        'rate_per_km': rate_per_km,
        'distance': distance,
        'total_amount': total_amount
    }
    return render(request, 'finish_ride.html', context)

#passanger data saved view
from django.shortcuts import render
from .models import pas_Entry, SupportEntry
from geopy.distance import geodesic
from django.utils import timezone
from django.shortcuts import render
from geopy.distance import geodesic
from .models import pas_Entry, SupportEntry
from django.shortcuts import render
from django.http import JsonResponse
from .models import pas_Entry, SupportEntry  # assuming name is in SupportEntry


def save_pas_info(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        vehicle_type = request.POST.get('vehicle_type')
        support_info = request.POST.get('support_info')

        # FROM (support) data
        support_lat = request.POST.get('support_lat')
        support_lon = request.POST.get('support_lon')
        support_area = request.POST.get('support_area')
        support_pin = request.POST.get('support_pincode')

        # TO data
        to_input = request.POST.get('to_location')
        to_lat = request.POST.get('to_lat')
        to_lon = request.POST.get('to_lon')
        to_area = request.POST.get('to_area')
        to_pin = request.POST.get('to_pincode')
        passengers=request.POST.get('passengers')
        # Get passenger name using number
        name = get_name_from_number(number)
        if not name:
            return HttpResponse("User not found.", status=404)

        # Get user type (passenger)
        user_type = get_user_type_from_number(number)
        if not user_type:
            return HttpResponse("User type not found.", status=404)

        # Reverse geocode if missing from frontend
        if support_area in [None, "", "Unknown"] or support_pin in [None, "", "N/A"]:
            area, pincode = reverse_geocode(support_lat, support_lon)
            support_area = area or support_area
            support_pin = pincode or support_pin

        if to_area in [None, "", "Unknown"] or to_pin in [None, "", "N/A"]:
            area, pincode = reverse_geocode(to_lat, to_lon)
            to_area = area or to_area
            to_pin = pincode or to_pin

        # Save the data to pas_Entry model
        passenger=pas_Entry.objects.create(
            name=name,
            number=number,
            user_type=user_type,
            vehicle_type=vehicle_type,
            support_info=support_info,
            latitude=support_lat,
            longitude=support_lon,
            area_name=support_area,
            pincode=support_pin,
            to_location=to_input,
            to_latitude=to_lat,
            to_longitude=to_lon,
            to_area=to_area,
            to_pincode=to_pin,
            passengers=passengers
        )
        # Automatically send requests to all drivers
        eligible_drivers = SupportEntry.objects.filter(
            user_type="Driver",
            vehicle_type=vehicle_type
        )

        for driver in eligible_drivers:
            RideRequest.objects.create(
                driver=driver,
                passenger=passenger,
            )

        return redirect('accepted_driver_view')

    else:
        # GET request – fetch user number from session
        number = request.session.get("number")  # Fetch from session
        return render(request, 'passengerscreen.html', {'data': f'Welcome {name}'})


def p_start_ride(request):
    return render(request, 'passenger_ride.html')

from django.shortcuts import render
from .models import RideRequest, pas_Entry, SupportEntry
from django.shortcuts import render
from JMate.models import pas_Entry, RideRequest, SupportEntry

def accepted_driver_view(request):
    passenger_number = request.session.get('number')
    if not passenger_number:
        return render(request, "accepted_driver.html", {
            "driver": None,
            "message": "Passenger number not found in session."
        })

    try:
        # Get the latest passenger entry for this number
        passenger = pas_Entry.objects.filter(number=passenger_number,status = 'picked').latest('id')
    except pas_Entry.DoesNotExist:
        return render(request, "accepted_driver.html", {
            "driver": None,
            "message": "No passenger entry found."
        })

    try:
        # Get the latest accepted ride request for this passenger
        ride_request = RideRequest.objects.filter(passenger=passenger, status='pending').latest('id')
        driver = ride_request.driver
        context = {
            "driver": driver,
            "message": "Driver has accepted your request."
        }
    except RideRequest.DoesNotExist:
        context = {
            "driver": None,
            "message": "No driver has accepted your request yet."
        }
        # Prepare data for map (use the passenger's location and driver's location)
    context = {
        'passenger_lat': passenger.latitude,
        'passenger_lon': passenger.longitude,
        'driver_lat': driver.latitude if driver else None,
        'driver_lon': driver.longitude if driver else None,
        'driver': driver,
        'message': 'Driver not accepted your request yet' if not driver else 'Driver accepted your request'
    }
    return render(request, "accepted_driver.html", context)

from django.shortcuts import render, get_object_or_404
from .models import pas_Entry

def passenger_ride_view(request):
    try:
        # Fetch the passenger using their ID
        passenger = pas_Entry.objects.get(id=passenger_id)

        # Send the passenger details to the template
        context = {
            'passenger': passenger,  # <-- Add this line
            'from_lat': passenger.latitude,
            'from_lon': passenger.longitude,
            'to_lat': passenger.to_latitude,
            'to_lon': passenger.to_longitude
        }
        return render(request, 'passenger_ride.html', context)
    except pas_Entry.DoesNotExist:
        return HttpResponse("Passenger not found", status=404)

from django.shortcuts import render, get_object_or_404
from .models import pas_Entry

def ride_tracking_view(request, passenger_id):
    passenger = get_object_or_404(pas_Entry, id=passenger_id)
    context = {
        'passenger': passenger,
        'from_lat': passenger.latitude,
        'from_lon': passenger.longitude,
        'to_lat': passenger.to_latitude,
        'to_lon': passenger.to_longitude,
    }
    return render(request, 'passenger_ride.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import pas_Entry

def finish_ride_view(request):
    if request.method == 'POST':
        passenger_number = request.session.get('number')
        if not passenger_number:
            return redirect('login')  # or show error page

        try:
            passenger = pas_Entry.objects.filter(number=passenger_number).latest('id')
        except pas_Entry.DoesNotExist:
            return render(request, 'passenger_ride.html', {"error": "Passenger not found."})

        passenger.status = 'completed'
        passenger.save()

        return render(request, 'finish.html')  # or redirect somewhere

    return redirect('passenger_ride')  # fallback for GET requests

#this view for get passanger list near 3km

from geopy.distance import geodesic
from .models import SupportEntry, pas_Entry
from django.shortcuts import render

def find_passengers_for_driver(request):
    try:
        driver_number = request.session.get("number")  # use session to get logged-in driver
        driver = SupportEntry.objects.filter(number=driver_number, user_type="driver").latest('id')
    except SupportEntry.DoesNotExist:
        return render(request, 'passenger_list.html', {'passengers': []})

    if not (driver.latitude and driver.longitude):
        return render(request, 'passenger_list.html', {'passengers': []})

    driver_from_coords = (driver.latitude, driver.longitude)
    driver_to_pincode = driver.to_pincode
    driver_vehicle_type = driver.vehicle_type.lower().strip()

    # Filter passengers by destination pincode and vehicle type
    passengers = pas_Entry.objects.filter(
        to_pincode=driver_to_pincode,
        vehicle_type__iexact=driver_vehicle_type  # case-insensitive match
    )

    matched_passengers = []
    for passenger in passengers:
        if passenger.latitude is None or passenger.longitude is None:
            continue

        passenger_from_coords = (passenger.latitude, passenger.longitude)
        try:
            distance_km = geodesic(driver_from_coords, passenger_from_coords).km
            if distance_km <= 3:
                passenger.distance = round(distance_km, 2)
                matched_passengers.append(passenger)
        except:
            continue

    return render(request, 'passenger_list.html', {'passengers': matched_passengers})


#for tatal passanger list for earn

# views.py
from django.shortcuts import render
from geopy.distance import geodesic
from .models import pas_Entry, SupportEntry
from collections import Counter

def top_destinations(request):
    entries = pas_Entry.objects.all()
    selected_pincode = request.GET.get('pincode')

    if selected_pincode:
        entries = entries.filter(to_pincode=selected_pincode)

    # Latest driver
    driver = SupportEntry.objects.filter(user_type="driver").last()

    # Count top 3
    all_pincodes = [entry.to_pincode for entry in pas_Entry.objects.all() if entry.to_pincode]
    pincode_counts = Counter(all_pincodes)
    top_pincodes = pincode_counts.most_common(3)

    top_destinations = []
    for pincode, count in top_pincodes:
        area_entry = pas_Entry.objects.filter(to_pincode=pincode).first()
        area_name = area_entry.to_area if area_entry else "Unknown"
        top_destinations.append({'pincode': pincode, 'count': count, 'area': area_name})

    enriched_entries = []
    for entry in entries:
        if driver and entry.latitude and entry.longitude and driver.latitude and driver.longitude:
            distance_km = geodesic(
                (driver.latitude, driver.longitude),
                (entry.latitude, entry.longitude)
            ).km
        else:
            distance_km = 0

        enriched_entries.append({
            'name': entry.name,
            'phone_number': entry.number,
            'from_area': entry.area_name,
            'to_area': entry.to_area,
            'to_pincode': entry.to_pincode,
            'distance': round(distance_km, 2)
        })

    return render(request, 'earn.html', {
        'top_destinations': top_destinations,
        'passengers': enriched_entries,
        'selected_pincode': selected_pincode
    })

from django.shortcuts import redirect

def send_request_to_driver(request, driver_id, passenger_id):
    driver = get_object_or_404(DriverEntry, id=driver_id)
    passenger = get_object_or_404(PassengerEntry, id=passenger_id)

    obj, created = RideRequest.objects.get_or_create(driver=driver, passenger=passenger)
    obj.passenger_requested = True
    obj.save()

    return redirect('send_request_to_driver')  # Redirect to driver list after sending request

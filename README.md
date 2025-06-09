# JM Project

A smart ride-sharing platform where users can register as drivers or passengers, share their routes or requests, and get matched based on real-time location, vehicle type, and proximity. JM Project is designed for seamless and efficient ride matching with a user-friendly interface.

---

## ✅ User Authentication:
- Register and login as either a driver or passenger using your mobile number and password.
- Session-based user tracking using Django's session framework.

## ✅ Ride Matching & Management:
- Drivers and passengers are matched based on pickup and drop locations, vehicle type, and distance (within 3 km).
- Real-time geolocation using geopy and Nominatim.
- Both driver and passenger dashboards for managing rides and requests.
- Drivers can view requests and accept or reject passengers.

## ✅ Ride Progress & History:
- Track ride progress, from request to pickup to completion.
- Fare calculation based on distance (e.g., ₹9 per km).
- Passengers and drivers can view their ride history.

## ✅ Top Destinations Analytics:
- Passengers can see the most popular destinations based on community demand.

## ✅ Admin Management:
- Django Admin interface for managing users, rides, and analytics.

---

## ⚙️ Tech Stack:

| Component       | Technology              |
| --------------  | ---------------------- |
| Backend         | Django, Python         |
| Frontend        | HTML, CSS, Django Templates |
| Database        | MySQL                  |
| Geolocation     | geopy, Nominatim       |
| Session/Auth    | Django Sessions        |
| Hosting         | Localhost / Custom server ready |

---

## 🚦 How It Works

1. **Sign Up** as a Driver or Passenger.
2. **Login** to your dashboard.
3. **Passengers:** Enter pickup and destination locations, select vehicle type, and request a ride.
4. **Drivers:** Enter your available route and vehicle, and view matching passenger requests.
5. **Matchmaking:** System automatically matches drivers and passengers within a 3 km radius and matching destination.
6. **Ride Progress:** Track rides, mark as picked/completed, and view fare breakdown.
7. **Analytics:** View top destinations and ride statistics.

---

## 🏁 Getting Started

### Requirements

- Python 3.x
- Django 5.1.7
- MySQL Server
- pip (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Siva2960/JM-project.git
   cd JM-project
   ```

2. **Install dependencies:**
   ```bash
   pip install django==5.1.7 pymysql geopy django-extensions
   ```

3. **Configure MySQL Database:**
   - Create a database named `JM`
   - Update credentials in `JM/JM/settings.py` if needed

4. **Apply migrations:**
   ```bash
   python JM/manage.py makemigrations
   python JM/manage.py migrate
   ```

5. **Create superuser (optional, for admin):**
   ```bash
   python JM/manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   python JM/manage.py runserver
   ```

7. **Open** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🌐 Notes
- Ensure required templates (e.g., `dri_list.html`) are present in your templates directory.
- Update static and media file paths in `settings.py` if deploying on a server.
- For geolocation features, ensure internet access for geocoding APIs.

---

## 🔒 Security
- CSRF protection on all forms.
- Session-based login system.
- Restricted ride and request management to authenticated users.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

*For demo/educational purposes. Inspired by the Rythukart project structure.*

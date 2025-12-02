import os
import uuid
import json
from datetime import datetime, date, timedelta
from functools import wraps
from io import BytesIO

from flask import (
    Flask, render_template, request, redirect, url_for, flash, jsonify,
    session, abort, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask import send_file

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import Image as RLImage, KeepTogether
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.graphics.barcode import qr
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab import rl_config
from werkzeug.utils import secure_filename
import pathlib


# load environment
load_dotenv()

# -----------------------
# Config
# -----------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'Admin@2025')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI',
    'mysql+pymysql://username:admin@localhost:3306/oceanline_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Stripe config (optional)
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Admin credentials (simple)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')  # put secure pwd in .env

# Config file for persistent settings
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    """Load configuration from JSON file or return defaults"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'ferry_capacity': int(os.getenv('FERRY_CAPACITY', 35)), 'route_prices': {}}

def save_config(config):
    """Save configuration to JSON file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

# Load config
config = load_config()
FERRY_CAPACITY = config.get('ferry_capacity', int(os.getenv('FERRY_CAPACITY', 35)))

# -----------------------
# Extensions
# -----------------------
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


# -----------------------
# Models
# -----------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to bookings
    bookings = db.relationship('FerryBooking', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class FerryBooking(db.Model):
    __tablename__ = 'ferry_bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # user relationship (optional - for logged in users)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # passenger info
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)

    # outbound trip
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10), nullable=False)  # HH:MM

    # seats + price
    seats = db.Column(db.Integer, nullable=False)
    selected_seats = db.Column(db.String(200))  # Comma-separated seat numbers
    total_price = db.Column(db.Float, nullable=False)

    # payment fields
    payment_method = db.Column(db.String(50), nullable=True)
    payment_status = db.Column(db.String(30), nullable=True)
    payment_info = db.Column(db.String(300), nullable=True)  # filename or masked card info

    # optional return trip fields (nullable)
    is_roundtrip = db.Column(db.Boolean, default=False)
    return_date = db.Column(db.Date, nullable=True)
    return_time = db.Column(db.String(10), nullable=True)
    return_selected_seats = db.Column(db.String(200))  # Comma-separated seat numbers for return

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'booking_reference': self.booking_reference,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'departure': self.departure,
            'destination': self.destination,
            'date': self.date.isoformat(),
            'time': self.time,
            'seats': self.seats,
            'selected_seats': self.selected_seats,
            'total_price': self.total_price,
            'is_roundtrip': self.is_roundtrip,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'return_time': self.return_time,
            'return_selected_seats': self.return_selected_seats,
            'created_at': self.created_at.isoformat()
        }


class Schedule(db.Model):
    """
    Recurring schedule entries (route -> time). Admin-managed.
    Each schedule represents a recurring departure time for a route.
    """
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(10), nullable=False)  # HH:MM
    # optional: note or active flag
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DailySchedule(db.Model):
    """
    Date-specific schedule entries. Used when admin wants schedules for specific dates.
    """
    __tablename__ = 'daily_schedules'
    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.String(10), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -----------------------
# Complete route prices and schedules
# -----------------------
# All routes from Male to every destination
MALE_ROUTES = {
    ('Male', 'Hulhumale'): 100,
    ('Male', 'K.Maafushi'): 200,
    ('Male', 'K.Guraidhoo'): 200,
    ('Male', 'K.Dhiffushi'): 300,
    ('Male', 'AA.Rasdhoo'): 300,
    ('Male', 'V.Thinadhoo'): 300,
    ('Male', 'Velana International Airport'): 100,
}

# All routes from Velana International Airport to every destination
AIRPORT_ROUTES = {
    ('Velana International Airport', 'Male'): 100,
    ('Velana International Airport', 'Hulhumale'): 100,
    ('Velana International Airport', 'K.Maafushi'): 200,
    ('Velana International Airport', 'K.Guraidhoo'): 200,
    ('Velana International Airport', 'K.Dhiffushi'): 300,
    ('Velana International Airport', 'AA.Rasdhoo'): 300,
    ('Velana International Airport', 'V.Thinadhoo'): 300,
}

# Combine all route prices
ROUTE_PRICES = {**MALE_ROUTES, **AIRPORT_ROUTES}

# Load custom prices from config
custom_prices = config.get('route_prices', {})
for route_key, price in custom_prices.items():
    # Convert string key back to tuple (e.g., "Male,Hulhumale" -> ("Male", "Hulhumale"))
    if ',' in route_key:
        dep, dest = route_key.split(',', 1)
        ROUTE_PRICES[(dep, dest)] = price

# Ensure reverse routes have prices when logically symmetric and missing
for (dep, dest), price in list(ROUTE_PRICES.items()):
    if (dest, dep) not in ROUTE_PRICES:
        ROUTE_PRICES[(dest, dep)] = price

# Fallback times for each route (when no schedule exists in database)
FALLBACK_ROUTE_TIMES = {
    ('Male', 'Hulhumale'): ['08:00', '10:00', '14:00', '18:00'],
    ('Male', 'K.Maafushi'): ['09:00', '13:00', '17:00'],
    ('Male', 'K.Guraidhoo'): ['07:30', '12:00', '16:00'],
    ('Male', 'K.Dhiffushi'): ['08:30', '15:00'],
    ('Male', 'AA.Rasdhoo'): ['09:30', '14:30'],
    ('Male', 'V.Thinadhoo'): ['07:00', '16:30'],
    ('Male', 'Velana International Airport'): ['07:00', '11:00', '15:00'],
    
    ('Velana International Airport', 'Male'): ['07:00', '11:00', '15:00'],
    ('Velana International Airport', 'Hulhumale'): ['08:00', '12:00', '16:00'],
    ('Velana International Airport', 'K.Maafushi'): ['09:00', '13:00', '17:00'],
    ('Velana International Airport', 'K.Guraidhoo'): ['07:30', '12:00', '16:00'],
    ('Velana International Airport', 'K.Dhiffushi'): ['08:30', '15:00'],
    ('Velana International Airport', 'AA.Rasdhoo'): ['09:30', '14:30'],
    ('Velana International Airport', 'V.Thinadhoo'): ['07:00', '16:30'],
}

# Default schedules for each route
SCHEDULES = {
    ('Male', 'Hulhumale'): ['08:00', '12:00', '16:00'],
    ('Male', 'K.Maafushi'): ['09:00', '13:00', '17:00'],
    ('Male', 'K.Guraidhoo'): ['07:30', '12:00', '16:00'],
    ('Male', 'K.Dhiffushi'): ['08:30', '15:00'],
    ('Male', 'AA.Rasdhoo'): ['09:30', '14:30'],
    ('Male', 'V.Thinadhoo'): ['07:00', '16:30'],
    ('Male', 'Velana International Airport'): ['07:00', '11:00', '15:00'],
    
    ('Velana International Airport', 'Male'): ['07:00', '11:00', '15:00'],
    ('Velana International Airport', 'Hulhumale'): ['08:00', '12:00', '16:00'],
    ('Velana International Airport', 'K.Maafushi'): ['09:00', '13:00', '17:00'],
    ('Velana International Airport', 'K.Guraidhoo'): ['07:30', '12:00', '16:00'],
    ('Velana International Airport', 'K.Dhiffushi'): ['08:30', '15:00'],
    ('Velana International Airport', 'AA.Rasdhoo'): ['09:30', '14:30'],
    ('Velana International Airport', 'V.Thinadhoo'): ['07:00', '16:30'],
}


# -----------------------
# Helper utilities
# -----------------------
def admin_required(fn):
    """Decorator to protect admin routes - uses session flag."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login', next=request.path))
        return fn(*args, **kwargs)
    return wrapper


def available_times_for_route(dep, dest, target_date: date):
    """
    Return list of times (strings) for a route and date where seats are still available.
    We look up Schedule entries first (active ones). If none exist, we use FALLBACK_ROUTE_TIMES.
    Then filter out times where already booked seats >= FERRY_CAPACITY.
    """
    key = (dep, dest)
    # First check for any date-specific schedules
    daily = DailySchedule.query.filter_by(departure=dep, destination=dest, date=target_date, active=True).order_by(DailySchedule.time).all()
    if daily:
        times = [d.time for d in daily]
    else:
        # query recurring schedule
        schedules = Schedule.query.filter_by(departure=dep, destination=dest, active=True).order_by(Schedule.time).all()
        if schedules:
            times = [s.time for s in schedules]
        else:
            times = FALLBACK_ROUTE_TIMES.get(key, [])

    # filter by seat availability for the specific date/time
    available = []
    for t in times:
        booked = db.session.query(db.func.coalesce(db.func.sum(FerryBooking.seats), 0)).filter(
            FerryBooking.departure == dep,
            FerryBooking.destination == dest,
            FerryBooking.date == target_date,
            FerryBooking.time == t
        ).scalar() or 0

        if booked < FERRY_CAPACITY:
            available.append(t)
    return available


def seats_left(dep, dest, target_date: date, ttime: str):
    booked = db.session.query(db.func.coalesce(db.func.sum(FerryBooking.seats), 0)).filter(
        FerryBooking.departure == dep,
        FerryBooking.destination == dest,
        FerryBooking.date == target_date,
        FerryBooking.time == ttime
    ).scalar() or 0
    return max(0, FERRY_CAPACITY - booked)


def get_taken_seats(dep, dest, date, time):
    """Get all seats that are already taken for this trip"""
    taken_seats = set()
    bookings = FerryBooking.query.filter_by(
        departure=dep,
        destination=dest,
        date=date,
        time=time
    ).all()
    
    for booking in bookings:
        if booking.selected_seats:
            for seat in booking.selected_seats.split(','):
                if seat.strip():
                    taken_seats.add(int(seat.strip()))
    
    return taken_seats


def get_taken_seats_return(dep, dest, date, time):
    """Get all seats that are already taken for return trip"""
    taken_seats = set()
    bookings = FerryBooking.query.filter_by(
        departure=dep,
        destination=dest,
        return_date=date,
        return_time=time
    ).all()
    
    for booking in bookings:
        if booking.return_selected_seats:
            for seat in booking.return_selected_seats.split(','):
                if seat.strip():
                    taken_seats.add(int(seat.strip()))
    
    return taken_seats


# -----------------------
# PDF Generation
# -----------------------

def generate_pdf_receipt(booking):
    # Professional ferry receipt - optimized for single A4 page
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=35, rightMargin=35, topMargin=30, bottomMargin=30)
    rl_config.pageCompression = 1

    # Color palette
    primary_blue = colors.HexColor('#2663EB')
    dark_blue = colors.HexColor('#0E3A96')
    light_blue = colors.HexColor('#DCEAFF')
    orange = colors.HexColor('#F25809')
    light_orange = colors.HexColor('#FFF2E6')
    gray_text = colors.HexColor('#6B7280')
    dark_text = colors.HexColor('#111827')

    styles = getSampleStyleSheet()
    
    elements = []

    # Compact top header
    header_data = [
        [Paragraph('<b>Ferry Booking Confirmation</b>', ParagraphStyle('h1', fontSize=16, textColor=colors.white, alignment=1, spaceAfter=2))],
        [Paragraph('OceanLine Ferry Service', ParagraphStyle('h2', fontSize=8, textColor=colors.white, alignment=1, spaceAfter=1))],
        [Paragraph(f'{booking.booking_reference} - {booking.name}', ParagraphStyle('h3', fontSize=5.5, textColor=colors.white, alignment=1))]
    ]
    header_table = Table(header_data, colWidths=[doc.width])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 2), primary_blue),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (0, 1), 6),
        ('BOTTOMPADDING', (0, 2), (0, 2), 10),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 6))

    # Centered QR Code
    qr_code = QrCodeWidget(booking.booking_reference)
    bounds = qr_code.getBounds()
    qr_size = 65
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(qr_size, qr_size)
    d.scale(qr_size / width, qr_size / height)
    d.add(qr_code)
    
    # Center the QR code
    qr_table = Table([[d]], colWidths=[doc.width])
    qr_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
    elements.append(qr_table)
    elements.append(Spacer(1, 5))

    # Compact Booking Reference Box
    ref_box = Table([[Paragraph(f'<b>BOOKING REFERENCE</b>', ParagraphStyle('rb1', fontSize=6, textColor=dark_blue, alignment=1))],
                     [Paragraph(f'<font size=10><b>{booking.booking_reference}</b></font>', ParagraphStyle('rb2', fontSize=10, textColor=dark_blue, alignment=1))]], 
                    colWidths=[doc.width])
    ref_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_blue),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
    ]))
    elements.append(ref_box)
    elements.append(Spacer(1, 8))

    # Journey Details Section
    trip_type = "Two-Way Trip" if booking.is_roundtrip else "One-Way Trip"
    elements.append(Paragraph(f'<b>Journey Details - {trip_type}</b>', ParagraphStyle('sec', fontSize=9, textColor=primary_blue, spaceAfter=3)))
    elements.append(Table([['']], colWidths=[doc.width], style=TableStyle([('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.HexColor('#E5E7EB'))])))
    elements.append(Spacer(1, 5))

    # Departure Trip - compact
    dep_header = Table([[Paragraph('<b>DEPARTURE TRIP</b>', ParagraphStyle('dh', fontSize=7, textColor=dark_blue, alignment=1))]], colWidths=[doc.width])
    dep_header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_blue),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    elements.append(dep_header)
    elements.append(Spacer(1, 4))

    # Compact departure details
    dep_data = [
        [Paragraph('<b>ROUTE</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(f'{booking.departure} to {booking.destination}', ParagraphStyle('val', fontSize=7, textColor=dark_text)),
         Paragraph('<b>DURATION</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph('90 min', ParagraphStyle('val', fontSize=7, textColor=dark_text))],
        [Paragraph('<b>FROM</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(booking.departure, ParagraphStyle('val', fontSize=7, textColor=dark_text)),
         Paragraph('<b>TO</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(booking.destination, ParagraphStyle('val', fontSize=7, textColor=dark_text))],
        [Paragraph('<b>DATE</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(booking.date.strftime('%A, %B %d, %Y'), ParagraphStyle('val', fontSize=7, textColor=dark_text)),
         Paragraph('<b>TIME</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(booking.time, ParagraphStyle('val', fontSize=7, textColor=dark_text))],
    ]
    
    dep_table = Table(dep_data, colWidths=[60, doc.width/2 - 70, 60, doc.width/2 - 70])
    dep_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(dep_table)
    elements.append(Spacer(1, 3))

    # Departure seat badges - compact
    elements.append(Paragraph('<b>SEATS</b>', ParagraphStyle('sl', fontSize=6, textColor=gray_text)))
    if booking.selected_seats:
        seat_badges = []
        for seat in booking.selected_seats.split(',')[:8]:  # Limit seats shown
            seat_badge = Table([[Paragraph(f'<b>{seat.strip()}</b>', ParagraphStyle('sb', fontSize=6, textColor=colors.white, alignment=1))]], colWidths=[24])
            seat_badge.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), primary_blue),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('ROUNDEDCORNERS', [3, 3, 3, 3]),
            ]))
            seat_badges.append(seat_badge)
        
        seats_row = Table([seat_badges], colWidths=[28] * len(seat_badges))
        seats_row.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 2)]))
        elements.append(seats_row)
    
    elements.append(Spacer(1, 7))

    # Return Trip if round trip - very compact
    if booking.is_roundtrip and booking.return_date and booking.return_time:
        ret_header = Table([[Paragraph('<b>RETURN TRIP</b>', ParagraphStyle('rh', fontSize=7, textColor=orange, alignment=1))]], colWidths=[doc.width])
        ret_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), light_orange),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        elements.append(ret_header)
        elements.append(Spacer(1, 4))

        ret_data = [
            [Paragraph('<b>ROUTE</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
             Paragraph(f'{booking.destination} to {booking.departure}', ParagraphStyle('val', fontSize=7, textColor=dark_text)),
             Paragraph('<b>DURATION</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
             Paragraph('90 min', ParagraphStyle('val', fontSize=7, textColor=dark_text))],
            [Paragraph('<b>FROM</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
             Paragraph(booking.destination, ParagraphStyle('val', fontSize=7, textColor=dark_text)),
             Paragraph('<b>TO</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
             Paragraph(booking.departure, ParagraphStyle('val', fontSize=7, textColor=dark_text))],
            [Paragraph('<b>DATE</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
             Paragraph(booking.return_date.strftime('%A, %B %d, %Y'), ParagraphStyle('val', fontSize=7, textColor=dark_text)),
             Paragraph('<b>TIME</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
             Paragraph(booking.return_time, ParagraphStyle('val', fontSize=7, textColor=dark_text))],
        ]

        ret_table = Table(ret_data, colWidths=[60, doc.width/2 - 70, 60, doc.width/2 - 70])
        ret_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(ret_table)
        elements.append(Spacer(1, 3))

        # Return seat badges
        elements.append(Paragraph('<b>SEATS</b>', ParagraphStyle('sl', fontSize=6, textColor=gray_text)))
        if booking.return_selected_seats:
            ret_seat_badges = []
            for seat in booking.return_selected_seats.split(',')[:8]:
                seat_badge = Table([[Paragraph(f'<b>{seat.strip()}</b>', ParagraphStyle('rsb', fontSize=6, textColor=colors.white, alignment=1))]], colWidths=[24])
                seat_badge.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), orange),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ('ROUNDEDCORNERS', [3, 3, 3, 3]),
                ]))
                ret_seat_badges.append(seat_badge)
            
            ret_seats_row = Table([ret_seat_badges], colWidths=[28] * len(ret_seat_badges))
            ret_seats_row.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 2)]))
            elements.append(ret_seats_row)
        
        elements.append(Spacer(1, 7))

    # Passenger Information - compact
    elements.append(Paragraph('<b>Passenger Information</b>', ParagraphStyle('sec2', fontSize=9, textColor=primary_blue, spaceAfter=3)))
    elements.append(Table([['']], colWidths=[doc.width], style=TableStyle([('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.HexColor('#E5E7EB'))])))
    elements.append(Spacer(1, 5))

    pass_data = [
        [Paragraph('<b>NAME</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(booking.name, ParagraphStyle('val', fontSize=7, textColor=dark_text)),
         Paragraph('<b>PASSENGERS</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(str(booking.seats), ParagraphStyle('val', fontSize=7, textColor=dark_text))],
        [Paragraph('<b>EMAIL</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(booking.email, ParagraphStyle('val', fontSize=7, textColor=dark_text)),
         Paragraph('<b>PHONE</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(booking.phone, ParagraphStyle('val', fontSize=7, textColor=dark_text))],
        [Paragraph('<b>PAYMENT METHOD</b>', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph(booking.payment_method if booking.payment_method else '—', ParagraphStyle('val', fontSize=7, textColor=dark_text)),
         Paragraph('', ParagraphStyle('lbl', fontSize=6, textColor=gray_text)),
         Paragraph('', ParagraphStyle('val', fontSize=7, textColor=dark_text))],
    ]

    pass_table = Table(pass_data, colWidths=[60, doc.width/2 - 70, 80, doc.width/2 - 90])
    pass_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(pass_table)
    elements.append(Spacer(1, 10))

    # Total Amount Box - compact
    total_box = Table([
        [Paragraph('<b>TOTAL AMOUNT PAID</b>', ParagraphStyle('tb1', fontSize=7, textColor=dark_blue, alignment=1))],
        [Paragraph(f'<font size=12><b>MVR {booking.total_price:.2f}</b></font>', ParagraphStyle('tb2', fontSize=12, textColor=primary_blue, alignment=1))]
    ], colWidths=[doc.width])
    total_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_blue),
        ('BOX', (0, 0), (-1, -1), 1.5, primary_blue),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    elements.append(total_box)
    elements.append(Spacer(1, 8))

    # Footer line
    elements.append(Table([['']], colWidths=[doc.width], style=TableStyle([('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.HexColor('#E5E7EB'))])))
    elements.append(Spacer(1, 4))

    # Compact footer text
    footer_style = ParagraphStyle('footer', fontSize=6, textColor=gray_text, alignment=1, leading=7)
    elements.append(Paragraph('Important: Please arrive at the ferry terminal at least 30 minutes before departure.', footer_style))
    elements.append(Paragraph('For any queries, contact us at support@oceanlineferry.com', footer_style))
    elements.append(Paragraph('Thank you for choosing OceanLine Ferry Service!', footer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# -----------------------
# Routes: Public (homepage, booking)
# -----------------------
PORTS = [
    'Male',
    'Hulhumale',
    'Velana International Airport',
    'K.Maafushi',
    'K.Dhiffushi',
    'K.Guraidhoo',
    'AA.Rasdhoo',
    'V.Thinadhoo',
]


# -----------------------
# Routes: Authentication
# -----------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([name, email, password]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('register'))
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists. Please login.', 'warning')
            return redirect(url_for('login'))
        
        # Create new user
        new_user = User(email=email, name=name, phone=phone)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to next page or index
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/')
def index():
    # homepage — shows highlights, quick book CTA; templates/index.html should be beautiful.
    # pass ROUTE_PRICES so templates that preview routes can access pricing
    # also provide today's date for template defaults
    today = date.today()
    return render_template('index.html', ports=PORTS, ROUTE_PRICES=ROUTE_PRICES, today=today)


@app.route('/get_price', methods=['POST'])
@csrf.exempt
def get_price():
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    if not departure or not destination:
        return jsonify({'error': 'missing'}), 400

    # robust lookup: try exact, then case-insensitive match on keys
    key = (departure, destination)
    price = ROUTE_PRICES.get(key)
    if price is None:
        # try normalized lookup
        dep_norm = departure.strip().lower()
        dest_norm = destination.strip().lower()
        for (kdep, kdest), p in ROUTE_PRICES.items():
            if kdep.strip().lower() == dep_norm and kdest.strip().lower() == dest_norm:
                price = p
                break

    # if still not found, try reverse route (maybe price symmetric)
    if price is None:
        rev_key = (destination, departure)
        price = ROUTE_PRICES.get(rev_key)
        if price is None:
            # try normalized reverse lookup
            rev_dep_norm = destination.strip().lower()
            rev_dest_norm = departure.strip().lower()
            for (kdep, kdest), p in ROUTE_PRICES.items():
                if kdep.strip().lower() == rev_dep_norm and kdest.strip().lower() == rev_dest_norm:
                    price = p
                    break

    if price is None:
        return jsonify({'error': 'no_price'}), 404
    return jsonify({'price': price})


@app.route('/get_timesold', methods=['POST'])
@csrf.exempt
def get_timesold():
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    date_str = request.form.get('date')
    if not (departure and destination and date_str):
        return jsonify({'error': 'missing'}), 400

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'bad_date'}), 400

    times = available_times_for_route(departure, destination, target_date)
    return jsonify({'times': times})


@app.route('/cancel/<int:id>')
def cancel(id):
    booking = FerryBooking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking cancelled successfully', 'success')
    return redirect(url_for('bookings'))


@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    """
    Handles both one-way and round-trip bookings.
    Expected form fields (POST):
      - name, email, phone
      - trip_type ('oneway'|'round')
      - departure, destination
      - date, time
      - seats
      - if roundtrip: return_date, return_time
    """
    if request.method == 'POST':
        # Basic validation (you can expand)
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        trip_type = request.form.get('trip_type', 'oneway')
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        seats = int(request.form.get('seats') or 0)

        if not all([name, email, phone, departure, destination, date_str, time_str, seats]):
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('book'))

        try:
            travel_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid travel date.', 'danger')
            return redirect(url_for('book'))

        # seat availability check for outbound
        outbound_booked = db.session.query(db.func.coalesce(db.func.sum(FerryBooking.seats), 0)).filter(
            FerryBooking.departure == departure,
            FerryBooking.destination == destination,
            FerryBooking.date == travel_date,
            FerryBooking.time == time_str
        ).scalar() or 0

        if outbound_booked + seats > FERRY_CAPACITY:
            flash(f'Not enough seats for outbound. Only {FERRY_CAPACITY - outbound_booked} left.', 'danger')
            return redirect(url_for('book'))

        # price calculation
        price_per_seat = ROUTE_PRICES.get((departure, destination))
        if price_per_seat is None:
            flash('Route not available', 'danger')
            return redirect(url_for('book'))

        total_price = price_per_seat * seats

        # prepare booking
        booking_ref = str(uuid.uuid4())[:8].upper()
        booking = FerryBooking(
            booking_reference=booking_ref,
            name=name,
            email=email,
            phone=phone,
            departure=departure,
            destination=destination,
            date=travel_date,
            time=time_str,
            seats=seats,
            total_price=total_price,
            is_roundtrip=(trip_type == 'round'),
            user_id=current_user.id
        )

        # if round-trip, store return fields (simple approach)
        if trip_type == 'round':
            return_date_str = request.form.get('return_date')
            return_time_str = request.form.get('return_time')

            if not (return_date_str and return_time_str):
                flash('Please select return date and time for round-trip.', 'danger')
                return redirect(url_for('book'))

            try:
                return_date_val = datetime.strptime(return_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid return date.', 'danger')
                return redirect(url_for('book'))

            # check return seat availability (note: return route is reversed)
            return_booked = db.session.query(db.func.coalesce(db.func.sum(FerryBooking.seats), 0)).filter(
                FerryBooking.departure == destination,
                FerryBooking.destination == departure,
                FerryBooking.date == return_date_val,
                FerryBooking.time == return_time_str
            ).scalar() or 0

            if return_booked + seats > FERRY_CAPACITY:
                flash(f'Not enough seats for return. Only {FERRY_CAPACITY - return_booked} left.', 'danger')
                return redirect(url_for('book'))

            # price for return (assuming same price)
            return_price = ROUTE_PRICES.get((destination, departure), price_per_seat)
            total_price += return_price * seats

            # set return info on booking
            booking.return_date = return_date_val
            booking.return_time = return_time_str
            booking.total_price = total_price

        # save booking to generate booking reference
        db.session.add(booking)
        db.session.commit()

        # Store booking info in session for seat selection
        session['temp_booking'] = {
            'booking_id': booking.id,
            'departure': departure,
            'destination': destination,
            'date': date_str,
            'time': time_str,
            'seats': seats,
            'is_roundtrip': (trip_type == 'round'),
            'return_date': return_date_str if trip_type == 'round' else None,
            'return_time': return_time_str if trip_type == 'round' else None
        }

        # Redirect to seat selection page
        return redirect(url_for('select_seats'))

    # GET - support prefill via query string (quick-book links)
    # Also pre-fill user info if logged in
    initial = {
        'departure': request.args.get('departure', ''),
        'destination': request.args.get('destination', ''),
        'date': request.args.get('date', ''),
        'time': request.args.get('time', ''),
        'seats': request.args.get('seats', ''),
        'name': current_user.name if current_user.is_authenticated else '',
        'email': current_user.email if current_user.is_authenticated else '',
        'phone': current_user.phone if current_user.is_authenticated else ''
    }
    return render_template('book.html', ports=PORTS, initial=initial)


@app.route('/select_seats', methods=['GET', 'POST'])
def select_seats():
    temp_booking = session.get('temp_booking')

    if not temp_booking:
        flash('No booking in progress. Please start a new booking.', 'danger')
        return redirect(url_for('book'))

    # Seats required (force integer)
    seats_required = int(temp_booking.get('seats', 0))

    # ------------------------ POST SUBMISSION ------------------------
    if request.method == 'POST':

        # ---------------- OUTBOUND SEATS ----------------
        selected_seats_raw = request.form.get('seats', '')  # "1,5" string
        selected_seats = [s.strip() for s in selected_seats_raw.split(',') if s.strip()]

        if len(selected_seats) != seats_required:
            flash(f'Please select exactly {seats_required} outbound seat(s).', 'danger')
            return redirect(url_for('select_seats'))

        # Load booking
        booking = FerryBooking.query.get(temp_booking['booking_id'])
        if not booking:
            flash('Booking not found.', 'danger')
            return redirect(url_for('book'))

        booking.selected_seats = ",".join(selected_seats)

        # ---------------- RETURN SEATS (IF ROUND TRIP) ----------------
        if temp_booking.get('is_roundtrip'):
            return_raw = request.form.get('return_seats', '')
            return_seats = [s.strip() for s in return_raw.split(',') if s.strip()]

            if len(return_seats) != seats_required:
                flash(f'Please select exactly {seats_required} return seat(s).', 'danger')
                return redirect(url_for('select_seats'))

            booking.return_selected_seats = ",".join(return_seats)

        # Save to DB
        db.session.commit()

        # Store reference in session for payment page
        session['payment_booking_ref'] = booking.booking_reference

        flash(f'Seats selected! Reference: {booking.booking_reference}', 'success')
        return redirect(url_for('payment', ref=booking.booking_reference))

    # ------------------------ GET (SHOW SEAT PAGE) ------------------------
    departure = temp_booking['departure']
    destination = temp_booking['destination']
    date = temp_booking['date']
    time = temp_booking['time']

    is_roundtrip = temp_booking.get('is_roundtrip', False)
    return_date = temp_booking.get('return_date')
    return_time = temp_booking.get('return_time')

    # Convert date strings safely
    trip_date = datetime.strptime(date, '%Y-%m-%d').date()

    # Get taken seats for outbound
    taken_seats = get_taken_seats(departure, destination, trip_date, time)

    # Return trip seats
    return_taken_seats = []
    if is_roundtrip and return_date and return_time:
        r_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        return_taken_seats = get_taken_seats_return(destination, departure, r_date, return_time)

    return render_template(
        'select_seats.html',
        departure=departure,
        destination=destination,
        date=date,
        time=time,
        seats_needed=seats_required,   # IMPORTANT: int only
        taken_seats=taken_seats,
        is_roundtrip=is_roundtrip,
        return_date=return_date,
        return_time=return_time,
        return_taken_seats=return_taken_seats
    )



@app.route('/payment/<ref>', methods=['GET', 'POST'])
def payment(ref):
    """Handle payment for a booking after seats have been selected"""
    booking = FerryBooking.query.filter_by(booking_reference=ref).first_or_404()
    
    # Ensure seats have been selected
    if not booking.selected_seats:
        flash('Please select your seats first.', 'warning')
        return redirect(url_for('select_seats'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        booking.payment_method = payment_method
        
        # Handle file uploads directory
        uploads_dir = os.path.join(app.root_path, 'uploads')
        pathlib.Path(uploads_dir).mkdir(parents=True, exist_ok=True)
        
        if payment_method == 'Bank Transfer':
            slip = request.files.get('bank_slip')
            if slip and slip.filename:
                filename = secure_filename(f"{booking.booking_reference}_" + slip.filename)
                save_path = os.path.join(uploads_dir, filename)
                slip.save(save_path)
                booking.payment_status = 'pending'
                booking.payment_info = filename
            else:
                booking.payment_status = 'pending'
                booking.payment_info = None
        
        elif payment_method == 'Card':
            card_number = request.form.get('card_number', '')
            card_expiry = request.form.get('card_expiry', '')
            card_cvc = request.form.get('card_cvc', '')
            masked = None
            if card_number:
                masked = '**** **** **** ' + card_number[-4:]
            booking.payment_status = 'paid'
            booking.payment_info = f"card:{masked} exp:{card_expiry}"
        
        else:
            # Stripe or PayPal - mark as redirected
            booking.payment_status = 'redirected'
            booking.payment_info = payment_method
        
        # Save payment info
        db.session.commit()
        
        # Clear temporary session data
        session.pop('temp_booking', None)
        session.pop('payment_booking_ref', None)
        
        # Store reference for confirmation
        session['last_booking_ref'] = booking.booking_reference
        
        flash(f'Payment processed! Booking Reference: {booking.booking_reference}', 'success')
        return redirect(url_for('confirmation', ref=booking.booking_reference))
    
    # GET - show payment form
    return render_template('payment.html', booking=booking)


@app.route('/confirmation/<ref>')
def confirmation(ref):
    booking = FerryBooking.query.filter_by(booking_reference=ref).first_or_404()
    outbound_price = ROUTE_PRICES.get((booking.departure, booking.destination))
    return_price = ROUTE_PRICES.get((booking.destination, booking.departure)) if booking.is_roundtrip else None
    return render_template('confirmation.html', booking=booking, outbound_price=outbound_price, return_price=return_price)


@app.route('/post-booking/<ref>')
def post_booking(ref):
    booking = FerryBooking.query.filter_by(booking_reference=ref).first_or_404()
    return render_template('post_booking.html', booking=booking)


@app.route('/my-booking')
def my_booking():
    """Booking summary page - shows last booking from session if present"""
    ref = session.get('last_booking_ref')
    if not ref:
        flash('No recent booking found.', 'info')
        return redirect(url_for('index'))
    return redirect(url_for('confirmation', ref=ref))


@app.route('/bookings')
@login_required
def bookings():
    """Show logged-in user's bookings only"""
    user_bookings = FerryBooking.query.filter_by(user_id=current_user.id).order_by(FerryBooking.created_at.desc()).all()
    return render_template('bookings.html', bookings=user_bookings)


@app.route('/get_times', methods=['POST'])
def get_times():
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    date_str = request.form.get('date')
    # Use the unified availability helper which prefers DailySchedule (date-specific)
    if not (departure and destination and date_str):
        return jsonify([])
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify([])

    times = available_times_for_route(departure, destination, target_date)
    return jsonify(times)

@app.route('/get_available_seats', methods=['POST'])
def get_available_seats():
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    date_str = request.form.get('date')
    time = request.form.get('time')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    booked_seats = db.session.query(db.func.sum(FerryBooking.seats)).filter_by(
        departure=departure,
        destination=destination,
        date=date,
        time=time
    ).scalar() or 0
    available = FERRY_CAPACITY - booked_seats
    return jsonify({'available': available})

# Route to generate PDF receipt
@app.route('/pay', methods=['POST'])
def pay():
    # In production, integrate payment gateways
    # Here we simulate success and generate PDF receipt
    booking_ref = request.form.get('booking_ref')
    
    # Get booking details
    booking = FerryBooking.query.filter_by(booking_reference=booking_ref).first_or_404()
    
    # Generate PDF
    pdf_buffer = generate_pdf_receipt(booking)
    
    # Return PDF as download
    return send_file(
        pdf_buffer,
        download_name=f"OceanLine_Booking_{booking_ref}.pdf",
        as_attachment=True
    )


@app.route('/available_seats')
def available_seats():
    """Return a simple page showing route availability summary"""
    # Date-specific schedules (upcoming)
    today = date.today()
    daily = DailySchedule.query.filter(DailySchedule.date >= today, DailySchedule.active == True).order_by(DailySchedule.date, DailySchedule.departure, DailySchedule.time).all()

    daily_list = []
    for d in daily:
        avail = seats_left(d.departure, d.destination, d.date, d.time)
        daily_list.append({
            'id': d.id,
            'date': d.date,
            'departure': d.departure,
            'destination': d.destination,
            'time': d.time,
            'available_seats': avail,
            'active': d.active
        })

    # Recurring schedules grouped by route
    recurring = {}
    schedules = Schedule.query.filter(Schedule.active == True).order_by(Schedule.departure, Schedule.destination, Schedule.time).all()
    for s in schedules:
        key = (s.departure, s.destination)
        recurring.setdefault(key, []).append(s.time)

    # fall back to FALLBACK_ROUTE_TIMES for any route missing schedules
    for key, times in FALLBACK_ROUTE_TIMES.items():
        if key not in recurring:
            recurring[key] = times

    return render_template('available_seats.html', daily_schedules=daily_list, recurring=recurring)


@app.route('/uploads/<path:filename>')
@admin_required
def uploaded_file(filename):
    uploads_dir = os.path.join(app.root_path, 'uploads')
    return send_from_directory(uploads_dir, filename, as_attachment=True)


@app.route('/admin/payments')
@admin_required
def admin_payments():
    bookings = FerryBooking.query.filter(FerryBooking.payment_status.in_(['pending','redirected'])).order_by(FerryBooking.created_at.desc()).all()
    return render_template('admin/payments.html', bookings=bookings)


@app.route('/admin/payments/<int:id>/confirm', methods=['POST'])
@admin_required
def admin_confirm_payment(id):
    b = FerryBooking.query.get_or_404(id)
    b.payment_status = 'paid'
    db.session.commit()
    flash('Payment marked as paid.', 'success')
    return redirect(url_for('admin_payments'))


@app.route('/create-checkout-session/<ref>')
def create_checkout_session(ref):
    booking = FerryBooking.query.filter_by(booking_reference=ref).first_or_404()
    if not STRIPE_SECRET_KEY:
        flash('Stripe is not configured on this server.', 'danger')
        return redirect(url_for('confirmation', ref=ref))

    try:
        import stripe
    except Exception:
        flash('Stripe library is not installed. Install `stripe` package to enable checkout.', 'danger')
        return redirect(url_for('confirmation', ref=ref))

    stripe.api_key = STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Ferry {booking.departure} → {booking.destination}'},
                    'unit_amount': int(booking.total_price * 100)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('stripe_success', ref=ref, _external=True),
            cancel_url=url_for('confirmation', ref=ref, _external=True),
            metadata={'booking_ref': ref}
        )
    except Exception as e:
        flash('Failed to create Stripe session: ' + str(e), 'danger')
        return redirect(url_for('confirmation', ref=ref))

    return redirect(session.url, code=303)


@app.route('/stripe/success')
def stripe_success():
    ref = request.args.get('ref')
    flash('Payment completed (webhook will confirm and update booking).', 'success')
    if ref:
        return redirect(url_for('confirmation', ref=ref))
    return redirect(url_for('index'))


@app.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    if not STRIPE_WEBHOOK_SECRET:
        return 'Webhook not configured', 400
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        return str(e), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        ref = session.get('metadata', {}).get('booking_ref')
        if ref:
            b = FerryBooking.query.filter_by(booking_reference=ref).first()
            if b:
                b.payment_status = 'paid'
                db.session.commit()
    return '', 200


# -----------------------
# Admin routes
# -----------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            flash('Welcome, admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials.', 'danger')
        return redirect(url_for('admin_login'))
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Logged out.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin landing: show quick stats"""
    total_bookings = FerryBooking.query.count()
    upcoming = FerryBooking.query.filter(FerryBooking.date >= datetime.utcnow().date()).count()
    total_schedules = Schedule.query.count()
    
    # Calculate daily revenue (today) - Database agnostic
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    daily_revenue = db.session.query(db.func.sum(FerryBooking.total_price)).filter(
        FerryBooking.created_at >= today,
        FerryBooking.created_at < tomorrow
    ).scalar() or 0
    
    # Calculate monthly revenue (current month) - Database agnostic
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    if current_month == 12:
        month_start = datetime(current_year, current_month, 1)
        month_end = datetime(current_year + 1, 1, 1)
    else:
        month_start = datetime(current_year, current_month, 1)
        month_end = datetime(current_year, current_month + 1, 1)
    
    monthly_revenue = db.session.query(db.func.sum(FerryBooking.total_price)).filter(
        FerryBooking.created_at >= month_start,
        FerryBooking.created_at < month_end
    ).scalar() or 0
    
    # Total all-time revenue
    total_revenue = db.session.query(db.func.sum(FerryBooking.total_price)).scalar() or 0
    
    return render_template(
        'admin/dashboard.html',
        total_bookings=total_bookings,
        upcoming=upcoming,
        total_schedules=total_schedules,
        daily_revenue=daily_revenue,
        monthly_revenue=monthly_revenue,
        total_revenue=total_revenue
    )


@app.route('/admin/reports')
@admin_required
def admin_reports():
    """Admin reports page with revenue analytics"""
    from collections import defaultdict
    from calendar import month_name
    
    # Get date filter from query params
    filter_type = request.args.get('filter', 'month')  # 'day', 'month', 'year'
    
    today = datetime.utcnow().date()
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    # Daily revenue (last 30 days) - Database agnostic approach
    daily_stats = []
    for i in range(29, -1, -1):
        target_date = today - timedelta(days=i)
        next_date = target_date + timedelta(days=1)
        revenue = db.session.query(db.func.sum(FerryBooking.total_price)).filter(
            FerryBooking.created_at >= target_date,
            FerryBooking.created_at < next_date
        ).scalar() or 0
        bookings = FerryBooking.query.filter(
            FerryBooking.created_at >= target_date,
            FerryBooking.created_at < next_date
        ).count()
        daily_stats.append({
            'date': target_date.strftime('%Y-%m-%d'),
            'revenue': float(revenue),
            'bookings': bookings
        })
    
    # Monthly revenue (current year) - Database agnostic approach
    monthly_stats = []
    for month in range(1, 13):
        # First day of month
        if month == 12:
            month_start = datetime(current_year, month, 1)
            month_end = datetime(current_year + 1, 1, 1)
        else:
            month_start = datetime(current_year, month, 1)
            month_end = datetime(current_year, month + 1, 1)
        
        revenue = db.session.query(db.func.sum(FerryBooking.total_price)).filter(
            FerryBooking.created_at >= month_start,
            FerryBooking.created_at < month_end
        ).scalar() or 0
        bookings = FerryBooking.query.filter(
            FerryBooking.created_at >= month_start,
            FerryBooking.created_at < month_end
        ).count()
        monthly_stats.append({
            'month': month_name[month],
            'revenue': float(revenue),
            'bookings': bookings
        })
    
    # Route popularity
    route_stats = db.session.query(
        FerryBooking.departure,
        FerryBooking.destination,
        db.func.count(FerryBooking.id).label('bookings'),
        db.func.sum(FerryBooking.total_price).label('revenue')
    ).group_by(FerryBooking.departure, FerryBooking.destination).order_by(db.desc('bookings')).limit(10).all()
    
    route_data = [{
        'route': f"{r.departure} → {r.destination}",
        'bookings': r.bookings,
        'revenue': float(r.revenue or 0)
    } for r in route_stats]
    
    # Payment method breakdown
    payment_stats = db.session.query(
        FerryBooking.payment_method,
        db.func.count(FerryBooking.id).label('count'),
        db.func.sum(FerryBooking.total_price).label('revenue')
    ).filter(FerryBooking.payment_method.isnot(None)).group_by(FerryBooking.payment_method).all()
    
    payment_data = [{
        'method': p.payment_method or 'Unknown',
        'count': p.count,
        'revenue': float(p.revenue or 0)
    } for p in payment_stats]
    
    # Summary stats
    total_revenue = db.session.query(db.func.sum(FerryBooking.total_price)).scalar() or 0
    total_bookings = FerryBooking.query.count()
    avg_booking_value = float(total_revenue) / total_bookings if total_bookings > 0 else 0
    
    return render_template(
        'admin/reports.html',
        daily_stats=daily_stats,
        monthly_stats=monthly_stats,
        route_data=route_data,
        payment_data=payment_data,
        total_revenue=float(total_revenue),
        total_bookings=total_bookings,
        avg_booking_value=avg_booking_value,
        filter_type=filter_type
    )


@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    bookings_list = FerryBooking.query.order_by(FerryBooking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings_list)


@app.route('/admin/schedules', methods=['GET', 'POST'])
@admin_required
def admin_schedules():
    if request.method == 'POST':
        # Create schedule
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        time_str = request.form.get('time')
        date_str = request.form.get('date')
        if not (departure and destination and time_str):
            flash('Missing fields for schedule.', 'danger')
            return redirect(url_for('admin_schedules'))

        # If a date was provided, create a date-specific DailySchedule
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Use YYYY-MM-DD.', 'danger')
                return redirect(url_for('admin_schedules'))

            ds_exists = DailySchedule.query.filter_by(departure=departure, destination=destination, date=target_date, time=time_str).first()
            if not ds_exists:
                daily = DailySchedule(departure=departure, destination=destination, date=target_date, time=time_str, active=True)
                db.session.add(daily)
                db.session.commit()
                flash('Daily schedule added for ' + target_date.isoformat(), 'success')
            else:
                flash('Daily schedule already exists for that date/time.', 'info')
            return redirect(url_for('admin_schedules'))

        # otherwise create recurring schedule
        schedule = Schedule(departure=departure, destination=destination, time=time_str, active=True)
        db.session.add(schedule)
        db.session.commit()
        flash('Schedule added.', 'success')
        return redirect(url_for('admin_schedules'))

    # GET
    schedules = Schedule.query.order_by(Schedule.departure, Schedule.destination, Schedule.time).all()
    # fetch upcoming daily schedules
    daily_schedules = DailySchedule.query.order_by(DailySchedule.date, DailySchedule.departure, DailySchedule.time).all()
    return render_template('admin/schedules.html', schedules=schedules, daily_schedules=daily_schedules, ports=PORTS)


@app.route('/admin/daily-schedules/<int:id>/delete', methods=['POST'])
@admin_required
def admin_daily_schedule_delete(id):
    s = DailySchedule.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Daily schedule deleted.', 'success')
    return redirect(url_for('admin_schedules'))


@app.route('/admin/schedules/<int:id>/delete', methods=['POST'])
@admin_required
def admin_schedule_delete(id):
    s = Schedule.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Schedule deleted.', 'success')
    return redirect(url_for('admin_schedules'))


@app.route('/admin/bookings/<int:id>/cancel', methods=['POST'])
@admin_required
def admin_cancel_booking(id):
    b = FerryBooking.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    flash('Booking cancelled.', 'success')
    return redirect(url_for('admin_bookings'))


@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    """Admin settings page for system configuration"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        # System Configuration
        if action == 'update_capacity':
            global FERRY_CAPACITY
            new_capacity = request.form.get('ferry_capacity')
            try:
                capacity = int(new_capacity)
                if capacity > 0 and capacity <= 100:
                    # Update in memory
                    FERRY_CAPACITY = capacity
                    # Save to config file
                    config['ferry_capacity'] = capacity
                    if save_config(config):
                        flash(f'Ferry capacity updated to {capacity} and saved successfully.', 'success')
                    else:
                        flash(f'Ferry capacity updated to {capacity} in memory but failed to save to config file.', 'warning')
                else:
                    flash('Capacity must be between 1 and 100.', 'danger')
            except ValueError:
                flash('Invalid capacity value.', 'danger')
        
        # Pricing Management - Update Route Price
        elif action == 'update_price':
            departure = request.form.get('price_departure')
            destination = request.form.get('price_destination')
            new_price = request.form.get('new_price')
            try:
                price = float(new_price)
                if price > 0:
                    key = (departure, destination)
                    if key in ROUTE_PRICES:
                        # Update in memory
                        ROUTE_PRICES[key] = price
                        # Save to config file (convert tuple key to string)
                        if 'route_prices' not in config:
                            config['route_prices'] = {}
                        route_key = f"{departure},{destination}"
                        config['route_prices'][route_key] = price
                        if save_config(config):
                            flash(f'Price updated for {departure} → {destination}: {price} MVR and saved successfully.', 'success')
                        else:
                            flash(f'Price updated for {departure} → {destination}: {price} MVR in memory but failed to save to config file.', 'warning')
                    else:
                        flash('Route not found.', 'danger')
                else:
                    flash('Price must be greater than 0.', 'danger')
            except ValueError:
                flash('Invalid price value.', 'danger')
        
        # Admin Account - Change Password
        elif action == 'change_password':
            global ADMIN_PASSWORD
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if current_password == ADMIN_PASSWORD:
                if new_password == confirm_password:
                    if len(new_password) >= 6:
                        # Note: This only changes it in memory, not in .env
                        ADMIN_PASSWORD = new_password
                        flash('Password changed successfully! Update your .env file to make it permanent.', 'success')
                    else:
                        flash('New password must be at least 6 characters.', 'danger')
                else:
                    flash('New passwords do not match.', 'danger')
            else:
                flash('Current password is incorrect.', 'danger')
        
        # Database Backup - Export bookings
        elif action == 'export_bookings':
            try:
                import csv
                from io import StringIO
                
                output = StringIO()
                writer = csv.writer(output)
                
                # Write header
                writer.writerow(['Booking Ref', 'Name', 'Email', 'Phone', 'Departure', 'Destination', 
                               'Date', 'Time', 'Seats', 'Total Price', 'Payment Status', 'Created At'])
                
                # Write data
                bookings = FerryBooking.query.all()
                for b in bookings:
                    writer.writerow([
                        b.booking_reference, b.name, b.email, b.phone,
                        b.departure, b.destination, b.date, b.time,
                        b.seats, b.total_price, b.payment_status or 'N/A',
                        b.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    ])
                
                # Create response
                from flask import make_response
                output.seek(0)
                response = make_response(output.getvalue())
                response.headers['Content-Disposition'] = f'attachment; filename=bookings_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                response.headers['Content-Type'] = 'text/csv'
                return response
            except Exception as e:
                flash(f'Export failed: {str(e)}', 'danger')
        
        # Database Maintenance - Clear old bookings
        elif action == 'clear_old_bookings':
            days_old = request.form.get('days_old')
            try:
                days = int(days_old)
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                old_bookings = FerryBooking.query.filter(FerryBooking.created_at < cutoff_date).all()
                count = len(old_bookings)
                
                for booking in old_bookings:
                    db.session.delete(booking)
                db.session.commit()
                
                flash(f'Deleted {count} bookings older than {days} days.', 'success')
            except ValueError:
                flash('Invalid number of days.', 'danger')
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
        
        return redirect(url_for('admin_settings'))
    
    # GET request - show settings page
    # Get current statistics
    total_bookings = FerryBooking.query.count()
    total_users = User.query.count()
    total_schedules = Schedule.query.count()
    daily_schedules = DailySchedule.query.count()
    
    # Get database size (approximate)
    db_size = "N/A"
    try:
        if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
            import os
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            if os.path.exists(db_path):
                size_bytes = os.path.getsize(db_path)
                db_size = f"{size_bytes / 1024:.2f} KB"
    except:
        pass
    
    return render_template(
        'admin/settings.html',
        ferry_capacity=FERRY_CAPACITY,
        route_prices=ROUTE_PRICES,
        ports=PORTS,
        total_bookings=total_bookings,
        total_users=total_users,
        total_schedules=total_schedules,
        daily_schedules=daily_schedules,
        db_size=db_size
    )


@app.route('/admin/generate-pdf')
@admin_required
def admin_generate_pdf():
    """Generate architecture documentation PDF"""
    try:
        from generate_architecture_pdf import create_architecture_pdf
        filename = create_architecture_pdf()
        return send_file(filename, as_attachment=True, download_name='OceanLine_Architecture_Diagram.pdf')
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/generate-frontend-pdf')
@admin_required
def admin_generate_frontend_pdf():
    """Generate frontend pages documentation PDF"""
    try:
        from generate_frontend_pdf import create_frontend_pdf
        filename = create_frontend_pdf()
        return send_file(filename, as_attachment=True, download_name='OceanLine_Frontend_Pages.pdf')
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/generate-diagrams-pdf')
@admin_required
def admin_generate_diagrams_pdf():
    """Generate system diagrams PDF (text-based)"""
    try:
        from generate_diagrams_pdf import create_diagrams_pdf
        filename = create_diagrams_pdf()
        return send_file(filename, as_attachment=True, download_name='OceanLine_System_Diagrams.pdf')
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/generate-visual-diagrams-pdf')
@admin_required
def admin_generate_visual_diagrams_pdf():
    """Generate visual diagrams PDF with graphviz images (requires Graphviz installed)"""
    try:
        from generate_visual_diagrams import create_visual_diagrams_pdf
        filename = create_visual_diagrams_pdf()
        return send_file(filename, as_attachment=True, download_name='OceanLine_Visual_Diagrams.pdf')
    except Exception as e:
        flash(f'Error generating visual diagrams PDF: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/generate-enhanced-diagrams-pdf')
@admin_required
def admin_generate_enhanced_diagrams_pdf():
    """Generate enhanced visual diagrams PDF (pure Python, no external dependencies)"""
    try:
        from generate_enhanced_diagrams import create_enhanced_diagrams_pdf
        filename = create_enhanced_diagrams_pdf()
        return send_file(filename, as_attachment=True, download_name='OceanLine_Enhanced_Diagrams.pdf')
    except Exception as e:
        flash(f'Error generating enhanced diagrams PDF: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/generate-dfd-pdf')
@admin_required
def admin_generate_dfd_pdf():
    """Generate Data Flow Diagram PDF"""
    try:
        from generate_dfd_pdf import create_dfd_pdf
        filename = create_dfd_pdf()
        return send_file(filename, as_attachment=True, download_name='OceanLine_Data_Flow_Diagram.pdf')
    except Exception as e:
        flash(f'Error generating DFD PDF: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/test-route')
@admin_required
def admin_test_route():
    """Test route to verify routing works"""
    return "Test route works! DFD route should work too."


# -----------------------
# Utilities & CLI helpers
# -----------------------
@app.cli.command('create-db')
def create_db():
    """Initialize DB tables"""
    db.create_all()
    print("Database tables created.")


@app.cli.command('migrate-add-users')
def migrate_add_users():
    """Add user_id column to existing ferry_bookings table"""
    with app.app_context():
        try:
            # Check if column exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('ferry_bookings')]
            
            if 'user_id' not in columns:
                # Add the column
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE ferry_bookings ADD COLUMN user_id INTEGER'))
                    conn.commit()
                print("Added user_id column to ferry_bookings table.")
            else:
                print("user_id column already exists.")
        except Exception as e:
            print(f"Migration error: {e}")


@app.cli.command('seed-schedules')
def seed_schedules():
    """Seed some default schedules into Schedule table (idempotent)"""
    defaults = []
    for (dep, dest), times in FALLBACK_ROUTE_TIMES.items():
        for t in times:
            defaults.append({'departure': dep, 'destination': dest, 'time': t})

    added = 0
    for item in defaults:
        exists = Schedule.query.filter_by(departure=item['departure'], destination=item['destination'], time=item['time']).first()
        if not exists:
            db.session.add(Schedule(**item))
            added += 1
    db.session.commit()
    print(f"Seeded {added} schedules.")


# -----------------------
# Run App
# -----------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
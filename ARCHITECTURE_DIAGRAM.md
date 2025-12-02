# OceanLine Ferry Service - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER (Browser)                          │
├─────────────────────────────────────────────────────────────────────────┤
│  HTML5 │ CSS3 │ Bootstrap 5.3 │ JavaScript/jQuery │ AJAX │ Animations   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ HTTP/HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       PRESENTATION LAYER                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                         Flask Templates (Jinja2)                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │  Public Pages    │  │  User Pages      │  │  Admin Pages     │      │
│  │  - index.html    │  │  - bookings.html │  │  - dashboard.html│      │
│  │  - book.html     │  │  - payment.html  │  │  - schedules.html│      │
│  │  - login.html    │  │  - confirm.html  │  │  - payments.html │      │
│  │  - register.html │  │  - select_seats  │  │  - bookings.html │      │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘      │
│                                                                           │
│                         base.html (Master Template)                      │
│                   [Navbar | Content Block | Footer]                      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      CONTROLLER LAYER (Flask Routes)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Public Routes                                                     │   │
│  │  ● / (index)                    ● /book                          │   │
│  │  ● /register                    ● /select_seats                  │   │
│  │  ● /login                       ● /payment/<ref>                 │   │
│  │  ● /logout                      ● /confirmation/<ref>            │   │
│  │  ● /bookings                    ● /available_seats               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ API Endpoints (AJAX)                                             │   │
│  │  ● POST /get_price              ● POST /get_times                │   │
│  │  ● POST /get_available_seats    ● POST /pay                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Admin Routes (@admin_required)                                   │   │
│  │  ● /admin/login                 ● /admin/dashboard               │   │
│  │  ● /admin/bookings              ● /admin/schedules               │   │
│  │  ● /admin/payments              ● /admin/bookings/<id>/cancel    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │ Helper Functions                                              │      │
│  │  ● available_times_for_route()    ● generate_booking_ref()   │      │
│  │  ● available_seats_for_time()     ● create_receipt_pdf()     │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │ Security & Authentication                                     │      │
│  │  ● Flask-Login (User Sessions)    ● CSRF Protection          │      │
│  │  ● Werkzeug (Password Hashing)    ● @login_required          │      │
│  │  ● Session-based Admin Auth       ● @admin_required          │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │ Business Constants                                            │      │
│  │  ● ROUTE_PRICES (Pricing Matrix)  ● FERRY_CAPACITY (35)      │      │
│  │  ● SCHEDULES (Route Times)        ● FALLBACK_ROUTE_TIMES     │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │ External Services                                             │      │
│  │  ● ReportLab (PDF Generation)     ● Stripe (Payment Gateway) │      │
│  └──────────────────────────────────────────────────────────────┘      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER (ORM)                               │
├─────────────────────────────────────────────────────────────────────────┤
│                         Flask-SQLAlchemy                                 │
│                                                                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐            │
│  │  User Model    │  │ FerryBooking   │  │  Schedule      │            │
│  │                │  │     Model      │  │    Model       │            │
│  │ - id           │  │ - id           │  │ - id           │            │
│  │ - email        │  │ - booking_ref  │  │ - departure    │            │
│  │ - password_hash│  │ - user_id (FK) │  │ - destination  │            │
│  │ - name         │  │ - passenger    │  │ - time         │            │
│  │ - phone        │  │ - trip details │  │ - active       │            │
│  │                │  │ - seats        │  │                │            │
│  │ Relationships: │  │ - payment info │  └────────────────┘            │
│  │ → bookings     │  │ - roundtrip    │                                │
│  │                │  │                │  ┌────────────────┐            │
│  │ Methods:       │  │ Relationships: │  │ DailySchedule  │            │
│  │ set_password() │  │ → user         │  │     Model      │            │
│  │ check_password │  │                │  │ - id           │            │
│  │                │  │ Methods:       │  │ - departure    │            │
│  └────────────────┘  │ as_dict()      │  │ - destination  │            │
│                      │                │  │ - date         │            │
│                      └────────────────┘  │ - time         │            │
│                                          │ - active       │            │
│                                          └────────────────┘            │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ PyMySQL
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATABASE LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                          MySQL Database                                  │
│                         (oceanline_db)                                   │
│                                                                           │
│  Tables:                                                                 │
│  ┌──────────────────┬──────────────────┬──────────────────┐            │
│  │ users            │ ferry_bookings   │ schedules        │            │
│  │ daily_schedules  │                  │                  │            │
│  └──────────────────┴──────────────────┴──────────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
```

## MVC Pattern Flow

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    VIEW     │◄────────│  CONTROLLER  │────────►│    MODEL    │
│  (Template) │         │   (Routes)   │         │ (Database)  │
└─────────────┘         └──────────────┘         └─────────────┘
      ▲                        │                        │
      │                        │                        │
      │                        ▼                        ▼
      │              ┌──────────────────┐    ┌──────────────────┐
      │              │ Business Logic   │    │  SQLAlchemy ORM  │
      │              │ - Validation     │    │  - Query Builder │
      └──────────────│ - Calculations   │    │  - Relationships │
                     │ - PDF Generation │    └──────────────────┘
                     └──────────────────┘
```

## Request-Response Flow

```
1. User Action (Browser)
         │
         ▼
2. HTTP Request → Flask Application
         │
         ▼
3. Route Handler (Controller)
         │
         ├──→ Authentication Check (@login_required/@admin_required)
         │
         ├──→ CSRF Validation (Flask-WTF)
         │
         ▼
4. Business Logic
         │
         ├──→ Validate Input
         ├──→ Check Availability
         ├──→ Calculate Pricing
         │
         ▼
5. Database Operations (via SQLAlchemy)
         │
         ├──→ Query Data
         ├──→ Insert/Update Records
         │
         ▼
6. Generate Response
         │
         ├──→ Render Template (HTML)
         ├──→ Return JSON (AJAX)
         ├──→ Generate PDF (Receipt)
         │
         ▼
7. HTTP Response → User Browser
         │
         ▼
8. Display Result (HTML/JavaScript)
```

## Authentication Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     User Authentication                       │
└──────────────────────────────────────────────────────────────┘

User Registration:
  Browser → POST /register → Hash Password → Save to DB → Auto Login

User Login:
  Browser → POST /login → Verify Password → Flask-Login Session → Dashboard

Protected Routes:
  @login_required → Check Session → Allow/Deny Access

┌──────────────────────────────────────────────────────────────┐
│                    Admin Authentication                       │
└──────────────────────────────────────────────────────────────┘

Admin Login:
  Browser → POST /admin/login → Verify Credentials → session['is_admin'] = True

Admin Routes:
  @admin_required → Check session['is_admin'] → Allow/Deny Access
```

## Database Schema Relationships

```
┌─────────────────┐
│     users       │
│─────────────────│
│ PK: id          │
│    email        │
│    password_hash│
│    name         │
│    phone        │
└────────┬────────┘
         │ 1
         │
         │ N
         ▼
┌─────────────────┐
│ ferry_bookings  │
│─────────────────│
│ PK: id          │
│ FK: user_id     │──┐
│    booking_ref  │  │ (Optional FK)
│    passenger    │  │ Allows guest bookings
│    trip_details │  │
│    seats        │  │
│    payment_info │  │
│    roundtrip    │  │
└─────────────────┘  │
                     │
         ┌───────────┘
         ▼
    NULL allowed
  (Guest bookings)


┌─────────────────┐         ┌──────────────────┐
│   schedules     │         │ daily_schedules  │
│─────────────────│         │──────────────────│
│ PK: id          │         │ PK: id           │
│    departure    │         │    departure     │
│    destination  │         │    destination   │
│    time         │         │    date          │
│    active       │         │    time          │
└─────────────────┘         │    active        │
                            └──────────────────┘
  (Recurring)                  (Date-specific)
```

## Technology Stack Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND STACK                            │
├─────────────────────────────────────────────────────────────┤
│  HTML5  │  CSS3  │  Bootstrap 5.3  │  JavaScript/jQuery    │
│  Bootstrap Icons  │  Custom Animations  │  AJAX             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BACKEND STACK                             │
├─────────────────────────────────────────────────────────────┤
│  Python 3.x  │  Flask 3.0  │  Flask-SQLAlchemy  │  Jinja2  │
│  Flask-Login │  Flask-WTF  │  Werkzeug Security │  PyMySQL │
│  ReportLab   │  Stripe API │  python-dotenv                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DATABASE STACK                            │
├─────────────────────────────────────────────────────────────┤
│              MySQL + SQLAlchemy ORM                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  DEPLOYMENT ENVIRONMENT                      │
├─────────────────────────────────────────────────────────────┤
│  Flask Development Server  │  Virtual Environment (.venv)   │
│  Windows/Linux/Mac         │  Port 5000                     │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
oceanline/
│
├── app.py                      # Main Flask application (1472 lines)
│   ├── Configuration
│   ├── Models (User, FerryBooking, Schedule, DailySchedule)
│   ├── Routes (Public, Admin, API)
│   └── Helper Functions
│
├── templates/                  # View Layer
│   ├── base.html              # Master template
│   ├── index.html             # Homepage
│   ├── book.html              # Booking form
│   ├── select_seats.html      # Seat selection
│   ├── payment.html           # Payment processing
│   ├── confirmation.html      # Booking confirmation
│   ├── bookings.html          # User bookings
│   ├── login.html             # User login
│   ├── register.html          # User registration
│   └── admin/                 # Admin templates
│       ├── dashboard.html
│       ├── bookings.html
│       ├── schedules.html
│       └── payments.html
│
├── uploads/                   # Payment proof uploads
├── instance/                  # SQLite database (if used)
├── scripts/                   # Utility scripts
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # Project documentation
```

---
**Created for:** ST7078 - Hassan Solih  
**Project:** OceanLine Ferry Booking System  
**Date:** November 29, 2025

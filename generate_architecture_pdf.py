"""
Generate Architecture Diagram PDF
Creates a professional PDF document from the architecture documentation
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, Preformatted
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime

def create_architecture_pdf():
    """Generate the architecture PDF document"""
    
    filename = "OceanLine_Architecture_Diagram.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                          rightMargin=50, leftMargin=50,
                          topMargin=50, bottomMargin=50)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0d6efd'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#495057'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        textColor=colors.black,
        backColor=colors.HexColor('#f8f9fa'),
        leftIndent=20,
        rightIndent=20,
        spaceAfter=10
    )
    
    # Title Page
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("OceanLine Ferry Service", title_style))
    elements.append(Paragraph("System Architecture Documentation", heading1_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Project info
    info_data = [
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Student ID:', 'ST7078'],
        ['Name:', 'Hassan Solih'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Technology:', 'Flask Web Application'],
    ]
    
    info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#495057')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(info_table)
    elements.append(PageBreak())
    
    # Table of Contents
    elements.append(Paragraph("Table of Contents", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        "1. System Architecture Overview",
        "2. MVC Pattern Flow",
        "3. Technology Stack",
        "4. Database Models",
        "5. Routes and Controllers",
        "6. Authentication Flow",
        "7. Request-Response Flow",
        "8. Advanced Features",
        "9. File Structure"
    ]
    
    for item in toc_items:
        elements.append(Paragraph(item, styles['Normal']))
        elements.append(Spacer(1, 6))
    
    elements.append(PageBreak())
    
    # Section 1: System Architecture Overview
    elements.append(Paragraph("1. System Architecture Overview", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    architecture_text = """
    The OceanLine Ferry Service follows a modern web application architecture built on the 
    Flask framework. The system implements the Model-View-Controller (MVC) pattern with clear 
    separation of concerns across multiple layers.
    """
    elements.append(Paragraph(architecture_text, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Architecture layers
    arch_code = """
CLIENT LAYER (Browser)
  ↓
PRESENTATION LAYER (Templates)
  ↓
CONTROLLER LAYER (Flask Routes)
  ↓
BUSINESS LOGIC LAYER
  ↓
DATA ACCESS LAYER (SQLAlchemy ORM)
  ↓
DATABASE LAYER (MySQL)
    """
    elements.append(Preformatted(arch_code, code_style))
    
    # Section 2: MVC Pattern
    elements.append(PageBreak())
    elements.append(Paragraph("2. MVC Pattern Implementation", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("Model Layer", heading2_style))
    model_text = """
    The Model layer represents the data and business logic. It includes four main database models:
    User, FerryBooking, Schedule, and DailySchedule. These models are implemented using 
    SQLAlchemy ORM and handle all database interactions.
    """
    elements.append(Paragraph(model_text, styles['BodyText']))
    
    elements.append(Paragraph("View Layer", heading2_style))
    view_text = """
    The View layer consists of Jinja2 templates that render HTML pages. The base.html template 
    serves as the master layout, with child templates extending it for specific pages. Templates 
    include public pages (homepage, booking, login) and admin pages (dashboard, schedules).
    """
    elements.append(Paragraph(view_text, styles['BodyText']))
    
    elements.append(Paragraph("Controller Layer", heading2_style))
    controller_text = """
    The Controller layer is implemented through Flask route handlers. These functions process 
    HTTP requests, interact with models, apply business logic, and return appropriate responses 
    (HTML templates or JSON data for AJAX calls).
    """
    elements.append(Paragraph(controller_text, styles['BodyText']))
    
    # Section 3: Technology Stack
    elements.append(PageBreak())
    elements.append(Paragraph("3. Technology Stack", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    tech_data = [
        ['Layer', 'Technology', 'Purpose'],
        ['Backend', 'Flask 3.1.2', 'Web framework'],
        ['', 'Flask-SQLAlchemy 2.0.44', 'Database ORM'],
        ['', 'Flask-Login', 'User authentication'],
        ['', 'Flask-WTF 1.2.2', 'CSRF protection'],
        ['', 'PyMySQL', 'MySQL connector'],
        ['Frontend', 'Bootstrap 5.3', 'UI framework'],
        ['', 'jQuery 3.6', 'JavaScript library'],
        ['', 'CSS3 Animations', 'Fade-in, slide effects'],
        ['', 'Chart.js 4.4.0', 'Revenue analytics charts'],
        ['Database', 'MySQL/SQLite', 'Dual database support'],
        ['Additional', 'ReportLab 4.4.5', 'PDF generation'],
        ['', 'Stripe API', 'Payment processing'],
        ['', 'Werkzeug', 'Security utilities'],
        ['', 'JSON Config', 'Persistent settings'],
    ]
    
    tech_table = Table(tech_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(tech_table)
    
    # Section 4: Database Models
    elements.append(PageBreak())
    elements.append(Paragraph("4. Database Models", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("User Model", heading2_style))
    user_code = """
User (UserMixin, db.Model)
├── id (PK)
├── email (Unique, Indexed)
├── password_hash
├── name
├── phone
├── created_at
├── Relationship: bookings (One-to-Many)
└── Methods: set_password(), check_password()
    """
    elements.append(Preformatted(user_code, code_style))
    
    elements.append(Paragraph("FerryBooking Model", heading2_style))
    booking_code = """
FerryBooking (db.Model)
├── id (PK)
├── booking_reference (Unique, Indexed)
├── user_id (FK to User, nullable)
├── Passenger Info: name, email, phone
├── Trip Details: departure, destination, date, time
├── Seats: seats, selected_seats, total_price
├── Payment: payment_method, payment_status, payment_info
├── Round-trip: is_roundtrip, return_date, return_time
└── Method: as_dict()
    """
    elements.append(Preformatted(booking_code, code_style))
    
    elements.append(Paragraph("Schedule Models", heading2_style))
    schedule_code = """
Schedule (db.Model) - Recurring schedules
├── id (PK)
├── departure
├── destination
├── time
└── active

DailySchedule (db.Model) - Date-specific schedules
├── id (PK)
├── departure
├── destination
├── date (Indexed)
├── time
└── active
    """
    elements.append(Preformatted(schedule_code, code_style))
    
    # Section 5: Routes
    elements.append(PageBreak())
    elements.append(Paragraph("5. Routes and Controllers", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("Public Routes", heading2_style))
    public_routes = """
/ (GET)                      - Homepage
/register (GET, POST)        - User registration
/login (GET, POST)           - User login
/logout (GET)                - User logout
/book (GET, POST)            - Booking form
/select_seats (GET, POST)    - Seat selection
/payment/<ref> (GET, POST)   - Payment processing
/confirmation/<ref> (GET)    - Booking confirmation
/bookings (GET)              - User's bookings list
/available_seats (GET)       - All schedules view
    """
    elements.append(Preformatted(public_routes, code_style))
    
    elements.append(Paragraph("AJAX API Endpoints", heading2_style))
    api_routes = """
POST /get_price              - Get route pricing
POST /get_times              - Get available times
POST /get_available_seats    - Check seat availability
POST /pay                    - Process payment
    """
    elements.append(Preformatted(api_routes, code_style))
    
    elements.append(Paragraph("Admin Routes (Protected)", heading2_style))
    admin_routes = """
/admin/login (GET, POST)               - Admin authentication
/admin/logout (GET)                    - Admin logout
/admin/dashboard (GET)                 - Admin overview with revenue stats
/admin/reports (GET)                   - Revenue analytics & charts
/admin/settings (GET, POST)            - System configuration
/admin/bookings (GET)                  - Manage bookings
/admin/schedules (GET, POST)           - Manage schedules
/admin/payments (GET)                  - Payment verification
/admin/bookings/<id>/cancel (POST)     - Cancel booking
/admin/schedules/<id>/delete (POST)    - Delete schedule
    """
    elements.append(Preformatted(admin_routes, code_style))
    
    # Section 6: Authentication
    elements.append(PageBreak())
    elements.append(Paragraph("6. Authentication Flow", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("User Authentication", heading2_style))
    user_auth_text = """
    The system uses Flask-Login for user session management. Password hashing is handled by 
    Werkzeug's security utilities. Users can register, login, and access protected routes 
    decorated with @login_required. Sessions persist across requests until logout.
    """
    elements.append(Paragraph(user_auth_text, styles['BodyText']))
    
    user_auth_flow = """
Registration: POST /register → Hash Password → Save to DB → Auto Login
Login:        POST /login → Verify Password → Create Session → Redirect
Protected:    @login_required → Check Session → Allow/Deny
    """
    elements.append(Preformatted(user_auth_flow, code_style))
    
    elements.append(Paragraph("Admin Authentication", heading2_style))
    admin_auth_text = """
    Admin authentication uses a simple session-based approach. Credentials are verified against 
    environment variables. The @admin_required decorator protects admin routes by checking the 
    session['is_admin'] flag.
    """
    elements.append(Paragraph(admin_auth_text, styles['BodyText']))
    
    admin_auth_flow = """
Login:     POST /admin/login → Verify Credentials → session['is_admin'] = True
Protected: @admin_required → Check session['is_admin'] → Allow/Deny
    """
    elements.append(Preformatted(admin_auth_flow, code_style))
    
    # Section 7: Request-Response Flow
    elements.append(PageBreak())
    elements.append(Paragraph("7. Request-Response Flow", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    flow_text = """
    The application follows a standard web request-response cycle with multiple processing layers:
    """
    elements.append(Paragraph(flow_text, styles['BodyText']))
    
    request_flow = """
1. User Action (Browser) → Click, Form Submit, AJAX Call
   ↓
2. HTTP Request → Flask Application (Port 5000)
   ↓
3. Route Handler (Controller)
   ├→ Authentication Check (@login_required / @admin_required)
   ├→ CSRF Validation (Flask-WTF)
   └→ Parse Request Data
   ↓
4. Business Logic Layer
   ├→ Validate Input
   ├→ Check Seat Availability
   ├→ Calculate Pricing
   └→ Apply Business Rules
   ↓
5. Database Operations (SQLAlchemy ORM)
   ├→ Query Data
   ├→ Insert/Update Records
   └→ Manage Transactions
   ↓
6. Generate Response
   ├→ Render HTML Template (Jinja2)
   ├→ Return JSON (for AJAX)
   ├→ Generate PDF (ReportLab)
   └→ Redirect to Another Route
   ↓
7. HTTP Response → User Browser
   ↓
8. Display Result (HTML, JavaScript updates DOM)
    """
    elements.append(Preformatted(request_flow, code_style))
    
    # Section 8: Advanced Features
    elements.append(PageBreak())
    elements.append(Paragraph("8. Advanced Features", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("CSS3 Animations", heading2_style))
    animation_text = """
    The application features smooth CSS3 animations for enhanced user experience. Custom 
    keyframe animations include fade-in, slide-in-left, slide-in-right, and slide-in-up 
    effects with staggered delays. These are applied to hero sections, feature cards, and 
    booking forms for a polished, modern interface.
    """
    elements.append(Paragraph(animation_text, styles['BodyText']))
    
    animation_code = """
@keyframes fadeIn { 
    from { opacity: 0; }
    to { opacity: 1; }
}
@keyframes slideInLeft {
    from { transform: translateX(-50px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
    """
    elements.append(Preformatted(animation_code, code_style))
    
    elements.append(Paragraph("Revenue Analytics", heading2_style))
    revenue_text = """
    The admin dashboard includes comprehensive revenue tracking with daily, monthly, and 
    total revenue calculations. Database-agnostic date filtering ensures compatibility with 
    both MySQL and SQLite. The reports page features interactive Chart.js visualizations 
    showing daily revenue trends, monthly comparisons, route popularity, and payment method 
    distribution.
    """
    elements.append(Paragraph(revenue_text, styles['BodyText']))
    
    revenue_code = """
Daily Revenue:   SUM(bookings from today)
Monthly Revenue: SUM(bookings from current month)
Total Revenue:   SUM(all bookings)
Average Booking: Total Revenue / Total Bookings
Route Analytics: Group by departure-destination pairs
    """
    elements.append(Preformatted(revenue_code, code_style))
    
    elements.append(Paragraph("Settings Management", heading2_style))
    settings_text = """
    The admin settings page provides centralized system configuration with five key features:
    1) Ferry capacity management with instant updates
    2) Dynamic route pricing with per-route customization
    3) Admin password changes with validation
    4) CSV export of all bookings for backup
    5) Database cleanup to remove old bookings
    
    All settings are persisted to a JSON configuration file (config.json) ensuring changes 
    survive server restarts without manual file editing.
    """
    elements.append(Paragraph(settings_text, styles['BodyText']))
    
    settings_code = """
Config File Structure (config.json):
{
  "ferry_capacity": 40,
  "route_prices": {
    "Male,Hulhumale": 120,
    "Male,K.Maafushi": 250
  }
}
    """
    elements.append(Preformatted(settings_code, code_style))
    
    elements.append(Paragraph("Database Flexibility", heading2_style))
    db_text = """
    The application supports both MySQL and SQLite databases through SQLAlchemy's abstraction 
    layer. All date-based queries use Python datetime ranges instead of database-specific 
    functions, ensuring full compatibility. The configuration automatically uses SQLite for 
    development and MySQL for production environments.
    """
    elements.append(Paragraph(db_text, styles['BodyText']))
    
    # Section 9: File Structure
    elements.append(PageBreak())
    elements.append(Paragraph("9. File Structure", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    file_structure = """
oceanline/
│
├── app.py                      Main Flask application (1768 lines)
│   ├── Configuration & Setup
│   ├── Config File Management (JSON-based persistence)
│   ├── Database Models
│   ├── Route Handlers
│   ├── Business Logic
│   ├── Revenue Calculations
│   └── Helper Functions
│
├── config.json                 Persistent settings (capacity, prices)
│
├── templates/                  Jinja2 Templates (View Layer)
│   ├── base.html              Master template with CSS animations
│   ├── index.html             Homepage with fade-in/slide effects
│   ├── book.html              Booking form with animations
│   ├── select_seats.html      Interactive seat selection
│   ├── payment.html           Payment processing
│   ├── confirmation.html      Booking confirmation
│   ├── bookings.html          User bookings list
│   ├── available_seats.html   All schedules view
│   ├── login.html             User login
│   ├── register.html          User registration
│   └── admin/                 Admin templates
│       ├── dashboard.html     Admin overview with revenue cards
│       ├── reports.html       Analytics with Chart.js graphs
│       ├── settings.html      System configuration panel
│       ├── bookings.html      Booking management
│       ├── schedules.html     Schedule management
│       ├── payments.html      Payment verification
│       └── login.html         Admin login
│
├── uploads/                   Payment proof file storage
├── instance/                  Instance-specific files (SQLite DB)
├── scripts/                   Utility scripts
│   ├── seed_daily_schedules.py
│   ├── check_schedules.py
│   └── generate_pdf_direct.py
│
├── generate_architecture_pdf.py  This PDF generator
├── requirements.txt           Python dependencies
├── .env                       Environment variables (not in git)
├── README.md                  Project documentation
└── ARCHITECTURE_DIAGRAM.md    Architecture documentation
    """
    elements.append(Preformatted(file_structure, code_style))
    
    # Footer section
    elements.append(PageBreak())
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("Summary", heading1_style))
    
    summary_text = """
    The OceanLine Ferry Service is a comprehensive web-based booking system built with modern 
    web technologies. It implements industry-standard architectural patterns including MVC, 
    layered architecture, and RESTful API design. The system provides a complete booking workflow 
    with user authentication, seat selection, payment processing, and administrative management 
    capabilities. The codebase is well-organized, maintainable, and scalable for future enhancements.
    """
    elements.append(Paragraph(summary_text, styles['BodyText']))
    
    elements.append(Spacer(1, 0.5*inch))
    
    footer_data = [
        ['Student:', 'Hassan Solih'],
        ['ID:', 'ST7078'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
    ]
    
    footer_table = Table(footer_data, colWidths=[1.5*inch, 3*inch])
    footer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    print(f"✅ PDF generated successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_architecture_pdf()

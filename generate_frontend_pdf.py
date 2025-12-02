"""
Generate Frontend Pages Documentation PDF
Creates a PDF document showcasing all frontend pages and features
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, Preformatted, Image as RLImage
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime

def create_frontend_pdf():
    """Generate the frontend documentation PDF"""
    
    filename = "OceanLine_Frontend_Pages.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                          rightMargin=50, leftMargin=50,
                          topMargin=50, bottomMargin=50)
    
    elements = []
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
    
    feature_style = ParagraphStyle(
        'Feature',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=6,
        bulletIndent=10,
        bulletFontName='Helvetica',
        bulletFontSize=10
    )
    
    # Title Page
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("OceanLine Ferry Service", title_style))
    elements.append(Paragraph("Frontend Pages Documentation", heading1_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Project info
    info_data = [
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Student ID:', 'ST7078'],
        ['Name:', 'Hassan Solih'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Pages:', '14 Frontend Pages'],
    ]
    
    info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#495057')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(info_table)
    elements.append(PageBreak())
    
    # Table of Contents
    elements.append(Paragraph("Table of Contents", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        "PUBLIC PAGES",
        "1. Homepage (index.html)",
        "2. User Registration (register.html)",
        "3. User Login (login.html)",
        "4. Ferry Booking Form (book.html)",
        "5. Seat Selection (select_seats.html)",
        "6. Payment Page (payment.html)",
        "7. Booking Confirmation (confirmation.html)",
        "8. My Bookings (bookings.html)",
        "9. Available Schedules (available_seats.html)",
        "",
        "ADMIN PAGES",
        "10. Admin Login (admin/login.html)",
        "11. Admin Dashboard (admin/dashboard.html)",
        "12. Manage Bookings (admin/bookings.html)",
        "13. Manage Schedules (admin/schedules.html)",
        "14. Payment Verification (admin/payments.html)",
        "15. Revenue Reports (admin/reports.html)",
        "16. System Settings (admin/settings.html)",
    ]
    
    for item in toc_items:
        if item == "":
            elements.append(Spacer(1, 12))
        elif item in ["PUBLIC PAGES", "ADMIN PAGES"]:
            elements.append(Paragraph(f"<b>{item}</b>", styles['Normal']))
            elements.append(Spacer(1, 6))
        else:
            elements.append(Paragraph(item, styles['Normal']))
            elements.append(Spacer(1, 4))
    
    elements.append(PageBreak())
    
    # PUBLIC PAGES SECTION
    elements.append(Paragraph("PUBLIC PAGES", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Page 1: Homepage
    elements.append(Paragraph("1. Homepage (index.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/</b> (GET)", heading2_style))
    
    homepage_desc = """
    The landing page showcases the OceanLine ferry service with a modern, animated design. 
    Features a hero section with call-to-action buttons and highlights key routes and services.
    """
    elements.append(Paragraph(homepage_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    features = [
        "• Hero section with fade-in animation",
        "• Quick booking button with slide-in effect",
        "• Featured routes grid with pricing (3-card layout)",
        "• Service highlights (Fast Boarding, Safe Journey, Comfortable Seats)",
        "• Responsive navigation bar with user login status",
        "• Bootstrap 5.3 responsive design",
        "• CSS3 animations (fadeIn, slideInLeft, slideInRight, slideInUp)"
    ]
    for feature in features:
        elements.append(Paragraph(feature, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Key Components:</b>", heading2_style))
    components = [
        "• Navigation: Logo, Home, Book Now, Schedules, My Bookings",
        "• Hero CTA: 'Book Your Ferry Now' and 'View Schedules' buttons",
        "• Route Cards: Male→Hulhumale (100 MVR), Airport→Male (100 MVR), Male→Maafushi (200 MVR)",
        "• Footer: Copyright and company info"
    ]
    for comp in components:
        elements.append(Paragraph(comp, feature_style))
    
    elements.append(PageBreak())
    
    # Page 2: User Registration
    elements.append(Paragraph("2. User Registration (register.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/register</b> (GET, POST)", heading2_style))
    
    register_desc = """
    User registration page with form validation. New users create an account to manage 
    their ferry bookings and access booking history.
    """
    elements.append(Paragraph(register_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Form Fields:</b>", heading2_style))
    reg_fields = [
        "• Full Name (required, text input)",
        "• Email Address (required, unique, email validation)",
        "• Phone Number (optional, tel input)",
        "• Password (required, minimum 6 characters)",
        "• Confirm Password (required, must match)",
        "• Submit button with CSRF protection"
    ]
    for field in reg_fields:
        elements.append(Paragraph(field, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Validation:</b>", heading2_style))
    validations = [
        "• Server-side: All required fields checked",
        "• Password length minimum 6 characters",
        "• Password confirmation matching",
        "• Email uniqueness verification",
        "• Flash messages for errors/success",
        "• Automatic login after successful registration"
    ]
    for val in validations:
        elements.append(Paragraph(val, feature_style))
    
    elements.append(PageBreak())
    
    # Page 3: User Login
    elements.append(Paragraph("3. User Login (login.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/login</b> (GET, POST)", heading2_style))
    
    login_desc = """
    Login page for registered users. Authenticates users and creates sessions for 
    accessing protected features like booking and viewing booking history.
    """
    elements.append(Paragraph(login_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Form Fields:</b>", heading2_style))
    login_fields = [
        "• Email Address (required)",
        "• Password (required)",
        "• Login button with CSRF protection",
        "• Link to registration page for new users"
    ]
    for field in login_fields:
        elements.append(Paragraph(field, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    login_features = [
        "• Flask-Login session management",
        "• Werkzeug password hash verification",
        "• Redirect to next page after login",
        "• Flash messages for invalid credentials",
        "• Remember user session across visits"
    ]
    for feat in login_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(PageBreak())
    
    # Page 4: Ferry Booking Form
    elements.append(Paragraph("4. Ferry Booking Form (book.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/book</b> (GET, POST)", heading2_style))
    
    book_desc = """
    Main booking interface with dynamic form fields, AJAX price lookups, and schedule 
    availability checks. Features animated form with real-time validation.
    """
    elements.append(Paragraph(book_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Form Sections:</b>", heading2_style))
    book_sections = [
        "• <b>Passenger Information:</b> Name, Email, Phone (pre-filled for logged-in users)",
        "• <b>Trip Details:</b> Departure port, Destination, Date, Time, Number of seats",
        "• <b>Round Trip:</b> Optional return date and time selection",
        "• <b>Booking Summary:</b> Real-time price calculation display"
    ]
    for section in book_sections:
        elements.append(Paragraph(section, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>AJAX Features:</b>", heading2_style))
    ajax_features = [
        "• <b>/get_price:</b> Fetch route price dynamically",
        "• <b>/get_times:</b> Load available departure times",
        "• <b>/get_available_seats:</b> Check seat availability",
        "• Real-time total price calculation",
        "• Form validation before submission"
    ]
    for feat in ajax_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Ports Available:</b>", heading2_style))
    ports = [
        "• Male (Capital)", 
        "• Hulhumale", 
        "• Velana International Airport",
        "• K.Maafushi (Resort Island)",
        "• K.Dhiffushi",
        "• K.Guraidhoo",
        "• AA.Rasdhoo",
        "• V.Thinadhoo"
    ]
    for port in ports:
        elements.append(Paragraph(port, feature_style))
    
    elements.append(PageBreak())
    
    # Page 5: Seat Selection
    elements.append(Paragraph("5. Seat Selection (select_seats.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/select_seats</b> (GET, POST)", heading2_style))
    
    seat_desc = """
    Interactive seat selection interface with visual grid layout. Shows available and 
    booked seats, allows users to select their preferred seats for the journey.
    """
    elements.append(Paragraph(seat_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    seat_features = [
        "• Visual seat grid (default: 35 seats, configurable via admin)",
        "• Color-coded seats: Available (green), Selected (blue), Booked (red)",
        "• Click-to-select interaction with jQuery",
        "• Seat limit validation based on booking quantity",
        "• Round-trip: Separate seat selection for outbound and return",
        "• Real-time seat selection counter",
        "• Trip summary with date, time, and route details"
    ]
    for feat in seat_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Seat Layout:</b>", heading2_style))
    layout_desc = """
    Seats are displayed in a grid format (5 columns) with numbers 1-35 (or custom capacity). 
    Previously booked seats are marked and cannot be selected. Users must select exact 
    number of seats matching their booking quantity.
    """
    elements.append(Paragraph(layout_desc, styles['BodyText']))
    
    elements.append(PageBreak())
    
    # Page 6: Payment
    elements.append(Paragraph("6. Payment Page (payment.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/payment/&lt;ref&gt;</b> (GET, POST)", heading2_style))
    
    payment_desc = """
    Payment processing page with multiple payment options. Displays booking summary 
    and allows users to complete payment via bank transfer or file upload.
    """
    elements.append(Paragraph(payment_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Payment Methods:</b>", heading2_style))
    payment_methods = [
        "• <b>Bank Transfer:</b> BML Account details provided",
        "• <b>Upload Payment Proof:</b> File upload for receipt/screenshot",
        "• Payment reference number displayed",
        "• Total amount highlighted"
    ]
    for method in payment_methods:
        elements.append(Paragraph(method, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Booking Summary Display:</b>", heading2_style))
    summary_items = [
        "• Booking Reference Number",
        "• Passenger Name, Email, Phone",
        "• Route: Departure → Destination",
        "• Date and Time",
        "• Selected Seat Numbers",
        "• Number of Seats",
        "• Total Price in MVR",
        "• Round-trip details (if applicable)"
    ]
    for item in summary_items:
        elements.append(Paragraph(item, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    payment_features = [
        "• File upload to /uploads directory",
        "• Payment status tracking",
        "• CSRF protection on form submission",
        "• Redirect to confirmation after payment"
    ]
    for feat in payment_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(PageBreak())
    
    # Page 7: Confirmation
    elements.append(Paragraph("7. Booking Confirmation (confirmation.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/confirmation/&lt;ref&gt;</b> (GET)", heading2_style))
    
    confirm_desc = """
    Success page showing complete booking details and download options. Confirms 
    successful booking and provides receipt download functionality.
    """
    elements.append(Paragraph(confirm_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    confirm_features = [
        "• Success message with checkmark icon",
        "• Complete booking details display",
        "• Booking reference prominently shown",
        "• Download receipt button (AJAX call to /pay endpoint)",
        "• PDF receipt generation using ReportLab",
        "• QR code on receipt for verification",
        "• Navigation to 'My Bookings' and 'Book Another Trip'"
    ]
    for feat in confirm_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Receipt PDF Contents:</b>", heading2_style))
    receipt_items = [
        "• OceanLine Ferry Service branding",
        "• Booking reference with QR code",
        "• Passenger information",
        "• Trip details (route, date, time)",
        "• Seat assignments",
        "• Payment information",
        "• Total amount paid",
        "• Terms and conditions"
    ]
    for item in receipt_items:
        elements.append(Paragraph(item, feature_style))
    
    elements.append(PageBreak())
    
    # Page 8: My Bookings
    elements.append(Paragraph("8. My Bookings (bookings.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/bookings</b> (GET) - Login Required", heading2_style))
    
    bookings_desc = """
    User's personal booking history page. Displays all bookings made by the logged-in 
    user with complete trip details and status information.
    """
    elements.append(Paragraph(bookings_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    bookings_features = [
        "• Login required (@login_required decorator)",
        "• List of all user bookings from database",
        "• Responsive card layout for each booking",
        "• Color-coded status indicators",
        "• Booking reference number display",
        "• View confirmation link for each booking"
    ]
    for feat in bookings_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Displayed Information:</b>", heading2_style))
    booking_info = [
        "• Booking Reference",
        "• Route (Departure → Destination)",
        "• Travel Date and Time",
        "• Number of Seats",
        "• Seat Numbers",
        "• Total Price",
        "• Payment Status",
        "• Round-trip indicator and return details"
    ]
    for info in booking_info:
        elements.append(Paragraph(info, feature_style))
    
    elements.append(PageBreak())
    
    # Page 9: Available Schedules
    elements.append(Paragraph("9. Available Schedules (available_seats.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/available_seats</b> (GET)", heading2_style))
    
    schedules_desc = """
    Public page showing all available ferry schedules. Allows users to browse 
    routes and departure times before making a booking.
    """
    elements.append(Paragraph(schedules_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    schedules_features = [
        "• Date filter to view schedules for specific dates",
        "• Default: Shows today's schedules",
        "• Grouped by route (Departure → Destination)",
        "• All available departure times listed",
        "• Responsive table layout",
        "• Quick 'Book Now' button navigation"
    ]
    for feat in schedules_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Schedule Display:</b>", heading2_style))
    schedule_info = [
        "• Route name",
        "• Departure times (e.g., 08:00, 10:00, 14:00, 16:00)",
        "• Price per seat",
        "• Ferry capacity information",
        "• Search by date functionality"
    ]
    for info in schedule_info:
        elements.append(Paragraph(info, feature_style))
    
    elements.append(PageBreak())
    
    # ADMIN PAGES SECTION
    elements.append(Paragraph("ADMIN PAGES", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Page 10: Admin Login
    elements.append(Paragraph("10. Admin Login (admin/login.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/admin/login</b> (GET, POST)", heading2_style))
    
    admin_login_desc = """
    Separate admin authentication page with session-based access control. 
    Uses environment variable credentials for security.
    """
    elements.append(Paragraph(admin_login_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    admin_login_features = [
        "• Username and password authentication",
        "• Credentials stored in .env file (ADMIN_USERNAME, ADMIN_PASSWORD)",
        "• Session-based admin flag (session['is_admin'])",
        "• @admin_required decorator protection",
        "• Flash messages for errors",
        "• Redirect to admin dashboard on success"
    ]
    for feat in admin_login_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(PageBreak())
    
    # Page 11: Admin Dashboard
    elements.append(Paragraph("11. Admin Dashboard (admin/dashboard.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/admin/dashboard</b> (GET) - Admin Required", heading2_style))
    
    dashboard_desc = """
    Central admin control panel with statistics, revenue tracking, and quick action buttons. 
    Provides overview of entire ferry booking system.
    """
    elements.append(Paragraph(dashboard_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Statistics Cards:</b>", heading2_style))
    stats = [
        "• <b>Total Bookings:</b> Count of all bookings",
        "• <b>Daily Revenue:</b> Today's earnings in MVR",
        "• <b>Monthly Revenue:</b> Current month's total",
        "• <b>Total Revenue:</b> All-time earnings",
        "• <b>Average Booking Value:</b> Revenue per booking",
        "• <b>Total Users:</b> Registered user count",
        "• <b>Active Schedules:</b> Number of routes"
    ]
    for stat in stats:
        elements.append(Paragraph(stat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Quick Actions:</b>", heading2_style))
    actions = [
        "• Manage Bookings - View/cancel bookings",
        "• Manage Schedules - Add/edit ferry schedules",
        "• View Payments - Verify payment proofs",
        "• Reports - Analytics and charts",
        "• Settings - System configuration"
    ]
    for action in actions:
        elements.append(Paragraph(action, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Recent Activity:</b>", heading2_style))
    activity_desc = """
    Shows last 10 bookings with reference numbers, passenger names, routes, dates, 
    and total amounts. Provides quick overview of recent transactions.
    """
    elements.append(Paragraph(activity_desc, styles['BodyText']))
    
    elements.append(PageBreak())
    
    # Page 12: Manage Bookings
    elements.append(Paragraph("12. Manage Bookings (admin/bookings.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/admin/bookings</b> (GET) - Admin Required", heading2_style))
    
    manage_bookings_desc = """
    Complete booking management interface. Allows admin to view all bookings, 
    search, filter, and cancel bookings if needed.
    """
    elements.append(Paragraph(manage_bookings_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    manage_features = [
        "• Paginated booking list (all bookings)",
        "• Search by booking reference or passenger name",
        "• Filter by date, route, payment status",
        "• Sortable columns",
        "• Cancel booking action (POST /admin/bookings/<id>/cancel)",
        "• View complete booking details",
        "• Payment status indicators"
    ]
    for feat in manage_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Table Columns:</b>", heading2_style))
    columns = [
        "• Booking Reference",
        "• Passenger Name & Email",
        "• Route (Departure → Destination)",
        "• Date & Time",
        "• Seats (count & numbers)",
        "• Total Price",
        "• Payment Method",
        "• Payment Status",
        "• Actions (View, Cancel)"
    ]
    for col in columns:
        elements.append(Paragraph(col, feature_style))
    
    elements.append(PageBreak())
    
    # Page 13: Manage Schedules
    elements.append(Paragraph("13. Manage Schedules (admin/schedules.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/admin/schedules</b> (GET, POST) - Admin Required", heading2_style))
    
    manage_schedules_desc = """
    Schedule management interface for creating and maintaining ferry departure times. 
    Supports both recurring schedules and date-specific schedules.
    """
    elements.append(Paragraph(manage_schedules_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    schedule_manage_features = [
        "• Add new schedule form (departure, destination, time)",
        "• Choose between recurring or date-specific",
        "• View all existing schedules",
        "• Delete schedules (POST /admin/schedules/<id>/delete)",
        "• Toggle active/inactive status",
        "• Grouped by route",
        "• Time format validation (HH:MM)"
    ]
    for feat in schedule_manage_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Schedule Types:</b>", heading2_style))
    types_desc = [
        "• <b>Recurring Schedules:</b> Apply to all dates (stored in 'schedules' table)",
        "• <b>Daily Schedules:</b> Specific date only (stored in 'daily_schedules' table)"
    ]
    for t in types_desc:
        elements.append(Paragraph(t, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Common Schedule Times:</b>", heading2_style))
    times = "08:00, 10:00, 12:00, 14:00, 16:00, 18:00"
    elements.append(Paragraph(times, styles['BodyText']))
    
    elements.append(PageBreak())
    
    # Page 14: Payment Verification
    elements.append(Paragraph("14. Payment Verification (admin/payments.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/admin/payments</b> (GET) - Admin Required", heading2_style))
    
    payments_desc = """
    Payment proof verification interface. Allows admin to review uploaded payment 
    receipts and update payment status.
    """
    elements.append(Paragraph(payments_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Features:</b>", heading2_style))
    payment_verify_features = [
        "• List all bookings with payment information",
        "• View uploaded payment proof files",
        "• Payment method display (Bank Transfer, Upload, etc.)",
        "• Payment status (Pending, Verified, Failed)",
        "• Filter by payment status",
        "• Search by booking reference",
        "• Download payment proof images"
    ]
    for feat in payment_verify_features:
        elements.append(Paragraph(feat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Payment Information Display:</b>", heading2_style))
    payment_display = [
        "• Booking Reference",
        "• Passenger Name",
        "• Total Amount",
        "• Payment Method",
        "• Payment Status",
        "• Uploaded File (if applicable)",
        "• Booking Date"
    ]
    for item in payment_display:
        elements.append(Paragraph(item, feature_style))
    
    elements.append(PageBreak())
    
    # Page 15: Revenue Reports
    elements.append(Paragraph("15. Revenue Reports (admin/reports.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/admin/reports</b> (GET) - Admin Required", heading2_style))
    
    reports_desc = """
    Advanced analytics page with interactive Chart.js visualizations. Provides 
    comprehensive revenue insights and booking trends.
    """
    elements.append(Paragraph(reports_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Charts & Analytics:</b>", heading2_style))
    charts = [
        "• <b>Daily Revenue Chart:</b> Line chart showing last 30 days earnings",
        "• <b>Monthly Revenue Chart:</b> Bar chart for year-to-date monthly totals",
        "• <b>Top Routes:</b> Pie chart of most popular routes by booking count",
        "• <b>Payment Methods:</b> Doughnut chart showing payment type distribution"
    ]
    for chart in charts:
        elements.append(Paragraph(chart, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Statistics Summary:</b>", heading2_style))
    report_stats = [
        "• Total revenue (all-time)",
        "• Average booking value",
        "• Total bookings count",
        "• Revenue growth percentage",
        "• Peak booking days",
        "• Most profitable routes"
    ]
    for stat in report_stats:
        elements.append(Paragraph(stat, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Technology:</b>", heading2_style))
    tech_desc = "Chart.js 4.4.0 for interactive, responsive charts with tooltips and legends. Database-agnostic queries using Python datetime filtering."
    elements.append(Paragraph(tech_desc, styles['BodyText']))
    
    elements.append(PageBreak())
    
    # Page 16: System Settings
    elements.append(Paragraph("16. System Settings (admin/settings.html)", heading1_style))
    elements.append(Paragraph("Route: <b>/admin/settings</b> (GET, POST) - Admin Required", heading2_style))
    
    settings_desc = """
    Comprehensive system configuration panel. Allows admin to modify core settings, 
    manage pricing, and maintain the application.
    """
    elements.append(Paragraph(settings_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("<b>Configuration Sections:</b>", heading2_style))
    
    elements.append(Paragraph("<i>1. System Configuration</i>", heading2_style))
    system_config = [
        "• Ferry Capacity: Set maximum seats (1-100)",
        "• Changes saved to config.json file",
        "• Immediate effect (no restart needed)",
        "• Current capacity displayed"
    ]
    for item in system_config:
        elements.append(Paragraph(item, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<i>2. Pricing Management</i>", heading2_style))
    pricing = [
        "• Select route from dropdown (all available routes)",
        "• Update price per seat in MVR",
        "• Real-time price updates",
        "• Saved to config.json for persistence",
        "• Current prices displayed in table"
    ]
    for item in pricing:
        elements.append(Paragraph(item, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<i>3. Admin Account</i>", heading2_style))
    account = [
        "• Change admin password",
        "• Current password verification",
        "• New password confirmation",
        "• Minimum 6 characters required",
        "• Session remains active after change"
    ]
    for item in account:
        elements.append(Paragraph(item, feature_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<i>4. Database Maintenance</i>", heading2_style))
    db_maintenance = [
        "• Export all bookings to CSV file",
        "• Clear old bookings (older than specified days)",
        "• Database size information",
        "• Backup functionality",
        "• CSRF protection on all forms"
    ]
    for item in db_maintenance:
        elements.append(Paragraph(item, feature_style))
    
    elements.append(PageBreak())
    
    # Summary Page
    elements.append(Paragraph("Frontend Features Summary", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    summary_text = """
    The OceanLine Ferry Service features a comprehensive frontend built with modern web 
    technologies. The application includes 16 responsive pages (9 public, 7 admin) with 
    CSS3 animations, AJAX-powered interactions, and Chart.js analytics. All pages follow 
    Bootstrap 5.3 design patterns with CSRF protection and form validation.
    """
    elements.append(Paragraph(summary_text, styles['BodyText']))
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("<b>Key Technologies:</b>", heading2_style))
    tech_summary = [
        "• Bootstrap 5.3 - Responsive UI framework",
        "• jQuery 3.6 - DOM manipulation and AJAX",
        "• Chart.js 4.4.0 - Data visualization",
        "• CSS3 Animations - Fade-in and slide effects",
        "• Jinja2 Templates - Server-side rendering",
        "• Flask-WTF - CSRF protection",
        "• Flask-Login - User session management"
    ]
    for tech in tech_summary:
        elements.append(Paragraph(tech, feature_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_data = [
        ['Student:', 'Hassan Solih'],
        ['ID:', 'ST7078'],
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Pages:', '16 Frontend Pages'],
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
    print(f"✅ Frontend PDF generated successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_frontend_pdf()

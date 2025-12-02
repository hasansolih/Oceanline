"""
Generate System Diagrams PDF
Creates visual diagrams for the OceanLine Ferry Booking System
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, Preformatted, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime

def create_diagrams_pdf():
    """Generate the diagrams PDF document"""
    
    filename = "OceanLine_System_Diagrams.pdf"
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
    
    diagram_style = ParagraphStyle(
        'Diagram',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.black,
        backColor=colors.HexColor('#f8f9fa'),
        leftIndent=10,
        rightIndent=10,
        spaceAfter=15,
        leading=14
    )
    
    # Title Page
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph("OceanLine Ferry Service", title_style))
    elements.append(Paragraph("System Diagrams", heading1_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Project info
    info_data = [
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Student ID:', 'ST7078'],
        ['Name:', 'Hassan Solih'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Diagrams:', '8 System Diagrams'],
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
        "1. System Architecture Diagram",
        "2. Database Schema (ERD)",
        "3. User Flow Diagram",
        "4. Admin Flow Diagram",
        "5. Booking Process Flowchart",
        "6. MVC Architecture",
        "7. API Request-Response Flow",
        "8. Deployment Architecture"
    ]
    
    for item in toc_items:
        elements.append(Paragraph(item, styles['Normal']))
        elements.append(Spacer(1, 6))
    
    elements.append(PageBreak())
    
    # Diagram 1: System Architecture
    elements.append(Paragraph("1. System Architecture Diagram", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    arch_desc = """
    High-level view of the OceanLine ferry booking system showing all major components 
    and their interactions across different layers.
    """
    elements.append(Paragraph(arch_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    arch_diagram = """
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Browser    │  │    Mobile    │  │   Desktop    │          │
│  │  (Chrome,    │  │   Browser    │  │   Browser    │          │
│  │   Safari)    │  │              │  │              │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │ HTTP/HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            Jinja2 Templates (HTML/CSS/JS)               │   │
│  │  • base.html (Master Layout)                            │   │
│  │  • Public Pages: index, book, login, register           │   │
│  │  • Admin Pages: dashboard, bookings, schedules          │   │
│  │  • Bootstrap 5.3 + jQuery + Chart.js                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONTROLLER LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Flask Routes (app.py)                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │   │
│  │  │   Public   │  │    API     │  │   Admin    │        │   │
│  │  │   Routes   │  │  Endpoints │  │   Routes   │        │   │
│  │  └────────────┘  └────────────┘  └────────────┘        │   │
│  │  • Authentication (@login_required, @admin_required)    │   │
│  │  • CSRF Protection (Flask-WTF)                          │   │
│  │  • Request Validation                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  • Seat Availability Checking                           │   │
│  │  • Price Calculation (ROUTE_PRICES)                     │   │
│  │  • Booking Reference Generation                         │   │
│  │  • Revenue Analytics                                    │   │
│  │  • Config Management (config.json)                      │   │
│  │  • PDF Generation (ReportLab)                           │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA ACCESS LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              SQLAlchemy ORM                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │   │
│  │  │   User   │  │  Ferry   │  │ Schedule │             │   │
│  │  │  Model   │  │ Booking  │  │  Models  │             │   │
│  │  └──────────┘  └──────────┘  └──────────┘             │   │
│  │  • Query Builder                                        │   │
│  │  • Transaction Management                               │   │
│  │  • Database Abstraction                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              MySQL / SQLite Database                    │   │
│  │  Tables: users, ferry_bookings, schedules,              │   │
│  │          daily_schedules                                │   │
│  │  • Indexes on: email, booking_reference, date           │   │
│  │  • Foreign Keys: user_id                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │   Stripe   │  │    File    │  │    PDF     │               │
│  │    API     │  │  Storage   │  │ Generation │               │
│  │ (Optional) │  │ (uploads/) │  │ (ReportLab)│               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
    """
    elements.append(Preformatted(arch_diagram, diagram_style))
    
    elements.append(PageBreak())
    
    # Diagram 2: Database Schema (ERD)
    elements.append(Paragraph("2. Database Schema (ERD)", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    erd_desc = """
    Entity-Relationship Diagram showing all database tables, columns, data types, 
    relationships, and constraints.
    """
    elements.append(Paragraph(erd_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    erd_diagram = """
┌─────────────────────────────────────────────────────────────────┐
│                             USERS                                │
├─────────────────────────────────────────────────────────────────┤
│ PK  id               INTEGER                                     │
│ UK  email            VARCHAR(100)      [INDEXED]                 │
│     password_hash    VARCHAR(255)                                │
│     name             VARCHAR(100)                                │
│     phone            VARCHAR(30)       [NULLABLE]                │
│     created_at       DATETIME          [DEFAULT: now()]          │
└─────────────┬───────────────────────────────────────────────────┘
              │ 1
              │
              │ has many
              │
              ▼ *
┌─────────────────────────────────────────────────────────────────┐
│                       FERRY_BOOKINGS                             │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                   INTEGER                                 │
│ UK  booking_reference    VARCHAR(20)   [INDEXED]                 │
│ FK  user_id              INTEGER       [NULLABLE → users.id]     │
│     name                 VARCHAR(100)                            │
│     email                VARCHAR(100)                            │
│     phone                VARCHAR(30)                             │
│     departure            VARCHAR(100)                            │
│     destination          VARCHAR(100)                            │
│     date                 DATE                                    │
│     time                 VARCHAR(10)                             │
│     seats                INTEGER                                 │
│     selected_seats       VARCHAR(200)                            │
│     total_price          FLOAT                                   │
│     payment_method       VARCHAR(50)   [NULLABLE]                │
│     payment_status       VARCHAR(30)   [NULLABLE]                │
│     payment_info         VARCHAR(300)  [NULLABLE]                │
│     is_roundtrip         BOOLEAN       [DEFAULT: False]          │
│     return_date          DATE          [NULLABLE]                │
│     return_time          VARCHAR(10)   [NULLABLE]                │
│     return_selected_seats VARCHAR(200) [NULLABLE]                │
│     created_at           DATETIME      [DEFAULT: now()]          │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                          SCHEDULES                               │
│                    (Recurring Schedules)                         │
├─────────────────────────────────────────────────────────────────┤
│ PK  id              INTEGER                                      │
│     departure       VARCHAR(100)                                 │
│     destination     VARCHAR(100)                                 │
│     time            VARCHAR(10)                                  │
│     active          BOOLEAN           [DEFAULT: True]            │
│     created_at      DATETIME          [DEFAULT: now()]           │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                      DAILY_SCHEDULES                             │
│                  (Date-Specific Schedules)                       │
├─────────────────────────────────────────────────────────────────┤
│ PK  id              INTEGER                                      │
│     departure       VARCHAR(100)                                 │
│     destination     VARCHAR(100)                                 │
│     date            DATE              [INDEXED]                  │
│     time            VARCHAR(10)                                  │
│     active          BOOLEAN           [DEFAULT: True]            │
│     created_at      DATETIME          [DEFAULT: now()]           │
└─────────────────────────────────────────────────────────────────┘


RELATIONSHIPS:
━━━━━━━━━━━━━
• users (1) ──── (0..*) ferry_bookings
  One user can have multiple bookings
  user_id in ferry_bookings is NULLABLE (allows guest bookings)

INDEXES:
━━━━━━━━
• users.email              (Unique, speeds up login)
• ferry_bookings.booking_reference (Unique, quick lookup)
• ferry_bookings.user_id   (Foreign key index)
• daily_schedules.date     (Fast date filtering)

CONSTRAINTS:
━━━━━━━━━━━━
• PK: Primary Keys auto-increment
• UK: Unique constraints prevent duplicates
• FK: Foreign key with CASCADE behavior
• DEFAULT: Auto-populated values
    """
    elements.append(Preformatted(erd_diagram, diagram_style))
    
    elements.append(PageBreak())
    
    # Diagram 3: User Flow
    elements.append(Paragraph("3. User Flow Diagram", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    user_flow_desc = """
    Complete user journey from landing on the website to receiving booking confirmation.
    """
    elements.append(Paragraph(user_flow_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    user_flow = """
                        ┌─────────────┐
                        │   START:    │
                        │  Homepage   │
                        │      /      │
                        └──────┬──────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
            ┌──────────────┐      ┌──────────────┐
            │ New User?    │      │ View         │
            │ Click        │      │ Schedules    │
            │ Register     │      │              │
            └──────┬───────┘      └──────┬───────┘
                   │                     │
                   ▼                     │
            ┌──────────────┐             │
            │  Register    │             │
            │  /register   │             │
            │ • Name       │             │
            │ • Email      │             │
            │ • Password   │             │
            └──────┬───────┘             │
                   │                     │
                   ▼                     │
            ┌──────────────┐             │
            │ Auto Login   │             │
            │ Session      │             │
            │ Created      │             │
            └──────┬───────┘             │
                   │                     │
                   └────────┬────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ Logged In?   │
                    └──────┬───────┘
                           │ Yes
                           ▼
                    ┌──────────────┐
                    │  Click       │
                    │  Book Now    │
                    │              │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Booking Form │
                    │    /book     │
                    │ • Route      │
                    │ • Date       │
                    │ • Time       │
                    │ • Seats      │
                    │ • Roundtrip? │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ AJAX Calls   │
                    │ • Get Price  │
                    │ • Get Times  │
                    │ • Check Seats│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Submit     │
                    │   Booking    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Seat         │
                    │ Selection    │
                    │/select_seats │
                    │ • Visual Grid│
                    │ • Pick Seats │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Booking      │
                    │ Reference    │
                    │ Generated    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Payment     │
                    │  /payment    │
                    │ • Bank Info  │
                    │ • Upload     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Confirmation │
                    │/confirmation │
                    │ • Success    │
                    │ • Download   │
                    │   Receipt    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ View in      │
                    │ My Bookings  │
                    │  /bookings   │
                    └──────────────┘
                           │
                           ▼
                        ┌──────┐
                        │ END  │
                        └──────┘
    """
    elements.append(Preformatted(user_flow, diagram_style))
    
    elements.append(PageBreak())
    
    # Diagram 4: Admin Flow
    elements.append(Paragraph("4. Admin Flow Diagram", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    admin_flow_desc = """
    Administrator workflow for managing the ferry booking system.
    """
    elements.append(Paragraph(admin_flow_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    admin_flow = """
                        ┌─────────────┐
                        │   START:    │
                        │Admin Login  │
                        │/admin/login │
                        └──────┬──────┘
                               │
                               ▼
                        ┌─────────────┐
                        │ Verify      │
                        │ Username &  │
                        │ Password    │
                        └──────┬──────┘
                               │
                               ▼
                        ┌─────────────┐
                        │ Set Session │
                        │ is_admin=   │
                        │    True     │
                        └──────┬──────┘
                               │
                               ▼
            ┌──────────────────┴──────────────────┐
            │         Admin Dashboard             │
            │        /admin/dashboard             │
            │  ┌────────────────────────────┐    │
            │  │ Stats:                     │    │
            │  │ • Total Bookings           │    │
            │  │ • Daily Revenue            │    │
            │  │ • Monthly Revenue          │    │
            │  │ • Total Revenue            │    │
            │  └────────────────────────────┘    │
            └──────────┬──────────────────────────┘
                       │
         ┌─────────────┼─────────────┬─────────────┬─────────────┐
         │             │             │             │             │
         ▼             ▼             ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│   Manage     │ │  Manage  │ │  Verify  │ │  View    │ │ System   │
│  Bookings    │ │Schedules │ │ Payments │ │ Reports  │ │ Settings │
│/admin/       │ │/admin/   │ │/admin/   │ │/admin/   │ │/admin/   │
│bookings      │ │schedules │ │payments  │ │reports   │ │settings  │
└──────┬───────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
       │              │            │            │            │
       ▼              ▼            ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│• View All    │ │• Add New │ │• Review  │ │• Daily   │ │• Ferry   │
│  Bookings    │ │  Schedule│ │  Upload  │ │  Revenue │ │  Capacity│
│• Search      │ │• Delete  │ │  Proofs  │ │  Chart   │ │• Route   │
│• Filter      │ │  Schedule│ │• Update  │ │• Monthly │ │  Prices  │
│• Cancel      │ │• Recurring│ │  Status  │ │  Revenue │ │• Password│
│  Booking     │ │  or Date │ │          │ │  Chart   │ │  Change  │
│              │ │  Specific│ │          │ │• Top     │ │• Export  │
│              │ │          │ │          │ │  Routes  │ │  CSV     │
└──────────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘

                        ┌─────────────┐
                        │   Logout    │
                        │/admin/logout│
                        └──────┬──────┘
                               │
                               ▼
                        ┌─────────────┐
                        │  END        │
                        └─────────────┘
    """
    elements.append(Preformatted(admin_flow, diagram_style))
    
    elements.append(PageBreak())
    
    # Diagram 5: Booking Process Flowchart
    elements.append(Paragraph("5. Booking Process Flowchart", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    booking_flowchart = """
                            START
                              │
                              ▼
                    ┌─────────────────┐
                    │ User Logged In? │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │ No              │ Yes
                    ▼                 ▼
            ┌───────────────┐   ┌──────────────┐
            │ Redirect to   │   │ Show Booking │
            │ Login Page    │   │ Form         │
            └───────────────┘   └──────┬───────┘
                    │                  │
                    └──────────────────┘
                                       │
                                       ▼
                            ┌──────────────────┐
                            │ Select Route     │
                            │ (Departure &     │
                            │  Destination)    │
                            └─────────┬────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │ AJAX: Get Price  │
                            │ from ROUTE_PRICES│
                            └─────────┬────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │ Select Date      │
                            └─────────┬────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │ AJAX: Get Times  │
                            │ (Check Schedules)│
                            └─────────┬────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │ Select Time      │
                            └─────────┬────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │ Select # of Seats│
                            └─────────┬────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │ AJAX: Check      │
                            │ Available Seats  │
                            └─────────┬────────┘
                                      │
                      ┌───────────────┴───────────────┐
                      │ Enough Seats Available?       │
                      └───────┬───────────┬───────────┘
                              │ No        │ Yes
                              ▼           ▼
                    ┌────────────────┐  ┌──────────────┐
                    │ Show Error:    │  │ Round Trip?  │
                    │ "Seats Full"   │  └──────┬───────┘
                    └────────────────┘         │
                                        ┌──────┴──────┐
                                        │ No          │ Yes
                                        ▼             ▼
                                ┌─────────────┐ ┌─────────────┐
                                │ Continue    │ │ Select      │
                                │             │ │ Return Date │
                                │             │ │ & Time      │
                                └──────┬──────┘ └──────┬──────┘
                                       │               │
                                       └───────┬───────┘
                                               │
                                               ▼
                                    ┌──────────────────┐
                                    │ Submit Form      │
                                    │ (POST /book)     │
                                    └─────────┬────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │ Create Booking   │
                                    │ in Database      │
                                    │ (Status: Pending)│
                                    └─────────┬────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │ Generate Booking │
                                    │ Reference (UUID) │
                                    └─────────┬────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │ Save to Session  │
                                    └─────────┬────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │ Redirect to      │
                                    │ Seat Selection   │
                                    └─────────┬────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │ Show Seat Grid   │
                                    │ (Visual Layout)  │
                                    └─────────┬────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │ User Selects     │
                                    │ Seats (jQuery)   │
                                    └─────────┬────────┘
                                              │
                                  ┌───────────┴───────────┐
                                  │ Correct # Selected?   │
                                  └───────┬───────┬───────┘
                                          │ No    │ Yes
                                          ▼       ▼
                                  ┌──────────┐ ┌──────────────┐
                                  │ Show     │ │ Update       │
                                  │ Warning  │ │ Booking with │
                                  └──────────┘ │ Seat Numbers │
                                               └──────┬───────┘
                                                      │
                                                      ▼
                                            ┌──────────────────┐
                                            │ Redirect to      │
                                            │ Payment Page     │
                                            └─────────┬────────┘
                                                      │
                                                      ▼
                                            ┌──────────────────┐
                                            │ Show Payment     │
                                            │ Options          │
                                            └─────────┬────────┘
                                                      │
                                            ┌─────────┴─────────┐
                                            │                   │
                                            ▼                   ▼
                                  ┌──────────────┐   ┌──────────────┐
                                  │ Bank Transfer│   │ Upload Proof │
                                  │ (Show Details)   │ (File Upload)│
                                  └──────┬───────┘   └──────┬───────┘
                                         │                  │
                                         └────────┬─────────┘
                                                  │
                                                  ▼
                                        ┌──────────────────┐
                                        │ Update Payment   │
                                        │ Info in Database │
                                        └─────────┬────────┘
                                                  │
                                                  ▼
                                        ┌──────────────────┐
                                        │ Redirect to      │
                                        │ Confirmation     │
                                        └─────────┬────────┘
                                                  │
                                                  ▼
                                        ┌──────────────────┐
                                        │ Show Success     │
                                        │ Message          │
                                        │ • Booking Ref    │
                                        │ • Download PDF   │
                                        └─────────┬────────┘
                                                  │
                                                  ▼
                                              END
    """
    elements.append(Preformatted(booking_flowchart, diagram_style))
    
    elements.append(PageBreak())
    
    # Diagram 6: MVC Architecture
    elements.append(Paragraph("6. MVC Architecture", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    mvc_desc = """
    Model-View-Controller pattern implementation in the OceanLine system.
    """
    elements.append(Paragraph(mvc_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    mvc_diagram = """
┌─────────────────────────────────────────────────────────────────┐
│                             VIEW                                 │
│                  (Jinja2 Templates + Frontend)                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Templates   │  │    Static    │  │  JavaScript  │          │
│  │              │  │    Assets    │  │              │          │
│  │ • base.html  │  │ • Bootstrap  │  │ • jQuery     │          │
│  │ • index.html │  │ • Custom CSS │  │ • AJAX Calls │          │
│  │ • book.html  │  │ • Animations │  │ • Chart.js   │          │
│  │ • admin/*    │  │              │  │              │          │
│  └──────┬───────┘  └──────────────┘  └──────┬───────┘          │
│         │                                    │                  │
│         └────────────────┬───────────────────┘                  │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           │ User Interaction
                           │ (HTTP Requests)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CONTROLLER                               │
│                    (Flask Route Handlers)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  @app.route('/book', methods=['GET', 'POST'])                   │
│  def book():                                                     │
│      # 1. Receive user request                                  │
│      # 2. Validate input data                                   │
│      # 3. Call Model for data operations                        │
│      # 4. Apply business logic                                  │
│      # 5. Pass data to View (template)                          │
│      # 6. Return rendered HTML or JSON                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Route Categories:                                     │    │
│  │  • Public Routes (/, /book, /login, /register)         │    │
│  │  • API Endpoints (/get_price, /get_times, /api/*)      │    │
│  │  • Protected Routes (@login_required)                  │    │
│  │  • Admin Routes (@admin_required)                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Decorators:                                                     │
│  • @login_required  → Check user session                        │
│  • @admin_required  → Verify admin access                       │
│  • @csrf.exempt     → Skip CSRF (for APIs)                      │
│                                                                  │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           │ Data Operations
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                           MODEL                                  │
│                   (SQLAlchemy ORM Classes)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  class User(UserMixin, db.Model):                               │
│      id = db.Column(db.Integer, primary_key=True)               │
│      email = db.Column(db.String(100), unique=True)             │
│      password_hash = db.Column(db.String(255))                  │
│      bookings = db.relationship('FerryBooking')                 │
│      def set_password(self, password): ...                      │
│      def check_password(self, password): ...                    │
│                                                                  │
│  class FerryBooking(db.Model):                                  │
│      id = db.Column(db.Integer, primary_key=True)               │
│      booking_reference = db.Column(db.String(20), unique=True)  │
│      user_id = db.Column(db.Integer, db.ForeignKey('users.id')) │
│      # ... more fields ...                                      │
│      def as_dict(self): ...                                     │
│                                                                  │
│  class Schedule(db.Model): ...                                  │
│  class DailySchedule(db.Model): ...                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Model Responsibilities:                               │    │
│  │  • Define database schema                              │    │
│  │  • Encapsulate data operations                         │    │
│  │  • Validate data integrity                             │    │
│  │  • Manage relationships                                │    │
│  │  • Provide query methods                               │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           │ Database Queries
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATABASE                                 │
│                      (MySQL / SQLite)                            │
├─────────────────────────────────────────────────────────────────┤
│  Tables: users, ferry_bookings, schedules, daily_schedules      │
└─────────────────────────────────────────────────────────────────┘


DATA FLOW:
──────────

User Action → VIEW → HTTP Request → CONTROLLER → MODEL → DATABASE
                ▲                                           │
                │                                           │
                │                                           ▼
                └──── Response ← Render ← Process ← Query Result
    """
    elements.append(Preformatted(mvc_diagram, diagram_style))
    
    elements.append(PageBreak())
    
    # Diagram 7: API Request-Response Flow
    elements.append(Paragraph("7. API Request-Response Flow", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    api_desc = """
    AJAX API endpoints for dynamic frontend interactions.
    """
    elements.append(Paragraph(api_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    api_flow = """
CLIENT (Browser)                        SERVER (Flask)
━━━━━━━━━━━━━━━                         ━━━━━━━━━━━━━━

┌─────────────────┐
│ User selects    │
│ route on form   │
└────────┬────────┘
         │
         │ POST /get_price
         │ { departure: "Male", 
         │   destination: "Hulhumale" }
         ▼
         ├──────────────────────────────→ ┌──────────────────┐
         │                                 │ @app.route(      │
         │                                 │   '/get_price',  │
         │                                 │   methods=['POST'])
         │                                 └────────┬─────────┘
         │                                          │
         │                                          ▼
         │                                 ┌──────────────────┐
         │                                 │ Extract request  │
         │                                 │ data from POST   │
         │                                 └────────┬─────────┘
         │                                          │
         │                                          ▼
         │                                 ┌──────────────────┐
         │                                 │ Lookup price in  │
         │                                 │ ROUTE_PRICES dict│
         │                                 └────────┬─────────┘
         │                                          │
         │                                          ▼
         │                                 ┌──────────────────┐
         │                                 │ jsonify({        │
         │                                 │   'price': 100   │
         │                                 │ })               │
         │                                 └────────┬─────────┘
         │                                          │
         │                 JSON Response            │
         │  ◄──────────────────────────────────────┘
         ▼
┌─────────────────┐
│ Receive JSON    │
│ { price: 100 }  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Update UI       │
│ Display: 100 MVR│
└─────────────────┘


SIMILAR FLOW FOR OTHER APIs:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POST /get_times
├─ Input: { departure, destination, date }
├─ Query: Schedule and DailySchedule models
└─ Output: { times: ["08:00", "10:00", "14:00"] }

POST /get_available_seats
├─ Input: { departure, destination, date, time }
├─ Query: FerryBooking.query.filter_by(...)
├─ Logic: Collect booked seats, calculate available
└─ Output: { booked_seats: ["1", "2", "5"] }

POST /pay
├─ Input: { booking_reference }
├─ Query: FerryBooking.query.filter_by(...)
├─ Logic: Generate PDF using ReportLab
└─ Output: Binary PDF file download

GET /api/bookings
├─ Query: FerryBooking.query.all()
├─ Logic: Convert to dict using as_dict()
└─ Output: [ {booking1}, {booking2}, ... ]


ERROR HANDLING:
━━━━━━━━━━━━━━━

┌─────────────────┐
│ Client Request  │
└────────┬────────┘
         │
         ▼
         ├──────────────────────────────→ Try:
         │                                    Process request
         │                                 Except Exception:
         │                                    Log error
         │                                    Return 500
         │                 Error Response     
         │  ◄──────────────────────────────  { error: "..." }
         ▼
┌─────────────────┐
│ Show error msg  │
└─────────────────┘
    """
    elements.append(Preformatted(api_flow, diagram_style))
    
    elements.append(PageBreak())
    
    # Diagram 8: Deployment Architecture
    elements.append(Paragraph("8. Deployment Architecture", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    deploy_desc = """
    Production deployment setup with recommended infrastructure.
    """
    elements.append(Paragraph(deploy_desc, styles['BodyText']))
    elements.append(Spacer(1, 0.2*inch))
    
    deploy_diagram = """
                        INTERNET
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DOMAIN & DNS                                │
│                  (oceanline.mv)                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SSL/TLS (HTTPS)                              │
│                   Let's Encrypt                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LOAD BALANCER                                  │
│              (nginx or AWS ALB)                                  │
│  • Route traffic to app servers                                 │
│  • SSL termination                                               │
│  • Static file serving                                           │
└──────────────┬──────────────────────────┬───────────────────────┘
               │                          │
      ┌────────┴────────┐        ┌───────┴────────┐
      ▼                 ▼        ▼                ▼
┌──────────┐      ┌──────────┐  ┌──────────┐  ┌──────────┐
│ APP      │      │ APP      │  │ APP      │  │ APP      │
│ SERVER 1 │      │ SERVER 2 │  │ SERVER 3 │  │ SERVER 4 │
└────┬─────┘      └────┬─────┘  └────┬─────┘  └────┬─────┘
     │                 │             │             │
     └─────────────────┴─────────────┴─────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              APPLICATION LAYER                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Gunicorn (WSGI Server)                                  │  │
│  │  • 4 worker processes                                    │  │
│  │  • worker_class: sync                                    │  │
│  │  • bind: 0.0.0.0:8000                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Flask Application (app.py)                              │  │
│  │  • Routes & Controllers                                  │  │
│  │  • Business Logic                                        │  │
│  │  • SQLAlchemy ORM                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────┬────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  MySQL Server (Primary)                                  │  │
│  │  • Connection Pool (SQLAlchemy)                          │  │
│  │  • InnoDB Engine                                         │  │
│  │  • Indexes on key fields                                 │  │
│  └─────────────────────┬────────────────────────────────────┘  │
│                        │                                         │
│  ┌─────────────────────▼────────────────────────────────────┐  │
│  │  MySQL Replica (Read-only)                               │  │
│  │  • For reporting queries                                 │  │
│  │  • Reduces load on primary                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    CACHING LAYER                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Redis Cache                                             │  │
│  │  • Session storage                                       │  │
│  │  • Frequently accessed data (schedules, prices)          │  │
│  │  • TTL: 5 minutes                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   FILE STORAGE                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  S3 / Object Storage                                     │  │
│  │  • Uploaded payment proofs                               │  │
│  │  • Generated PDF receipts                                │  │
│  │  • Static assets (if not using CDN)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  MONITORING & LOGGING                            │
│  • Application Logs → CloudWatch / ELK Stack                    │
│  • Performance Metrics → New Relic / Datadog                    │
│  • Error Tracking → Sentry                                      │
│  • Uptime Monitoring → UptimeRobot                              │
└─────────────────────────────────────────────────────────────────┘


DEVELOPMENT vs PRODUCTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Development:
• Flask dev server (single-threaded)
• SQLite database
• DEBUG = True
• Local file storage

Production:
• Gunicorn (multi-process)
• MySQL with replica
• DEBUG = False
• S3 object storage
• Redis caching
• Load balancer
• SSL/HTTPS
    """
    elements.append(Preformatted(deploy_diagram, diagram_style))
    
    elements.append(PageBreak())
    
    # Summary
    elements.append(Paragraph("Summary", heading1_style))
    elements.append(Spacer(1, 0.2*inch))
    
    summary_text = """
    The OceanLine Ferry Booking System implements a well-structured architecture with clear 
    separation of concerns across multiple layers. The system follows MVC pattern, uses RESTful 
    APIs for dynamic interactions, maintains data integrity through proper database design, and 
    provides comprehensive user and admin workflows. The deployment architecture supports 
    scalability and high availability for production environments.
    """
    elements.append(Paragraph(summary_text, styles['BodyText']))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_data = [
        ['Student:', 'Hassan Solih'],
        ['ID:', 'ST7078'],
        ['Project:', 'OceanLine Ferry Booking System'],
        ['Diagrams:', '8 System Diagrams'],
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
    print(f"✅ Diagrams PDF generated successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_diagrams_pdf()

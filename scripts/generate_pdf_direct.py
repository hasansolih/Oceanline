from app import app, FerryBooking, generate_pdf_receipt
import os

OUT = 'scripts/latest_receipt_direct.pdf'

with app.app_context():
    b = FerryBooking.query.order_by(FerryBooking.created_at.desc()).first()
    if not b:
        print('No bookings found.')
    else:
        print('Using booking ref:', b.booking_reference)
        buf = generate_pdf_receipt(b)
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, 'wb') as f:
            f.write(buf.getvalue())
        print('Saved PDF to', OUT)

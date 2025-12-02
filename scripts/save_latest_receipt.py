from app import app, FerryBooking
import os

OUT = 'scripts/latest_receipt.pdf'

with app.app_context():
    b = FerryBooking.query.order_by(FerryBooking.created_at.desc()).first()
    if not b:
        print('No bookings found.')
    else:
        ref = b.booking_reference
        print('Using booking ref:', ref)
        app.testing = True
        client = app.test_client()
        resp = client.post('/pay', data={'booking_ref': ref})
        if resp.status_code == 200 and resp.data:
            os.makedirs(os.path.dirname(OUT), exist_ok=True)
            with open(OUT, 'wb') as f:
                f.write(resp.data)
            print('Saved PDF to', OUT)
        else:
            print('Failed to get PDF: status', resp.status_code)

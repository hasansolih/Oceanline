from app import app, FerryBooking
import traceback

if __name__ == '__main__':
    with app.app_context():
        b = FerryBooking.query.order_by(FerryBooking.created_at.desc()).first()
        if not b:
            print('No bookings found in the database. Create a booking first.')
        else:
            ref = b.booking_reference
            print(f'Using booking reference: {ref}')
            # Use test client to fetch confirmation without starting server
            app.testing = True
            client = app.test_client()
            try:
                resp = client.get(f'/confirmation/{ref}')
                print('Status code:', resp.status_code)
                data = resp.get_data(as_text=True)
                print('\n--- Begin response snippet ---\n')
                print(data[:4000])
                print('\n--- End response snippet ---\n')
            except Exception:
                print('Exception occurred while rendering confirmation:')
                traceback.print_exc()

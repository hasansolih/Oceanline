from app import app, FerryBooking

if __name__ == '__main__':
    with app.app_context():
        bookings = FerryBooking.query.order_by(FerryBooking.created_at.desc()).limit(20).all()
        if not bookings:
            print('No bookings found in the database.')
        for b in bookings:
            print(f"ID: {b.id} | Ref: {b.booking_reference} | Name: {b.name} | Date: {b.date} | Time: {b.time} | Seats: {b.seats}")

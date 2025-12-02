import re
import io
from app import app

# Simple test to check bank slip upload
with app.test_client() as client:
    res = client.get('/book')
    html = res.get_data(as_text=True)
    m = re.search(r'name="csrf_token" value="([^"]+)"', html)
    csrf = m.group(1) if m else ''
    print('Got csrf:', bool(csrf))

    # Prepare form fields - use first available route from PORTS if possible
    # We'll choose sample values that should exist in the seeded schedules
    data = {
        'csrf_token': csrf,
        'departure': 'Male',
        'destination': 'Hulhumale',
        'date': '2025-12-01',
        'time': '08:00',
        'seats': '1',
        'trip_type': 'oneway',
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '12345',
        'payment_method': 'Bank Transfer'
    }

    # Create a fake file
    data['bank_slip'] = (io.BytesIO(b"fake-image-data"), 'slip.jpg')

    resp = client.post('/book', data=data, content_type='multipart/form-data', follow_redirects=True)
    print('POST /book status:', resp.status_code)
    text = resp.get_data(as_text=True)
    # show if redirected to select_seats
    if 'select seats' in text.lower() or '/select_seats' in resp.request.path:
        print('Redirected to select_seats or contains select seats text')
    # check uploads dir
    import os
    uploads = os.path.join(app.root_path, 'uploads')
    print('Uploads dir exists:', os.path.exists(uploads))
    if os.path.exists(uploads):
        print('Files in uploads:', os.listdir(uploads))

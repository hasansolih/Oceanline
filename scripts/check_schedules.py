from app import app

with app.test_client() as c:
    resp = c.get('/available_seats')
    print('STATUS', resp.status_code)
    if resp.status_code!=200:
        print(resp.data.decode('utf-8', errors='replace')[:2000])
    else:
        print('Rendered OK, length:', len(resp.data))

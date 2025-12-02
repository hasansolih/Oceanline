from app import app

tests = [
    ('Male','Hulhumale'),
    ('Hulhumale','Male'),
    ('Male','Velana International Airport'),
    ('Velana International Airport','Male'),
    ('K.Maafushi','Male'),
    ('Male','K.Maafushi'),
    ('Unknown','Male')
]

with app.test_client() as c:
    for dep, dest in tests:
        resp = c.post('/get_price', data={'departure': dep, 'destination': dest})
        print(dep, '->', dest, '=>', resp.status_code, resp.get_data(as_text=True)[:200])

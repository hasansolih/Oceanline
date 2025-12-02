from app import app, db
from sqlalchemy import inspect, text

with app.app_context():
    inspector = inspect(db.engine)
    if 'ferry_bookings' not in inspector.get_table_names():
        print('Table ferry_bookings does not exist. Nothing to do.')
        raise SystemExit(1)

    cols = [c['name'] for c in inspector.get_columns('ferry_bookings')]
    print('Existing columns:', cols)

    expected = {
        'payment_method': 'VARCHAR(50)',
        'payment_status': 'VARCHAR(30)',
        'payment_info': 'VARCHAR(300)',
        'is_roundtrip': 'BOOLEAN',
        'return_date': 'DATE',
        'return_time': 'VARCHAR(10)',
        'return_selected_seats': 'VARCHAR(200)'
    }

    for col, coltype in expected.items():
        if col in cols:
            print('Column exists:', col)
            continue
        print('Adding column:', col)
        dialect = db.engine.dialect.name
        try:
            with db.engine.connect() as conn:
                conn.execute(text(f"ALTER TABLE ferry_bookings ADD COLUMN {col} {coltype}"))
                conn.commit()
            print('Added', col)
        except Exception as e:
            print('Failed to add', col, '->', e)

    print('Done')

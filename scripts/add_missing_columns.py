import os
import sqlite3
from urllib.parse import urlparse

# Determine SQLite DB path from environment or default
db_url = os.getenv('DATABASE_URL', 'sqlite:///oceanline.db')
if db_url.startswith('sqlite:///'):
    db_path = db_url.replace('sqlite:///', '')
else:
    # if it's just a filename
    db_path = db_url

print('Using DB path:', db_path)
if not os.path.exists(db_path):
    print('Database file not found:', db_path)
    raise SystemExit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Columns we expect on ferry_bookings
expected = {
    'payment_method': 'TEXT',
    'payment_status': 'TEXT',
    'payment_info': 'TEXT',
    'is_roundtrip': 'INTEGER',
    'return_date': 'DATE',
    'return_time': 'TEXT',
    'return_selected_seats': 'TEXT'
}

# Get existing columns
cur.execute("PRAGMA table_info('ferry_bookings')")
cols = [r[1] for r in cur.fetchall()]
print('Existing columns:', cols)

for col, coltype in expected.items():
    if col not in cols:
        sql = f"ALTER TABLE ferry_bookings ADD COLUMN {col} {coltype}"
        print('Adding column:', col, 'SQL:', sql)
        try:
            cur.execute(sql)
            conn.commit()
            print('Added', col)
        except Exception as e:
            print('Failed to add', col, '->', e)
    else:
        print('Column exists:', col)

conn.close()
print('Done')

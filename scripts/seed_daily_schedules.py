"""
Seed date-specific schedules for the next N days using existing recurring schedules/times.
Creates DB entries in `daily_schedules` and writes a CSV `scripts/schedules_YYYYMMDD.csv`.
"""
from app import app, db, DailySchedule, SCHEDULES, FALLBACK_ROUTE_TIMES, PORTS
from datetime import date, timedelta, datetime
import csv

DAYS = 30
START = date.today()
CSV_PATH = f"scripts/schedules_{START.strftime('%Y%m%d')}_+{DAYS}d.csv"

# Build route -> times mapping: prefer SCHEDULES, else FALLBACK_ROUTE_TIMES
route_times = {}
for dep in PORTS:
    for dest in PORTS:
        if dep == dest:
            continue
        if (dep, dest) in SCHEDULES:
            route_times[(dep, dest)] = SCHEDULES[(dep, dest)]
        elif (dep, dest) in FALLBACK_ROUTE_TIMES:
            route_times[(dep, dest)] = FALLBACK_ROUTE_TIMES[(dep, dest)]

# Fallback default times
DEFAULT = ['09:00', '15:00']

rows = []
added = 0
with app.app_context():
    for day_offset in range(DAYS):
        d = START + timedelta(days=day_offset)
        for (dep, dest), times in route_times.items():
            if not times:
                times = DEFAULT
            for t in times:
                # avoid duplicates
                exists = DailySchedule.query.filter_by(departure=dep, destination=dest, date=d, time=t).first()
                if not exists:
                    ds = DailySchedule(departure=dep, destination=dest, date=d, time=t, active=True)
                    db.session.add(ds)
                    added += 1
                    rows.append({'departure': dep, 'destination': dest, 'date': d.isoformat(), 'time': t})
    db.session.commit()

# write CSV
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['departure','destination','date','time'])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"Seeded {added} daily schedule entries and wrote CSV to {CSV_PATH}")

from app import app, db, Schedule, FALLBACK_ROUTE_TIMES, SCHEDULES, PORTS

if __name__ == '__main__':
    with app.app_context():
        added = 0
        targets = ['Male', 'Velana International Airport']
        for p in PORTS:
            if p in targets:
                continue
            for target in targets:
                # try to find times for (p,target) or reverse
                times = FALLBACK_ROUTE_TIMES.get((p, target)) \
                        or FALLBACK_ROUTE_TIMES.get((target, p)) \
                        or SCHEDULES.get((p, target)) \
                        or SCHEDULES.get((target, p)) \
                        or ['09:00', '15:00']
                for t in times:
                    exists = Schedule.query.filter_by(departure=p, destination=target, time=t).first()
                    if not exists:
                        db.session.add(Schedule(departure=p, destination=target, time=t, active=True))
                        added += 1
        db.session.commit()
        print(f"Added {added} schedules for routes to Male and Velana International Airport from other ports.")

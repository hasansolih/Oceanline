from app import app, Schedule

if __name__ == '__main__':
    with app.app_context():
        schedules = Schedule.query.order_by(Schedule.departure, Schedule.destination, Schedule.time).all()
        from collections import defaultdict
        d = defaultdict(list)
        for s in schedules:
            d[(s.departure, s.destination)].append(s.time)

        for k in sorted(d.keys()):
            times = sorted(set(d[k]))
            print(f"{k[0]} -> {k[1]}: {', '.join(times)}")

        print(f"\nTotal schedule entries: {len(schedules)}")

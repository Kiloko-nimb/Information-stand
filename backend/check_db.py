from app.core.database import SessionLocal
from app.models.schedule import Schedule

db = SessionLocal()
count = db.query(Schedule).count()
print(f'Records in DB: {count}')

if count > 0:
    sample = db.query(Schedule).first()
    print(f'Sample: {sample.group_name} - {sample.subject}')

    # Show all groups
    groups = db.query(Schedule.group_name).distinct().all()
    print(f'\nGroups ({len(groups)}):')
    for g in groups[:5]:
        print(f'  - {g[0]}')

db.close()

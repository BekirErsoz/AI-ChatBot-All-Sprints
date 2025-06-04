import datetime, asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from api.db import SessionLocal, Preference

sch=AsyncIOScheduler()

@sch.scheduled_job("cron", minute=0)
def push():
    hour=datetime.datetime.utcnow().hour
    with SessionLocal() as db:
        for user, in db.execute(select(Preference.user).where(Preference.hour==hour)):
            print(f"[PUSH] {user}: mood check prompt")

def start(): sch.start()

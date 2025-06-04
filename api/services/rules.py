import datetime
from durable.lang import ruleset, when_all, m, post
from sqlalchemy import select, func
from api.db import SessionLocal, Mood

with ruleset("moods") as rs:
    @when_all(+m.user)
    def check(c):
        user=c.m.user
        with SessionLocal() as db:
            th=datetime.datetime.utcnow()-datetime.timedelta(days=3)
            cnt=db.scalar(select(func.count()).where(Mood.user==user, Mood.emotion=="negative", Mood.ts>=th))
            if cnt and cnt>=3:
                print(f"[RULE] {user} needs self-care suggestion")

def post_mood(user, emotion):
    post("moods", {"user":user,"emotion":emotion,"ts":datetime.datetime.utcnow().isoformat()})

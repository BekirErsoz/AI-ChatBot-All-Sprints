from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from jose import jwt
import datetime, secrets
from api.config import settings
from api.db import SessionLocal, User, Mood, Preference
from api.services.emotion import detect
from api.services.rules import post_mood
from api.services.crisis import is_crisis

router=APIRouter()
ALG="HS256"

def token(username, role):
    return jwt.encode({"sub":username,"role":role,"exp":datetime.datetime.utcnow()+datetime.timedelta(hours=6)}, settings.secret, ALG)

def auth(token:str=Depends(lambda: None)):
    if not token: raise HTTPException(401)
    try:
        d=jwt.decode(token,settings.secret,ALG)
        return d["sub"], d["role"]
    except: raise HTTPException(401)

class Reg(BaseModel):
    username:str
    password:str
    role:str=Field("normal", pattern="^(admin|normal|ogrenci|misafir)$")

@router.post("/register")
def register(r:Reg):
    with SessionLocal() as db:
        if db.query(User).filter_by(username=r.username).first():
            raise HTTPException(400,"exists")
        db.add(User(username=r.username,password=r.password,role=r.role)); db.commit()
    return {"ok":True}

class Login(BaseModel):
    username:str
    password:str

@router.post("/login")
def login(body:Login):
    with SessionLocal() as db:
        u=db.query(User).filter_by(username=body.username,password=body.password).first()
        if not u: raise HTTPException(400,"bad creds")
        return {"token":token(u.username,u.role)}

class Chat(BaseModel):
    text:str

@router.post("/chat")
def chat(c:Chat, bg:BackgroundTasks, u=Depends(auth)):
    if is_crisis(c.text):
        return {"reply":"Lütfen hemen 112'yi arayın veya bir profesyonele ulaşın."}
    emo,score=detect(c.text)
    with SessionLocal() as db:
        db.add(Mood(user=u[0],emotion=emo,score=score)); db.commit()
    bg.add_task(post_mood,u[0],emo)
    sugg = "Kısa bir yürüyüş yapmayı düşün!" if emo=="negative" else None
    return {"reply":f"({emo}) seni anlıyorum.", "suggestion":sugg}

class PrefIn(BaseModel):
    hour:int=Field(ge=0,le=23)

@router.post("/pref")
def pref(p:PrefIn, u=Depends(auth)):
    with SessionLocal() as db:
        pr=db.query(Preference).filter_by(user=u[0]).first() or Preference(user=u[0])
        pr.hour=p.hour; db.add(pr); db.commit()
    return {"ok":True}

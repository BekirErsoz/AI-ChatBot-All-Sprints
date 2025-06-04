import fastapi_admin
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Model
from fastapi import FastAPI
from starlette.requests import Request
from api.db import engine, AsyncSessionLocal, User, MoodLog, Base
from api.config import settings
import jinja2, uvicorn, asyncio

class UserResource(Model):
    label="Kullanıcılar"
    model=User
    page_size=20

class MoodResource(Model):
    label="Duygu Kayıtları"
    model=MoodLog
    page_size=50

async def create_admin():
    await fastapi_admin.app.configure(
        engine=engine,
        session_maker=AsyncSessionLocal,
        admin_secret=settings.admin_password,
        templates=jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates"), autoescape=True
        ),
        providers=[
            UsernamePasswordProvider(
                admin_model=User,
                login_logo_url="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
            )
        ],
        resources=[UserResource, MoodResource],
    )

def build_app():
    app=FastAPI()
    app.mount("/admin", admin_app)
    return app

asyncio.run(create_admin())
app=build_app()

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.models import User, Publication, Comment, Favorite, Report, Sanction
from app.routers import auth, users, publications, comments, favorites, reports, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Emprendedores IPN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("app/static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(publications.router)
app.include_router(comments.router)
app.include_router(favorites.router)
app.include_router(reports.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"mensaje": "API del Sistema de Emprendedores IPN funcionando"}
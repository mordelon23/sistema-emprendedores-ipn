"""
Script para crear el primer administrador (admin semilla).
Ejecutar UNA SOLA VEZ con: python create_admin.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.utils.security import hash_password

Base.metadata.create_all(bind=engine)

EMAIL_ADMIN = "admin@alumno.ipn.mx"
PASSWORD_ADMIN = "Admin1234"
NOMBRE = "Admin"
APELLIDO = "Sistema"

db = SessionLocal()

existente = db.query(User).filter(User.email == EMAIL_ADMIN).first()
if existente:
    print(f"Ya existe un usuario con el correo {EMAIL_ADMIN}")
    if not existente.is_admin:
        existente.is_admin = True
        db.commit()
        print("El usuario fue promovido a administrador.")
    else:
        print("El usuario ya es administrador.")
else:
    admin = User(
        nombre=NOMBRE,
        apellido=APELLIDO,
        email=EMAIL_ADMIN,
        password_hash=hash_password(PASSWORD_ADMIN),
        is_admin=True,
        is_active=True,
    )
    db.add(admin)
    db.commit()
    print("✅ Admin creado correctamente.")
    print(f"   Correo: {EMAIL_ADMIN}")
    print(f"   Contraseña: {PASSWORD_ADMIN}")
    print("   ⚠️  Cambia esta contraseña después del primer login.")

db.close()
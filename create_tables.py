# Script para crear las tablas en la base de datos

from src.database.database import engine, Base
from src.models.user import User
from src.models.session import Session

def create_tables():
    """Crea todas las tablas definidas en los modelos"""
    print("Creando tablas en la base de datos.")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")

if __name__ == "__main__":
    create_tables()

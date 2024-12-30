from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv
import os
import logging

# Logging aktivieren
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


load_dotenv(override=True)

# Datenbank-URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL ist nicht in der Umgebung definiert.")

# Engine erstellen (verbindet SQLAlchemy mit der Datenbank)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session erstellen (für Abfragen und Transaktionen)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basis-Klasse für alle Modelle
Base = declarative_base()

# Testfunktion
def test_database_connection():
    """Testet die Verbindung zur Datenbank."""
    try:
        # Versuche eine Verbindung herzustellen
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))  # Verwende text()
            if result.scalar() == 1:
                print("Erfolgreiche Verbindung zur Datenbank!")
            else:
                print("Verbindung hergestellt, aber unerwartetes Ergebnis erhalten.")
    except Exception as e:
        print(f"Fehler bei der Verbindung zur Datenbank: {e}")

# __main__ Block
if __name__ == "__main__":
    test_database_connection()

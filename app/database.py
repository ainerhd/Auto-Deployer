from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
import logging

# Logging aktivieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env-Datei laden
load_dotenv(override=True)

# Datenbank-URL aus Umgebungsvariablen abrufen
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL ist nicht in der Umgebung definiert.")

# Engine erstellen (verbindet SQLAlchemy mit der Datenbank)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session erstellen (für Abfragen und Transaktionen)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basis-Klasse für alle Modelle
Base = declarative_base()

def test_database_connection():
    """Testet die Verbindung zur Datenbank."""
    try:
        # Verbindung testen
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                logger.info("Erfolgreiche Verbindung zur Datenbank!")
            else:
                logger.warning("Verbindung hergestellt, aber unerwartetes Ergebnis erhalten.")
    except Exception as e:
        logger.error(f"Fehler bei der Verbindung zur Datenbank: {e}")

def initialize_database():
    """Erstellt die Tabellen, falls sie noch nicht existieren."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Datenbanktabellen erfolgreich erstellt.")
    except Exception as e:
        logger.error(f"Fehler beim Initialisieren der Datenbank: {e}")

def get_database_structure():
    """Zeigt die aktuelle Struktur der Datenbank an (Tabellen, Spalten, Relationen, Primary Keys, Indizes und Unique Constraints)."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if not tables:
            logger.info("Keine Tabellen in der Datenbank gefunden.")
            return

        logger.info("Aktuelle Struktur der Datenbank:")
        for table in tables:
            logger.info(f"Tabelle: {table}")

            # Spalten anzeigen
            columns = inspector.get_columns(table)
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                default = f"Default: {column['default']}" if column['default'] else ""
                logger.info(f"  - {column['name']} ({column['type']}, {nullable}) {default}")

            # Relationen anzeigen
            foreign_keys = inspector.get_foreign_keys(table)
            if foreign_keys:
                logger.info("  Relationen:")
                for fk in foreign_keys:
                    logger.info(
                        f"    - {fk['constrained_columns']} referenziert {fk['referred_table']}({fk['referred_columns']})"
                    )

            # Primary Key anzeigen
            pk = inspector.get_pk_constraint(table)
            if pk and pk.get('constrained_columns'):
                logger.info(f"  Primary Key: {pk['constrained_columns']}")

            # Indizes anzeigen
            indexes = inspector.get_indexes(table)
            if indexes:
                logger.info("  Indizes:")
                for index in indexes:
                    unique = "UNIQUE" if index['unique'] else ""
                    logger.info(f"    - {index['name']} ({', '.join(index['column_names'])}) {unique}")

            # Unique Constraints anzeigen
            unique_constraints = inspector.get_unique_constraints(table)
            if unique_constraints:
                logger.info("  Unique Constraints:")
                for uc in unique_constraints:
                    logger.info(f"    - {uc['name']} ({', '.join(uc['column_names'])})")

            # Engine-Typ (nur für MySQL/MariaDB)
            with engine.connect() as connection:
                result = connection.execute(text(f"SHOW TABLE STATUS LIKE '{table}'"))
                table_status = result.fetchone()
                if table_status and 'Engine' in table_status:
                    logger.info(f"  Engine: {table_status['Engine']}")

    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Datenbankstruktur: {e}")


if __name__ == "__main__":
    test_database_connection()
    get_database_structure()

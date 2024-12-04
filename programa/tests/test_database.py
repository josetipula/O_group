import sqlite3
import pytest
from sqlite3 import Error
from programa.scripts.create_db import create_connection, create_tables, insert_initial_data
@pytest.fixture
def setup_database():
    # Crear una base de datos temporal para pruebas
    db_file = ":memory:"  # Usamos la base de datos en memoria para pruebas rápidas
    conn = create_connection(db_file)
    create_tables(conn)  
    insert_initial_data(conn)  # Insertar datos iniciales
    yield conn
    conn.close()

def test_tables_created(setup_database):
    conn = setup_database
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuarios';")
    result = c.fetchone()
    assert result is not None, "La tabla 'Usuarios' no fue creada."

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Conciertos';")
    result = c.fetchone()
    assert result is not None, "La tabla 'Conciertos' no fue creada."

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Tickets';")
    result = c.fetchone()
    assert result is not None, "La tabla 'Tickets' no fue creada."

def test_initial_data_inserted(setup_database):
    conn = setup_database
    c = conn.cursor()

    c.execute("SELECT nombre, email FROM Usuarios WHERE email = 'juan.arez@email.com';")
    result = c.fetchone()
    assert result is not None, "El usuario 'Juan arez' no fue insertado."
    assert result[0] == 'Juan arez', "El nombre del usuario no es correcto."

    c.execute("SELECT nombre, fecha FROM Conciertos WHERE nombre = 'Concierto A';")
    result = c.fetchone()
    assert result is not None, "El concierto 'Concierto A' no fue insertado."
    assert result[0] == 'Concierto A', "El nombre del concierto no es correcto."

    c.execute("SELECT estado, usuario_id, concierto_id FROM Tickets WHERE estado = 'comprado';")
    result = c.fetchone()
    assert result is not None, "El ticket 'comprado' no fue insertado."
    assert result[0] == 'comprado', "El estado del ticket no es correcto."
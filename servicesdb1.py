import psycopg2
from psycopg2 import sql

DB_HOST = "127.0.0.1"
DB_NAME = "database1"
DB_USER = "user1"
DB_PASS = "password1"

def get_db_connection():
    try:
      conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
      )
      return conn
    except Exception as e:
      print(f"Erro ao conectar ao banco de dados: {e}")
      return None

def create_table():
    conn = get_db_connection()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS backup-db1 (
                id SERIAL PRIMARY KEY,
                file VARCHAR(255)
            );
        """)
        conn.commit()
        print("Tabela criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        cur.close()
        conn.close()

def insert_data(file):
    conn = get_db_connection()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO backup-db1 (file) VALUES (%s)",
            (file)
        )
        conn.commit()
        print("Dados inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        cur.close()
        conn.close()

def read_data():
    conn = get_db_connection()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM backup-db1;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Erro ao ler dados: {e}")
    finally:
        cur.close()
        conn.close()

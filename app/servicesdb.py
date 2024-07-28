import psycopg2
from psycopg2 import sql

def get_db_connection(DB_HOST,DB_PORT, DB_NAME, DB_USER, DB_PASS):
  try:
    conn = psycopg2.connect(
      host=DB_HOST,
      port=DB_PORT,
      database=DB_NAME,
      user=DB_USER,
      password=DB_PASS
    )
    return conn
  except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    return None

def create_table(TABLE_NAME, connection):
  if connection is None:
    return

  cur = connection.cursor()
  try:
    query = sql.SQL("""
      CREATE TABLE IF NOT EXISTS {} (
        id SERIAL PRIMARY KEY,
        file VARCHAR(255)
      );
    """).format(sql.Identifier(TABLE_NAME))

    cur.execute(query)
    connection.commit()
    print("Tabela criada com sucesso.")
  
  except Exception as e:
    print(f"Erro ao criar tabela: {e}")
  finally:
    cur.close()
    connection.close()

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

def read_data(connection):
  if connection is None:
    return

  cur = connection.cursor()
  try:
    cur.execute("SELECT * FROM backup-db1;")
    rows = cur.fetchall()
    for row in rows:
      print(row)
  except Exception as e:
    print(f"Erro ao ler dados: {e}")
  finally:
    cur.close()
    connection.close()

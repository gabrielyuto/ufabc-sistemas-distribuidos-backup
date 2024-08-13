import psycopg2
from psycopg2 import sql

def get_db_connection():
  DB_HOST = "localhost"
  DB_PORT = "5432"
  DB_USER = "user"
  DB_PASS = "password"
  DB_NAME = "database"

  try:
    conn = psycopg2.connect(
      host=DB_HOST,
      port=DB_PORT,
      user=DB_USER,
      password=DB_PASS,
      database=DB_NAME,
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
        file BYTEA,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def prepare_db():
  connection = get_db_connection()
  create_table("server1", connection)

  connection = get_db_connection()
  create_table("server2", connection)

  connection = get_db_connection()
  create_table("server3", connection)

def count_register(TABLE_NAME):
  connection = get_db_connection()

  if connection is None:
    return

  cur = connection.cursor()
  try:
    query = sql.SQL(
      """
      SELECT COUNT(*) FROM {};
      """
    ).format(sql.Identifier(TABLE_NAME))    

    cur.execute(query)
    total = cur.fetchone()[0]
    
    return total
  except Exception as e:
    print(f"Erro ao ler dados: {e}")
  finally:
    cur.close()
    connection.close()

def save(TABLE_NAME, file_value):
  conn = get_db_connection()
  
  if conn is None:
    return

  cur = conn.cursor()
  try:
    query = sql.SQL("""
            INSERT INTO {} (file) VALUES (%s);
        """).format(sql.Identifier(TABLE_NAME)) 

    cur.execute(query, [psycopg2.Binary(file_value)])
    conn.commit()
    print("Dados inseridos com sucesso.")
  except Exception as e:
    print(f"Erro ao inserir dados: {e}")
  finally:
    cur.close()
    conn.close()

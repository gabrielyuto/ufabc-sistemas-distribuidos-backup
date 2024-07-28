import servicesdb

def execute():
  # Cria a tabela do banco do servidor 1
  DB_HOST = "127.0.0.1"
  DB_PORT = "5432"
  DB_NAME = "database1"
  DB_USER = "user1"
  DB_PASS = "password1"

  connection = servicesdb.get_db_connection(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
  servicesdb.create_table("server1", connection)

  # Cria a tabela do banco do servidor 2

  DB_HOST2 = "127.0.0.1"
  DB_PORT2 = "5433"
  DB_NAME2 = "database2"
  DB_USER2 = "user2"
  DB_PASS2 = "password2"

  connection = servicesdb.get_db_connection(DB_HOST2, DB_PORT2, DB_NAME2, DB_USER2, DB_PASS2)
  servicesdb.create_table("server2", connection)
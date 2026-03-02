from dotenv import load_dotenv
import os
import pymysql
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

class DatabaseWrapper:
    

    #costruttore, contiene i dati di connessione al db
    def __init__(self, host, user, password, database, port):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port, 
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.create_table()  #chiama il metodo sotto

    @classmethod
    def from_env(cls):
        host = os.getenv("DB_HOST", "localhost")
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "")
        database = os.getenv("DB_NAME", "spesa_db")
        port = int(os.getenv("DB_PORT", "3306"))
        return cls(host, user, password, database, port)

    def get_db_connection(self):
        return self.connect()

    #apre la connessione ogni volta che serve
    def connect(self):
        return pymysql.connect(**self.db_config)

    #operazioni INSERT, DELETE (tutte le op di DML e DDL)
    def execute_query(self, query, params=()):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
        conn.close()

    #SELECT (ritorna lista di dizionari)
    def fetch_query(self, query, params=()):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        conn.close()
        return result
    
    #da qui in poi dipende dal progetto
    #prima uguale x ogni progetto

    #qui creiamo la/le tabella/e
    def create_table(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS shopping_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                elemento VARCHAR(100) NOT NULL
            )
        ''')

    def get_user_items(self, username):
        rows = self.fetch_query(
            "SELECT elemento FROM shopping_items WHERE username = %s ORDER BY id",
            (username,)
        )
        return [row["elemento"] for row in rows]

    def add_user_item(self, username, elemento):
        self.execute_query(
            "INSERT INTO shopping_items (username, elemento) VALUES (%s, %s)",
            (username, elemento)
        )

    def delete_user_item_by_index(self, username, item_index):
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id
                    FROM shopping_items
                    WHERE username = %s
                    ORDER BY id
                    LIMIT 1 OFFSET %s
                    """,
                    (username, item_index),
                )
                row = cursor.fetchone()
                if not row:
                    return False

                cursor.execute(
                    "DELETE FROM shopping_items WHERE id = %s",
                    (row["id"],),
                )
                conn.commit()
                return True
        finally:
            conn.close()

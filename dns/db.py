import mysql.connector
from mysql.connector.errors import DatabaseError
from time import sleep

config = {
        'user': 'user',
        'password': 'test_pass',
        'host': 'mysql',
        'port': '3306',
        'database': 'db'
      }

def execute(statement, args={}, node_factory=False, factory=False):
    while True:
        try:
            db = mysql.connector.connect(**config)
        except DatabaseError as e:
            print(f"Recieved DatabaseError: {e}")
            sleep(1)
            continue
        break
    cursor = db.cursor(dictionary=True)
    cursor.execute(statement, args)

    if factory:
        return [ row for row in cursor ]
    else:
        db.commit()

def dns_lookup():
    query = query = """
    SELECT ip FROM nodes
    WHERE connection = 1
    ORDER BY RAND()
    LIMIT 25
    """
    return execute(query, factory=True)

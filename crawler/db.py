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
create_nodes_table_query = """
CREATE TABLE IF NOT EXISTS nodes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    ip VARCHAR(255),
    port INT DEFAULT 8333,
    version INT,
    services INT,
    user_agent VARCHAR(255),
    latest_block INT,
    relay BOOLEAN,
    connection BOOLEAN DEFAULT 0,
    connection_failures INT DEFAULT 0,
    UNIQUE(ip, port)
)
"""
create_relationship_table_query = """
CREATE TABLE IF NOT EXISTS relationships (
    node_id INT,
    peer_id INT,
    FOREIGN KEY(node_id) REFERENCES nodes(id),
    FOREIGN KEY(peer_id) REFERENCES nodes(id),
    UNIQUE(node_id, peer_id),
    constraint not_equal check (node_id <> peer_id)
)
"""

def add_columns_to_nodes():
  query = """
  ALTER TABLE nodes
  ADD tor BOOLEAN,
  ADD failures INT
  """


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

    if node_factory:
        from node import Node
        return [ Node(**row) for row in cursor ]
    elif factory:
        return [ row for row in cursor ]
    else:
        db.commit()

# def executemany(statement, args={}, row_factory=None):
#     with mysql.connector.connect(**config) as conn:
#         if row_factory:
#             conn.row_factory = row_factory
#         return conn.executemany(statement, args)

def create_tables():
    execute(create_nodes_table_query)
    # execute(create_relationship_table_query)

def drop_tables():
    # execute('DROP TABLE IF EXISTS relationships')
    execute('DROP TABLE IF EXISTS nodes')

def drop_and_create_tables():
    drop_tables()
    create_tables()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# def node_factory(cursor):
#     from node import Node
#     print("hello world")
#     for row in cursor:
#         print(row)
#     # return Node(*dictionary.generate())

def relationship_factory(cursor, row):
    d = {}
    keys = ["source", "target"]
    for idx, col in enumerate(cursor.description):
        d[keys[idx]] = row[idx]
    return d

def all_nodes():
    return execute("SELECT * FROM nodes", node_factory=True)

def all_ids():
    return execute("SELECT id FROM nodes WHERE connection = 1", node_factory=True)

def create_node(query_args):
    query = """
    INSERT IGNORE INTO nodes (
        {keys_1}
    ) VALUES (
        {keys_2}
    )
    """.format(
        keys_1=", ".join(query_args.keys()),
        keys_2=", ".join([f"%({key})s" for key in query_args.keys()])
    )
    execute(query, query_args)
    return execute(f"SELECT * FROM nodes WHERE ip = '{query_args['ip']}'", node_factory=True)[0]

def format_keys(keys):
    return ", ".join([f"{key} = %({key})s" for key in keys])

def find_node_by(args):
    query = """
    SELECT * FROM nodes WHERE
    {formatted_keys}
    """.format(formatted_keys=format_keys(args.keys()))

    return execute(query, args, node_factory=True)[0]

def nodes_where(args):
    query = """
    SELECT * FROM nodes WHERE
    {formatted_keys}
    """.format(formatted_keys=format_keys(args.keys()))

    return execute(query, args, node_factory=True)

def update_node(node_id, query_args):
    query = """
    UPDATE nodes
    SET
        {formatted_keys}
    WHERE
        id = {node_id}
    """.format(formatted_keys=format_keys(query_args.keys()), node_id=node_id)
    execute(query, query_args)
    return execute(f"SELECT * FROM nodes WHERE id = '{node_id}'", node_factory=True)[0]

def node_count():
    return execute("SELECT COUNT(*) FROM nodes", factory=True)[0]['COUNT(*)']

def unconnected_nodes(count):
    query = """
    SELECT * FROM nodes
    WHERE connection = 0
    ORDER BY connection_failures
    LIMIT {count}
    """.format(count=count)
    return execute(query, node_factory=True)


# def add_peers(node_id, peer_ids):
#     query = """
#       INSERT or IGNORE INTO relationships (
#         node_id, peer_id
#       ) VALUES (
#         :node_id, :peer_id
#       )
#     """
#     args = [ { "node_id": node_id, "peer_id": peer_id } for peer_id in peer_ids ]
#     executemany(query, args)

# def all_relationships():
#     query = """
#     SELECT node_id, peer_id FROM relationships
#     LEFT JOIN nodes ON relationships.peer_id=nodes.id
#     WHERE nodes.connection = 1
#     """
#     return [execute(query, row_factory=relationship_factory).fetchall()]

def tor_nodes():
    return  execute("SELECT * FROM nodes WHERE ip like '%fd87:d87e:eb43%'",  node_factory=True)

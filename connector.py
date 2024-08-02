import psycopg2 as pg

connection_string = "host=localhost dbname=cashflow user=postgres password=secret"

def select(query: str) -> list:
    """ Select query to PG """
    with pg.connect(connection_string) as conn:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()

def update(query: str):
    """ Update query to PG """
    with pg.connect(connection_string) as conn:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

def insert(query: str):
    """ Insert query to PG """
    with pg.connect(connection_string) as conn:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

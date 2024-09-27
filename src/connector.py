import psycopg2 as pg

class Connector:
    __connection_string = "host=localhost dbname=cashflow user=postgres password=secret"

    def __execute_query(self, query: str):
        """Query execution"""

        with pg.connect(self.__connection_string) as conn:
            cur = conn.cursor()
            cur.execute(query) 
            conn.commit()
            
            return cur

    def select(self, query: str) -> list:
        """Select query to PG"""

        cur = self.__execute_query(query)
        return cur.fetchall()

    def update(self, query: str):
        """Update query to PG"""
        self.__execute_query(query)

    def insert(self, query: str):
        """Insert query to PG"""
        self.__execute_query(query)

from connector import Connector
from utils import today_int

class Logger:

    def __init__(self) -> None:
        self.conn = Connector()

    def info(self, message: str):
        """ Info log message """

        query = f"""
        insert into public.game_log (game_id, message_txt)
        VALUES ({today_int()}, '{message}')
        """
        self.conn.insert(query)

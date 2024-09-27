from connector import Connector
from utils import today_int

class Api:

    def __init__(self) -> None:
        self.conn = Connector()

    def get_balance(self, user_id: int) -> int:
        """ Current user`s balance """

        game_id = today_int()
        query = f"""
        select sum(value) as balance
        from transaction
        where game_id = {game_id} and user_id = {user_id}
        """
        return self.conn.select(query)[0][0]

    def transaction(self, user_id:int, value: int, desc: str = None) -> None:
        """ Transaction """

        game_id = today_int()
        query = f"""
        insert into public.transaction (game_id, user_id, value, description) 
        VALUES ({game_id}, {user_id}, {value}, '{desc}')
        """
        self.conn.insert(query)

    def get_cashflow(self, user_id: int) -> int:
        """ Get current cashflow """

        game_id = today_int()
        query = f"""
        select value
        from public.cashflow
        where game_id = {game_id} and user_id = {user_id}
        order by changed_dttm DESC
        limit 1
        """
        return self.conn.select(query)[0][0]

    def set_cashflow(self, user_id: int, cashflow: int) -> None:
        """ Set new cashflow value """

        game_id = today_int()
        query = f"""
        insert into public.cashflow (game_id, user_id, value) 
        VALUES ({game_id}, {user_id}, {cashflow})
        """
        self.conn.insert(query)

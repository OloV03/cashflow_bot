from datetime import datetime
from connector import insert, select

def today_int():
    """ Today date in int format """
    dt_time = datetime.today()
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

def get_balance(user_id: int) -> int:
    """ Current user`s balance """
    
    game_id = today_int()
    query = f"""
    select sum(value) as balance
    from transaction
    where game_id = {game_id} and user_id = {user_id}
    """
    return select(query)[0][0]

def transaction(user_id:int, value: int, desc: str = None) -> None:
    game_id = today_int()
    query = f"""
    insert into public.transaction (game_id, user_id, value, description) 
    VALUES ({game_id}, {user_id}, {value}, '{desc}')
    """
    insert(query)

def get_cashflow(user_id: int) -> int:
    pass

def get_costs(user_id: int) -> int:
    pass

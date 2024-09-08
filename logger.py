from connector import insert
from datetime import datetime

def today_int():
    """ Today date in int format """
    
    dt_time = datetime.today()
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

def info(message: str):
    """ Info log message """

    query = f"""
    insert into public.game_log (game_id, message_txt)
    VALUES ({today_int()}, '{message}')
    """
    insert(query)

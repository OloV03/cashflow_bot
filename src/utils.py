from datetime import datetime

def today_int() -> int:
    """ Today date in int format """
    dt_time = datetime.today()
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

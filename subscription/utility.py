def calculate_amount(interval):  
    if interval == 'm':  
        return 165  
    elif interval == 's':  
        return 495 
    elif interval == 'h':  
        return 990
    elif interval == 'y':
        return 1980    
     

def calculate_end_date(interval):  
    from datetime import timedelta  
    import datetime

    if interval == 'm':  
        return datetime.date.today() + timedelta(days=30)  
    elif interval == 's':  
        return datetime.date.today() + timedelta(days=90)  
    elif interval == 'h':  
        return datetime.date.today() + timedelta(days=180)
    elif interval == 'y':
        return datetime.date.today() + timedelta(days=365)    
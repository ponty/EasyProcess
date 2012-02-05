

def uniencode(s):
    if isinstance(s, unicode):
        s = s.encode('utf-8')      
    return s  

def unidecode(s):
    if isinstance(s, str):
        s = s.decode('utf-8')      
    return s  

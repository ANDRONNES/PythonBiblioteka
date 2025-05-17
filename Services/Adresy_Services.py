import sqlite3

conn = sqlite3.connect('Data Base/biblioteka.db')
cursor = conn.cursor()

# Zrobie tak bo wszystkie wartości są kluczami głównymi
def isAdresExists(Miasto:str,Ulica:str,Numer_Domu:int,Numer_Mieszkania)->bool:
    cursor.execute('Select count(*) from Adres where Miasto = ? AND Ulica =? AND Numer_Domu = ? AND Numer_Mieszkania = ?',(Miasto,Ulica,Numer_Domu,Numer_Mieszkania))
    result = cursor.fetchone()[0]
    return result > 0
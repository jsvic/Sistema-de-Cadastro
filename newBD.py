import sqlite3 as lite

# Connecting to the database
con = lite.connect('database.db')

# Creating a table 'inventario'
with con:
    cur = con.cursor()
    cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, cpf TEXT, rg TEXT, ufRG text,  marital_status TEXT, date_birth DATE, address TEXT, number TEXT, complement TEXT, neighborhood TEXT, city TEXT, uf TEXT, cep TEXT, home_phone TEXT, phone TEXT, email TEXT, admission_date DATE, sector TEXT, cep_sector TEXT, phone_sector TEXT, bank TEXT, agency TEXT, account TEXT, image TEXT)')
    
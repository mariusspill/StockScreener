import mysql.connector as sqlc

connection = sqlc.connect(
    user = "root",
    host = "localhost",
    database = "stockdb",
    passwd = "OpenPassword123"
)

cursor = connection.cursor()

def add_entry_company(name: str):
    cursor.execute(f"INSERT INTO company (name) VALUES ('{name}');")
    connection.commit()

def add_entry_company_identifiers(id: int, ticker: str, isin: str, wkn: str):
    cursor.execute(f"INSERT INTO company_identifiers (company_id, ticker, isin, wkn) VALUES ({id}, '{ticker}', '{isin}', '{wkn}');")
    connection.commit()


def get_data_identifiers():
    cursor.execute(f"""SELECT Company.id,
                    Company.name, 
                    Company_Identifiers.ticker, 
                    Company_Identifiers.isin, 
                    Company_Identifiers.wkn 
                    FROM Company JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id;""")
    return cursor.fetchall()

table = get_data_identifiers()
print(table)
import mysql.connector as sqlc
import data

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


def add_entry_income_statement(company_id: int, year: int, revenue: int = None, gross_profit:int = None, 
                               operating_income: int = None, net_income: int = None, EBIT: int = None, EBITDA: int = None,
                               cost_of_revenue:int = None, operating_expense: int = None, interest_cost: int = None, taxes: int = None):
    sql = """INSERT INTO income_statements (company_id, year, revenue, gross_profit,
                   operating_income, net_income, EBIT, EBITDA, cost_of_revenue, operating_expense, interest_cost, taxes) VALUES 
                   (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    params = (
        company_id,
        year,
        revenue,
        gross_profit,
        operating_income,
        net_income,
        EBIT,
        EBITDA,
        cost_of_revenue,
        operating_expense,
        interest_cost,
        taxes
    )

    cursor.execute(sql, params)
    connection.commit()


def update_entry_income_statement(id: int, column: str, value: int):
    cursor.execute(f"UPDATE income_statements SET {column} = {value} WHERE id = {id};")
    connection.commit()


def get_data_identifiers():
    cursor.execute(f"""SELECT Company.id,
                    Company.name, 
                    Company_Identifiers.ticker, 
                    Company_Identifiers.isin, 
                    Company_Identifiers.wkn 
                    FROM Company JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id;""")
    return cursor.fetchall()


def get_net_income(ticker: int, year: int):
    cursor.execute(f"""SELECT company.id, company_identifiers.ticker, income_statements.net_income
                   FROM Company INNER JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id
                   INNER JOIN income_statements ON company.id = income_statements.company_id
                   WHERE company_identifiers.ticker = '{ticker}' AND income_statements.year = {year};""")
    data = cursor.fetchall()
    print(data)
    return data[0][2]



def automate_data_insertion():
    # does this entry exist:
    cursor.execute(f"""SELECT company.id, company_identifiers.ticker, income_statements.net_income
                   FROM Company INNER JOIN Company_Identifiers ON Company.id = Company_Identifiers.company_id
                   INNER JOIN income_statements ON company.id = income_statements.company_id
                   WHERE company_identifiers.ticker = 'IBM' AND income_statements.year = 2023;""")
    data = cursor.fetchall()
    if data == []:
        print("record doesnt exist")
    else:
        print("record exists already")
        print(data)


automate_data_insertion()
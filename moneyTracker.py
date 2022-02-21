import sqlite3

connection = sqlite3.connect('transactionHistory.db')
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS money ( id varchar ,balance varchar )")

def moneyChecker ():
    cur.execute("SELECT balance FROM money WHERE id = 'CHEESE'")
    currentBalance = cur.fetchone()[0]

    return float(currentBalance)

def moneyUpdater (money):
    cur.execute("UPDATE money SET balance = '" +str(money)+ "' WHERE id = 'CHEESE'")
    connection.commit()

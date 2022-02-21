import yfinance as yf
import time
import sqlite3

con = sqlite3.connect('transactionHistory.db')
cur = con.cursor()


def addTransaction (purchaseTicker, purchaseAmount):
    ticker = yf.Ticker(purchaseTicker)
    todays_data = ticker.history(period='1d')
    currentPrice = todays_data['Close'][0]
    stocksOwned = float(purchaseAmount) / currentPrice
    #print(stocksOwned)
    cur.execute("SELECT EXISTS(SELECT 1 FROM history WHERE stockTicker='" + purchaseTicker + "')")
    checker = cur.fetchone()
    if checker[0] == 0:
        cur.execute("INSERT INTO history(stockTicker, stocksOwned, purchasePrice) VALUES ('" + str(purchaseTicker) + "','"+ str(stocksOwned) + "','" + str(currentPrice) + "')")
        con.commit()
        #cur.execute("UPDATE history SET stocksOwned = '"+str(stocksOwned)+"' WHERE sto)
    elif checker[0] == 1:
        cur.execute("SELECT stocksOwned, purchasePrice FROM history WHERE stockTicker='"+purchaseTicker+"'")
        amountandPrice = cur.fetchmany()
        #print(amountandPrice)
        amount = amountandPrice[0][0]
        price = amountandPrice[0][1]
        totalAmount = float(amount) + stocksOwned
        avgPrice = (float(price) + float(currentPrice)) / 2
        cur.execute("UPDATE history SET stocksOwned = '"+str(totalAmount)+"', purchasePrice = '"+str(avgPrice)+"' WHERE stockTicker='"+purchaseTicker+"'")
        con.commit()
        cur.execute("SELECT stocksOwned, purchasePrice from history WHERE stockTicker='"+purchaseTicker+"'")
        updatedAandP = cur.fetchmany()
        print(updatedAandP)

def sell_stock (sellTicker):
    #print(sellTicker)
    ticker = yf.Ticker(sellTicker)
    todays_data = ticker.history(period='1d')
    currentPrice = todays_data['Close'][0]
    cur.execute("SELECT EXISTS(SELECT 1 FROM history WHERE stockTicker='" + sellTicker + "')")
    #print(cur.fetchmany())
    cur.execute("SELECT stocksOwned, purchasePrice FROM history WHERE stockTicker='" + str(sellTicker) + "'")
    sellData = cur.fetchmany()
    #print(sellData)
    cur.execute("DELETE FROM history WHERE stockTicker='" + str(sellTicker) + "'")
    con.commit()
    sellData_ownedShares = sellData[0][0]
    sellData_purchasePrice = sellData[0][1]
    oP = float(sellData_purchasePrice) * float(sellData_ownedShares)
    profit = ((float(currentPrice) - float(sellData_purchasePrice)) * float(sellData_ownedShares)) + float(oP)
    return profit

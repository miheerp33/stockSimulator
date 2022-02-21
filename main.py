import yfinance
import plotly
import plotly.graph_objects as graphobjects
import PySimpleGUI as sg

import moneyTracker
import transactions
import sqlite3

#desiredTicker = input('Desired ticker: ')
#desiredTime = input('Desired time periiod: ')

con = sqlite3.connect('transactionHistory.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS history (id AutoNumber, stockTicker varchar, stocksOwned DOUBLE, purchasePrice DOUBLE)")


timeValues = ['1d', '1w', '1mo', '1y']



sg.theme('BluePurple')

layout = [[sg.Text('Insert ticker below.', key='bank')],
          [sg.Input(key='-IN-'), sg.Listbox( values=timeValues, key='time',
                                                                      select_mode='LISTBOX_SELECT_MODE_SINGLE',
                                             default_values=['1mo'])],
          [sg.Button('Search'), sg.Button('Exit')],
          [sg.Text('Stock info: '), sg.Text(size=(20,1), key='OUTPUT')],
          [sg.Input(key='purchaseAmount')], [sg.Button('Purchase')], [sg.Text(size=(20,1), key='ownedStocks')],
          [sg.Button('Sell', key="-SELL-")]]

window = sg.Window('Pattern 2B', layout)


total_bank = moneyTracker.moneyChecker()
while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Search':
        desiredTicker = values['-IN-']
        desiredTime = values['time'][0]
        ticker = yfinance.Ticker(desiredTicker)
        history = ticker.history(period=desiredTime)
        todays_data = ticker.history(period='1d')
        figure = graphobjects.Figure(data=graphobjects.Scatter(x=history.index, y=history['Close'],
                                                               mode='lines+markers'))
        figure.update_layout(title=ticker.info['longName'], font=dict(family="Courier New, monospace",
                                                                      size=18,
                                                                      color="Blue")
                             )
        figure.update_traces(marker=dict(color='red'))
        plotly.offline.plot(figure)
        window['OUTPUT'].update(todays_data['Close'][0])

        # Update the "output" text element to be the value of "input" element
    if event == 'Purchase':
        desiredTicker = values['-IN-']
        purchaseAmount = values['purchaseAmount']
        transactions.addTransaction(desiredTicker, purchaseAmount)
        total_bank = float(total_bank) - float(purchaseAmount)
        if total_bank < 0:
            window['bank'].update(str(total_bank) + '!!! IN DEBT !!!')
            moneyTracker.moneyUpdater(total_bank)
        else:
            window['bank'].update(total_bank)
            moneyTracker.moneyUpdater(total_bank)

    if event == '-SELL-':
        desiredTicker = values['-IN-']
        total_bank = moneyTracker.moneyChecker() + transactions.sell_stock(desiredTicker)
        window['bank'].update(total_bank)
        moneyTracker.moneyUpdater(total_bank)



window.close()
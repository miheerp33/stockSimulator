import yfinance
import plotly
import plotly.graph_objects as graphobjects
import PySimpleGUI as sg
#desiredTicker = input('Desired ticker: ')
#desiredTime = input('Desired time periiod: ')



timeValues = ['1d', '1w', '1mo', '1y']



sg.theme('BluePurple')

layout = [[sg.Text('Insert ticker below.')],
          [sg.Input(key='-IN-'), sg.Listbox( values=timeValues, key='time',
                                                                      select_mode='LISTBOX_SELECT_MODE_SINGLE')],
          [sg.Button('Search'), sg.Button('Exit')],
          [sg.Text('Stock info: '), sg.Text(size=(20,1), key='OUTPUT')]]

window = sg.Window('Pattern 2B', layout)

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


window.close()
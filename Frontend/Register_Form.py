import PySimpleGUI as sg
import Login

"""
    Simple Form (a one-shot data entry window)
    Use this design pattern to show a form one time to a user that is "submitted"
"""
def main():
    layout = [[sg.Text('Please enter your Username, Name, E-Mail Address, Password')],
              [sg.Text('Username', size=(10, 1)), sg.InputText(key='-USER-')],
              [sg.Text('E-Mail Address', size=(10, 1)), sg.InputText(key='-MAIL-')],
              [sg.Text('Repeat E-Mail Address', size=(10, 1)), sg.InputText(key='-REPEATMAIL-')],
              [sg.Text('Password', size=(10, 1)), sg.InputText(key="-PASSWORD-", password_char='*')],
              [sg.Text('Repeat Password', size=(10, 1)), sg.InputText(key="-REPEATEPASSWORD-", password_char='*')],
              [sg.Button('Absenden'), sg.Button('Zum Login')]]

    window = sg.Window('Simple Data Entry Window', layout)
    event, values = window.read(close=True)

    if event == 'Absenden':
        print('The events was ', event, 'You input',values['-USER-'], values['-MAIL-'], values['-REPEATMAIL-'], values['-PASSWORD-'], values['-REPEATEPASSWORD-'])
        #TODO Passwort & MAIL Validation


    if event == 'Zum Login':
        Login.main()

    else:
        print('User cancelled')
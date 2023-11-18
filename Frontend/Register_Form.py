import PySimpleGUI as sg
import Login

def main():
    custom_font = ('Helvetica', 16)
    layout = [
        [sg.Text('Please enter your:', font=('Helvetica', 24))],
        [sg.Text('Username', size=(25, 1), font=('Helvetica', 20)), sg.InputText(key='-USER-', font=('Helvetica', 20), size=(20, 1), pad=((0, 10), 10))],
        [sg.Text('E-Mail Addresse', size=(25, 1), font=('Helvetica', 20)), sg.InputText(key='-MAIL-', font=('Helvetica', 20), size=(20, 1), pad=((0, 10), 10))],
        [sg.Text('E-Mail Addresse wiederholen', size=(25, 1), font=('Helvetica', 20)), sg.InputText(key='-REPEATMAIL-', font=('Helvetica', 20), size=(20, 1), pad=((0, 10), 10))],
        [sg.Text('Passwort', size=(25, 1), font=('Helvetica', 20)), sg.InputText(key="-PASSWORD-", password_char='*', font=('Helvetica', 20), size=(20, 1), pad=((0, 10), 10))],
        [sg.Text('Passwort wiederholen', size=(25, 1), font=('Helvetica', 20)), sg.InputText(key="-REPEATEPASSWORD-", password_char='*', font=('Helvetica', 20), size=(20, 1), pad=((0, 10), 10))],
        [sg.Button('Absenden', size=(15, 1), font=custom_font, pad=(10, 10)), sg.Button('Zum Login', size=(15, 1), font=custom_font, pad=(10, 10))]
    ]

    window = sg.Window('Simple Data Entry Window', layout, size=(800, 350), font=custom_font, element_justification='center')

    event, values = window.read(close=True)

    if event == 'Absenden':
        print('The event was ', event, 'You input', values['-USER-'], values['-MAIL-'], values['-REPEATMAIL-'], values['-PASSWORD-'], values['-REPEATEPASSWORD-'])
        # TODO: Password & MAIL Validation

    if event == 'Zum Login':
        window.close()
        Login.main()

    else:
        print('User cancelled')


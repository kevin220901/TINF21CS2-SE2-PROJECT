import PySimpleGUI as sg
import Register_Form
import Login

# Define a custom font size
custom_font = ('Helvetica', 16)

layout = [
    [sg.Text("WELCOME TO BLOKUS!", font=('Helvetica', 24), justification='center')],
    [sg.Button("Login", size=(15, 2), font=custom_font, pad=(20, 10), key='login_button')],
    [sg.Button("Registrieren", size=(15, 2), font=custom_font, pad=(20, 10), key='register_button')],
    [sg.Button("Spiel verlassen", size=(15, 2), font=custom_font, pad=(20, 10), key='leave_button')]
]

window = sg.Window("BLOKUS", layout, size=(600, 400), font=custom_font, element_justification='center')

# Event loop
while True:
    event, values = window.read()

    if event == 'login_button':
        window.close()
        Login.main()
        break
    elif event == 'register_button':
        window.close()
        Register_Form.main()
        break
    elif event == 'leave_button':
        break
    elif event == sg.WIN_CLOSED:
        break

window.close()

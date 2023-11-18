import PySimpleGUI as sg
import Register_Form
import Blokus_Menu

# Define a custom font size
custom_font = ('Helvetica', 16)

# Define padding for buttons
button_padding = (10, 5)


def main():

    layout = [
        [sg.Text('Username:', font=('Helvetica', 24), justification='left'), sg.InputText(key='username', size=(20, 1))],
        [sg.Text('Password:', font=('Helvetica', 24), justification='left'), sg.InputText(key='password', password_char='*', size=(20, 1))],
        [sg.Button('Login', size=(15, 1), font=custom_font, pad=(10, 10)), sg.Button('Zur Registrierung', size=(15, 1), font=custom_font, pad=button_padding)]
    ]

    # Create the window
    window = sg.Window("BLOKUS", layout, size=(600, 150), font=custom_font, element_justification='center')

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        # Check if the login button is clicked
        if event == 'Login':
            username = values['username']
            password = values['password']
            window.close()
            Blokus_Menu.main()

            # Add your login logic here (for simplicity, just print the entered username and password)
            print(f'Username: {username}, Password: {password}')

        if event == 'Zur Registrierung':
            window.close()
            Register_Form.main()
            break

    # Close the window
    window.close()


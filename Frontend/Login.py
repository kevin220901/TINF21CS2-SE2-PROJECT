import PySimpleGUI as sg
import Register_Form
import Blokus_Menu


def main():
    # Define the layout of the GUI
    layout = [
        [sg.Text('Username:'), sg.InputText(key='username')],
        [sg.Text('Password:'), sg.InputText(key='password', password_char='*')],
        [sg.Button('Login'), sg.Button('Zur Registrierung')]
    ]

    # Create the window
    window = sg.Window('Login Window', layout)

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        # Check if the login button is clicked
        if event == 'Login':
            username = values['username']
            password = values['password']
            Blokus_Menu.main()

            # Add your login logic here (for simplicity, just print the entered username and password)
            print(f'Username: {username}, Password: {password}')

        if event == 'Zur Registrierung':
            Register_Form.main()
    # Close the window
    window.close()

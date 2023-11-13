import PySimpleGUI as sg

import Blokus_Menu

def main():
    # Sample user data
    user_data = {
        'username': 'JohnDoe',
        'email': 'john.doe@example.com',
        'password': 'securepassword'
    }

    # Define the layout of the GUI
    layout = [
        [sg.Text('Dein Profil', font=('Helvetica', 20))],
        [sg.Text('User Name'), sg.InputText(default_text=user_data['username'], key='username')],
        [sg.Text('E-Mail'), sg.InputText(default_text=user_data['email'], key='email')],
        [sg.Text('Password'), sg.InputText(password_char='*', key='password')],
        [sg.Text('Repeate Password'), sg.InputText(password_char='*', key='repeat_password')],
        [sg.Button('Änderungen speichern', key='save_changes'),
         sg.Button('Abbrechen', key='cancel')]
    ]

    # Create the window
    window = sg.Window('Dein Profil', layout, finalize=True)

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED or event == 'cancel':
            break

        # Handle button events
        if event == 'save_changes':
            new_username = values['username']
            new_email = values['email']
            new_password = values['password']
            repeated_password = values['repeat_password']

            # Add your logic for saving changes to the user profile
            if new_password == repeated_password:
                # Update the user data with the new values
                user_data['username'] = new_username
                user_data['email'] = new_email
                user_data['password'] = new_password

                sg.popup('Änderungen gespeichert!')
                Blokus_Menu.main()
            else:
                sg.popup('Passwörter stimmen nicht überein. Bitte wiederholen.')

        elif event == 'cancel':
            Blokus_Menu.main()
            sg.popup('Änderungen verworfen!')
            window.close()
    # Close the window
    window.close()

import PySimpleGUI as sg
import Blokus_Menu

# Define a custom font size
custom_font = ('Helvetica', 16)

# Define padding for buttons
button_padding = (10, 10)

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
        [sg.Text('User Name', font=custom_font, size=(20, 1)), sg.InputText(default_text=user_data['username'], key='username', font=custom_font, size=(25, 1))],
        [sg.Text('E-Mail', font=custom_font, size=(20, 1)), sg.InputText(default_text=user_data['email'], key='email', font=custom_font, size=(25, 1))],
        [sg.Text('Passwort', font=custom_font, size=(20, 1)), sg.InputText(password_char='*', key='password', font=custom_font, size=(25, 1))],
        [sg.Text('Passwort wiederholen', font=custom_font, size=(20, 1)), sg.InputText(password_char='*', key='repeat_password', font=custom_font, size=(25, 1))],
        [sg.Button('Änderungen speichern', key='save_changes', font=custom_font, pad=button_padding),
         sg.Button('Abbrechen', key='cancel', font=custom_font, pad=button_padding)]
    ]

    # Create the window
    window = sg.Window('Dein Profil', layout, finalize=True)

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED:
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

                sg.popup('Änderungen gespeichert!', font=('Helvetica', 18))
                Blokus_Menu.main()
            else:
                sg.popup('Passwörter stimmen nicht überein. Bitte wiederholen.')

        elif event == 'cancel':
            Blokus_Menu.main()
            sg.popup('Änderungen verworfen!', font=('Helvetica', 18))
            window.close()

    # Close the window
    window.close()


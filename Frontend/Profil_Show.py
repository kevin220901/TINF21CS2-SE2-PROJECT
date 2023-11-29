import PySimpleGUI as sg
import Blokus_Menu
import Profil_change

def main():
    # Sample user data
    user_data = {
        'username': 'JohnDoe',
        'email': 'john.doe@example.com'#,
        #'preferred_color': 'red'
    }

    # Define the layout of the GUI
    layout = [
        [sg.Text('Dein Profil', font=('Helvetica', 20))],
        [sg.Text(f'User Name: {user_data["username"]}', font=('Helvetica', 16))],
        [sg.Text(f'E-Mail: {user_data["email"]}', font=('Helvetica', 16))],
        #[sg.Text('Bevorzugte Farbe:'), sg.Button('', key='color_button', button_color=(user_data['preferred_color']), size=(5, 2))],
        [sg.Button('Profil bearbeiten', key='edit_profile', font=('Helvetica', 16), pad=(10, 5)),
         sg.Button('Profil löschen', key='delete_profile', font=('Helvetica', 16), pad=(10, 5)),
         sg.Button('Hauptmenü', key='main_menu', font=('Helvetica', 16), pad=(10, 5))]
    ]

    # Create the window
    window = sg.Window('Dein Profil', layout, finalize=True)

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED:
            window.close()
            break

        # Handle button events
        if event == 'edit_profile':
            window.close()
            Profil_change.main()
        elif event == 'delete_profile':
            # Add your logic for deleting the user profile
            sg.popup('Profil gelöscht!',font=('Helvetica', 18))
            window.close()
        elif event == 'main_menu':
            window.close()
            Blokus_Menu.main()

    # Close the window
    window.close()



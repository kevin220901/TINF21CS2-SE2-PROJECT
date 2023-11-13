import PySimpleGUI as sg
import Blokus_Menu


def main():
    # Define the layout of the GUI
    layout = [
        [sg.Text('Lobby Konfiguration', font=('Helvetica', 20))],

        # Section 1
        [sg.Text('Lobby Name')],
        [sg.InputText(key='lobby_name')],

        [sg.Radio('Öffentlich', 'lobby_type', key='public', default=True),
         sg.Radio('Privat', 'lobby_type', key='private')],

        [sg.Text('Passwort')],
        [sg.InputText(key='password', password_char='*')],

        # Section 2
        [sg.Text('AI-Schwierigkeit')],
        [sg.Radio('Leicht', 'ai_difficulty', key='easy', default=True),
         sg.Radio('Schwer', 'ai_difficulty', key='hard')],

        # Buttons
        [sg.Button('Lobby erstellen', key='create_lobby'),
         sg.Button('Abbrechen', key='cancel')]
    ]

    # Create the window
    window = sg.Window('Lobby Konfiguration', layout, finalize=True)

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED or event == 'cancel':
            break

        # Handle button events
        if event == 'create_lobby':
            lobby_name = values['lobby_name']
            lobby_type = 'Öffentlich' if values['public'] else 'Privat'
            password = values['password'] if values['private'] else 'Kein Passwort'
            ai_difficulty = 'Leicht' if values['easy'] else 'Schwer'

            # Add your logic for creating a lobby with the gathered information
            sg.popup(
                f'Lobby erstellt:\nName: {lobby_name}\nTyp: {lobby_type}\nPasswort: {password}\nAI-Schwierigkeit: {ai_difficulty}')

        if event == 'cancel':
            Blokus_Menu.main()



    # Close the window
    window.close()

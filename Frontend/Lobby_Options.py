import PySimpleGUI as sg
import Blokus_Menu
import Lobby_start

def main():
    # Define the layout of the GUI
    layout = [
        [sg.Text('Lobby Konfiguration', font=('Helvetica', 24), justification='center')],
        # Section 1
        [sg.Text('Lobby Name', font=('Helvetica', 16))],
        [sg.InputText(key='lobby_name', font=('Helvetica', 16))],

        [sg.Radio('Öffentlich', 'lobby_type', key='public', default=True, font=('Helvetica', 16)),
         sg.Radio('Privat', 'lobby_type', key='private', font=('Helvetica', 16))],

        [sg.Text('Passwort', font=('Helvetica', 16))],
        [sg.InputText(key='password', password_char='*', font=('Helvetica', 16))],

        # Section 2
        [sg.Text('AI-Schwierigkeit', font=('Helvetica', 16))],
        [sg.Radio('Leicht', 'ai_difficulty', key='easy', default=True, font=('Helvetica', 16)),
         sg.Radio('Schwer', 'ai_difficulty', key='hard', font=('Helvetica', 16))],

        # Buttons
        [sg.Button('Lobby erstellen', key='create_lobby', font=('Helvetica', 16)),
         sg.Button('Abbrechen', key='cancel', font=('Helvetica', 16))]
    ]

    # Create the window
    window = sg.Window('Lobby Konfiguration', layout, finalize=True, size=(600, 400), font=('Helvetica', 16), element_justification='center')

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED:
            break

        # Handle button events
        if event == 'create_lobby':
            lobby_name = values['lobby_name']
            lobby_type = 'Öffentlich' if values['public'] else 'Privat'
            password = values['password'] if values['private'] else 'Kein Passwort'
            ai_difficulty = 'Leicht' if values['easy'] else 'Schwer'

            # Add your logic for creating a lobby with the gathered information
            sg.popup(
                f'Lobby erstellt:\nName: {lobby_name}\nTyp: {lobby_type}\nPasswort: {password}\nAI-Schwierigkeit: {ai_difficulty}',
                font=('Helvetica', 18)  # Adjust the font size here
            )
            window.close()
            Lobby_start.main()

        if event == 'cancel':
            window.close()
            Blokus_Menu.main()


    # Close the window
    window.close()


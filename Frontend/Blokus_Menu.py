import PySimpleGUI as sg
import Profil_Show
import Lobby_beitreten
import Lobby_Options
import Options
def main():
    # Define the layout of the GUI
    layout = [
        [sg.Text('BLOKUS', font=('Helvetica', 20))],
        [sg.Button('Optionen', key='options', size=(10, 1), button_color=('white', '#333'))],
        [sg.Button('Lobby Erstellen', size=(20, 2), key='create_lobby')],
        [sg.Button('Lobby Beitreten', size=(20, 2), key='join_lobby')],
        [sg.Button('Profil', size=(20, 2), key='profile')],
        [sg.Button('Spiel Verlassen', size=(20, 2), key='leave_game')],
    ]

    # Create the window
    window = sg.Window('BLOKUS', layout, finalize=True)

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED:
            break

        # Handle button events
        if event == 'options':
            Options.main()
        elif event == 'create_lobby':
            Lobby_Options.main()
        elif event == 'join_lobby':
            Lobby_beitreten.main()
        elif event == 'profile':
            Profil_Show.main()
        elif event == 'leave_game':
            window.close()

    # Close the window
    window.close()
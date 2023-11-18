import PySimpleGUI as sg
import Profil_Show
import Lobby_beitreten
import Lobby_Options
import Options

# Define a custom font size
custom_font = ('Helvetica', 16)

# Define padding for buttons
button_padding = (20, 10)

def main():
    # Define the layout of the GUI
    layout = [
        [sg.Text('BLOKUS', font=('Helvetica', 20))],
        [sg.Button('Optionen', key='options', size=(10, 1), button_color=('white', '#333'), font=custom_font, pad=button_padding)],
        [sg.Button('Lobby Erstellen', size=(20, 2), key='create_lobby', font=custom_font, pad=button_padding)],
        [sg.Button('Lobby Beitreten', size=(20, 2), key='join_lobby', font=custom_font, pad=button_padding)],
        [sg.Button('Profil', size=(20, 2), key='profile', font=custom_font, pad=button_padding)],
        [sg.Button('Spiel Verlassen', size=(20, 2), key='leave_game', font=custom_font, pad=button_padding)],
    ]

    # Create the window
    window = sg.Window('BLOKUS', layout, finalize=True, size=(600, 600), font=custom_font, element_justification='center')

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED:
            break

        # Handle button events
        if event == 'options':
            window.close()
            Options.main()
        elif event == 'create_lobby':
            window.close()
            Lobby_Options.main()
        elif event == 'join_lobby':
            window.close()
            Lobby_beitreten.main()
        elif event == 'profile':
            window.close()
            Profil_Show.main()
        elif event == 'leave_game':
            window.close()

    # Close the window
    window.close()



import PySimpleGUI as sg
import Blokus_Menu

# Define a custom font size
custom_font = ('Helvetica', 16)

# Define padding for buttons
button_padding = (10, 5)

def create_lobby_layout(lobby_name, player_data):
    lobby_layout = [
        [sg.Text(lobby_name, font=('Helvetica', 24), justification='center')],
        [sg.Table(values=player_data, headings=['Player', 'Ready'], auto_size_columns=True, justification='center', display_row_numbers=False, num_rows=min(25, len(player_data)), font=custom_font, key='player_table', size=(100, 15))],
        [sg.Button('Ready', key='ready_button', size=(15, 2), font=custom_font, pad=button_padding),
         sg.Button('Spiel Starten', key='start_game_button', size=(15, 2), font=custom_font, pad=button_padding),
         sg.Button('Spiel Verlassen', key='leave_game_button', size=(15, 2), font=custom_font, pad=button_padding)]
    ]
    return lobby_layout

def create_chat_layout():
    chat_layout = [
        [sg.Multiline(size=(30, 15), key='chat_output', font=('Helvetica', 12))],
        [sg.InputText(key='chat_input', font=('Helvetica', 12), size=(20, 1)), sg.Button('Send', key='send_button', size=(15, 1), font=custom_font, pad=button_padding)]
    ]
    return chat_layout

def main():
    # Sample data for the lobby
    lobby_name = 'My Lobby'  # Lobby name here
    player_data = [['Player 1', False], ['Player 2', False], ['Player 3', False], ['Player 4', False]]  # Player names here

    # Create the lobby layout
    lobby_layout = create_lobby_layout(lobby_name, player_data)

    # Create the chat layout
    chat_layout = create_chat_layout()

    # Create the main layout
    main_layout = [
        [sg.Column(chat_layout), sg.VSeparator(), sg.Column(lobby_layout)]
    ]

    window = sg.Window('Game Lobby', main_layout, finalize=True, size=(1200, 400), font=custom_font, element_justification='center')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'ready_button':
            # Update the 'Ready' status for the current player
            selected_row = values['player_table']
            if selected_row:
                player_index = selected_row[0]  # Get the row index
                if 0 <= player_index < len(player_data):
                    player_data[player_index][1] = not player_data[player_index][1]
                    window['player_table'].update(values=player_data)

        elif event == 'start_game_button':
            # Check if all players are ready before starting the game
            all_players_ready = all(player[1] for player in player_data)
            if all_players_ready:
                sg.popup('Game starting!')
                window.close()
                # Game link here !!!

        elif event == 'leave_game_button':
            window.close()
            Blokus_Menu.main()

    window.close()



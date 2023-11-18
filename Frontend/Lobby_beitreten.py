import PySimpleGUI as sg
import Lobby_start

# Define a custom font size
custom_font = ('Helvetica', 16)

# Define padding for buttons
button_padding = (20, 10)

def main():
    # Sample data for the table
    lobbies = [
        ['Lobby 1', 3, 'Leicht'],
        ['Lobby 2', 2, 'Schwer'],
        ['Lobby 3', 4, 'Mittel'],
    ]

    # Define the layout of the GUI
    layout = [
        [sg.Text('Lobby suchen', font=('Helvetica', 24), justification='center')],
        [sg.Table(values=lobbies, headings=['Name', 'Spielerzahl', 'Schwierigkeit'],
                  auto_size_columns=False, justification='right',
                  display_row_numbers=False, num_rows=min(25, len(lobbies)),
                  col_widths=[15, 10, 15],
                  key='table')],
        [sg.Button('Beitreten', key='join_button', font=custom_font, pad=button_padding),
         sg.Button('Abbrechen', key='cancel', font=custom_font, pad=button_padding)]
    ]

    # Create the window
    window = sg.Window('Lobby suchen', layout, finalize=True, size=(800, 300), font=custom_font, element_justification='center')

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED:
            break

        # Handle button events
        if event == 'join_button':
            window.close()
            Lobby_start.main()
            selected_row = values['table'][0]

            if selected_row:
                lobby_name, player_count, difficulty = selected_row
                # Add your logic for joining the selected lobby
                sg.popup(f'Beitreten button clicked!\nLobby: {lobby_name}\nSpielerzahl: {player_count}\nSchwierigkeit: {difficulty}')

    # Close the window
    window.close()


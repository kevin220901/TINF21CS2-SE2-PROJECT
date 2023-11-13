import PySimpleGUI as sg
import Blokus_Menu
def main():
    # Define the layout of the GUI
    layout = [
        [sg.Text('Einstellungen', font=('Helvetica', 20))],

        # Section 1
        [sg.Text('Musik Lautstärke')],
        [sg.Slider(range=(0, 100), orientation='h', size=(20, 10), default_value=50, key='music_volume')],
        [sg.Text('Effekt Einstellung')],
        [sg.Slider(range=(0, 100), orientation='h', size=(20, 10), default_value=50, key='effect_volume')],

        # Section 2
        [sg.Text('Vollbild/Fenster')],
        [sg.Radio('Vollbild', 'fullscreen', key='fullscreen', default=True), sg.Radio('Fenster', 'fullscreen', key='windowed')],

        # Buttons
        [sg.Button('Einstellungen zurücksetzen', key='reset_settings'),
         sg.Button('Einstellungen Speichern', key='save_settings'),
         sg.Button('Zurück zum Spiel', key='back_to_game')]
    ]

    # Create the window
    window = sg.Window('Einstellungen', layout, finalize=True)

    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WINDOW_CLOSED:
            break

        # Handle button events
        if event == 'reset_settings':
            # Add logic for resetting settings
            sg.popup('Settings reset button clicked!')
        elif event == 'save_settings':
            # Add logic for saving settings
            sg.popup('Save settings button clicked!')
        elif event == 'back_to_game':
            Blokus_Menu.main()

    # Close the window
    window.close()


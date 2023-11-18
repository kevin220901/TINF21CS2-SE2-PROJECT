import PySimpleGUI as sg
import Blokus_Menu

# Define a custom font size
custom_font = ('Helvetica', 16)

# Define padding for buttons
button_padding = (20, 10)


def main():
    # Define the layout of the GUI
    layout = [
        [sg.Text('Einstellungen', font=('Helvetica', 24), justification='center')],

        # Section
        [sg.Text('Musik Lautstärke', font=('Helvetica', 16)),
         sg.Slider(range=(0, 100), orientation='h', size=(20, 10), default_value=50, key='music_volume')],
        [sg.Text('Effekt Einstellung', font=('Helvetica', 16)),
         sg.Slider(range=(0, 100), orientation='h', size=(20, 10), default_value=50, key='effect_volume')],


        # Buttons
        [sg.Button('Einstellungen zurücksetzen', key='reset_settings', font=custom_font, pad=button_padding),
         sg.Button('Einstellungen Speichern', key='save_settings', font=custom_font, pad=button_padding),
         sg.Button('Zurück zum Spiel', key='back_to_game', font=custom_font, pad=button_padding)]
    ]

    # Create the window
    window = sg.Window('Einstellungen', layout, finalize=True, size=(700, 200), font=custom_font,
                       element_justification='center')

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
            window.close()
            Blokus_Menu.main()

    # Close the window
    window.close()


# Run the main function if this script is executed
if __name__ == '__main__':
    main()

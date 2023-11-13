import PySimpleGUI as sg

import os.path

#layout 2 Spalten - blokus links - chat rechts

file_List_colum = [
    [
        sg.Text("BLOKUS"),
        sg.In(size=25,1), enable_events=True, key="GAME"
        #Import of the userinterface here
    ],
    [
        sg.Listbox(
            values = [], enable_events=True, size=(40,20),
            key="CHAT"
        )
    ],
]

game_integration_colum = [
    [sg.Text("BOILERPLATE TEXT HERE FOR GAME LATER")],
    [sg.Text(size=40,1), key="GAME"],
    [sg.Image(key="-IMAGE-")],
]

# Full layout
layout = [
    [
        sg.Column(file_List_colum),
        sg.VSeparator(),
        sg.Column
    ]
]

window = sg.Window("BLOKUS", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED
        break

window.close()
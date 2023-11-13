import PySimpleGUI as sg


import Register_Form
import Login

layout = [
    [sg.Text("WELCOME TO BLOKUS!")],
    [sg.Button("LOGIN")],
    [sg.Button("REGISTER")],
    [sg.Button("Spiel verlassen")]
        ]



window = sg.Window("BLOKUS", layout)

#eventloop
while True:
    event, values = window.read()
    if event == "LOGIN":
        Login.main()
        break
    elif event == "REGISTER" :
        Register_Form.main()
        break
    elif event == "Spiel verlassen":
        break
    elif event == sg.WIN_CLOSED:
        break
window.close()
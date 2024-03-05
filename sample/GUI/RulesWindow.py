import PySimpleGUI as sg
from sample.GUI import MainMenuWindow


class RulesWindow:
    def __init__(self, window):
        self.window = window

    def run(self):
        self.window.close()
        self.window = sg.Window('EpidemicSimulator', self.setLayout(), size=(800, 600), element_justification='center')
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
                break
            if event == '-MAIN MENU-':
                self.window.close()
                MainMenuWindow.MainMenuWindow().run()

    def setLayout(self):
        rules = self.readRules()
        return [[sg.Button('Main menu', font=('Helvetica', 16), key='-MAIN MENU-')],
                [sg.Text("Rules:", font=('Helvetica', 24))],
                [sg.Multiline(rules, size=(400, 300), font=('Helvetica', 16), justification='center')]]

    def readRules(self):
        with open('../resources/rules.txt') as f:
            contents = f.read() ##todo exception
        return contents

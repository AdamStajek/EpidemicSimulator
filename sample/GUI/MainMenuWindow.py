import PySimpleGUI as sg
from sample.GUI import GameWindow
from sample.GUI import RulesWindow


class MainMenuWindow:
    def run(self):
        self.setGuiParameters('darkgreen', '../resources/skull.ico')
        layout = self.setLayout()
        window = self.setWindow(layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
                break
            elif event == '-START-':
                self.startGameWindow(values, window)
            elif event == '-RULES-':
                RulesWindow.RulesWindow(window).run()

    def startGameWindow(self, values, window):
        try:
            initialPopulation = int(values['-POP-'])
            worldSize = int(values['-WSIZE-'])
            percentOfInitialInfected = int(values['-PER-'])
        except ValueError:
            raise ValueError("Incorrect parameters!") #todo error popup
        finally:
            if initialPopulation <= 0 or worldSize <= 0 or percentOfInitialInfected <= 0:
                raise ValueError("Incorrect parameters!")
            else:
                GameWindow.GameWindow(window, initialPopulation, worldSize, percentOfInitialInfected).run()

    def setGuiParameters(self, theme, icon):
        self.setTheme(theme)
        self.setIcon(icon)

    def setTheme(self, theme):
        sg.theme(theme)

    def setIcon(self, icon):
        sg.set_global_icon(icon)

    def setLayout(self):
        return [
            [sg.Text('Epidemic Simulator', font=('Helvetica', 40), justification='center', key='-TITLE-')],
            [sg.Image('../resources/main_menu.png', subsample=2)],
            [sg.Text("Enter parameters of the game:", font=('Helvetica', 14))],
            [sg.Text("Initial population:", size=20, font=('Helvetica', 14)), sg.Input(key='-POP-')],
            [sg.Text("World size:", size=20, font=('Helvetica', 14)), sg.Input(key='-WSIZE-')],
            [sg.Text("Percent of initial infected:", size=20, font=('Helvetica', 14)), sg.Input(key='-PER-')],
            [sg.Button('Rules', size=(10, 2), font=('Helvetica', 14), key='-RULES-'),
             sg.Button('Start Game', size=(10, 2), font=('Helvetica', 14), key='-START-'),
             sg.Button('Exit', size=(10, 2), font=('Helvetica', 14), key='-EXIT-')]
        ]

    def setWindow(self, layout):
        return sg.Window('Epidemic Simulator', layout, size=(800, 600), element_justification='center')

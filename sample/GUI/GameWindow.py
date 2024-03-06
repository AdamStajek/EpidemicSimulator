import PySimpleGUI as sg


class GameWindow:
    def __init__(self, window, game):
        self.window = window
        self.game = game

    def run(self):
        self.window.close()
        self.window = sg.Window('EpidemicSimulator', self.setLayout(), size=(1200, 800),
                                element_justification='center')
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
                break
            if event == '-BUTTON-':
                self.window['-SQUARE11-'].update(background_color='red')

    def setLayout(self):
        default_size = self.setSquaresSize()
        return [[sg.Text('Infected: ' + str(self.game.world.infected), font=('Helvetica', 24)), sg.Push(),
                 sg.Text('Dead: ' + str(self.game.world.dead), font=('Helvetica', 24))],
                [sg.Text('The World:', font=('Helvetica', 24))]] \
            + [[sg.Canvas(background_color='green', size=(default_size, default_size), pad=(1,1),
                          key='-SQUARE' + str(i) + ',' + str(j) + '-') for i in range(self.game.worldSize)] for j in
               range(self.game.worldSize)]

    def setSquaresSize(self):
        worldSize = self.game.worldSize
        if worldSize <= 10:
            return 550 / worldSize
        elif worldSize <= 50:
            return 450 / worldSize
        else:
            return 400 / worldSize

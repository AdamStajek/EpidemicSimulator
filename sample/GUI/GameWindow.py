import PySimpleGUI as sg
from sample.GUI.PlotWindow import PlotWindow


class GameWindow:
    def __init__(self, window, game):
        self.window = window
        self.game = game
        self.ended = False

    def run(self):
        self.window.close()
        self.game.startGame()
        self.window = sg.Window('EpidemicSimulator', self.setLayout(), size=(1200, 800),
                                element_justification='center')
        while True:
            event, values = self.window.read(timeout=300)
            if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
                break
            elif event == '-END-' or self.game.world.infected == 0:
                self.ended = True
            if event == '-IAGD-':
                PlotWindow('Infected against days', [i for i in range(self.game.day)], self.game.infectedHistory).run()
            elif event == '-DAGD-':
                PlotWindow('Dead against days', [i for i in range(self.game.day)], self.game.deadHistory).run()
            elif event == '-CPAGD-':
                PlotWindow('Current Population against days', [i for i in range(self.game.day)],
                           self.game.currentPopulationHistory).run()

            if not self.ended:
                self.window['-INFECTED-'].update(f'Infected: {self.game.world.infected}')
                self.window['-DEAD-'].update(f'Dead: {self.game.world.dead}')
                self.window['-DAY-'].update(f'Day: {self.game.day}')
                self.window['-CURRENTPOPULATION-'].update(f'CurrentPopulation: {self.game.world.currentPopulation}')
                for i in range(self.game.world.worldSize):
                    for j in range(self.game.world.worldSize):
                        grid = self.game.world.map[i][j]
                        if grid.currentPopulation != 0:
                            percentOfInfected = grid.infected / grid.currentPopulation
                            if grid.dead > grid.currentPopulation:
                                self.window[f'-SQUARE{i},{j}-'].update(background_color='black')
                            elif grid.infected / grid.currentPopulation > 3 / 4:
                                self.window[f'-SQUARE{i},{j}-'].update(background_color='red')
                            elif percentOfInfected > 1 / 2:
                                self.window[f'-SQUARE{i},{j}-'].update(background_color='orange')

            self.game.proceedDay()

    def setLayout(self):
        default_size = self.setSquaresSize()
        return [[sg.Text(f'Infected: {self.game.world.infected} ', font=('Helvetica', 24), key='-INFECTED-'), sg.Push(),
                 sg.Text(f'Dead: {self.game.world.dead}', font=('Helvetica', 24), key='-DEAD-')],
                [sg.Text('The World:', font=('Helvetica', 24))]] \
            + [[sg.Canvas(background_color='green', size=(default_size, default_size), pad=(1, 1),
                          key=f'-SQUARE{i},{j}-') for i in range(self.game.world.worldSize)] for j in
               range(self.game.world.worldSize)] \
            + [[sg.Text(f'Day: {self.game.day}', font=('Helvetica', 24), key='-DAY-'), sg.Push(),
                sg.Text(f'CurrentPopulation: {self.game.world.currentPopulation}', font=('Helvetica', 24),
                        key='-CURRENTPOPULATION-')],
               [sg.Button('End the simulation', font=('Helvetica', 24), key='-END-')],
               [sg.Button('Infected against days', font=('Helvetica', 16), key='-IAGD-'),
                sg.Button('Dead against days', font=('Helvetica', 16), key='-DAGD-'),
                sg.Button('Current population against days', font=('Helvetica', 16), key='-CPAGD-')]]

    def setSquaresSize(self):
        worldSize = self.game.world.worldSize
        if worldSize <= 10:
            return 500 / worldSize
        elif worldSize <= 50:
            return 400 / worldSize
        else:
            return 350 / worldSize

import PySimpleGUI as sg
from sample.Simulator.World import World


class GameWindow:
    def __init__(self, window, initialPopulation, worldSize, percentOfInitialInfected):
        self.window = window
        self.initialPopulation = initialPopulation
        self.worldSize = worldSize
        self.percentOfInitialInfected = percentOfInitialInfected

    def run(self):
        self.window.close()
        world = World(self.initialPopulation, self.worldSize)
        world.initializeInfected(self.percentOfInitialInfected)
        self.window = sg.Window('EpidemicSimulator', self.setLayout(world), size=(1200, 800),
                                element_justification='center')
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
                break
            if event == '-BUTTON-':
                self.window['-SQUARE11-'].update(background_color='red')

    def setLayout(self, world: World):
        default_size = self.setSquaresSize()
        return [[sg.Text('Infected: ' + str(world.infected), font=('Helvetica', 24)), sg.Push(),
                 sg.Text('Dead: ' + str(world.dead), font=('Helvetica', 24))],
                [sg.Text('The World:', font=('Helvetica', 24))]] \
            + [[sg.Canvas(background_color='green', size=(default_size, default_size), pad=(1,1),
                          key='-SQUARE' + str(i) + ',' + str(j) + '-') for i in range(self.worldSize)] for j in
               range(self.worldSize)]

    def setSquaresSize(self):
        if self.worldSize <= 10:
            return 550 / self.worldSize
        elif self.worldSize <= 50:
            return 450 / self.worldSize
        else:
            return 400 / self.worldSize

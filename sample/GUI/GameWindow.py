import PySimpleGUI as sg
from sample.GUI.PlotWindow import PlotWindow
from sample.Simulator.Game import Game


class GameWindow:
    """
    A class which represents game window
    """
    def __init__(self, window: sg.Window, game: Game):
        """
        Constructs game window
        :param window: main window of the app
        :param game: the game
        """
        self._window: sg.Window = window
        self._game: Game = game
        self._isEnded: bool = False

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, value):
        self._window = value

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, value):
        self._game = value

    @property
    def isEnded(self):
        return self._isEnded

    @isEnded.setter
    def isEnded(self, value):
        self._isEnded = value


    def run(self) -> None:
        """
        Runs game window.
        :return: None
        """
        self.window.close()
        self.game.startGame()
        self.window = sg.Window('EpidemicSimulator', self._setLayout(), size=(1200, 800),
                                element_justification='center')
        while True:
            event, values = self.window.read(timeout=300)
            if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
                break
            self._endGameIfNeeded(event)
            self._displayPlots(event)
            if not self.isEnded:
                self._updateStatisticsOnTheScreen()
                self._calculateSquaresColors()
            self.game.proceedDay()


    def _updateStatisticsOnTheScreen(self) -> None:
        """
        Updates statistics displayed on the screen
        :return: None
        """
        self.window['-INFECTED-'].update(f'Infected: {self.game.world.infected}')
        self.window['-DEAD-'].update(f'Dead: {self.game.world.dead}')
        self.window['-DAY-'].update(f'Day: {self.game.day}')
        self.window['-CURRENTPOPULATION-'].update(f'CurrentPopulation: {self.game.world.currentPopulation}')

    def _endGameIfNeeded(self, event: str) -> None:
        """
        ends the game if number of infected people is 0 or player clicked the end button
        :param event: event string returned by window.read()
        :return: None
        """
        if event == '-END-' or self.game.world.infected == 0:
            self.isEnded = True

    def _displayPlots(self, event) -> None:
        """
        Displays plot if the button has been clickec
        :param event: event string returned by window.read()
        :return: None
        """
        if event == '-IAGD-':
            PlotWindow('Infected against days', [i for i in range(self.game.day)], self.game.infectedHistory).run()
        if event == '-DAGD-':
            PlotWindow('Dead against days', [i for i in range(self.game.day)], self.game.deadHistory).run()
        if event == '-CPAGD-':
            PlotWindow('Current Population against days', [i for i in range(self.game.day)],
                       self.game.currentPopulationHistory).run()

    def _calculateSquaresColors(self) -> None:
        """
        Calculates the color of every square
        black means that there is more people dead than alive in a grid
        red means that more than 3/4 people in a grid is infected
        orange means that more than 1/2 people in a grid is infected

        :return: None
        """
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

    def _setLayout(self) -> list:
        """
        Sets the layout of game window
        :return: list containing the layout
        """
        squareSize = self._setSquaresSize()
        return [[sg.Text(f'Infected: {self.game.world.infected} ', font=('Helvetica', 24), key='-INFECTED-'), sg.Push(),
                 sg.Text(f'Dead: {self.game.world.dead}', font=('Helvetica', 24), key='-DEAD-')],
                [sg.Text('The World:', font=('Helvetica', 24))]] \
            + [[sg.Canvas(background_color='green', size=(squareSize, squareSize), pad=(1, 1),
                          key=f'-SQUARE{i},{j}-') for i in range(self.game.world.worldSize)] for j in
               range(self.game.world.worldSize)] \
            + [[sg.Text(f'Day: {self.game.day}', font=('Helvetica', 24), key='-DAY-'), sg.Push(),
                sg.Text(f'CurrentPopulation: {self.game.world.currentPopulation}', font=('Helvetica', 24),
                        key='-CURRENTPOPULATION-')],
               [sg.Button('End the simulation', font=('Helvetica', 24), key='-END-')],
               [sg.Button('Infected against days', font=('Helvetica', 16), key='-IAGD-'),
                sg.Button('Dead against days', font=('Helvetica', 16), key='-DAGD-'),
                sg.Button('Current population against days', font=('Helvetica', 16), key='-CPAGD-')]]

    def _setSquaresSize(self) -> int:
        """
        Calculates one square size for different numbers of squares needed to be displayed,
        so that every square fits one the screen
        :return: square size
        """
        worldSize = self.game.world.worldSize
        if worldSize <= 10:
            return int(500 / worldSize)
        elif worldSize <= 50:
            return int(400 / worldSize)
        else:
            return int(350 / worldSize)

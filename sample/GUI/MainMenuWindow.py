import PySimpleGUI as sg
from sample.GUI import GameWindow
from sample.GUI import RulesWindow
from sample.Simulator.Game import Game


class MainMenuWindow:
    """
    A class which represents main menu window.
    """

    def run(self) -> None:
        """
        Runs main menu window.
        :return: None
        """
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

    def startGameWindow(self, values: dict, window: sg.Window) -> None:
        """
        Starts game window.
        :param values: values dict returned by window.read()
        :param window: main window of the application
        :return: None
        """
        parameters = self.validateParameters(values, window)
        if parameters:
            game = Game(*parameters)
            GameWindow.GameWindow(window, game).run()

    def validateParameters(self, values: dict, window: sg.Window) -> tuple | bool:
        """
        Validates parameters entered in main menu.
        :param values: values dict returned by window.read()
        :param window: main window of the application
        :return: tuple of parameters or false if exception occured
        """
        try:
            initialPopulation = int(values['-POP-'])
            worldSize = int(values['-WSIZE-'])
            percentOfInitialInfected = int(values['-PER-'])
            transmissionRate = float(values['-TRANSMISSIONRATE-'])
            deadRate = float(values['-DEADRATE-'])
        except ValueError:
            self._handleIncorrectParameters(window)
            return False
        if initialPopulation <= 0 or not (0 <= worldSize <= 70) or not (0 <= percentOfInitialInfected <= 100) \
                or not (0 < deadRate <= 1) or not (0 < transmissionRate <= 1):
            self._handleIncorrectParameters(window)
        return initialPopulation, worldSize, percentOfInitialInfected, transmissionRate, deadRate

    def _handleIncorrectParameters(self, window: sg.Window):
        """
        Shows pop up if set parameters are incorrect.
        :param window: Main window of the application
        :return: None
        """
        sg.popup("Incorrect parameters!", font=('Helvetica', 16))
        window.close()
        self.run()

    def setGuiParameters(self, theme: str, icon: str) -> None:
        """
        Sets GUI parameters.
        :param theme: theme of the app, one of possible strings which can be found in PySimpleGUI docs
        :param icon: relative path to the icon from MainMenuWindow.py folder
        :return: None
        """
        self.setTheme(theme)
        self.setIcon(icon)

    def setTheme(self, theme: str) -> None:
        """
        Sets GUI theme.
        :param theme: theme of the app, one of possible strings which can be found in PySimpleGUI docs
        :return: None
        """
        sg.theme(theme)

    def setIcon(self, icon: str) -> None:
        """
        Sets GUI Icon visible in the main menu.
        :param icon: theme of the app, one of possible strings which can be found in PySimpleGUI docs
        :return: None
        """
        sg.set_global_icon(icon)

    def setLayout(self) -> list:
        """
        Sets MainMenuWindow layout
        :return: None
        """
        return [
            [sg.Text('Epidemic Simulator', font=('Helvetica', 40), justification='center', key='-TITLE-')],
            [sg.Image('../resources/main_menu.png', subsample=2)],
            [sg.Text("Enter parameters of the game:", font=('Helvetica', 14))],
            [sg.Text("Initial population:", size=20, font=('Helvetica', 14)), sg.Input(key='-POP-')],
            [sg.Text("World size:", size=20, font=('Helvetica', 14)), sg.Input(key='-WSIZE-')],
            [sg.Text("Percent of initial infected:", size=20, font=('Helvetica', 14)), sg.Input(key='-PER-')],
            [sg.Text("Transmission rate:", size=20, font=('Helvetica', 14)), sg.Input(key='-TRANSMISSIONRATE-')],
            [sg.Text("Death rate:", size=20, font=('Helvetica', 14)), sg.Input(key='-DEADRATE-')],
            [sg.Button('Rules', size=(10, 2), font=('Helvetica', 14), key='-RULES-'),
             sg.Button('Start Game', size=(10, 2), font=('Helvetica', 14), key='-START-'),
             sg.Button('Exit', size=(10, 2), font=('Helvetica', 14), key='-EXIT-')],

        ]

    def setWindow(self, layout: list) -> sg.Window:
        """
        Creates main menu window.
        :param layout: layout of the window
        :return: main menu window
        """
        return sg.Window('Epidemic Simulator', layout, size=(800, 600), element_justification='center')

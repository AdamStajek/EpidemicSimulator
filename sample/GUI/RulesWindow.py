import PySimpleGUI as sg
from sample.GUI import MainMenuWindow


class RulesWindow:
    """
    A class which represents a rules window.
    """
    def __init__(self, window: sg.Window):
        """
        Constructs rules window.
        :param window: pysimplegui main window
        """
        self.window: sg.Window = window

    def run(self) -> None:
        """
        Runs rules window.
        :return: None
        """
        self.window.close()
        self.window = sg.Window('EpidemicSimulator', self.setLayout(), size=(800, 600), element_justification='center')
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
                self.window.close()
                break
            if event == '-MAIN MENU-':
                self.window.close()
                MainMenuWindow.MainMenuWindow().run()

    def setLayout(self) -> list:
        """
        Sets the layout for rules window
        :return: layout of the window
        """
        rules = self.readRules()
        return [[sg.Button('Main menu', font=('Helvetica', 16), key='-MAIN MENU-')],
                [sg.Text("Rules:", font=('Helvetica', 24))],
                [sg.Multiline(rules, size=(400, 300), font=('Helvetica', 16), justification='center')]]

    def readRules(self) -> list | str:
        """
        reads rules from a file
        :return: rules as a string or "Error!" string if the file does not exist
        """
        try:
            with open('../resources/rues.txt') as f:
                contents = f.read()
                return contents
        except FileNotFoundError:
            sg.popup("rules.txt in resources folder does not exist!", font=('Helvetica', 16))
            return "Error!"

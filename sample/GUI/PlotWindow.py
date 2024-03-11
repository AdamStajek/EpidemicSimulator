import PySimpleGUI as sg
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PlotWindow:
    """
    A class which represents a plot window.
    """

    def __init__(self, name: str, x: list[int], y: list[int]):
        """
        Constructs rules window.
        :param name: Name of the plot
        :param x: array of values for the x axis
        :param y: array of values for the y axis
        """
        self._name: str = name
        self._yName: str = name.split(' ')[0]
        self._x: list[int] = x
        self._y: list[int] = y

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def yName(self) -> str:
        return self._yName

    @property
    def x(self) -> list[int]:
        return self._x

    @x.setter
    def x(self, value: list[int]):
        self._x = value

    @property
    def y(self) -> list[int]:
        return self._y

    @y.setter
    def y(self, value: list[int]):
        self._y = value

    def run(self) -> None:
        """
        Runs plot window.
        :return: None
        """
        window = sg.Window(self.name, self.setLayout(), finalize=True, element_justification='center',
                           font='Helvetica 18')
        while True:
            fig = self.createPlot()
            self.drawFigure(window['-PLOT-'].TKCanvas, fig)
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit' or event == '-EXIT-':
                window.close()
                break

    def setLayout(self) -> list:
        """
        Sets the layout for rules window
        :return: layout of the window
        """
        return [[sg.Canvas(key='-PLOT-')],
                [sg.Button('Exit', key='-EXIT-')]]

    def createPlot(self) -> matplotlib.pyplot.Figure:
        """
        Creates the plot.
        :return: None
        """
        matplotlib.use('TkAgg')
        fig = matplotlib.pyplot.figure(figsize=(7, 5), dpi=100)
        fig.add_subplot(111).plot(self.x, self.y)
        matplotlib.pyplot.title(self.name, fontdict={'family': 'sans-serif', 'size': 16})
        matplotlib.pyplot.ylabel(self.yName, fontdict={'family': 'sans-serif', 'size': 16})
        matplotlib.pyplot.xlabel('day', fontdict={'family': 'sans-serif', 'size': 16})
        return fig

    def drawFigure(self, canvas: sg.Canvas, fig: matplotlib.pyplot.Figure) -> matplotlib.backends.backend_tkagg.FigureCanvasTkAgg:
        """
        Draws the figure.
        :param canvas: object to draw plot into
        :param fig: the plot object
        :return: drawing of the plot
        """
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

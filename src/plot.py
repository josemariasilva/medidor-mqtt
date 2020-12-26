from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import mplcursors





sns.set_style("darkgrid")


class Plotting(FigureCanvas):
    
    def __init__(self, parent=None):
        
        
        self.fig = Figure(tight_layout=True)
        self.fig.patch.set_visible(False)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,
                                         QSizePolicy.Expanding
                                         )
        self.refresh()

        self.ax.set_xlabel("Tempo(s)")
        self.ax.set_ylabel("Torque(Nm)")

        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')

        FigureCanvas.updateGeometry(self)

    def plot(self, x, y, title="",path=None):
        
        self.ax.set_xlabel("Tempo(s)")
        self.ax.set_ylabel("Torque(Nm)")

        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')

        self.ax.set_title(title)
        self.ax.plot(x, y)
        mplcursors.cursor(self.ax)
        #self.ax.scatter(x,y, c='red', marker = '.')
        #self.ax.fill_between(x, y, alpha=0.1)
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.draw()

    def refresh(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)

        
        self.ax.grid(color='black', linestyle='--', linewidth=0.5, axis='x')
        self.ax.grid(color='black', linestyle='--', linewidth=0.5, axis='y')
        self.ax.grid(True)
        #self.ax.patch.set_facecolor('white')
        


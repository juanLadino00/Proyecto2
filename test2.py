import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from time import sleep
import random

class InteractiveCircle(object):
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        #self.ax.axis('equal')
        self.ax.set_xlim(0,20)
        self.ax.set_ylim(0,20)

        self.circ = Circle((10, 10), 2)
        self.ax.add_artist(self.circ)
        #self.ax.set_title('Click to move the circle')

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.inaxes is None:
            return
        temp = [(random.randint(2,18),random.randint(2,18)) for j in range(50)]
        for k in temp:
            print(k)
        for i in temp:
            self.circ.center = i[0], i[1]
            self.fig.canvas.draw()
            plt.pause(1)
        #self.circ.center = 18,18
        #self.fig.canvas.draw()

    def show(self):
        plt.show()


InteractiveCircle().show()

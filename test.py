import sys
sys.path.insert(0, '../')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as cir
import random

import disk
import event as ev
from system import System as sy

NoPart = 50
colors = ['red', 'blue', 'green']

hola = sy(window = True)
for i in range(NoPart):
    hola.p.append(disk.Disk(rad = 0.5, col = random.choice(colors), tag = str(i)))

hola.set_random_positions()
for j in hola.p:
    j.stat = cir((j.dir[0], j.dir[1]), j.r, color = j.col)
m=hola.main_loop(sim_time=300)
fig, ax = plt.subplots()
tiempo = [i for i in range(0, len(m))]
ax.plot(tiempo, m,'r')
ax.set(xlabel = 'Tiempo', ylabel = 'Momentum', title = 'Momentum lineal total del sistema de discos')
ax.grid()
plt.show()


##ax.grid()
# plt.savefig("241Ptot.PNG")
# plt.show()


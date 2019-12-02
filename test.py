import sys
sys.path.insert(0, '../')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as cir
import random

import disk
import event as ev
from system import System as sy

################################################################################
# BLOQUE PRINCIPAL DE INSTRUCCIONES ############################################

NoPart = 10
colors = ['red', 'blue', 'green', 'yellow', 'pink', 'magenta', 'cyan', 'orange', 'purple']

wind = True
hola = sy(window = wind)
for i in range(NoPart):
    hola.p.append(disk.Disk(rad = 2, col = random.choice(colors), tag = str(i)))

hola.set_random_positions()
for j in hola.p:
    # print(j)
    j.stat = cir((j.dir[0], j.dir[1]), j.r, color = j.col)
m=hola.main_loop(sim_time=1000)

# 2.4.1 check_overlap()
##System.check_overlap()
##
##cont = 0
##for j in System.particles:
##    # print(j)
##    cont += 1
##    j.obj = Circle((j.x, j.y), j.rad, color = j.col)
##
##sim_time = 20000
##Ptot = System.main_loop(sim_time) # Retorna el Momentum en un tiempo t
##
### 2.4.1 Grafica del Momentum Lineal
### print(Ptot)
### print("len =", len(Ptot))
##fig, ax = plt.subplots()
##time = [i for i in range(0, len(Ptot))]
##ax.plot(time, Ptot)
##ax.set(xlabel = 't (tiempo)', ylabel = 'Ptot(t) (Momentum)', title = 'Momentum Particle Collitions')
##ax.grid()
# plt.savefig("241Ptot.PNG")
# plt.show()


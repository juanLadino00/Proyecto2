import numpy as np

LX, LY = 10, 8 #Limites del contenedor
VEL_SCALE = .9 #escala que multiplica el random de num.py

class Disk:
    def __init__(self, state=None, mass=1.0, rad=1.0, col=(0, 0, 0), tag=-1)
    def __str__(self)
    def horz_wall_coll(self) #retorna el tiempo que tarda en ocurrirun evento horz-Wall-Coll
    def vert_wall_coll(self) #retorna el tiempo que tarda en ocurrirun evento horz-Wall-Coll
    def disk_coll(self, other) #retorna el tiempo que tarda en ocurrirun evento diskA-diskOther
    def move(self, time) #Actualiza la posicion del diskA dado un tiempo y la velocidad
    def update_velocity_vert(self) #
    def update_velocity_horz(self) #
    def update_velocity_disk(self, other) #
    def position(self, pos=None) #
    def velocity(self, vel=None) #
    def num_colls(self) #
    def speed(self) #

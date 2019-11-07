import numpy as np
import heapq as pq
import turtle as tt
import disk
import event as ev
import frame as fr


class System:
    def __init__(self, particles, window=None, fpe=None)
    def __str__(self)
    # Todas las colisiones de ese disco con los n-1 discos y con las 4 paredes
    # Crea el heap quoe
    def check_colls(self, saucer, sim_time):
    # Bool que verifica que la colision sea valida
    def valid(self, event)
    # Verifica que la siguiente colision es valida
    def next_valid_event(self)
    # Se mueven las parejas
    def move_all_particles(self, event)
    def update_velocities(self, event)
    # Siguientes colisiones
    def predict_colls(self, event, sim_time)
    # 
    def main_loop(self, sim_time, fpe=None)
    def write_time_to_screen(self)
    def create_all_artists(self)
    def draw_all_artists(self)
    def set_random_positions(self)

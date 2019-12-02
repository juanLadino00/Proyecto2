import numpy as np
import heapq as pq
import matplotlib as plt
import disk
import event as ev
import frame as fr


import sys
sys.path.insert(0,'../')

class System:
    def __init__(self, particles, window=None, fpe=None):
        # Tiempo
        self.t=0
        # Cola de eventos
        self.pq=[]
        # Partículas
        self.p=particles
        # Ventana
        self.w=window
        # Grafico
        self.frame=0
        self.fpe=fpe
        
    def __str__(self):
        strg= "Particulas: {}\n".format(len(self.p))
        strg+= "Cola prioritaria: {}\n".format(len(self.pq))
        strg+= "Tiempo: {:2f}".format(self.t)

        return strg
    
    # Todas las colisiones de ese disco con los n-1 discos y con las 4 paredes
    # Crea el heap quoe
    def check_colls(self, saucer, sim_time):
        # Esta funcion retorna evento
        for i in self.p:
            '''
             Retorna tiempo de colision disco-disco con el disco que estamos
             analizando vs todos los demas que se encuentran en el sistema
            '''
            tiempo_colision=saucer.disk_coll(i)
            # Revisamos que la suma de tiempos tenga sentido para crear el evento
            if (self.t+tiempo_colision)<=sim_time:
                nuevo_evento=ev.Event(self.t+tiempo_colision,saucer,i)
                # Agregamos el evento a la cola
                pq.heappush(self.pq,nuevo_evento)
        '''
        Ahora tenemos que verificar el tiempo de colision de particula con
        las paredes del contenededor
        '''
        tiempo_paredes=[saucer.vert_wall_coll(),saucer.horz_wall_coll()]
        for j in tiempo_paredes:
            if self.t+j<=sim_time:
                nuevo_evento=ev.Event(self.time+j, saucer, None)
                pq.heappush(self.pq,nuevo_evento)
    
    # Bool que verifica que la colision sea valida
    def valid(self, event):
        '''
        Seleccionamos los dos discos o disco y muro que estan dentro de la
        colision, y revisamos las colisiones de dicha particula   
        '''
        if event.this_tag is not None:
            # Si las colisiones dentro del sistema de la particula son mayores que las que registra el
            # ..evento se retorna falso
            if self.p[int(event.this_tag)].num_colls()>event.this_colls:
                return False
        # hacemos lo mismo con el otro objeto que esta en colision
        if event.that_tag is not None:
            # Si las colisiones dentro del sistema de la particula son mayores que las que registra el
            # ..evento se retorna falso
            if self.p[int(event.that_tag)].num_colls()>event.that_colls:
                return False
        #
        return True
    
    # Verifica que la siguiente colision es valida
    def next_valid_event(self):
        # Recorremos la cola prioritaria y si el evento es valido se retorna
        while self.pq !=[]:
            e=pq.heappop(self.pq)
            if self.valid(e):
                return e
        return None
        
    # Se mueven las parejas
    def move_all_particles(self, event):
        tiempo_e=event.t
        for i in self.p:
            # Actualizamos posicion
            i.move(tiempo_e-self.t)
        self.t=event.t
        
    def update_velocities(self, event):
        # Seleccionamos las particulas
        this_tag, that_tag=event.this_tag, event.that_tag
        if this_tag is not None and that_tag is not None:
            self.p[int(this_tag)].update_velocity_disk(self.p[int(that_tag)])
        elif this_tag is not None and that_tag is None:
            self.p[int(this_tag)].update_velocity_vert()
        elif this_tag is None and that_tag is not None:
            self.p[int(that_tag)].update_velocity_horz()
        
    # Siguientes colisiones
    def predict_colls(self, event, sim_time):
        # Seleccionamos las particulas
        this_tag, that_tag=event.this_tag, event.that_tag
        if this_tag is not None:
            self.check_colls(self.particles[int(this_tag)], sim_time)

        if tag_b is not None:
            self.check_colls(self.particles[int(that_tag)], sim_time)        

    '''
    Funcion para graficar
    '''    
    def main_loop(self, sim_time, fpe=None):
        Ptot = []
        if self.window == True:
            fig, ax = plt.subplots()
            fig.set_size_inches(disk.LX/100, disk.LY/100)
            fig.patch.set_facecolor('xkcd:lightgreen')

            ax.set_facecolor('xkcd:black')
            ax.set_aspect('equal')
            ax.set_xlim(0, disk.LX)
            ax.set_ylim(0, disk.LY)
            ax.set_title('Simulation Collition Particles')
            plt.grid(True, color = 'w')

        for i in self.p:
            self.check_colls(i, sim_time)
            if self.window == True:
                ax.add_artist(i.obj)
        if self.window == True:
            fig.canvas.draw()

        cont = 0
        while(len(self.pq) != 0):
            event = self.next_valid_event()
            if event is None:
                break
            self.move_all_particles(event)
            self.update_velocities(event)
            self.predict_colls(event, sim_time)
            cont += 1

            for k in self.particles:
                k.obj.center = k.x, k.y
            if self.window == True:
                fig.canvas.draw()
                plt.pause(0.000000000000001)

            Pt = self.Ptot()
            Ptot.append(round(Pt, 2))

        if self.window == True:
            plt.show()

        print("      Ptot(): Calculando Momentum y graficando.")

        return Ptot
    def write_time_to_screen(self)
    def create_all_artists(self)
    def draw_all_artists(self)
    def set_random_positions(self)

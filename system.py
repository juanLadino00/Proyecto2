import numpy as np
import heapq as pq
import matplotlib.pyplot as plt
import disk
import event as ev
from scipy.constants import k as kb
##import frame as fr


import sys
sys.path.insert(0,'../')

class System:
    def __init__(self, particles=[], window=None, fpe=None):
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
        t1=saucer.vert_wall_coll()
        t2=saucer.horz_wall_coll()
        if (self.t+t1)<=sim_time:
            nuevo_evento=ev.Event(self.t+t1, saucer, None)
            pq.heappush(self.pq,nuevo_evento)
        if (self.t+t2)<=sim_time:
            nuevo_evento=ev.Event(self.t+t2, None, saucer)                
            pq.heappush(self.pq,nuevo_evento)
        
##        tiempo_paredes=[saucer.vert_wall_coll(),saucer.horz_wall_coll()]
##        for j in range(0,2):
##            if self.t+tiempo_paredes[j]<=sim_time and j==0:
##                nuevo_evento=ev.Event(self.t+tiempo_paredes[j], saucer, None)
##                pq.heappush(self.pq,nuevo_evento)
##            elif self.t+tiempo_paredes[j]<=sim_time and j==1:
##                nuevo_evento=ev.Event(self.t+tiempo_paredes[j], None, saucer)                
##                pq.heappush(self.pq,nuevo_evento)

    
    
    # Bool que verifica que la colision sea valida
    def valid(self, event):
        '''
        Seleccionamos los dos discos o disco y muro que estan dentro de la
        colision, y revisamos las colisiones de dicha particula   
        '''
        if event.this_tag is not None:
            # Si las colisiones dentro del sistema de la particula son mayores que las que registra el
            # ..evento se retorna falso
            a=self.p[int(event.this_tag)].num_colls()
            if a>event.this_colls:# and type(event.this_colls)==int or event.this_colls>5:
                return False
        # hacemos lo mismo con el otro objeto que esta en colision
        if event.that_tag is not None:
            # Si las colisiones dentro del sistema de la particula son mayores que las que registra el
            # ..evento se retorna falso
            b=self.p[int(event.that_tag)].num_colls()
            if b>event.that_colls:# and type(event.that_colls)==int or event.that_colls>5:
                return False
        #
        return True
    
    # Verifica que la siguiente colision es valida
    def next_valid_event(self):
        # Recorremos la cola prioritaria y si el evento es valido se retorna
        while self.pq !=[]:
            e=pq.heappop(self.pq)
            if self.valid(e):
                print(e)
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
            self.check_colls(self.p[int(this_tag)], sim_time)

        if that_tag is not None:
            self.check_colls(self.p[int(that_tag)], sim_time)        

    # Para asignar particulas en posiciones aleatorias pero coherentes
    # Para realizar esta funcion se reviso el cap 8 del libro
    def check_overlap(self):
        for i in self.p:
            for h in self.p:
                # Si la pasticulas son diferentes
                if i.tag != h.tag:
                    # Se mira la separacion entre ambas
                    dx= np.sqrt((j.dir[0] - i.dir[0])**2 + (j.dir[1] - i.dir[1])**2)
                    dy= i.r+j.r
                    if dx<dy:
                        return False
        return True
    
    def set_random_positions(self):
        # Posicion de la primera particula
        self.p[0].dir[0]=disk.LX/2
        self.p[0].dir[1]=disk.LY/2

        for i in range(1,len(self.p)):
            radio=self.p[i].r
            overlap=True

            while overlap:
                j, overlap = 0, False
                dx = (disk.LX - 2.0 * radio) * np.random.random() + radio
                dy = (disk.LY - 2.0 * radio) * np.random.random() + radio
                # Nueva posicion del disco
                tmp = np.array([dx, dy])

                while j < i and not overlap:
                    # Seleccionamos el segundo disco
                    jd = self.p[j]
                    # Ubicacion del segundo disco
                    js = np.array([jd.dir[0], jd.dir[1]])
                    # Distancia entre discos
                    m = np.linalg.norm(tmp - js)
                    a= radio + jd.r
                    #print(str(a)+"/"+str(m))      
                    if m <= radio + jd.r:
                        overlap = True
                    j += 1

                self.p[i].dir[0] = tmp[0]
                self.p[i].dir[1] = tmp[1]
                
    def momemtum_lineal(self):
        numero_particulas=len(self.p)
        p_tot=0
        for i in range(0,numero_particulas):
            p_tot+= self.p[i].m *self.p[i].speed()
        res=p_tot/numero_particulas
        return res

    def defi_momentum(self,sim_time=100):
        pm=[]
        for i in self.p:
            self.check_colls(i, sim_time)
        print("voy aca")
        while(len(self.pq) != 0):
            event = self.next_valid_event()
            if event is None:
                break
            self.move_all_particles(event)
            self.update_velocities(event)
            self.predict_colls(event, sim_time)
            b=self.momemtum_lineal()
            pm.append(b)
            print(b)
        fig, ax = plt.subplots()
        tiempo = [i for i in range(0, len(pm))]
        ax.plot(tiempo, pm)
        ax.set(xlabel = 'Tiempo', ylabel = 'Momentum', title = 'Momentum lineal total del sistema de discos')
        ax.grid()
        plt.show()

##    def densidad(self):
##        n=len(self.p)/(disk.LX*disk.lY)
##        return n
    '''
    Funciones buscadas en el libro
    '''
##    def triangular_lattice(self,nx,ny):
##        dx=disk.LX/nx
##        dy=disk.LY/ny
##        for i in range(0,nx):
##            for j in range(0,ny):
##                k=i+j*ny
                
    def cuadro_lattice(self,nx,ny):
        dx=disk.LX/nx
        dy=disk.LY/ny

        vary=dy-self.p[0].r
        var=0
        for i in range(0,ny):
            varx=dx-self.p[var].r
            for j in range(0,nx):
                self.p[var].dir[0]=varx
                self.p[var].dir[1]=vary
                varx=varx+vary
                var+=1
            vary=vary+varx
        

    def temperatura(self):
        k = kb
        temp = self.momemtum_lineal()/2*len(self.p)*k

    '''
    Funcion principal
    '''    
    def main_loop(self, sim_time, fpe=None):
        pm=[]
        if self.w == True:
            fig, ax = plt.subplots()
            fig.set_size_inches(disk.LX, disk.LY)
            fig.patch.set_facecolor('xkcd:white')

            ax.set_facecolor('xkcd:white')
            ax.set_aspect('equal')
            ax.set_xlim(0, disk.LX)
            ax.set_ylim(0, disk.LY)
            ax.set_title('Simulacion')
            plt.grid(True, color = 'black')

        for i in self.p:
            self.check_colls(i, sim_time)
            if self.w == True:
                ax.add_artist(i.stat)
        if self.w == True:
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

            for k in self.p:
                k.stat.center = k.dir[0], k.dir[1]
            if self.w == True:
                fig.canvas.draw()
                plt.pause(1.e-17)

            Pt = self.momemtum_lineal()
            pm.append(round(Pt, 2))

        if self.w == True:
            plt.show()

        return pm
##    def write_time_to_screen(self)
##    def create_all_artists(self)
##    def draw_all_artists(self)
##    def set_random_positions(self)

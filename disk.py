import numpy as np

LX, LY = 10, 8 #Limites del contenedor
VEL_SCALE = .9 #escala que multiplica el random de num.py

class Disk:
    def __init__(self, state=None, mass=1.0, rad=1.0, col=(0, 0, 0), tag=-1):
        self.m,self.r,self.col,self.tag=mass,rad,col,tag
        self.disk_colls,self.wall_colls=0,0

        dix=(LX-2.*self.r)*np.random.random()+self.r
        diy=(LY-2.*self.r)*np.random.random()+self.r
        diskr=np.array([dix,diy])
        self.dir=diskr
        diskv=VEL_SCALE*(2.*np.random.random(2)-1.)
        self.vel=diskv
        
    def __str__(self):
        strng= "Disk {} state\n".format(self.tag)
        strng += "m={:.2f}, r={:.2f}, ".format(self.m,self.r)
        strng += "c={}\n".format.(self.c)
        strng += "r= " +str(self.dir)
        strng += "v= " +str(self.vel)
        strng += "disk-disk colls={}, ".format(self.disk_colls)
        strng += "disk-wall colls={}, ".format(self.wall_colls)
        return strng

    def horz_wall_coll(self):
        #retorna el tiempo que tarda en ocurrirun evento horz-Wall-Coll
        y, vy= self.dir[1], self.vel[1]
        if vy=0:
            choque=np.inf
        elif vy>0:
            choque=(LY-self.r-y)/vy
        else:
            choque=(self.r-y)/vy
        return choque

    def vert_wall_coll(self):
        #retorna el tiempo que tarda en ocurrirun evento horz-Wall-Coll
        x, vx=self.dir[0], self.vel[0]
        if vx=0:
            choque=np.inf
        elif vx>0:
            choque=(LX-self.r-x)/vx
        else:
            choque=(self.r-x)/vx
        return choque
    def disk_coll(self, other):
        #retorna el tiempo que tarda en ocurrirun evento diskA-diskOther
        x1,y1,vx1,vy1=self.dir[0],self.dir[1],self.vel[0],self.vel[1]
        x2,y2,vx2,vy2=other.dir[0],other.dir[1],other.vel[0],other.vel[1]
        dx=x1-x2
        dy=y1-y2
        dvx=vx1-vx2
        dvy=vy1-vy2
        dvdr=dx*dvx+dy*dvy
        if dvdr>0:
            return np.inf
        
        dvdv=dvx*dvx+dvy*dvy
        if dvdv==0:
            return np.inf

        drdr=dx*dx+dy*dy
        sigma=other.r+self.r
        d=(dvdr*dvdr)-dvdv*(drdr-sigma*sigma)
        if d<0:
            return np.inf
        else:
            return -((dvdr)+(d)**(1/2))/(dvdv)
        
    def move(self, time):
        #Actualiza la posicion del diskA dado un tiempo y la velocidad
        nuevo_x=self.dir[0]+self.vel[0]*time
        nuevo_y=self.dir[1]+self.vel[1]*time
        self.dir[0]=nuevo_x
        self.dir[1]=nuevo_y
        
    def update_velocity_vert(self):
        
    def update_velocity_horz(self) #
    def update_velocity_disk(self, other) #
    def position(self, pos=None) #
    def velocity(self, vel=None) #
    def num_colls(self) #
    def speed(self) #

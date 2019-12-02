import numpy as np

LX, LY = 200, 200 #Limites del contenedor
VEL_SCALE = .9 #escala que multiplica el random de num.py

class Disk:
    def __init__(self, state=None, mass=1.0, rad=1.0, col=(0, 0, 0), tag=-1):
        self.m,self.r,self.col,self.tag=mass,rad,col,tag
        self.disk_colls,self.wall_colls=0,0

        dix=(LX-2.*self.r)*np.random.random()+self.r
        diy=(LY-2.*self.r)*np.random.random()+self.r
        diskr=np.array([dix,diy])
        self.dir=diskr
        #diskv=VEL_SCALE*(2.*np.random.random(2)-1.)
        diskv=np.array([0.9,0.9])
        self.vel=diskv
        self.stat=None
        
    def __str__(self):
        strng= "Disk {} state\n".format(self.tag)
        strng += "m={:.2f}, r={:.2f}, ".format(self.m,self.r)
        strng += "c={}\n".format(self.c)
        strng += "r= " +str(self.dir)
        strng += "v= " +str(self.vel)
        strng += "disk-disk colls={}, ".format(self.disk_colls)
        strng += "disk-wall colls={}, ".format(self.wall_colls)
        return strng

    def horz_wall_coll(self):
        #retorna el tiempo que tarda en ocurrirun evento horz-Wall-Coll
        y, vy= self.dir[1], self.vel[1]
        if vy==0:
            choque=np.inf
        elif vy>0:
            choque=(LY-self.r-y)/vy
        else:
            choque=(self.r-y)/vy
        return choque

    def vert_wall_coll(self):
        #retorna el tiempo que tarda en ocurrirun evento horz-Wall-Coll
        x, vx=self.dir[0], self.vel[0]
        if vx==0:
            choque=np.inf
        elif vx>0:
            choque=(LX-self.r-x)/vx
        else:
            choque=(self.r-x)/vx
        return choque
    
    def disk_coll(self, other):
        if self is other:
            return np.inf
        #retorna el tiempo que tarda en ocurrirun evento diskA-diskOther
        x1,y1,vx1,vy1=self.dir[0],self.dir[1],self.vel[0],self.vel[1]
        x2,y2,vx2,vy2=other.dir[0],other.dir[1],other.vel[0],other.vel[1]
        dx=x2-x1
        dy=y2-y1
        dvx=vx2-vx1
        dvy=vy2-vy1
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
        vx=self.vel[0]
        self.vel[0]=-vx
        self.wall_colls += 1
        
    def update_velocity_horz(self):
        vy=self.vel[1]
        self.vel[1]=-vy
        self.wall_colls += 1

        
    def update_velocity_disk(self, other):
        self.disk_colls += 1
        other.disk_colls += 1
        
        x1,y1,vx1,vy1=self.dir[0],self.dir[1],self.vel[0],self.vel[1]
        x2,y2,vx2,vy2=other.dir[0],other.dir[1],other.vel[0],other.vel[1]

        c=(self.m-other.m)/(self.m+other.m)
        
        c_disco=(2*self.m)/(self.m+other.m)
        c_other_d=(2*other.m)/(self.m+other.m)

        rij=(x1-x2,y1-y2)
        vij=(vx1-vx2,vy1-vy2)

        rji=(x2-x1,y2-y1)
        
        vr=vij[0]*rij[0]+vij[1]*rij[1]

        constante_i=-(c_disco/((self.r+other.r)**2))
        constante_j=-(c_other_d/((self.r+other.r)**2))


        self.vel[0]=(constante_j*vr*rij[0])+self.vel[0]
        self.vel[1]=(constante_j*vr*rij[1])+self.vel[1]
        other.vel[0]=(constante_i*vr*rji[0])+other.vel[0]
        other.vel[1]=(constante_i*vr*rji[1])+self.vel[1]
        
    def position(self, pos=None):
        if pos==None:
            return self.dir[0],self.dir[1]
        else:
            self.dir[0]=pos[0]
            self.dir[1]=pos[1]
            
    def velocity(self, vel=None):
        if vel==None:
            return self.vel[0],self.vel[1]
        else:
            self.vel[0]=vel[0]
            self.vel[1]=vel[1]
            
    def num_colls(self):
        return self.disk_colls+self.wall_colls
    
    def speed(self):
        return np.sqrt(self.vel[0]**2 + self.vel[1]**2)

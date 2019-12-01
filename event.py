class Event:
    # Evento tiene 5 atributos: tiempo de colosion, las dos particulas y los atributos
    # Numero de colisiones de han tenido cada una de las particulas
    def __init__(self, t, this, that):
        self.time = t
        self.this_tag = None if this is None else this.tag
        self.that_tag = None if that is None else that.tag
        self.this_colls = None if this is None else this.num_colls()
        self.that_colls = None if that is None else that.num_colls()
        
    # Metodos para imprimir
    def __str__(self):
        strg = "Inicia evento: \n"
        strg += " Tiempo: {:.2f} \n".format(self.time)
        strg += " Particula uno: {} {} \n".format(self.this_tag, self.this_colls)
        strg += " Otra particula: {} {} \n".format(self.that_tag, self.that_colls)
        strg += "Fin Evento. \n"
        return strg
        
    # Impresion fina    
    def __repr__(self):
        strg = "{:.2f}".format(self.time)
        strg += "{} {}".format(self.this_tag, self.that_tag)
        strg += "{} {}".format(self.this_colls, self.that_colls)
        return strg

    # Metodo less than
    def __lt__(self, other):
        return self.time < other.time
    
    def get_time(self):
        return self.time
    
    # Retorna tupla con las particulas que estan en la colision
    def get_tags(self):
        return (self.this_tag,self.that_tag)
    
    # tupla colision 
    def get_colls(self):
        return (self.this_colls,self.that_colls)

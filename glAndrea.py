#Andrea Estefania Elias Cobar
#17048

import struct
import math


def char(c):
	return struct.pack("=c", c.encode('ascii'))
def word(c):
	return struct.pack("=h", c)
def dword(c):
	return struct.pack("=l", c)
def color(r,g,b):
	return bytes([b,g,r])


class ArchivoObj(object):
    def __init__(self,filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.faces = []
        self.lectura()

 
    def eliminarEspacio(self,cara):
       
        almacenarDatos = cara.split('/')

      
        if ("") in almacenarDatos:
                almacenarDatos.remove("")

      
        return map(int,almacenarDatos)

  
    def readLines(self):
        #Se lee cada una de las lineas guardadas
        for line in self.lines:
           
            if line:
                prefix, value = line.split(' ', 1)

                #Si el prefix es una v es que estamos leyendo los vertices del cual sus coordenadas son mapeados en el value separados por espacios ' '
                if prefix == 'v':
                    self.vertices.append(list(map(float,value.split(' '))))
                #Si el prefix es un f es que estamos leyendo una cara de la cual guardaremos una coleccion de datos que nos brindaran los vertices que se usan para formar la cara separados por una diagonal en bloques separados por espacios
                elif prefix == 'f':    
                    self.faces.append([list(self.eliminarEspacio(face)) for face in value.split(' ')])
                    

class Bitmap(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.clearColor = color(0,0,0)
        self.vertexColor = color(255,255,0)
        self.glClear()
        
   
    def glInit(self):
            pass
        
   
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

   
    def glClear(self):
        self.framebuffer = [
            [
                self.clearColor	for x in range(self.width)
                ]
            for y in range(self.height)
            ]
        
  
    def glClearColor(self,r,g,b):
        try:
                self.rc = round(255*r)
                self.gc = round(255*g)
                self.bc = round(255*b)
                self.clearColor = color(self.rc,self.gc,self.bc)
        except ValueError:
                print("No puede ingresar un numero mayor a 1 ni menor que 0 en el color")

   
    def glColor(self,r,g,b):
        try:
                self.rv = round(255*r)
                self.gv = round(255*g)
                self.bv = round(255*b)
                self.vertexColor = color(self.rv,self.gv,self.bv)
        except ValueError:
                print("No puede ingresar un numero mayor a 1 ni menor que 0 en el color")

    #Coloca un Pixel dentro del framebuffer para colocarlo en el renderizado con valores entre -1 y 1
    def glPoint(self,x,y,color):
        #Convertimos los valores entre -1 y 1 a valores enteros de acuerdo a las dimensiones del window
        x = int(round((x+1) * self.width / 2))
        y = int(round((y+1) * self.height / 2))
        try:
                self.framebuffer[y][x] = color
        except IndexError:
                print("No fue imposible imprimir el punto dado que esta fuera de los limites de la imagen")

    #Crea una linea formada por la sucesion de puntos equivalentes a pixeles mandando una coordenada x,y inicia y una x,y final, osea 2 pixeles con valores x,y entre -1 y 1
    def glLine(self,x0, y0, x1, y1):
        #Convertimos los valores entre -1 y 1 a valores enteros de acuerdo a las dimensiones del window
        x0 = int(round((x0+1) * self.width / 2))
        y0 = int(round((y0+1) * self.height / 2))
        x1 = int(round((x1+1) * self.width / 2))
        y1 = int(round((y1+1) * self.height / 2))

        #Calulamos las diferencias entre las x y y        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Creamos un boolean que nos permita conocer cual es la mayor diferencia
        steep = dy > dx

        #Si dy es mayor a dx entonces intercambiamos cada una de las coordenadas
        if steep:
                x0,y0 = y0,x0
                x1,y1 = y1,x1

        #Si el punto inicial en x es mayor que el final entonces intercambiamos los puntos
        if x0 > x1:
                x0,x1 = x1,x0
                y0,y1 = y1,y0

        #Calculamos nuevamente las diferencias
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Realizamos el calculo de los puntos que formaran la linea
        offset = 0 * 2 * dx 
        threshold = 0.5 * 2 * dx
        y = y0
        #Ciclo for para rellenar la linea con puntos sucesivos sin dejar espacio
        for x in range(x0, x1 + 1):
                if steep:
                        self.glPoint((float(y)/(float(self.width)/2))-1,(float(x)/(float(self.height)/2))-1,self.vertexColor)
                else:
                        self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertexColor)
                offset += dy
                if offset >= threshold:
                        y += 1 if y0 < y1 else -1
                        threshold += 1 * dx


    #Funcion para cargar un archivo .obj para renderizarlo
    def glLoad(self, filename,translate=(0,0), scale=(1,1)):
        #Se realiza la lectura del archivo .obj
        modelo3D = ArchivoObj(filename)
        modelo3D.lectura()

        #Se realiza un recorrido de las caras del modelo para conocer su numero de vertices
        for face in modelo3D.faces:
                contadorVertices = len(face)

                #Se recorre la cantidad de vertices para hacer las lineas del renderizado
                for j in range(contadorVertices):
                        #Se obtienen un par de vertices de las caras
                        f1 = face[j][0]
                        f2 = face[(j+1)%contadorVertices][0]

                        #Se obtiene cada vertice indicado anteriormente del modelo, obteniendo asi sus coordenadas
                        v1 = modelo3D.vertices[f1 - 1]
                        v2 = modelo3D.vertices[f2 - 1]

                        #Se obtienen los valores de los vertives x,z guardados en la posicion 0 y 1 de los vertices y se le da escala y traslacion a estos
                        x1 = (v1[0] + translate[0]) * scale[0]
                        y1 = (v1[1] + translate[1]) * scale[1]
                        x2 = (v2[0] + translate[0]) * scale[0]
                        y2 = (v2[1] + translate[1]) * scale[1]

                        #Se dibuja la linea con los puntos obtenidos
                        self.glLine(x1,y1,x2,y2)

    #Conversion de numero normal a -1 a 1
    def glConvert(self, number, coordenada):
        if coordenada == "x":
                numeroNuevo = (float(number)/((self.width)/2))-1
        elif coordenada =="y":
                numeroNuevo = (float(number)/((self.height)/2))-1
        return float(numeroNuevo)

    #Rellena una figura delimitada por vertices que se unen en el orden que se mandan
    #Basado en Algoritmo Punto en Poligono y modificado para pintar los puntos dentro del poligono
    def glFill(self, poligono):
        #Se recorre cada punto de la imagen por coordenadas x,y con ciclos for
        for y in range(self.height):
                for x in range(self.width): 
                        i = 0
                        j = len(poligono) - 1
                        resultado = False
                        #Se realiza un ciclo que revisa si el punto siempre se encuentra entre los limites de los vertices planteados
                        for i in range(len(poligono)):
                                #Si el poligono se encuentra dentro de los limites la variable resultado esta dentro de los limites obtiene un valor True 
                                if (poligono[i][1] < y and poligono[j][1] >= y) or (poligono[j][1] < y and poligono[i][1] >= y):
                                        if poligono[i][0] + (y - poligono[i][1]) / (poligono[j][1] - poligono[i][1]) * (poligono[j][0] - poligono[i][0]) < x:
                                                resultado = not resultado
                                j = i
                        #Si el resultado es True entonces se pinta el punto 
                        if resultado == True:
                                self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertexColor)
                        else:
                                pass

    
    def glFinish(self, filename):
        f = open(filename, 'wb')
        #file header 14
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(54 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(54))

        
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()

#Se crea un objeto para manejo de renderizados
objeto = Bitmap(800,600)

#Funciones SR2
def glInit():
        objeto = Bitmap(800,600)
        
def glCreateWindow(width,height):
        objeto.glCreateWindow(width,height)
        
def glClear():
        objeto.glClear()

def glClearColor(r,g,b):
        objeto.glClearColor(r,g,b)

#Funcion de linea que recibe coordenadas de un punto inicial y uno final con valores x,y entre -1 y 1
def glLine(x0,y0,x1,y1):
        objeto.glLine(x0,y0,x1,y1)
#Funcion de punto que recibe una coordenada x,y con valores entre -1 y 1
def glPoint(x,y,color):
        objeto.glPoint(x,y,color)
        
def glColor(r,g,b):
        objeto.glColor(r,g,b)

#cargar un archivo .obj para ser renderizado con traslado de sus puntos y a cierta escala
def glLoad(filename,translate,scale):
        objeto.glLoad(filename,translate,scale)
        
def glFinish(filename):
        objeto.glFinish(filename)

def glConvert(number,coordenada):
        num = objeto.glConvert(number,coordenada)
        return num

#Pintar un poligono internamente mandandole las coordenadas de los vertices del poligono en el orden en que se unen
def glFill(poligono):
        objeto.glFill(poligono)

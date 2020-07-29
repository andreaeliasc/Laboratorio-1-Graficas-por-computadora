#Andrea Elias
#17048

from glAndrea import *

glInit()
glCreateWindow(800,600)
glClear()

#Rellenamos el Poligono 1
glColor(0.5,1,0.75)
poligono1 = ((165, 380),(185, 360),(180, 330),(207, 345),(233, 330),(230, 360),(250, 380),(220, 385),(205, 410),(193, 383))
glFill(poligono1)

#Rellenamos el Poligono 2
glColor(1,1,0.5)
poligono2 = ((321, 335),(288, 286),(339, 251),(374, 302))
glFill(poligono2)

#Rellenamos el Poligono 3
glColor(1,0.5,1)
poligono3 = ((377, 249),(411, 197),(436, 249))
glFill(poligono3)

#Relleneamos el Poligono 4
glColor(0.5,1,1)
poligono4 = ((413, 177),(448, 159),(502, 88),(553, 53),(535, 36),(676, 37),(660, 52),(750, 145),(761, 179),(672, 192),(659, 214),(615, 214),(632, 230),(580, 230),(597, 215),(552, 214),(517, 144),(466, 180))
glFill(poligono4)

#Rellenamos el Poligono 5
glColor(0,0,0)
poligono5 = ((682, 175),(708, 120),(735, 148),(739, 170))
glFill(poligono5)

#Renderizamos los poligonos en un archivo llamado Poligono.bmp
glFinish("HolaPanda.bmp")
        

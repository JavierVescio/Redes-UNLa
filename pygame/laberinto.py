#TP de Redes - 2017 - UNLa

import pygame
import math
from managerGeneral import *

pygame.init()

dimensionDeUnaPosicion = 120
screen_height=600
screen_width=800
gameDisplay = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Laberinto')
pygame.display.update()

########COLORES########
blanco = (255,255,255)
negro = (0,0,0)
rojo = (255,0,0)
gris = (166,166,166)
naranja = (255,192,0)
celeste = (0,176,240)
verde = (146,208,80)
violeta = (112,48,160)
amarillo = (255,255,0)
#######################


########IMAGENES########
fueraImg = pygame.image.load('data/image/fuera.jpg')
guardiaImg = pygame.image.load('data/image/guardia.JPG')
llaveImg = pygame.image.load('data/image/llave.png')
oroImg = pygame.image.load('data/image/oro.png')
paredImg = pygame.image.load('data/image/pared.jpg')
personajeImg = pygame.image.load('data/image/personaje.png')
entradaImg = pygame.image.load('data/image/entrada.png')
salidaImg = pygame.image.load('data/image/salida.png')

fueraImg = pygame.transform.scale(fueraImg, (dimensionDeUnaPosicion, dimensionDeUnaPosicion))
guardiaImg = pygame.transform.scale(guardiaImg, (dimensionDeUnaPosicion, dimensionDeUnaPosicion))
llaveImg = pygame.transform.scale(llaveImg, (dimensionDeUnaPosicion, dimensionDeUnaPosicion))
oroImg = pygame.transform.scale(oroImg, (dimensionDeUnaPosicion, dimensionDeUnaPosicion))
paredImg = pygame.transform.scale(paredImg, (dimensionDeUnaPosicion, dimensionDeUnaPosicion))
personajeImg = pygame.transform.scale(personajeImg, (dimensionDeUnaPosicion, dimensionDeUnaPosicion))
entradaImg = pygame.transform.scale(entradaImg, (dimensionDeUnaPosicion, dimensionDeUnaPosicion))
salidaImg = pygame.transform.scale(salidaImg, (dimensionDeUnaPosicion, dimensionDeUnaPosicion))
########################

def blitImg(img,x,y):
    gameDisplay.blit(img,(x,y));

def mostrarTexto(texto,color,x,y,tamanio=15,negrita=False,cursiva=False):
    myfont = pygame.font.SysFont("monospace", tamanio, negrita, cursiva)
    label = myfont.render(texto,1,color)
    gameDisplay.blit(label,(x,y))

def determinarImagenDelElemento(letraDelElemento):
    imagenes = [fueraImg,guardiaImg,llaveImg,oroImg,paredImg,entradaImg,salidaImg]
    letras = "FGLOPES"
    posicion = letras.find(letraDelElemento)
    if (posicion == -1):
        return -1;
    else:
        return imagenes[posicion]

def determinarColorDelElemento(letraDelElemento):
    """
    Pared	P (Gris)
    Guardia	G (Rojo)
    Camino	C (Blanco)
    Llave	L (Naranja)
    Entrada	E (Celeste)
    Salida	S (Verde)
    Fuera	F (Violeta)
    Oro	        O (Amarillo)
    """
    colores = [gris,rojo,blanco,naranja,celeste,verde,violeta,amarillo]
    letras = "PGCLESFO"
    posicion = letras.find(letraDelElemento)
    if (posicion == -1):
        return black
    else:
        return colores[posicion]

def main(dimensionDeUnaPosicion):
    managerGeneral = ManagerGeneral()

    salirDelJuego = False
    
    while not salirDelJuego:
        sentido = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Si cierra la ventana el juego termina
                salirDelJuego = True
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_q): #Si presiona Q el juego termina
                    salirDelJuego = True
                elif (event.key == pygame.K_UP):
                    #Arriba
                    sentido = 1
                elif (event.key == pygame.K_DOWN):
                    #Abajo
                    sentido = 2
                elif (event.key == pygame.K_LEFT):
                    #Izquierda
                    sentido = 3
                elif (event.key == pygame.K_RIGHT):
                    #Derecha
                    sentido = 4

                elementos = managerGeneral.moverse(sentido)
        
        elementos = "PPPPCECCPGPPCPCPPCPCLOCPS"
        #elementos = "FFFFFFFPPPFFECCFFPPCFFPPC"
        
        #Como es una matriz cuadrada, la raiz cuadrada del total de elementos
        #sera el total de filas y tambien sera el total de columnas.
        #Ejemplo: si hay 9 elementos es porque es una matriz de 3 filas x 3 columnas.
        totalElementos = len(elementos)
        totalColFilDeMatrizCuadrada = math.sqrt(totalElementos)
        
        #Cuando recibo del server un nuevo string de elementos con posiciones, limpio la pantalla.
        gameDisplay.fill(blanco)
        
        iteracion=0
        columna=0
        while(columna<totalColFilDeMatrizCuadrada):
            fila=0
            while(fila<totalColFilDeMatrizCuadrada):
                posY = columna * dimensionDeUnaPosicion
                posX = fila * dimensionDeUnaPosicion

                if ((2*iteracion) - 1 == totalElementos):
                    #Se dibuja el jugador
                    blitImg(personajeImg,posX-dimensionDeUnaPosicion,posY)
                
                letraDelElemento = elementos[iteracion]
                imagenDelElemento = determinarImagenDelElemento(letraDelElemento)                
                #Si no tiene imagen asociada, le asigno color
                if (imagenDelElemento == -1):
                    colorDelElemento = determinarColorDelElemento(letraDelElemento)
                    gameDisplay.fill(colorDelElemento,rect=[posX,posY,dimensionDeUnaPosicion,dimensionDeUnaPosicion])
                else:
                    blitImg(imagenDelElemento,posX,posY)

                iteracion = iteracion + 1
                fila = fila + 1
            columna = columna + 1

        #Trazo una linea vertical negra
        ubicacionEnX = totalColFilDeMatrizCuadrada*dimensionDeUnaPosicion
        gameDisplay.fill(negro,rect=[ubicacionEnX,0,10,screen_height])

        #def mostrarTexto(texto,color,x,y,tamanio=15,negrita=False,cursiva=False):

        posXTextos = ubicacionEnX+25
        posYTextoOroRecodigo = 10
        mostrarTexto("ORO RECOGIDO",negro,posXTextos,posYTextoOroRecodigo,20,True)
        mostrarTexto(str(managerGeneral.oroRecogido),rojo,posXTextos,posYTextoOroRecodigo+25,25, False,True)

        posYTextoOroRecodigo = posYTextoOroRecodigo + 80
        mostrarTexto("POSESION LLAVE",negro,posXTextos,posYTextoOroRecodigo,20,True)
        mostrarTexto(managerGeneral.decirSiTieneLaLlave(),rojo,posXTextos,posYTextoOroRecodigo+25,25,False,True)

        posYTextoMensajeServidor = posYTextoOroRecodigo + 80
        mostrarTexto("MENSAJE SERVER",negro,posXTextos,posYTextoMensajeServidor,20,True)
        mostrarTexto(managerGeneral.mostrarMensajeServidor(),rojo,posXTextos,posYTextoMensajeServidor+25,25,False,True)
        
        pygame.display.update()

    #####  Desconectarse del server  #####
    #>>>>                            <<<<#
    ######################################
    pygame.quit()

main(dimensionDeUnaPosicion)

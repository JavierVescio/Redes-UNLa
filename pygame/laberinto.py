#TP de Redes - 2017 - UNLa

import pygame
import math

pygame.init()

screen_height=600
screen_width=800
gameDisplay = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Laberinto')
pygame.display.update()

salirDelJuego = False
dimensionDeUnaPosicion = 120

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

while not salirDelJuego:
    for event in pygame.event.get():
        #Aca se tiene que capturar cuando el usuario usa izq,der,arr,aba para enviar al server.
        
        if event.type == pygame.QUIT:
            salirDelJuego = True

    #Cuando recibo del server un nuevo string de elementos con posiciones, limpio la pantalla.
    gameDisplay.fill(blanco)
    elementos = "PPPPCECCPGPPCPCPPCPCLOCPS"
    #elementos = "FFFFFFFPPPFFECCFFPPCFFPPC"
    
    #Como es una matriz cuadrada, la raiz cuadrada del total de elementos
    #sera el total de filas y tambien sera el total de columnas.
    #Ejemplo: si hay 9 elementos es porque es una matriz de 3 filas x 3 columnas.
    totalElementos = len(elementos)
    totalColFilDeMatrizCuadrada = math.sqrt(totalElementos)

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
    gameDisplay.fill(negro,rect=[totalColFilDeMatrizCuadrada*dimensionDeUnaPosicion,0,10,screen_height])
    pygame.display.update()
pygame.quit()


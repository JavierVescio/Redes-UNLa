import socket
import thread
import sys
import time
import struct
import uuid
from encrip import * 

HOST = '0.0.0.0'
SOCKET_LIST = []
RECV_BUFFER = 1024
PORT = 9000
CLAVEMAESTRA = '0123456789111222'

#Simulacion de usuarios para evitar archivos o BD.
#3f1131a93d30f2fe66a57de1c8c8a042 = unla2017
#5b5462d75b2dac55d1c783e30a391597 = casa256
#74eb73ef2066 8fe689851ecfc225d168 = cualquiera123
hardcodeminimap = 'PPPPCECCPGPPCPCPPCPCLOCPS'

USUARIOS=[['jose','3f1131a93d30f2fe66a57de1c8c8a042'],
          ['agus','5b5462d75b2dac55d1c783e30a391597'],
          ['javi','74eb73ef20668fe689851ecfc225d168']]
MAPAS=[
      ['P','P','C','P','P','P','P','P','G','P','P','P','P','P','P','P','P','P','P','0'],
      ['E','C','C','C','O','C','C','P','C','P','P','P','P','C','C','C','C','C','C','C'],
      ['P','P','C','P','P','P','C','P','C','C','C','P','P','C','P','C','P','P','P','P'],
      ['P','P','C','C','C','G','C','P','P','P','C','C','C','G','P','C','C','C','C','G'],
      ['P','P','C','P','P','P','P','P','C','C','C','P','P','P','P','C','P','P','P','C'],
      ['P','P','O','P','P','C','C','C','C','P','P','P','C','C','C','C','P','P','P','C'],
      ['C','C','C','C','P','P','P','P','G','P','C','P','C','P','C','P','P','P','P','C'],
      ['P','P','P','C','P','P','P','C','C','C','C','P','P','P','C','C','P','C','P','C'],
      ['P','P','P','G','C','C','P','P','C','P','O','P','P','P','P','C','P','O','P','P'],
      ['O','O','P','P','P','C','P','P','C','P','C','P','P','P','P','C','C','C','P','P'],
      ['C','P','P','P','P','C','P','C','C','C','C','P','C','P','P','P','P','C','P','P'],
      ['C','P','P','C','C','C','C','C','P','P','C','C','C','P','P','C','C','C','C','C'],
      ['C','C','C','C','P','P','P','P','P','P','C','P','P','P','P','C','P','P','P','P'],
      ['P','C','P','C','P','P','C','C','C','C','C','P','G','C','C','C','O','C','C','P'],
      ['P','C','P','C','P','P','C','P','P','C','P','P','C','P','P','P','P','P','C','P'],
      ['C','C','C','G','P','C','C','P','P','C','P','P','C','P','P','P','P','P','C','P'],
      ['P','P','P','P','P','C','P','P','G','G','P','P','C','C','P','P','G','C','C','P'],
      ['P','C','O','C','C','C','P','P','C','P','P','P','P','C','P','P','G','P','P','P'],
      ['P','C','P','P','P','G','P','P','C','C','C','P','P','O','P','P','C','P','P','P'],
      ['P','C','C','C','C','C','P','L','P','O','P','P','O','P','P','S','P','P','P','P'],
      ]

def login(usuario, password):
  ret=False
  for user in USUARIOS:
    if (user[0] == usuario):
      if (user[1] == encrypt_md5(password)): 
        ret = True
        print "si"
  
  return ret
  
class Client:
    pass

def conexion(client):
  print "Se conecto: ", client.addr
  #espera a recibir el bufferdel login
  data = client.socket.recv(RECV_BUFFER)
  #desencriptamos el buffer recivido del cliente
  data = decrypt_val(data,CLAVEMAESTRA)
  comando = data.split('|')
  if (comando[0]=='log'):
  #aca verificamos el usuario
    if login(comando[1],comando[2]):
    #Login exitoso.
    #Este bucle se repite cada vez que se encuentran datos en el bufer
      cliente_conectado = True
      mensaje = 'log|ok'
      mensaje = encrypt_val(mensaje, CLAVEMAESTRA)
      try:
        client.socket.send(mensaje)        
      except:
        print("Error no se pudo enviar msg")
        cliente_conectado = False
        try:
          client.socket.close()          
        finally:
          SOCKET_LIST.remove(client)
#aca empieza el juego
      gameover = False
      #time.sleep(1)
      while gameover==False:
        oro = 0
        llave = 0
        msg = 'Juege'
        pos = [1,0]
        mapaactual = []
        mapaactual = MAPAS
        movimientovalido = True
        movimiento = True
        while movimiento:
          #try:
          minimap=''
          fila = 0 
          if movimientovalido:         
            x=pos[0]-2
            while (fila < 5):
              columna=0
              y=pos[1]-2
              while (columna < 5):
                if x>=0 and y>=0 and x<20 and y<20:
                  minimap=minimap+mapaactual[x][y]
                else:
                  minimap=minimap+'F'
                y=y+1  
                columna = columna + 1
              fila = fila + 1
              x=x+1
            
            print minimap
            if minimap[12]== 'O':
              oro=oro+1
              mapaactual[pos[0]][pos[1]]='C'
            if minimap[12]== 'L':
              llave = 1
              mapaactual[pos[0]][pos[1]]='C'
            if minimap[12]== 'G':
              if oro > 0:
                oro=oro-1
                mapaactual[pos[0]][pos[1]]='C'
              else:
                #si no tiene oro termina el juego y vuelve a empezar
                gameover=True
                movimiento = False
                msg = 'No tienes ORO!! GAMEOVER'
                #despues analizar si el oro es negativo fin de juego
            if minimap[12]== 'S':
              if llave == 1 :
                win = True
              else :           
                msg = 'Falta la llave'
            minimap=minimap[0:11] + 'J' + minimap[13:]
            
          else:
                #MOVIMIENTO INVALIDO volvemos a mandar el minimap anterior
            msg = 'Movimiento INVALIDO!!'

          mensaje = 'map|'+minimap+'-'+str(oro)+str(llave)+msg

          mensaje = encrypt_val(mensaje, CLAVEMAESTRA)
          print len(mensaje)
          print mensaje
          client.socket.send(mensaje)
          time.sleep(1)
          data = client.socket.recv(RECV_BUFFER)
          data = decrypt_val(data,CLAVEMAESTRA)
          comando = data.split('|')
          if comando[0] == 'exit':
            cliente.socket.close()
            SOCKET_LIST.remove(c)
            print "Cliente " + c.code + " solicita desconeccion - Cerrando..."
            movimiento=False
            gameover = True
                  
          if comando[0] == 'mov':
            if comando[1]=='up':  
              if pos[1]-1<=0:
                if mapaactual[pos[0]][pos[1]-1]=='P':
                  movimientovalido = False
                else:
                  pos[1]=pos[1]-1
              else:
                movimientovalido = False
            elif comando[1]=='do':  
              if pos[1]+1>20:
                if mapaactual[pos[0]][pos[1]+1]=='P':
                  movimientovalido = False
                else:
                  pos[1]=pos[1]+1
              else:
                movimientovalido = False
            elif comando[1]=='le':  
              if pos[0]-1<=0:
                if mapaactual[pos[0]-1][pos[1]]=='P':
                  movimientovalido = False
                else:
                  pos[0]=pos[0]-1
              else:
                movimientovalido = False
            elif comando[1]=='ri':  
              if pos[0]+1>20:
                if mapaactual[pos[0]+1][pos[1]]=='P':
                  movimientovalido = False
                else:
                  pos[0]=pos[0]+1
              else:
                movimientovalido = False
                """
                for c in SOCKET_LIST:
                    # Enviar mensaje al cliente
                    if not c.socket.send("chau"):
                        try:
                            c.socket.close()
                        finally:
                            SOCKET_LIST.remove(c)
                            print "Cliente " + c.code + " no econtrado - Cerrando..."
                            cliente_conectado=False
                print "Total clients: " + str(len(SOCKET_LIST))
                """
                 
        """  except Exception as e:
            print "Excepcion en socket de cliente:"
            print e
            try:
              client.socket.close()
            finally:
              SOCKET_LIST.remove(client)
              print "Cliente " + client.code + " no encontrado - Socket cerrado - Total clients: " + str(len(SOCKET_LIST))
              movimiento = False
              gameover = True"""
              
  return
def server():

    # Declaracion del socket
    server_addr = (HOST, PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_addr)
    server_socket.listen(10)

    print "Esperando conexion...\n"
    while 1:

        # Esto ocurre antes de que se conecte un nuevo cliente
        c = Client()
        c.code = str(uuid.uuid4().fields[-1])[:5]

        # El server se queda en el bucle server_socket.accept()
        # hasta que se conecte un cliente y entonces se devuelven
        # el socket y la direccion desde donde se ha conectado
        c.socket, c.addr = server_socket.accept()

        # Lo aÃÂ±adimos a una lista
        SOCKET_LIST.append(c)

        # Y lo lanzamos en un hilo para gestionar su conexiÃÂ³n
        thread.start_new_thread(conexion, (c,))

    server_socket.close()

if __name__ == "__main__":
    sys.exit(server())

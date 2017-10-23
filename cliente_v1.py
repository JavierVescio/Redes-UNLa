# coding=utf-8
import sys
import socket
import random
import time
import struct
import thread
from encrip import * 

HOST = 'localhost'
PORT = 9000
RECV_BUFFER = 1024
CLAVEMAESTRA = '0123456789111222'

def conexion(socket,texto):
    hola = ""
    


def client():
    addr = (HOST, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
    try:
        client_socket.connect(addr)
    except:
        print "No se pudo conectar con el servidor."
        exit()
    
    #Enviar Mensaje al Srvidor
    user = input("Ingrese Usuario: ")
    passw = input("Ingrese Password: ")
    texto= "log|" + user + "|" + passw
    data = encrypt_val(texto,CLAVEMAESTRA)
    client_socket.send(data)
    data = client_socket.recv(RECV_BUFFER)
    data = decrypt_val(data,CLAVEMAESTRA)
    comando = data.split('|')
    
    if (comando[0]=='log' and comando[1] == 'ok'):
        conected=True
        while conected:
            #Leer respuesta del servidor
            try:
                data = client_socket.recv(RECV_BUFFER)
                data = decrypt_val(data,CLAVEMAESTRA)
                comando = data.split('|')
                datos = comando[1].split('-')
                if comando[0] == 'map':
                    minimap = datos[0]
                    oro = datos[1]
                    llave = datos[2]
                    mensaje = datos[3]
                    print "llego todo"
                else:
                    print "El servidor envio un comando invalido"
            except:
                print "El servidor se desconecto."
            exit()
    else:
        print "Error en el inicio de sesion."
        exit()
  
if __name__ == "__main__":
    sys.exit(client())
    
    
    """
cliente
log|usuario:pass
mov|up/do/le/ri
exi|1

servidor
log|ok/no
map|dddddddddddgddddddddddddd-cant_oro-0/1(llave)-gameover/win!!/movimiento invalido/up/do/le/ri/time over
"""  

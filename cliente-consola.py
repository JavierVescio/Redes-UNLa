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
def client():
    addr = (HOST, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
    try:
        client_socket.connect(addr)
    except:
        print "No se pudo conectar con el servidor."
        exit()
    print("Consola de cliente(ingrese exi|ok para salir")
    bandera = 0
    while True:
        #Enviar Mensaje al Srvidor     
        msg= raw_input("Ingrese el mensaje que desea enviar al servidor: ")
        data = encrypt_val(msg,CLAVEMAESTRA)
        client_socket.send(data)
        data = client_socket.recv(RECV_BUFFER)
        data = decrypt_val(data,CLAVEMAESTRA)
        comando = data.split('|')
        print "comando recibido: "+comando[0]
        print "Datos recibidos: "+comando[1]
        if bandera == 0:
            print "aca entra cuando el log es ok y manda el primer minimapa"
            print "despues de logear ya no hace caso a los comandos log "
            data = client_socket.recv(RECV_BUFFER)
            data = decrypt_val(data,CLAVEMAESTRA)
            comando = data.split('|')
            print "comando recibido: "+comando[0]
            print "Datos recibidos: "+comando[1]
            bandera = 1 
if __name__ == "__main__":
    sys.exit(client())
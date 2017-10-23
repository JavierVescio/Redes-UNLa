# coding=utf-8
import sys
import socket
import random
import time
import struct
import thread
from encrip import * 

class ManagerGeneral():
    HOST = 'localhost'
    PORT = 9000
    RECV_BUFFER = 1024
    CLAVEMAESTRA = '0123456789111222'

    def __init__(self):
        self.llaveRecogida = True
        self.oroRecogido = 0
        self.mensajeServidor = "-"

    def moverse(self,sentido):
        elementos = ""
        #elementos = Lo que el server responda
        return elementos

    def decirSiTieneLaLlave(self):
        if (self.llaveRecogida):
            return "Si"
        else:
            return "No"

    def mostrarMensajeServidor(self):
        return self.mensajeServidor

    def conexion(self,socket,texto):
        hola = ""

    def client(self):
        print "MI HOST ES " +self.HOST
        addr = (self.HOST, self.PORT)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(addr)
        except:
            print "No se pudo conectar con el servidor."
            exit()
        
        #thread.start_new_thread(self.escucharServer, (client_socket,))
                #Enviar Mensaje al Srvidor
        user = raw_input("Ingrese Usuario: ")
        passw = raw_input("Ingrese Password: ")
        texto= "log|" + user + "|" + passw
        data = encrypt_val(texto,self.CLAVEMAESTRA)
        
        client_socket.send(data)
        data = client_socket.recv(self.RECV_BUFFER)
        data = decrypt_val(data,self.CLAVEMAESTRA)
        comando = data.split('|')
        
        if (comando[0]=='log' and comando[1] == 'ok'):
            conected=True
            while conected:
                #Leer respuesta del servidor
                print "1.- me conecte"
                try:
                    data = client_socket.recv(self.RECV_BUFFER)
                    data = decrypt_val(data,self.CLAVEMAESTRA)
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

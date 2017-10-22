class ManagerGeneral():
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

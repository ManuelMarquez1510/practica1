#!/usr/bin/env python3

import socket
import sys
import time
import random
import pickle


# Variable que indica jugador 1 activo
jugador1Activo = True

# contador de pares
scoreJugador1 = 0
scoreJugador2 = 0
# control despliegue
bDespliegue = False
def tableroCrear():
    # cliclo para generar tablero vacio
    for lineas in range(ordenTablero):

        # inicializa la linea
        linea = []

        # ciclo para las columnas
        for columnas in range(ordenTablero):
            linea.append("------")

        # agrega la linea al tablero
        t.tablero.append(linea)


# funcion para desplegar tablero
def tableroDesplegar(enJuego):
    # ciclo por linea
    for linea in t.tablero:

        # ciclo por columnas
        for palabra in linea:
            if palabra == "**J1**" or palabra == "**J2**":
                print(palabra, end="  ")
            else:
                if enJuego:
                    print("------", end="  ")
                else:
                    print(palabra, end="  ")

        # cambio de linea
        print()

    # deja una linea
    print()


# funcion para iniciar el tablero  con los numero
def tableroIniciar():
    # variable para saber si se ha llenado el tablero
    paresColocados = 0

    # control de la carta
    bCarta2 = False

    # ciclo mientras noo este completado el tablero
    while (paresColocados < (ordenTablero * ordenTablero) / 2):

        # Ciclo para colocar la carta
        while (True):

            # Genera un numero aleatorio para la linea
            linea = random.randrange(ordenTablero)

            # Genera un numero aleatorio para la columna
            columna = random.randrange(ordenTablero)

            # si es la carta1
            if (not bCarta2):
                # obtiene la carta
                t.carta = random.choice(t.cartas)

            # verifica que no este desponible
            if (t.tablero[linea][columna] == '------'):

                # coloca la carta
                t.tablero[linea][columna] = t.carta

                # verifica si es la carta2
                if (bCarta2):
                    # incrementa el contador de casillasLlenadas
                    paresColocados = paresColocados + 1

                    # elimina la carta del mazo
                    if (bDespliegue):
                        print("Se elimina la carta:", t.carta)

                    # remueve la carta
                    t.cartas.remove(t.carta)

                    if (bDespliegue):
                        print(t.cartas)
                        input()

                # cambia el estado de la carta
                bCarta2 = not bCarta2

                # sale del ciclo
                break
            else:
                if (bDespliegue):
                    print("Fila:", linea, "Columna:", columna)
                    print("Pares colocados:", paresColocados)
                    tableroDesplegar(False)
                    input("choque...\n")


def activa(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col):
    activa = False

    if (J1carta1ren == J1carta2ren and J1carta1col == J1carta2col):
        activa = True
    else:
        activa = False
    return activa


# Funcion que despliega el marcador
def marcadorDesplegar():
    print("El marcador es:")
    print("El jugador 1:", scoreJugador1)
    print("El jugador 2:", scoreJugador2)
    print()


class Tablero(object):
    def __init__(self):
        self.carta = None
        self.tablero = []
        self.cartas = ["Arbol", "Bombo", "Caldo", "Dados", "Elote", "Fiona", "Grito", "Higos", "Impar", "Julia", "Karma",
          "Lapiz", "Manta", "Nariz", "Oreja", "Perro", "Queso", "Ratas", "Salir", "Talco", "Union", "Viejo", "Wendy",
          "Xolos", "Yarda", "Zorro"]

    def esParJ1(self, J1carta1ren, J1carta1col, J1carta2ren, J1carta2col):
        # variable para resultado
        bEsPar = False

        # compara
        if (self.tablero[J1carta1ren][J1carta1col] == self.tablero[J1carta2ren][J1carta2col]):
            self.tablero[J1carta1ren][J1carta1col] = "**J1**"
            self.tablero[J1carta2ren][J1carta2col] = "**J1**"

            # Variable de resultado
            bEsPar = True
        return bEsPar

    def esParJ2(self,J2carta1ren, J2carta1col, J2carta2ren, J2carta2col):
        # variable para resultado
        bEsPar = False

        # compara
        if (self.tablero[J2carta1ren][J2carta1col] == self.tablero[J2carta2ren][J2carta2col]):
            # coloca a que jugador pertenece el par realizado
            self.tablero[J2carta1ren][J2carta1col] = "**J2**"
            self.tablero[J2carta2ren][J2carta2col] = "**J2**"

            # Variable de resultado
            bEsPar = True

        return bEsPar

    # funcion para obtener  una carta seleccionada
    def cartaSeleccionadaValida(self,ren, col):
        valida = True
        if (self.tablero[ren][col] == "**J1**" or self.tablero[ren][col] == "**J2**"):
            valida = False

        else:
            valida = True
        # retorna la carta seleccionada
        return valida

    def cartaSeleccionada(self, ren, col):
        return (self.tablero[ren][col])


# print("Indique la ip donde recibira solicitudes")
# input()  # Direccion de la interfaz de loopback estándar (localhost) "127.0.0.1"
HOST = "localhost"
# print("Indique el puerto donde recibira las solucitudes")
# int(input())  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
PORT = 12345
buffer_size = 1024

t = Tablero()
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(1)
    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()
    
    print("Conectado a", Client_addr)
    
    print("Esperando a recibir dificultad... ")
    dificultad = Client_conn.recv(buffer_size)
    
    if dificultad.decode('utf-8') == "1":
        ordenTablero = 4

    elif dificultad.decode('utf-8') == "2":
        ordenTablero = 6

    Client_conn.send(str(ordenTablero).encode('utf-8'))
    print("\nGenerando tablero...")
    print("creando tablero")
    tableroCrear()
    print("tablero creado exitosamente")
    print("iniciando tablero")
    tableroIniciar()
    print("tablero iniciado correctamente")
    print("enviando tablero...")
    Client_conn.send(pickle.dumps(t.tablero))

    with Client_conn:

        while (scoreJugador1 + scoreJugador2 < ordenTablero * ordenTablero / 2):

            if (jugador1Activo == True):
                while True:
                    sys.stdout.flush()
                    print("activo jugador 1")
                    print("\nRecibiendo el par de casillas de la primera carta del jugador 1...")
                    #recibiendo datos 1
                    jugada = Client_conn.recv(buffer_size)

                    jugadaDecode = jugada.decode('utf-8')
                    listaJugada = jugadaDecode.split(",")
                    J1carta1ren = int(listaJugada[0])
                    J1carta1col = int(listaJugada[1])
                    print(f"x = {J1carta1ren} , y = {J1carta1col} ")
                    print(f"Enviando {listaJugada} a {Client_addr}")

                    if (t.cartaSeleccionadaValida(J1carta1ren, J1carta1col) == True):
                        # despliega lo que hay en esa posicion
                        cartaValida = "cartaValida1On"

                        #enviando datos 2
                        cartasEnviar = cartaValida+"*"+t.cartaSeleccionada(J1carta1ren, J1carta1col)
                        Client_conn.send(cartasEnviar.encode('utf-8'))
                        valida = True
                    else:
                        print("la carta seleccionada del jugadro 1 esta en juego, vuelva a intentarlo...")
                        tableroDesplegar(True)
                        cartaValida = "cartaValida1Off"
                        cartasEnviar = cartaValida+ "*" + t.cartaSeleccionada(J1carta1ren, J1carta1col)
                        # enviando datos 2
                        Client_conn.send(cartasEnviar.encode('utf-8'))

                        valida = False
                        continue
                    while True:
                        sys.stdout.flush()
                        print("\nRecibiendo el par de casillas de la segunda carta del jugador 1...")
                        #recibiendo datos 2
                        jugada = Client_conn.recv(buffer_size)

                        jugadaDecode=jugada.decode('utf-8')
                        print("esta es la jugada decode:",jugadaDecode)
                        listaJugada = jugadaDecode.split(",")
                        J1carta2ren = int(listaJugada[0])
                        J1carta2col = int(listaJugada[1])
                        print(f"x = {J1carta2ren} , y = {J1carta2col} ")
                        print(f"Enviando {listaJugada} a {Client_addr}")

                        if (activa(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col)):
                            cartaActiva="cartaActiva1On"
                            cartaValida = "cartaValida2Off"
                            #enviando datos 3
                            cartasEnviar = cartaActiva+"*"+cartaValida + "*" + t.cartaSeleccionada(J1carta2ren, J1carta2col)
                            Client_conn.send(cartasEnviar.encode('utf-8'))
                            print("la carta seleccionada del jugadro 1 esta en juego, vuelva a intentarlo...")
                            tableroDesplegar(True)
                            continue
                        else:
                            if (t.cartaSeleccionadaValida(J1carta2ren, J1carta2col) == True):
                                # despliega lo que hay en esa posicion
                                cartaActiva = "cartaActiva1Off"
                                cartaValida = "cartaValida2On"
                                cartasEnviar = cartaActiva + "*" + cartaValida + "*" + t.cartaSeleccionada(J1carta2ren, J1carta2col)
                                #enviando datos 4
                                Client_conn.send(cartasEnviar.encode('utf-8'))
                                valida = True
                            else:
                                print("la carta seleccionada del jugador 1 esta en juego, vuelva a intentarlo...")
                                cartaActiva = "cartaActiva1Off"
                                cartaValida = "cartaValida2Off"
                                cartasEnviar = cartaActiva + "*" + cartaValida + "*" + t.cartaSeleccionada(J1carta2ren, J1carta2col)
                                Client_conn.send(cartasEnviar.encode('utf-8'))
                                tableroDesplegar(True)
                                valida = False
                                continue
                            if valida:
                                break
                    if (t.esParJ1(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col)):
                        print("\n¡El jugador 1 hizo par!\n")
                        par = "esPar1"
                        Client_conn.send(par.encode('utf-8'))
                        # incrementa el contador del jugador 1
                        scoreJugador1 = scoreJugador1 + 1
                        tableroDesplegar(True)
                        marcadorDesplegar()
                        jugador1Activo = True
                        if (scoreJugador1 + scoreJugador2 >= ordenTablero * ordenTablero / 2):
                            break
                    else:
                        print("\n¡El jugador 1 Fallo!\n")
                        par  = "noPar1"
                        Client_conn.send(par.encode('utf-8'))
                        jugador1Activo = False

                    if jugador1Activo == False:
                        break
                    # despliega el tablero y el marcador
                tableroDesplegar(True)
                marcadorDesplegar()

            elif (jugador1Activo == False):
                while True:
                    sys.stdout.flush()
                    print("Jugador 2 activo")
                    if (ordenTablero == 4):
                        # obtiendo las coordenadas de la
                        J2carta1ren = random.randrange(4)
                        J2carta1col = random.randrange(4)
                    else:
                        J2carta1ren = random.randrange(6)
                        J2carta1col = random.randrange(6)

                    if (t.cartaSeleccionadaValida(J2carta1ren, J2carta1col) == True):
                        # despliega lo que hay en esa posicion
                        valida = True
                    else:
                        print("la carta seleccionada del jugador 2 esta en juego, vuelva a intentarlo...")
                        tableroDesplegar(True)
                        valida = False
                        continue
                    while True:
                        sys.stdout.flush()
                        if (ordenTablero == 4):

                            J2carta2ren = random.randrange(4)
                            J2carta2col = random.randrange(4)
                        else:
                            J2carta2ren = random.randrange(6)
                            J2carta2col = random.randrange(6)

                        if (activa(J2carta1ren, J2carta1col, J2carta2ren, J2carta2col)):

                            print("la carta del jugador 2 esta en juego, vuelva a intentarlo...")
                            tableroDesplegar(True)
                            continue
                        else:
                            if (t.cartaSeleccionadaValida(J2carta2ren, J2carta2col) == True):
                                # despliega lo que hay en esa posicion
                                valida = True
                            else:
                                print("la carta seleccionada del jugador 2 esta en juego, vuelva a intentarlo...")
                                tableroDesplegar(True)
                                valida = False
                                continue
                            if valida:
                                break
                    # llama a funcion que verifica si coinciden
                    if (t.esParJ2(J2carta1ren, J2carta1col, J2carta2ren, J2carta2col)):
                        print("\n¡El jugador 2 hizo par!\n")
                        par = "esPar2"

                        data = par+"*"+str(J2carta1ren)+"*"+str(J2carta1col)+"*"+str(J2carta2ren)+"*"+str(J2carta2col)
                        Client_conn.send(data.encode("utf-8"))
                        # incrementa el contador del jugador 2
                        scoreJugador2 = scoreJugador2 + 1
                        tableroDesplegar(True)
                        marcadorDesplegar()
                        jugador1Activo = False
                        if (scoreJugador1 + scoreJugador2 >= ordenTablero * ordenTablero / 2):
                            break
                    else:
                        print("\n!El jugador 2 fallo!\n")
                        par="noPar2"
                        data = par + "*" + str(J2carta1ren) + "*" + str(J2carta1col) + "*" + str(J2carta2ren) + "*" + str(J2carta2col)
                        Client_conn.send(data.encode("utf-8"))
                        jugador1Activo = True

                    if jugador1Activo == True:
                        break
                # despliega el tablero y el marcador
                tableroDesplegar(True)
                marcadorDesplegar()
        # validacion final
        if (scoreJugador1 > scoreJugador2):
            print("El jugador 1 ha ganado")
            jugador1="jugador1"
            Client_conn.send(jugador1.encode('utf-8'))
        else:
            if (scoreJugador2 > scoreJugador1):
                jugador2="jugador2"
                Client_conn.send(jugador2.encode('utf-8'))
                print("El jugador 2 ha ganado")
            else:
                print("Ha sido un empate")
        print("\nSe acabo el juego\n")
        print("cerrare la conexion")
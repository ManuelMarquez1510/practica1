#!/usr/bin/env python3

import socket
import time
import pickle
import random
import sys


def tableroCrear():
    # cliclo para generar tablero vacio
    for lineas in range(ordenTablero):

        # inicializa la linea
        linea = []

        # ciclo para las columnas
        for columnas in range(ordenTablero):
            linea.append("------")

        # agrega la linea al tablero
        tablero.append(linea)

# funcion para desplegar tablero
def tableroDesplegar(enJuego):
    # ciclo por linea
    for linea in tablero:

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

# Funcion que despliega el marcador
def marcadorDesplegar():
    print("El marcador es:")
    print("El jugador 1:", scoreJugador1)
    print("El jugador 2:", scoreJugador2)
    print()

scoreJugador1=0
scoreJugador2=0
jugadorActivo = True

#print("Indique la ip del servidor")
HOST = "localhost"  # input()  # El hostname o la IP del servidor "127.0.0.1"
#print("Indique el puerto que utiliza el servidor")
PORT = 12345  # int(input())  # El puerto que usa el servidor 12345
buffer_size = 1024

tablero = []

print("Elige la dificultad el juego")
print("1 : Principiante")
print("2 : Avanzado")
dificultad = input()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando dificultad...\n")
    TCPClientSocket.send(dificultad.encode('utf-8'))
    print("Esperando una respuesta...\n")
    data = TCPClientSocket.recv(buffer_size)
    if(data.decode() == "4"):
        ordenTablero = 4
        print("Se ha creado un tablero nivel Principiante!!")
        print()
    else:
        ordenTablero = 6
        print("Se ha creado un tablero nivel Avanzado!!")
        print()

    # Recibe el tablero del servidor
    tablero = pickle.loads(TCPClientSocket.recv(buffer_size))

    print("Cartas a jugar")
    print()
    tableroDesplegar(False)

    print("Tablero a jugar")
    print()
    tableroDesplegar(True)

    while (scoreJugador1 + scoreJugador2 < ordenTablero * ordenTablero / 2):
        if jugadorActivo == True:
            while True:
                sys.stdout.flush()
                print("jugador 1 activo")
                jugada = input("Ingrese la primera carta: renglon, columna: \n")
                # convirtiendo a listas
                listaJugadas = jugada.split(",")
                # obtiendo las coordenadas de la carta1
                J1carta1ren = int(listaJugadas[0])
                J1carta1col = int(listaJugadas[1])
                #enviando datos  1
                TCPClientSocket.send(jugada.encode('utf-8'))
                #recibiendo datos 1
                cartasRecibir= TCPClientSocket.recv(buffer_size)
                cartasRecibirDecode= cartasRecibir.decode('utf-8')
                listaCartas=cartasRecibirDecode.split("*")
                cartaValida = listaCartas[0]
                #print(cartaValida)
                cartaSeleccionada = listaCartas[1]
                #print(cartaSeleccionada)
                if cartaValida == "cartaValida1On":
                    print("La carta 1 seleccionada del jugador 1 es:", cartaSeleccionada,"\n")
                    valida = True
                else:
                    print("la carta seleccionada esta en juego, vuelva a intentarlo...")
                    tableroDesplegar(True)
                    valida = False
                    continue
                while True:
                    sys.stdout.flush()
                    jugada = input("Ingrese la segunda carta: renglon, columna: \n")
                    # convirtiendo a listas
                    listaJugadas = jugada.split(",")
                    # obtiendo las coordenadas de la carta1
                    J1carta2ren = int(listaJugadas[0])
                    J1carta2col = int(listaJugadas[1])
                    TCPClientSocket.send(jugada.encode('utf-8'))
                    sys.stdout.flush()
                    cartasRecibir = TCPClientSocket.recv(buffer_size)
                    cartasRecibirDecode = cartasRecibir.decode('utf-8')
                    listaCartas = cartasRecibirDecode.split("*")
                    cartaValida = listaCartas[1]
                    #print(cartaValida)
                    cartaSeleccionada = listaCartas[2]
                    #print(cartaSeleccionada)
                    cartaActiva = listaCartas[0]
                    #print("carta activa: ",cartaActiva)
                    if cartaActiva == "cartaActiva1On":
                        print("la carta seleccionada esta en juego, vuelva a intentarlo...")
                        tableroDesplegar(True)
                        continue
                    else:
                        #print("carta valida 2: ", cartaValida)
                        if cartaValida == "cartaValida2On":
                            print("La carta 2 seleccionada del jugador 1 es: ", cartaSeleccionada,"\n")
                            valida = True
                        else:
                            print("la carta del jugador 1 esta en juego, vuelva a intentarlo...")
                            tableroDesplegar(True)
                            valida = False
                            continue
                        if valida:
                            break
                par=TCPClientSocket.recv(buffer_size)
                parDecode=par.decode('utf-8')
                if (parDecode=="esPar1"):
                    # incrementa el contador del jugador 1
                    print("\n¡El jugador 1 hizo par!\n")
                    scoreJugador1 = scoreJugador1 + 1
                    tablero[J1carta1ren][J1carta1col] = "**J1**"
                    tablero[J1carta2ren][J1carta2col] = "**J1**"
                    tableroDesplegar(True)
                    marcadorDesplegar()
                    jugadorActivo = True
                    if (scoreJugador1 + scoreJugador2 >= ordenTablero * ordenTablero / 2):
                        break
                else:
                    print("\n¡El jugador 1 Fallo!\n")
                    jugadorActivo = False

                if jugadorActivo == False:
                    break
            #despliega el tablero y el marcador
            tableroDesplegar(True)
            marcadorDesplegar()

        elif jugadorActivo == False:
            while True:

                print("jugador 2 activo")
                """
                cartaValida = TCPClientSocket.recv(buffer_size)
                print(cartaValida.decode("utf-8"))
                if cartaValida.decode("utf-8") == "True":
                    cartaSeleccionada = TCPClientSocket.recv(buffer_size)
                    print("La carta 1 seleccionada del jugador 2 es:", cartaSeleccionada.decode("utf-8"),"\n")
                    valida = True
                elif cartaValida.decode("utf-8")== "False":
                    print("la carta seleccionada del jugador 2 esta en juego, vuelva a intentarlo...")
                    tableroDesplegar(True)
                    valida = False
                    continue
                while True:
                    cartaActiva = TCPClientSocket.recv(buffer_size)
                    if cartaActiva.decode("utf-8") == "True":
                        print("la carta seleccionada del jugador 2 esta en juego, vuelva a intentarlo...")
                        tableroDesplegar(True)
                        continue
                    else:
                        cartaValida = TCPClientSocket.recv(buffer_size)
                        if cartaValida.decode("utf-8") == "True":
                            cartaSeleccionada = TCPClientSocket.recv(buffer_size)
                            print("La carta 2 seleccionada del jugador 2 es:",cartaSeleccionada.decode(),"\n")
                            valida = True
                        else:
                            print("la carta seleccionada del jugador 2 esta en juego, vuelva a intentarlo...")
                            tableroDesplegar(True)
                            valida = False
                            continue
                        if valida:
                            break
                    """
                data = TCPClientSocket.recv(buffer_size)
                dataDecode=data.decode('utf-8')
                listaData = dataDecode.split("*")
                par=listaData[0]
                #print(par)
                J2carta1ren = int(listaData[1])
                #print("Renglon carta1:",J2carta1ren)
                J2carta1col= int(listaData[2])
                #print("columna carta1:",J2carta1col)
                J2carta2ren = int(listaData[3])
                #print("Renglon carta2:",J2carta2ren)
                J2carta2col= int(listaData[4])
                #print("columna carta2:",J2carta2col)
                if (par == "esPar2"):
                    # incrementa el contador del jugador 1
                    print("¡El jugador 2 hizo par!\n")
                    scoreJugador2 = scoreJugador2 + 1
                    # coloca a que jugador pertenece el par realizado

                    tablero[J2carta1ren][J2carta1col] = "**J2**"
                    tablero[J2carta2ren][J2carta2col] = "**J2**"

                    tableroDesplegar(True)
                    marcadorDesplegar()
                    jugadorActivo = False
                    if (scoreJugador1 + scoreJugador2 >= ordenTablero * ordenTablero / 2):
                        break
                else:
                    print("\n¡El jugador 2 fallo!\n")
                    jugadorActivo = True

                if jugadorActivo == True:
                    break
            # despliega el tablero y el marcador
            tableroDesplegar(True)
            marcadorDesplegar()
    jugador = TCPClientSocket.recv(buffer_size)
    if jugador.decode('utf-8')=="jugador1":
        print("El jugador 1 ha ganado")
        tableroDesplegar(False)
    else:
        if jugador.decode('utf-8') == "jugador2":
            print("El jugador 2 ha ganado")
            tableroDesplegar(False)
        else:
            print("ha sido un empate")
            tableroDesplegar(False)
    print("\nSe acabo el juego\n")
    print("Conexion cerrada")
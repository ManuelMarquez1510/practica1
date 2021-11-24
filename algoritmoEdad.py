from datetime import date

fechaNacimiento =date(1998,8,22)
fechaAsignada =date(2021,9,10)

numDias= fechaAsignada - fechaNacimiento
numDiasTotal = numDias.days
print(f"El numero de dias desde que naci hasta el 21 de agosgo del 2021 es: {numDiasTotal}")

R = numDiasTotal%3
if R == 0:
    print(f" {R} - Toca hacer buscaminas")
elif R == 1:
    print(f" {R} - Toca hacer Gato Dummy")
else:
    print(f" {R} - Toca hacer Memoria")


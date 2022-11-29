import funciones as f
from colored import fg, bg, attr
from colorama import init
import pickle

def menu():
    v=("{0}Salir{1}".format(fg('red'),attr(0)))
    print("\n")
    print("{0}{1}\t\t--- MENU PRINCIPAL ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    opcion=input(f"\n 1- Gestión de partidos y estadios\n 2- Gestión de venta de entradas\n 3- Gestión de asistencia a partidos\n 4- Gestión de restaurantes\n 5- Gestión de venta de restaurantes\n 6- Indicadores de gestión (estadísticas)\n 7- {v}\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")
    while not opcion.isnumeric() or int(opcion) not in range(1,8):
        f.error()
        print("{0}{1}\t\t--- MENU PRINCIPAL ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
        opcion=input(f"\n 1- Gestión de partidos y estadios\n 2- Gestión de venta de entradas\n 3- Gestión de asistencia a partidos\n 4- Gestión de restaurantes\n 5- Gestión de venta de restaurantes\n 6- Indicadores de gestión (estadísticas)\n 7- {v}\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")
        
    return int(opcion)

def main():
    try:
        entradas=pickle.load(open("archivo_entradas.txt","rb"))

    except:
        entradas=dict()

    try:
        clientes=pickle.load(open("archivo_clientela.txt","rb"))

    except:
        clientes=dict()

    print(entradas)
    print(clientes)
    equipos=f.registrar_equipos()
    estadios=f.registrar_estadios()
    partidos=f.registrar_partidos(equipos,estadios)
    restaurantes=f.registrar_restaurantes(estadios)
    print("\n\n")
    print("{0}{1}\t--- BIENVENIDO AL SISTEMA DE 'Qatar 2022' ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    

    while True:
        opcion=menu()

        if opcion==1:
            f.opcion_1(equipos,partidos,estadios)

        elif opcion==2:
            clientes,entradas=f.opcion_2(partidos,clientes,entradas)

        elif opcion==3:
            clientes=f.opcion_3(clientes,entradas)

        elif opcion==4:
            f.opcion_4(estadios,restaurantes)

        elif opcion==5:
            restaurantes=f.opcion_5(clientes,partidos,estadios,restaurantes)

        elif opcion==6:
            f.opcion_6(clientes,entradas,restaurantes)

        else:
            pickle.dump(clientes,open("archivo_clientela.txt","wb"))
            pickle.dump(entradas,open("archivo_entradas.txt","wb"))
            break
main()
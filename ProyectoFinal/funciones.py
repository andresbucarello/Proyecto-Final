import requests
import json
from Equipo import Equipo
from Estadio import Estadio
from Partido import Partido
import random
from Cliente import Cliente
from Boleto import Boleto
from Bebida import Bebida
from Alimento import Alimento
from colored import fg, bg, attr
from colorama import init
import matplotlib.pyplot as plt
from tabulate import tabulate
import itertools as it

def crear_estadio(filas,columnas):
    ''' Crea la matriz del estadio '''

    mapa = []
    for y in range(filas):
        aux = []
        for x in range(columnas):
            aux.append(False)
        mapa.append(aux)
    return mapa

def registrar_equipos():
    ''' Toma la estructura de la api, convierte cada elemento en un objeto y lo agrega a una nueva estructura '''

    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json"
    r=requests.get(url)
    equipos_json=r.json()
    equipos={}

    for equipo in equipos_json:
        current=[]
        for k,v in equipo.items():
            
            if k=="name" or k=="fifa_code" or k=="group" or k=="id":
                
                current.append(v)

        x=Equipo(current[0],current[1],current[2])

        equipos[current[-1]]=x

    return equipos

def registrar_estadios():
    ''' Toma la estructura de la api, convierte cada elemento en un objeto y lo agrega a una nueva estructura '''

    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json"
    r=requests.get(url)
    estadios_json=r.json()
    estadios={}

    for estadio in estadios_json:
        current=[]
        for k,v in estadio.items():
            current.append(v)

        mapa=crear_estadio(current[2][0],current[2][1])
        x=Estadio(current[1],current[2],current[3],current[4],mapa)

        estadios[current[0]]=x

    return estadios

def registrar_partidos(equipos,estadios):
    ''' Toma la estructura de la api, con objetos ya creados anteriormente y ciertos elementos de la api, crea un nuevo objeto y lo agrega a una nueva estructura '''

    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json"
    r=requests.get(url)
    partidos_json=r.json()
    partidos={}

    for partido in partidos_json:
        estadio=0
        id=0
        fecha=0
        current=[]
        cont=0
        for k,v in partido.items():
            cont+=1
            for ke,va in equipos.items():
                if va.nombre==v:
                    current.append(va)
            
            if cont==3:
                fecha=v

            for ke,va in estadios.items():
                if ke==v:
                    estadio=va
                    break

            if cont==5:
                id=v

        x=Partido(current[0],current[1],fecha,estadio)
        partidos[id]=x

    return partidos

def error():
    ''' Imprime error para que el usuario sepa que el dato ingresado no es valido '''

    v=("{0}*** ERROR! * DATO INGRESADO NO VALIDO ***{1}".format(fg('red'),attr(0)))
    print(f"\n\n\t\t{v}\n\n")


######################################## GESTION DE PARTIDOS Y ESTADIOS ########################################

def opcion_1(equipos,partidos,estadios):
    ''' Muestra la opcion "Gestion de partidos y estadios" '''

    v=("{0}Retroceder{1}".format(fg('red'),attr(0)))
    while True:
        
        m=("{0}{1}--- GESTION DE PARTIDOS Y ESTADIOS ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
        opcion=input(f"\n\n\t\t{m}\n\n 1- Buscar todos los partidos de un país\n 2- Buscar todos los partidos que se jugarán en un estadio específico\n 3- Buscar todos los partidos que se jugarán en una fecha determinada\n 4- {v}\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")
        while not opcion.isnumeric() or int(opcion) not in range(1,5):
            error()
            opcion=input(f"\t\t{m}\n\n 1- Buscar todos los partidos de un país\n 2- Buscar todos los partidos que se jugarán en un estadio específico\n 3- Buscar todos los partidos que se jugarán en una fecha determinada\n 4- {v}\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")

        opcion=int(opcion)

        if opcion==1:
            opcion_1_1(equipos,partidos)
        
        elif opcion==2:
            opcion_1_2(estadios,partidos)

        elif opcion==3:
            opcion_1_3(partidos)

        else:
            break

def el_pais_existe(equipos,pais):
    ''' Verifica si el pais ingresado existe '''

    for k,v in equipos.items():
        if v.nombre==pais:
            return True
    
    return False

def opcion_1_1(equipos,partidos):
    ''' Muestra los partidos de un pais "Gestion de partidos y estadios" '''

    print("\n\n\t--- Busqueda de todos los partidos de un país ---\n")
    pais=input("\n - Ingrese el nombre (EN INGLES) del pais: ")
    pais=pais.title()
    existe=el_pais_existe(equipos,pais)
    
    while pais.isnumeric():
        error()
        pais=input(" - Ingrese el nombre (EN INGLES) del pais: ")
        pais=pais.title()
        existe=el_pais_existe(equipos,pais)

    if not existe:
        error()
        v=("{0}*** NO SE ENCONTRO AL PAIS INGRESADO ***{1}".format(fg('red'),attr(0)))
        print(f"\t\t{v}\n\n")
    
    else:
        v=("{0}*** PARTIDOS ENCONTRADOS ***{1}".format(fg('green'),attr(0)))
        print(f"\n\n\t\t\t\t{v}\n")
        for k,v in partidos.items():
            if v.equipo_l.nombre==pais or v.equipo_v.nombre==pais:
                print(f"\n - ID:{k} || L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}")

def el_estadio_existe(estadios,estadio):
    ''' Verifica si el estadio ingresado existe '''

    for k,v in estadios.items():
        if v.nombre==estadio:
            return True
    
    return False

def opcion_1_2(estadios,partidos):
    ''' Muestra la opcion 2 del menu "Gestion de partidos y estadios" '''

    print("\n\n\t--- Busqueda de todos los partidos de un estadio ---\n")
    estadio=input("\n - Ingrese el nombre del estadio: ")
    estadio=estadio.title()
    existe=el_estadio_existe(estadios,estadio)
    
    if not existe:
        error()
        e=("{0}*** NO SE ENCONTRARON PARTIDOS EN EL ESTADIO INGRESADO ***{1}".format(fg('red'),attr(0)))
        print(f"\t{e}\n\n")

    else:
        v=("{0}*** PARTIDOS ENCONTRADOS ***{1}".format(fg('green'),attr(0)))
        print(f"\n\n\t\t\t\t{v}\n")
        for k,v in partidos.items():
            if v.estadio.nombre==estadio:
                print(f"\n - ID:{k} || L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}")

def la_fecha_existe(fecha_part,partidos):
    ''' Verifica si en la fecha ingresada existen partidos '''

    for k,v in partidos.items():
        if fecha_part in v.fecha:
            return True
    
    return False

def opcion_1_3(partidos):
    ''' Muestra la opcion 3 del menu "Gestion de partidos y estadios" '''

    while True:
        print("\n\n\t--- Busqueda de todos los partidos en una fecha determinada ---\n")
        dia=input("\n - Ingrese en numeros el dia: ")
        while not dia.isnumeric() or int(dia) not in range(1,32):
            error()
            dia=input(" - Ingrese en numeros el dia: ")

        mes=input("\n - Ingrese en numeros el mes: ")
        while not mes.isnumeric() or int(mes) not in range(1,13):
            error()
            mes=input(" - Ingrese en numeros el mes: ")

        fecha_part=f"{mes}/{dia}/2022"
        existe=la_fecha_existe(fecha_part,partidos)

        if existe:
            v=("{0}*** PARTIDOS ENCONTRADOS ***{1}".format(fg('green'),attr(0)))
            print(f"\n\n\t\t\t\t{v}\n")
            for k,v in partidos.items():
                if fecha_part in v.fecha:
                    print(f"\n - ID:{k} || L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}")

            break
        
        else:
            error()
            e=("{0}*** NO SE ENCONTRARON PARTIDOS EN LA FECHA ***{1}".format(fg('red'),attr(0)))
            print(f"\t\t{e}\n\n")
            
            break
    

######################################## GESTION DE VENTAS Y ENTRADAS ########################################

def val_nombre():
    ''' Valida y recoleta el nombre '''

    nombre=input("\n - Ingrese el nombre del cliente: ")
    while not nombre.isalpha():
        error()
        nombre=input(" - Ingrese el nombre del cliente: ")
    nombre=nombre.capitalize()

    return nombre

def val_cedula():
    ''' Valida y recolecta la cedula '''

    cedula=input("\n - Ingrese la cedula del cliente: ")
    while not cedula.isnumeric() or len(cedula)<7:
        error()
        cedula=input(" - Ingrese a cedula del cliente: ")

    return cedula

def val_edad():
    ''' Valida y recolecta la edad '''

    edad=input("\n - Ingrese la edad del cliente: ")
    while not edad.isnumeric() or int(edad) not in range(1,110):
        error()
        edad=input(" - Ingrese a edad del cliente: ")
    edad=int(edad)
    return edad

def numero_partido(partidos):
    ''' Recoleta e imprime los partidos '''

    print("\n\n\t\t\t\t========== PARTIDOS ==========\n\n")
    cont=0
    for k,v in partidos.items():
        cont+=1
        print(f" {k}- L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}\n")

    partido=input(" ---> Ingrese el numero correspondiente al partido que desea asistir: ")

    while not partido.isnumeric() or int(partido) not in range(1,cont+1):
        error()
        cont=0
        for k,v in partidos.items():
            cont+=1
            print(f" {k}- L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}\n")

        partido=input(" ---> Ingrese el numero correspondiente al partido que desea asistir: ")
    
    cont=0
    for k,v in partidos.items():
        cont+=1
        if cont==int(partido):
            return v

def tipo_entrada(tipos_entradas):
    ''' Recoleta e imprime los tipos de entradas  '''

    m=("{0}{1}--- TIPOS DE ENTRADA ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    print(f"\n\n\t\t{m}\n\n")
    cont=0
    for k,v in tipos_entradas.items():
        cont+=1
        print(f" {cont}- '{k}'    || Precio: ${v}")
    
    tipo=input("\n - Ingrese el numero correspondiente a la opcion que desea: ")

    while not tipo.isnumeric() or int(tipo) not in range(1,cont+1):
        error()
        m=("{0}{1}--- TIPOS DE ENTRADA ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
        print(f"\n\t\t{m}\n\n")
        cont=0
        for k,v in tipos_entradas.items():
            cont+=1
            print(f" {cont}- '{k}'    || Precio: ${v}")
        
        tipo=input("\n - Ingrese el numero correspondiente a la opcion que desea: ")

    cont=0
    for k,v in tipos_entradas.items():
        cont+=1
        if cont==int(tipo):
            return k,v

def val_existe(clientes,cedula):
    ''' Verifica si el cliente ya existe '''

    for k,v in clientes.items():
        if k.cedula==cedula:
            return True,k
    return False,"no"

def val_partido(entradas,ticket):
    ''' Verifica si ya se han comprado entradas para ese partido '''

    for k,v in entradas.items():
            if ticket.partido==k:
                return True
    return False

def val_ocupado(mapa,fila,columna):
    ''' Determina si el puesto estaba ocupado '''

    f=0
    for x in mapa:
        f+=1
        if f==(int(fila)):
            c=0
            for y in x:
                c+=1
                if c==(int(columna)):
                    if y==False:
                        mapa[f-1][c-1]=True
                        return True
                    else:
                        return False

def imprimir_estadio(partido):
    ''' Imprime el estadio '''

    mapa=partido.estadio.mapa
    nombre=partido.estadio.nombre
    filas=partido.estadio.capacidad[0]
    columnas=partido.estadio.capacidad[1]

    while True:
        m=("{0}{1}--- SELECIONANDO ASIENTO ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
        print(f"\n\n\t\t{m}\n\n")
        fila = input(" - Seleccione la fila:  ")
        while not fila.isnumeric() or int(fila) not in range(1,filas+1):
            error()
            fila = input(" - Seleccione la fila:  ")

        columna = input("\n - Seleccione la columna: ")
        while not columna.isnumeric() or int(columna) not in range(1,columnas+1):
            error()
            columna = input(" - Seleccione la columna: ")

        puede=val_ocupado(mapa,fila,columna)

        if puede:
            v=("{0}*** ASIENTO GUARDADO CON EXITO ***{1}".format(fg('green'),attr(0)))
            print(f"\n\n\t\t\t\t{v}\n\n")
            break

        else:
            error()
            v=("{0}*** EL ASIENTO ESCOGIDO YA ESTA OCUPADO ***{1}".format(fg('red'),attr(0)))
            print(f"\t\t{v}\n\n")
            print("*"*(len(mapa[1])-5)+ f" ESTADIO '{nombre}' "+"*"*(len(mapa[1])-5))
            print("\n")

            nums = "    "
            for i,x in enumerate(mapa[1]):
                if i >8:
                    nums+=str(i+1)+"| "
                else:
                    nums+=str(i+1)+" | "
            print(nums)
            for i,x in enumerate(mapa):
            
                if i>8:
                    auxiliar= str(i+1)
                else:
                    auxiliar= str(i+1)+" "

                for y in x:
                    if y ==True:
                        v=("{0}X{1}".format(fg('red'),attr(0)))
                        auxiliar+=f"| {v} "
                    else:
                        auxiliar+="|   "

                print("   "+"-"*len(mapa[1]*4))
                print(auxiliar)

            continue
    
    print("*"*(len(mapa[1])-5)+ f" ESTADIO '{nombre}' "+"*"*(len(mapa[1])-5))
    print("\n")

    nums = "    "
    for i,x in enumerate(mapa[1]):
        if i >8:
            nums+=str(i+1)+"| "
        else:
            nums+=str(i+1)+" | "
    print(nums)

    for i,x in enumerate(mapa):
        if i>8:
            auxiliar= str(i+1)
        else:
            auxiliar= str(i+1)+" "
        for y in x:
            if y ==True:
                v=("{0}X{1}".format(fg('red'),attr(0)))
                auxiliar+=f"| {v} "
            else:
                auxiliar+="|   "

        print("   "+"-"*len(mapa[1]*4))
        print(auxiliar)

    asiento=f" F: {fila} C: {columna}"
    return asiento,mapa,fila,columna

def dientes(num_str):
    ''' Determina los dientes'''
    
    num_iter = it.permutations(num_str, len(num_str))
    for num_list in num_iter:
        v = ''.join(num_list)
        x, y = v[:int(len(v)/2)], v[int(len(v)/2):]
        if x[-1] == '0' and y[-1] == '0':
            continue
        if int(x) * int(y) == int(num_str):
            return x,y
    return False

def es_vampiro(numero):
    ''' Determina si un numero es vampiro '''
    
    if len(numero) % 2 == 1:
        return False
    d = dientes(numero)
    if not d:
        return False
    return True

def opcion_2(partidos,clientes,entradas):
    ''' Ejecuta la opcion "Gestión de venta de entradas" '''

    m=("{0}{1}--- GESTION DE VENTAS DE ENTRADAS ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    v=("{0}Retroceder{1}".format(fg('red'),attr(0)))
    tipos_entradas={"General":50,"VIP":120}
    opcion=input(f"\n\n\t\t{m}\n\n 1- Registrar cliente\n 2- {v}\n\n ---> Ingrese el numero correspondiente al opcion que desea: ")
    while not opcion.isnumeric() or int(opcion) not in range(1,3):
        error()
        opcion=input(f"\t\t{m}\n\n 1- Registrar cliente\n 2- {v}\n\n ---> Ingrese el numero correspondiente al opcion que desea: ")

    if opcion=="1":
        m=("{0}{1}--- REGISTRANDO CLIENTE ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
        print(f"\n\n\t\t{m}\n")
        cedula=val_cedula()
        existe,c=val_existe(clientes,cedula)

        if not existe:
            nombre=val_nombre()
            edad=val_edad()

        else:
            comprador=c
            nombre=c.nombre

        partido=numero_partido(partidos)
        tipo,costo=tipo_entrada(tipos_entradas)
        asiento,mapa,fila,columna=imprimir_estadio(partido)
        descuento=0
        vampiro=es_vampiro(cedula)
        if vampiro:
            descuento+=0.50

        subttl=costo-costo*descuento
        iva=subttl*0.16
        total=subttl+iva
        print(f'''
        ======================================= FACTURA ===================================

            - Nombre: {nombre} || - Cedula: {cedula}

            * Informacion de la compra *

            - Partido: 
                    L: '{partido.equipo_l.nombre}' vs V: '{partido.equipo_v.nombre}' 
                    Estadio: '{partido.estadio.nombre}' ||| Fecha: {partido.fecha}
            
            - Tipo de entrada: '{tipo}'  --- Costo: ${costo}
            - Asiento: {asiento}

                                        Descuento: ${descuento}
                                        SUBTTL: ${subttl}
                                        IVA: ${iva} (16%)

                                        TOTAL: ${total}
        ====================================================================================
        ''')

        continuar=input("\n - Desea proceder con el pago? (S: SI ó N: NO): ")
        continuar=continuar.capitalize()
        while not continuar.isalpha() or continuar!="N" and continuar!="S":
            error()
            continuar=input(" - Desea proceder con el pago? (S: SI ó N: NO): ")
            continuar=continuar.capitalize()

        if continuar=="S":
            
            letras="abcdefghijklmnopqrstuvwxyz"
            numeros="0123456789"
            simbolos="!@#$%&*_-:;Æ?€€°·”/"
            codigo=""

            cont=0
            while cont<5:
                cont+=1
                x=random.randint(0, len(letras)-1)
                y=random.randint(0, len(numeros)-1)
                z=random.randint(0, len(simbolos)-1)
                letra=letras[x]
                numero=numeros[y]
                simbolo=simbolos[z]
                x=f"{letra}{simbolo}{numero}"
                codigo+=x
            v=("{0}PAGO REGISTRADO CON EXITO{1}".format(fg('green'),attr(0)))
            print(f"\n\n\t *** {v} ***\n\n")
            asistencia=False
            ticket=Boleto(partido,tipo,total,codigo,asistencia)
            
            partido_regis=val_partido(entradas,ticket)
            if not partido_regis:
                entradas[ticket.partido]=[]
                entradas[ticket.partido].append(ticket)

            elif partido_regis:
                entradas[ticket.partido].append(ticket)


            if not existe:
                comprador=Cliente(nombre,cedula,edad)
                clientes[comprador]=[]

            clientes[comprador].append(ticket)
            
            v=("{0}Su codigo de entrada es (RECUERDELO):{1}".format(fg('green'),attr(0)))
            print(f" * {v} {codigo} *")
        
        else:
            mapa[int(fila)-1][int(columna)-1]=False

        return clientes,entradas

    else:
        return clientes,entradas

######################################## GESTION DE ASISTENCIA Y PARTIDOS ########################################

def val_ticket(clientes,codigo):
    ''' Valida que el codigo ingresado pertenezca a una entrada '''

    for cliente,tickets in clientes.items():
        for ticket in tickets:
            if ticket.codigo==codigo:
                return True
    return False

def val_asistencia(clientes,codigo):
    ''' Verifica si ya el ticket fue utilizado '''

    for cliente,tickets in clientes.items():
            for ticket in tickets:
                if ticket.codigo==codigo and ticket.asistencia==True:
                    return True

def cambiar_asistencia(clientes,codigo,entradas):
    ''' Cambia el estado de asistencia de una entrada '''

    for cliente,tickets in clientes.items():
            for ticket in tickets:
                if ticket.codigo==codigo:
                    ticket.asistencia=True
    
    for k,v in entradas.items():
        for x in v:
            if ticket.codigo==codigo:
                ticket.asistencia=True
                return

def opcion_3(clientes,entradas):
    ''' Ejecuta la opcion "Gestión de asistencia y partidos" '''

    v=("{0}Retroceder{1}".format(fg('red'),attr(0)))
    m=("{0}{1}--- MENU DE ASISTENCIA Y PARTIDOS ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    while True:
        opcion=input(f"\n\n\t\t{m}\n\n 1- Ingresar al estadio \n 2- {v}\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")
        while not opcion.isnumeric() or int(opcion )not in range(1,3):
            error()
            opcion=input(f"\t\t{m}\n\n 1- Ingresar al estadio \n 2- {v}\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")

        if opcion=="1":
            m=("{0}{1}--- GESTION DE ASISTENCIA Y PARTIDOS ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
            print(f"\n\n\t\t{m}\n\n")
            codigo=input(" - Ingrese el codigo de verificacion de su entrada: ")
            while len(codigo)!=15:
                error()
                codigo=input(" - Ingrese el codigo de verificacion de su entrada: ")

            existe=val_ticket(clientes,codigo)
            asistencia=val_asistencia(clientes,codigo)

            if existe and not asistencia:
                cambiar_asistencia(clientes,codigo,entradas)
                v=("{0}*** TICKET INGRESADO CON EXITO ***{1}".format(fg('green'),attr(0)))
                print(f"\n\n\t\t\t\t{v}\n")
                return clientes

            else:
                error()
                e=("{0}*** EL TICKET YA INGRESÓ O CODIGO NO VALIDO ***{1}".format(fg('red'),attr(0)))
                print(f"\t\t{e}\n\n")
                

        else:
            return clientes


######################################## GESTION DE RESTAURANTES ########################################

def registrar_restaurantes(estadios):
    ''' A partir del objeto ESTADIO creado anteriormente, recorre todos los restaurantes, crea los objetos de sus productos 
    correspondientes y genera un diccionario con key: NOMBRE DEL RESTAURANTE y value: Lista de los objetos productos correspondientes'''

    restaurantes={}
    for k,v in estadios.items():
        for restaurant in v.restaurantes:
            productos=[]
            for ke,va in restaurant.items():

                if type(va)==str:
                    nombre=va
                    restaurantes[nombre]=[]

                elif type(va)==list:
                    for producto in va:
                        current=[]
                        for key,val in producto.items():
                            current.append(val)

                        precio=current[2]
                        iva=precio*0.16
                        precio=precio+iva
                       
                        if current[3]=="beverages":
                            x=Bebida(current[0],precio,current[3],current[4],current[1])
                            restaurantes[nombre].append(x)

                        else:
                            x=Alimento(current[0],precio,current[3],current[4],current[1])
                            restaurantes[nombre].append(x)

    return restaurantes

def val_nombre_prod():
    ''' Valida el nombre del producto ingresado'''

    nombre=input("\n - Ingrese el nombre del producto: ")
    while nombre.isnumeric():
        error()
        nombre=input("\n - Ingrese el nombre del producto: ")
    
    return nombre.title()

def existe_prod(nombre,restaurantes):
    ''' Valida que el producto ingresado exista '''

    for k,v in restaurantes.items():
        for x in v:
            if x.nombre==nombre:
                return True

    return False

def busqueda_1(nombre,restaurantes):
    ''' Muestra los productos por el nombre ingresado '''
    
    v=("{0}--- ARTICULOS ENCONTRADOS ---{1}".format(fg('green'),attr(0)))
    print(f"\n\n\n\t\t\t{v}\n")
    for k,v in restaurantes.items():
        for x in v:
            if x.nombre==nombre:
                if type(x)==Alimento:
                    print(f"\n - Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Estado: {x.estado}")

                else:
                    print(f" \n- Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Alcohol: {x.alcoholica}")
                return

def busqueda_2(restaurantes):
    ''' Muestra los productos del tipo ingresado '''

    tipos=[]
    for k,v in restaurantes.items():
        for x in v:
            if x.tipo not in tipos:
                tipos.append(x.tipo)
    
    cont=0
    m=("{0}{1}--- BUSQUEDA POR TIPO ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    print(f"\n\n\t\t{m}\n\n")
    for x in tipos:
        cont+=1
        print(f" {cont}- '{x}' ")
    tipo=input("\n - Ingrese el numero correspondiente al tipo de que desea buscar: ")

    while not tipo.isnumeric() or int(tipo) not in range(1,cont+1):
        error()
        print(f"\t\t{m}\n\n")
        cont=0
        for x in tipos:
            cont+=1
            print(f" {cont}- '{x}' ")
        tipo=input("\n - Ingrese el numero correspondiente al tipo de que desea buscar: ")

    tipo=int(tipo)
    cont=0
    for x in tipos:
        cont+=1
        if cont==tipo:
            tipo=x
            break

    v=("{0}--- ARTICULOS ENCONTRADOS ---{1}".format(fg('green'),attr(0)))
    print(f"\n\n\n\t\t\t{v}\n")
    impresos=[]
    for k,v in restaurantes.items():
        for x in v:
            if x.tipo==tipo:
                if x.nombre not in impresos:
                    impresos.append(x.nombre)
                    if type(x)==Alimento:
                        print(f"\n - Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Estado: {x.estado}")

                    else:
                        print(f"\n - Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Alcohol: {x.alcoholica}")

    return 

def val_numero():
    ''' Valida que el numero ingresado por el usuario sea entero'''

    numero=input("\n - Ingrese en numeros enteros el monto: ")
    while not numero.isnumeric() or int(numero)<=0:
        error()
        numero=input(" - Ingrese en numeros enteros el monto: ")
    return int(numero)

def busqueda_3(restaurantes):
    ''' Muestra los productos en el rango ingresado '''

    m=("{0}{1}--- BUSQUEDA POR RANGO ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    print(f"\n\n\t\t{m}\n\n")
    print(" * Precio minino: ")
    p_min=val_numero()

    print("\n * Precio maximo: ")
    p_max=val_numero()
    
    impresos=[]
    for k,v in restaurantes.items():
        for x in v:
            if x.precio>=p_min and x.precio<=p_max:
                if x.nombre not in impresos:
                    impresos.append(x.nombre)
                    if len(impresos)==1:
                        v=("{0}--- ARTICULOS ENCONTRADOS ---{1}".format(fg('green'),attr(0)))
                        print(f"\n\n\n\t\t\t{v}\n")
                    if type(x)==Alimento:
                        print(f"\n - Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Estado: {x.estado}")

                    else:
                        print(f"\n - Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Alcohol: {x.alcoholica}")

    if len(impresos)==0:
        error()
        e=("{0}*** NO HAY PRODUCTOS EN ESE RANGO ***{1}".format(fg('red'),attr(0)))
        print(f"\t\t{e}\n\n")

def opcion_4(estadios,restaurantes):
    ''' Ejecuta la opcion "Gestión de Restaurantes" '''

    v=("{0}Retroceder{1}".format(fg('red'),attr(0)))
    
    while True:
        m=("{0}{1}--- BUSQUEDA DE PRODUCTOS ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
        busqueda=input(f"\n\n\t\t{m}\n\n 1- Busqueda por nombre\n 2- Busqueda por tipo\n 3- Busqueda por rango de precio\n 4- {v}\n\n ---> Ingrese el numero correspondiente al tipo de busqueda que desea realizar: ")
        while not busqueda.isnumeric() or int(busqueda) not in range(1,5):
            error()
            busqueda=input(f"\t\t{m}\n\n 1- Busqueda por nombre\n 2- Busqueda por tipo\n 3- Busqueda por rango de precio\n 4- {v}\n\n ---> Ingrese el numero correspondiente al tipo de busqueda que desea realizar: ")

        if busqueda=="1":
            m=("{0}{1}--- BUSQUEDA POR NOMBRE ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
            print(f"\n\n\t\t{m}\n\n")
            nombre=val_nombre_prod()
            existe=existe_prod(nombre,restaurantes)
            
            if not existe:
                error()
                e=("{0}*** EL PRODUCTO INGRESADO NO EXISTE O NO ES VALIDO ***{1}".format(fg('red'),attr(0)))
                print(f"\t{e}\n\n")
            
            else:
                busqueda_1(nombre,restaurantes)

        elif busqueda=="2":
            busqueda_2(restaurantes)

        elif busqueda=="3":
            busqueda_3(restaurantes)

        else:
            break
     

######################################## GESTION DE VENTAS DE RESTAURANTE ########################################

def sumar_cant(comercios_del_estadio,n_restaurant,restaurantes,compra):
    ''' Suma la cantidad de los productos seleccionados por el cliente'''

    for pedido in compra:
        for comercio in comercios_del_estadio:
            if comercio==n_restaurant:
                for nombre,inventario in restaurantes.items():
                    if nombre==comercio:
                        for objeto in inventario:
                            if pedido[0].nombre==objeto.nombre:
                                objeto.cantidad+=pedido[1]
    return restaurantes

def es_numero_perfecto(cedula):
    ''' Determina si la cedula es numero perfecto'''

    cedula=int(cedula)

    divisores=[]
    div=0
    while div<cedula-1:
        div+=1
        if cedula%div==0:
            divisores.append(div)
        

    if sum(divisores)==cedula:
        return True

    else:
        return False

def desea_comprar_mas():
    ''' Pregunta al usuario si desea comprar algun otro producto de ese restaurante '''

    continuar=input("\n - ¿Desea comprar algo mas? (S: SI ó N: NO): ")
    continuar=continuar.capitalize()
    while not continuar.isalpha() or continuar!="N" and continuar!="S":
        error()
        continuar=input(" - ¿Desea comprar algo mas? (S: SI ó N: NO): ")
        continuar=continuar.capitalize()

    if continuar=="S":
        return True

    else:
        return False

def rescatar_producto_elegido(comercios_del_estadio,restaurantes,opcion,producto,cliente,cantidad):
    ''' Rescata el producto elegido por el usuario '''

    if cliente.edad<18:
        for x in comercios_del_estadio:
            if x==opcion:
                for k,v in restaurantes.items():
                    cont=0
                    if k==x:
                        for y in v: 
                            cont+=1
                            if type(y)==Bebida:
                                if y.alcoholica=="alcoholic":
                                    cont-=1

                            if cont==int(producto):
                                if y.cantidad<cantidad:
                                    return y,False,restaurantes
                                else:
                                    y.cantidad-=cantidad
                                    return y,True,restaurantes
                                

    else:
        for x in comercios_del_estadio:
            if x==opcion:
                for k,v in restaurantes.items():
                    cont=0
                    if k==x:
                        for y in v:
                            cont+=1
                            if cont==int(producto):
                                if y.cantidad<cantidad:
                                    return y,False,restaurantes
                                
                                else:
                                    y.cantidad-=cantidad
                                    return y,True,restaurantes

def val_cant():
    ''' Valida la cantidad del producto '''

    cant=input(" \n - Ingrese en numeros la cantidad que desea: ")
    while not cant.isnumeric() or int(cant)<=0:
        error()
        cant=input(" - Ingrese en numeros la cantidad que desea: ")

    return int(cant)

def imprimir_productos(comercios_del_estadio,restaurantes,n_restaurant,cliente):
    ''' Imprime los productos del restaurante seleccionado '''

    print(f'\n\n\t--- RESTAURANT "{n_restaurant}" ---\n\n')
    for x in comercios_del_estadio:
            for k,v in restaurantes.items():
                cont=0
                if x==k and x==n_restaurant:
                    for x in v:
                        if cliente.edad<18:
                            if x.cantidad>0:
                                if type(x)==Bebida:
                                    if x.alcoholica=="non-alcoholic":
                                        cont+=1
                                        print(f" {cont}- Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Alcohol: {x.alcoholica} || Cantidad disponible: {x.cantidad}\n")

                                else:
                                    cont+=1
                                    print(f" {cont}- Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Estado: {x.estado} || Cantidad disponible: {x.cantidad}\n")
                                

                        else:
                            if x.cantidad>0:
                                if type(x)==Bebida:
                                    cont+=1
                                    print(f" {cont}- Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Alcohol: {x.alcoholica} || Cantidad disponible: {x.cantidad}\n")

                                else:
                                    cont+=1
                                    print(f" {cont}- Nombre: {x.nombre} || Precio: ${x.precio} || Tipo: {x.tipo} || Estado: {x.estado} || Cantidad disponible: {x.cantidad}\n")
                    return cont 

def opcion_restaurante(comercios_del_estadio):
    ''' Rescata el restaurante que el usuaria desea ver '''

    m=("{0}{1}--- RESTAURANTEs ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    print(f"\n\n\t\t{m}\n\n")
    cont=0
    for x in comercios_del_estadio:
        cont+=1
        print(f" {cont}- '{x}'\n")

    opcion=input("\n - Ingrese el numero correspondiente al restaurante que desea ver: ")

    while not opcion.isnumeric() or int(opcion) not in range(1,cont+1):
        error()
        print(f"\n\n\t\t{m}\n\n")
        cont=0
        for x in comercios_del_estadio:
            cont+=1
            print(f" {cont}- '{x}'\n")

        opcion=input("\n - Ingrese el numero correspondiente al restaurante que desea ver: ")

    cont=0
    for x in comercios_del_estadio:
        cont+=1
        if cont==int(opcion):
            return x

def comercios_estadio(partidos,estadio):
    ''' Rescata los restaurantes del estadio '''

    comercios=[]
    for k,v in partidos.items():
        if v.estadio.nombre==estadio:
            for x in v.estadio.restaurantes:
                for ke,va in x.items():
                    if ke=="name":
                        if va not in comercios:
                            comercios.append(va)
    return comercios

def opcion_5_1():
    ''' Sub-menu de "GESTION DE VENTAS DE RESTAURANTE" '''

    m=("{0}{1}--- MENU DE RESTAURANTE ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
    v=("{0}Retroceder{1}".format(fg('red'),attr(0)))
    opcion=input(f"\n\n\t\t{m}\n\n 1- Ingresar a un restaurante\n 2- {v}\n\n ---> Ingresar el numero correspondiente a la opcion que desea: ")
    while not opcion.isnumeric() or int(opcion) not in range(1,3):
        error()
        opcion=input(f"\t\t{m}\n\n 1- Ingresar a un restaurante\n 2- {v}\n\n ---> Ingresar el numero correspondiente a la opcion que desea: ")

    return int(opcion)

def val_entrada(clientes,cedula):
    ''' Valida que la cedula ingresada pertenezca a una entrada VIP '''
    
    ticke=0
    clien=0
    for cliente,tickets in clientes.items():
        if cliente.cedula==cedula:
            for ticket in tickets:
                if ticket.asistencia==True and ticket.tipo_entrada=="VIP":
                    return True,ticket,cliente

    return False,ticke,clien

def opcion_5(clientes,partidos,estadios,restaurantes):
    ''' Ejecuta la opcion "Gestión de ventas de restaurante '''

    while True:
        opcion=opcion_5_1()
        
        if opcion==1:
            m=("{0}{1}--- INGRESANDO AL RESTAURANTE ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
            print(f"\n\n\t\t{m}\n\n")
            cedula=input(" - Ingrese la cedula asociada a su entrada: ")
            valido,ticket,cliente=val_entrada(clientes,cedula)

            if valido:
                estadio=ticket.partido.estadio.nombre
                comercios_del_estadio=comercios_estadio(partidos,estadio)

                while True:
                    n_restaurant=opcion_restaurante(comercios_del_estadio)
                    compra=[]
                    while True:
                        pedido=[]
                        limite=imprimir_productos(comercios_del_estadio,restaurantes,n_restaurant,cliente)
                        n_producto=input("\n - Ingrese el numero correspondiente al producto que desea: ")
                        while not n_producto.isnumeric() or int(n_producto) not in range(1,limite+1):
                            error()
                            limite=imprimir_productos(comercios_del_estadio,restaurantes,n_restaurant,cliente)
                            n_producto=input("\n - Ingrese el numero correspondiente al producto que desea: ")
                        
                        cant=val_cant()
                        producto,puede,restaurantes=rescatar_producto_elegido(comercios_del_estadio,restaurantes,n_restaurant,n_producto,cliente,cant)

                        while not puede:
                            v=("{0}*** CANTIDAD NO PERMITIDA ***{1}".format(fg('red'),attr(0)))
                            print(f"\n\n\t\t{v}\n\n")
                            cant=val_cant()
                            producto,puede,restaurantes=rescatar_producto_elegido(comercios_del_estadio,restaurantes,n_restaurant,n_producto,cliente,cant)

                        subttl=producto.precio*cant
                        pedido.append(producto)
                        pedido.append(cant)
                        pedido.append(subttl)
                        compra.append(pedido)

                        continuar=desea_comprar_mas()
                        if continuar:
                            continue

                        else:
                            break
                    
                    descuento=0
                    cont=0
                    subttl=0
                    print('''
            ======================================= FACTURA ===================================''')
                    for x in compra:
                        subttl+=x[-1]
                        cont+=1
                        print(f'''
            - Pedido {cont}:

                        * {x[0].nombre} || Precio: ${x[0].precio}
                                        Cant.: {x[1]} ---> Subttl: ${x[-1]}''')

                    perfecto=es_numero_perfecto(cliente.cedula)
                    if perfecto:
                        descuento+=0.15

                    descuento=subttl*descuento
                    total=subttl-descuento
                    print(f'''
                                        SUBTTL: ${subttl}
                                        Descuento: ${descuento}

                                        TOTAL: ${total}
            ====================================================================================''')
                    continuar=input("\n - Desea proceder con el pago? (S: SI ó N: NO): ")
                    continuar=continuar.capitalize()
                    while not continuar.isalpha() or continuar!="N" and continuar!="S":
                        error()
                        continuar=input(" - Desea proceder con el pago? (S: SI ó N: NO): ")
                        continuar=continuar.capitalize()

                    if continuar=="S":
                        ticket.total+=total
                        break

                    else:
                        restaurantes=sumar_cant(comercios_del_estadio,n_restaurant,restaurantes,compra)
                        break

                    

            else:
                v=("{0}*** TU ENTRADA NO HA SIDO REGISTRADA O NO ES VALIDA PARA ACCEDER A LOS RESTAURANTES ***{1}".format(fg('red'),attr(0)))
                print(f"\n\n\t{v}")

        else:
            break
    
    return restaurantes


######################################## INDICADORES DE GESTION  ########################################

def estadistica_1(clientes):
    """ Calcula el promedio de gasto de un cliente VIP en un partido (ticket + restaurante) """

    total=0
    cant=0
    for cliente,tickets in clientes.items():
        cant+=1
        for ticket in tickets:
            if ticket.total>139.2 and ticket.tipo_entrada=="VIP":
                total+=ticket.total

    if cant==0:
        v=("{0}*** NO SE ENCONTRARON GASTOS DE CLIENTES VIP ***{1}".format(fg('red'),attr(0)))
        print(f"\n\n\t\t{v}")

    else:
        if total/cant==0:
            v=("{0}*** NO SE ENCONTRARON GASTOS DE CLIENTES VIP ***{1}".format(fg('red'),attr(0)))
            print(f"\n\n\t\t{v}")
        else:
            v=("{0}--- PROMEDIO DE GASTO CLIENTE VIP ---{1}".format(fg('green'),attr(0)))
            print(f"\n\n\t\t\t{v}\n\n")
            print(f"\t*** El promedio de gasto de un cliente VIP en un partido es: {total/cant} ***\n")

def estadistica_2(entradas):
    ''' Crea la tabla con la estadistica de las entradas vendidas '''

    quan=[]
    cont=0
    for k,v in entradas.items():
        cont+=1
        quan.append(len(v))
        
    if cont==0:
        v=("{0}*** NO SE HAN COMPRADO ENTRADAS ***{1}".format(fg('red'),attr(0)))
        print(f"\n\n\t\t{v}")

    else:
        asis=[]
        for k,v in entradas.items():
            cont=0
            for x in v:
                if x.asistencia==True:
                    cont+=1
            asis.append(cont)

        asis.sort()
        tamano_p=[]
        tamano_e=[]
        datos=[]
        impresos=[]
        for y in asis:
            for k,v in entradas.items():
                cont=0
                cant=0
                for x in v:
                    cant+=1
                    if x.asistencia==True:
                        cont+=1

                if cont==y:
                    partido=f"|    '{k.equipo_l.nombre}' vs '{k.equipo_v.nombre}'    |"
                    if partido not in impresos:
                        impresos.append(partido)
                        dato=[]
                        

                        estadio=f"|    {k.estadio.nombre}    |"
                        relacion=f"|    {cont}/{cant}    |"
                        asistentes=f"|    {cont}    |"
                        cantidad=f"|    {cant}    |"
                        tamano_p.append(len(partido))
                        tamano_e.append(len(estadio))
                        
                        dato.append(partido)
                        dato.append(estadio)
                        dato.append(asistentes)
                        dato.append(cantidad)
                        dato.append(relacion)
                        datos.append(dato)
    
        if len(impresos)==0:
            print("HOLA")
        
        else:
            tamano_p.sort()
            p_d=tamano_p[-1]/2
            p_d=int(p_d)
            p_d-=2
            tamano_e.sort()
            p_e=tamano_e[-1]/2
            p_e=int(p_e)
            p_e-=2
            v=("{0}--- ASISTENCIA A LOS PARTIDOS ---{1}".format(fg('green'),attr(0)))
            print(f"\n\n\t\t\t{v}\n\n")
            print(" "*(p_d)+f"PARTIDO"+" "*(p_d)+" "*(p_e)+f"ESTADIO"+" "*(p_e)+"ASISTENCIA    VENDIDAS      RELACION")
            #print("\t  PARTIDO\t\t\t\tESTADIO\t\t\tASISTENCIA    VENDIDAS      RELACION")
            print(tabulate(datos))

def estadistica_3(entradas):
    '''Imprime el partido con mayor asistencia '''

    asistencia=[]

    for k,v in entradas.items():
        cont=0
        for x in v:
            if x.asistencia==True:
                cont+=1
                asistencia.append(cont)

    if len(asistencia)==0:
        p=("{0}*** NO SE HAN REGISTRADO ASISTENCIA A NINGUN PARTIDO ***{1}".format(fg('red'),attr(0)))
        print(f"\n\n\t\t{p}")
    
    else:
        asistencia.sort()
        for v,k in entradas.items():
            cont=0
            for x in k:
                if x.asistencia==True:
                    cont+=1

            if cont==asistencia[-1]:
                p=("{0}--- MAYOR ASISTENCIA ---{1}".format(fg('green'),attr(0)))
                print(f"\n\n\t\t\t{p}\n\n")
                
                print(f" ---> 'L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}' ")
                break

def estadistica_4(entradas):
    '''Imprime el partido con mayor venta '''

    asistencia=[]
    for k,v in entradas.items():
        asistencia.append(len(v))

    if len(asistencia)==0:
        p=("{0}*** NO SE HAN COMPRADO ENTRADAS ***{1}".format(fg('red'),attr(0)))
        print(f"\n\n\t\t{p}")
    
    else:
        asistencia.sort()
        for v,k in entradas.items():
            if len(k)==asistencia[-1]:
                p=("{0}--- MAYOR VENTA ---{1}".format(fg('green'),attr(0)))
                print(f"\n\n\t\t\t{p}\n\n")
                print(f"---> 'L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}' ")
                break

def estadistica_5(restaurantes):
    ''' Top 3 productos más vendidos en el restaurante. '''

    cantidades=[]
    for k,v in restaurantes.items():
        for y in v:
            cantidades.append(y.cantidad)
    
    
    cantidades.sort()


    if cantidades[0]==25:
        if cantidades[1]==25:
            if cantidades[2]==25:
                v=("{0}*** NO SE HAN VENDIDO PRODUCTOS ***{1}".format(fg('red'),attr(0)))
                print(f"\n\n\t\t{v}")

    else:
        v=("{0}--- TOP PRODUCTOS VENDIDOS ---{1}".format(fg('green'),attr(0)))
        print(f"\n\n\t\t{v}\n\n")
        impresos=[]
        for k,v in restaurantes.items():
            for y in v:
                if y.cantidad==25:
                    continue

                else:

                    if y.nombre not in impresos:
                        if cantidades[0]==y.cantidad:
                            impresos.append(y.nombre)
                            print(f" - Nombre: {y.nombre} || Cantidad vendida: {25-y.cantidad}\n")

                        elif cantidades[1]==y.cantidad:
                            impresos.append(y.nombre)
                            print(f" - Nombre: {y.nombre} || Cantidad vendida: {25-y.cantidad}\n")

                        elif cantidades[2]==y.cantidad:
                            impresos.append(y.nombre)
                            print(f" - Nombre: {y.nombre} || Cantidad vendida: {25-y.cantidad}\n")

def estadistica_6(clientes):
    ''' Top 3 de clientes (clientes que más compraron boletos) '''

    cantidad=[]
    for k,v in clientes.items():
        cantidad.append(len(v))

    if len(cantidad)==0:
        v=("{0}*** NO SE HAN COMPRADO ENTRADAS ***{1}".format(fg('red'),attr(0)))
        print(f"\n\n\t\t{v}")

    else:
        y=[]
        x=[]
        cantidad.sort()
        v=("{0}--- TOP CLIENTES CON MAYOR CANTIDAD DE ENTRADAS ---{1}".format(fg('green'),attr(0)))
        print(f"\n\n\n\t\t{v}\n")
        for k,v in clientes.items():
            print()
            if cantidad[-1]==len(v) or cantidad[-2]==len(v) or cantidad[-3]==len(v):
                x.append(k.nombre)
                y.append(len(v))

        plt.bar(x,y)
        plt.ylabel("CANTIDAD DE ENTRADAS")
        plt.xlabel("CLIENTES")
        plt.show()

def opcion_6(clientes,entradas,restaurantes):
    ''' Ejecuta la opcion "Indicadores de gestión" '''
    
    while True:
        m=("{0}{1}--- MENU DE INDICADORES DE GESTION ---{2}".format(fg('dark_red_2'), bg('white'),attr(0)))
        v=("{0}Retroceder{1}".format(fg('red'),attr(0)))
        opcion=input(f"\n\n\t\t{m}\n\n 1- Promedio de gasto de un cliente VIP en un partido (ticket + restaurante)\n 2- Mostrar tabla con la asistencia a los partidos\n 3- Partido con mayor asistencia\n 4- Partido con mayor boletos vendidos\n 5- Top 3 productos más vendidos en el restaurante\n 6- Top 3 de clientes (clientes que más compraron boletos) \n 7- {v} \n\n ---> Ingrese el numero correpondiente al opcion que desea: ")
        while not opcion.isnumeric() or int(opcion) not in range(1,8):
            error()
            opcion=input(f"\n\n\t\t{m}\n\n 1- Promedio de gasto de un cliente VIP en un partido (ticket + restaurante)\n 2- Mostrar tabla con la asistencia a los partidos\n 3- Partido con mayor asistencia\n 4- Partido con mayor boletos vendidos\n 5- Top 3 productos más vendidos en el restaurante\n 6- Top 3 de clientes (clientes que más compraron boletos)\n 7- {v} \n\n ---> Ingrese el numero correpondiente al opcion que desea: ")

        if opcion=="1":
            estadistica_1(clientes)

        elif opcion=="2":
            estadistica_2(entradas)
            
        elif opcion=="3":
            estadistica_3(entradas)

        elif opcion=="4":
            estadistica_4(entradas)

        elif opcion=="5":
            estadistica_5(restaurantes)

        elif opcion=="6":
            estadistica_6(clientes)

        else:
            break

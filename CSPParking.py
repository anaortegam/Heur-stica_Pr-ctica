from constraint import *
import random
import sys


class Ambulancia():
    def __init__(self, id, tipo, congelador):
        self.id = id
        self.tipo = tipo
        self.congelador = congelador

    # Este método permite comparar las instancias de Ambulancia usando el operador <
    def __lt__(self, other):
        return self.id < other.id
def main():
    if len(sys.argv) != 2:
        print("Uso: python CSPParking.py <path parking>")
        sys.exit(1)

    path_parking = sys.argv[1]
    nombre_fichero_salida = f"{path_parking}.csv"
    dimensiones, plazas_electricas, vehiculos,  dominio_electricas, dominio_parking = leer_fichero(sys.argv[1])
    dimensiones = list(dimensiones)  # Convierte 'dimensiones' a una lista
    print(f'Dimensiones: {dimensiones}')
    print(f'Plazas: {dominio_parking}')
    print(f'Plazas con conexión eléctrica: {dominio_electricas}')
    problem = crear_restricciones(dimensiones, plazas_electricas, vehiculos,  dominio_electricas, dominio_parking)

    soluciones = problem.getSolutions()
    generar_fichero_salida(soluciones, path_parking)



def crear_restricciones(dimensiones, plazas_electricas, vehiculos,  dominio_electricas, dominio_parking):
    problem = Problem()

    #Restricción 3
    for vehiculo in vehiculos:
        if vehiculo.congelador == "C":
            problem.addVariable(vehiculo, dominio_electricas)
    
        else:
            problem.addVariable(vehiculo, dominio_parking)

    #Restricción 1/2
    problem.addConstraint(AllDifferentConstraint(), vehiculos)

    # Restricción 4
    for vehiculo1 in vehiculos:
        if vehiculo1.tipo == "TSU":
            for vehiculo2 in vehiculos:
                if vehiculo1 != vehiculo2 and vehiculo2.tipo == "TNU":
                    problem.addConstraint(lambda x, y: int(x.split(',')[1]) >= int(y.split(',')[1]) if x.split(',')[0] == y.split(',')[0] else True, (vehiculo1, vehiculo2))
    # Restriccion 5
    for vehiculo1 in vehiculos:
        for vehiculo2 in vehiculos:
            if vehiculo1 != vehiculo2:
                for vehiculo3 in vehiculos:
                    if vehiculo1 != vehiculo3 and vehiculo2 != vehiculo3:
                        problem.addConstraint(lambda v1, v2, v3: arriba_abajo(v1, v2, v3, dimensiones),
                                              (vehiculo1, vehiculo2, vehiculo3))


    return problem

def arriba_abajo(v1, v2, v3, dimensiones):
    if v1.split(',')[0] == "1" and int(v3.split(',')[0]) == int(v1.split(',')[0])+1 and v3.split(',')[1] == v1.split(',')[1]:
        return False
    if v1.split(',')[0] == str(dimensiones[0]) and int(v2.split(',')[0]) == int(v1.split(',')[0])-1 and \
       v2.split(',')[1] == v1.split(',')[1]:
        return False
    if int(v2.split(',')[0]) == int(v1.split(',')[0])-1 and v2.split(',')[1] == v1.split(',')[1] and \
       int(v3.split(',')[0]) == int(v1.split(',')[0])+1 and v3.split(',')[1] == v1.split(',')[1]:
        return False
    return True

def leer_fichero(nombre_fichero):
    vehiculos = []
    with open(nombre_fichero, 'r') as f:
        lineas = f.readlines()

    dimensiones = map(int, lineas[0].strip().split('x'))

    filas, columnas = map(int, lineas[0].strip().split('x'))

    dominio_parking = [f'{fila},{columna}' for fila in range(1, filas + 1) for columna in range(1, columnas + 1)]

    # Procesar la línea de las plazas eléctricas
    plazas_electricas = []
    plazas_electricas_linea = lineas[1][4:].strip().split(')(')
    for plaza in plazas_electricas_linea:
        plaza = plaza.replace('(', '').replace(')', '')
        plazas_electricas.append(tuple(map(int, plaza.split(','))))
    dominio_electricas = [','.join(map(str, plaza)) for plaza in plazas_electricas]


    for i in range(2, len(lineas)):
        id, tipo, congelador = lineas[i].strip().split('-')
        vehiculos.append(Ambulancia(id, tipo, congelador))

    return dimensiones, plazas_electricas, vehiculos, dominio_electricas, dominio_parking

def generar_fichero_salida(soluciones, nombre_fichero_entrada):
    nombre_fichero_salida = f'{nombre_fichero_entrada}.csv'
    with open(nombre_fichero_salida, 'w', encoding='utf-8') as f:
        # Selecciona 3 soluciones al azar
        soluciones_seleccionadas = random.sample(soluciones, min(3, len(soluciones)))
        f.write(f'N. Sol: {len(soluciones)}\n')
        if soluciones_seleccionadas:
            for i, solucion in enumerate(soluciones_seleccionadas, start=1):  # Añade un índice a las soluciones
                f.write(f'\nSolución {i}:\n')  # Imprime el número de solución
                parking = [["−" for _ in range(6)] for _ in range(5)]
                for vehiculo, plaza in solucion.items():
                    fila, columna = map(int, plaza.split(','))
                    parking[fila-1][columna-1] = f'"{vehiculo.id}-{vehiculo.tipo}-{vehiculo.congelador}"'
                for fila in parking:
                    f.write(','.join(fila) + '\n')
                f.write('\n')

if __name__ == "__main__":
   main()
    
 
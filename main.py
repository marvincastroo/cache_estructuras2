import numpy as np
# Funcion que obtiene los parámetros del tamaño de cache
# no se si se va a usar pero puede ser para debugging
def getValues():
    stop = False
    while not stop:
        try:
            cache = input("Ingrese el tamaño del cache  (32 a 128 KB): ")
            cache_int = int(cache)  # Try to convert the input to an integer
            if (cache_int % 2 == 0 and cache_int < 129 and cache_int > 31):
                stop = True
        except ValueError:
            print("Input no válido. Ingrese un número entero.")
    stop = False
    while not stop:
        try:
            linea = input("Ingrese el tamaño de línea de cache (32 a 128 bytes): ")
            linea_int = int(linea)  # Try to convert the input to an integer
            if (linea_int % 2 == 0 and linea_int < 129 and linea_int > 31):
                stop = True
        except ValueError:
            print("Input no válido. Ingrese un número entero.")
    stop = False
    while not stop:
        try:
            ways = input("Ingrese el tamaño de asociatividad (4 a 16 ways):  ")
            ways_int = int(ways)  # Try to convert the input to an integer
            if (ways_int < 17 and ways_int > 3):
                stop = True
        except ValueError:
            print("Input no válido. Ingrese un número entero.")
    index_int = cache_int*1024/(linea_int*ways_int)
    print("---------Especificaciones del Cache---------")
    print(f"   Tamaño de línea: {linea_int}")
    print(f"   Tamaño de Index: {index_int}")
    print(f"   Tamaño de asociatividad: {ways_int}")
    print(f"   Tamaño de Cache: {cache_int*1024}")
    print("--------------------------------------------")

    return linea_int, index_int, ways_int, cache_int*1024

# Funcion que construye la matriz que representan el cache, según el tamaño
# que haya sido especificado
def buildCache(data):
    linea, index, ways, cache_size = data
    # podemos hacer una sola matriz, que sea de tamaño filas = index, y columna = linea*ways
    cache = np.zeros((index, linea*ways))
    return cache



def processTrace():
    with open('trace.out', 'r') as file:
        for line in file:
                print(line)

    return


if __name__ == '__main__':
    #especificaciones_cache = getValues()
    data = 32, 256, 4, 32768
    cache = buildCache(data)
    print(data)

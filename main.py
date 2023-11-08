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

# funcion que calcula la cantidad de bits necesarios para la direccion dado el tamaño de la cache
def tagBlockBits(cache):
    linea, index, ways, cache_size = cache
    block_offset_bits = np.log2(linea)
    index_bits = np.log2(index)
    tag_bits = 32 - block_offset_bits - index_bits
    print(block_offset_bits, index_bits, tag_bits)
    return block_offset_bits, index_bits, tag_bits



def processTrace(cache, data, address_bits, way_size):
    # creación de máscaras para obtener tag, index y block offset dada la dirección

    block_offset_bits, index_bits, tag_bits = int(address_bits[0]), int(address_bits[1]), int(address_bits[2])
    mask_block_offset = (1 << block_offset_bits) - 1
    mask_index_bits   = ((1 << index_bits) - 1) << block_offset_bits
    mask_tag_bits     = ((1 << tag_bits) - 1) << (block_offset_bits + index_bits)

    i = 0
    with open('trace.out', 'r') as file:
        queue_LRU = []
        for line in file:
            i = i + 1
            #print(i)
            if (i < 10e38):
                print(line)
                line_splitted = line.split()
                instruction_type = int(line_splitted[1])  # tipo de instrucción: 0 = load, 1 = store
                address_value = int(line_splitted[2], 16) # dirección
                address_hex = hex(address_value)
                print(address_hex)

                block_number = (address_value & mask_block_offset)
                index_number = (address_value & mask_index_bits) >> block_offset_bits
                tag_number = (address_value & mask_tag_bits) >> (block_offset_bits + index_bits)

                print("block: ", hex(block_number))
                print("index: ", hex(index_number))
                print("tag: ", hex(tag_number))

                # empezar a llenar el cache
                # 1. revisar que haya espacio, si no hay espacio, ir al otro way
                way_iterador = 0
                parar = False

                while not parar:
                    if (cache[index_number - 1][way_iterador*block_number : ((way_iterador + 1) * block_number) - 1 ].all() == 0):
                        cache[index_number - 1][way_iterador*block_number: ((way_iterador + 1) * block_number) - 1] = 1
                        queue_LRU.append((index_number, way_iterador))  # se añade el elemento a la lista de LRU para el reemplazo
                        print(f"linea puesta en {index_number}, way: {way_iterador}")
                        parar = True
                    else:
                        way_iterador = way_iterador + 1
                        # si iteramos en todos los ways y no hay espacio, hay que reemplazar
                        # reemplazamos el primer elemento de la lista queue_LRU, y luego lo borramos de la lista
                        if way_iterador >= way_size:
                            parar = True
                            way_iterador = 0

                            cache[(queue_LRU[0])[0] - 1][(queue_LRU[0])[0] * block_number: (((queue_LRU[0])[1] + 1) * block_number) - 1] = 1
                            print(f"linea puesta en {(queue_LRU[0])[0]}, way: {(queue_LRU[0])[1]}")
                            queue_LRU.append(((queue_LRU[0])[0], (queue_LRU[0])[1]))
                            queue_LRU.pop(0)

                            print("Nos pasamos del way, hay que reemplazar")

                print(queue_LRU)
                print((queue_LRU[0])[0])








    return


if __name__ == '__main__':
    #especificaciones_cache = getValues()
    data = 32, 256, 4, 32768
    cache = buildCache(data)
    address_bits = tagBlockBits(data)
    way_size = 4
    processTrace(cache, data, address_bits, way_size)
    print(np.shape(cache))
    #print(data)

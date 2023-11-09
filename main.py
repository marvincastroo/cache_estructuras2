import numpy as np


# Funcion que construye la matriz que representan el cache de tamaño (index, linea cache*numero ways)
# Recibe: tuple "data" con la información de tamaño de linea, index, numero de ways y tamaño de cache
# Retorna: matriz (index, linea cache*numero ways)
def buildCache(data):
    linea, index, ways, cache_size = data
    cache = np.zeros((index, linea*ways))
    return cache

# funcion que, dada las especificaciones del tamaño de cache, calcula la cantidad de bits necesarios
# para direcciones (tag, index, block offset)
# Recibe: tuple "data" con la información de tamaño de linea, index, numero de ways y tamaño de cache
# Retorna: cantidades de bits para block offset, index, tag
def tagBlockBits(cache):
    linea, index, ways, cache_size = cache
    block_offset_bits = np.log2(linea)
    index_bits = np.log2(index)
    tag_bits = 32 - block_offset_bits - index_bits
    print(block_offset_bits, index_bits, tag_bits)
    return block_offset_bits, index_bits, tag_bits


# Función principal que se encarga de leer el trace e ir escribiendo las direcciones en el cache
# Recibe: matriz del cache, información de la cantidad de bits para direccion, y tamaño del way
# Retorna: cache escrita, archivo logfile
def processTrace(cache, data, address_bits, way_size):

    linea, index, ways, cache_size = data
    # creación de máscaras para obtener tag, index y block offset dada la dirección
    block_offset_bits, index_bits, tag_bits = int(address_bits[0]), int(address_bits[1]), int(address_bits[2])
    mask_block_offset = (1 << block_offset_bits) - 1
    mask_index_bits   = ((1 << index_bits) - 1) << block_offset_bits
    mask_tag_bits     = ((1 << tag_bits) - 1) << (block_offset_bits + index_bits)

    i = 0
    with open('test.out', 'r') as file:
        with open("logfile.txt", "w") as logfile:
            queue_LRU = []                  # Lista que guarda los primeros elementos, para el reemplazo de LRU
            for line in file:
                i = i + 1
                #print(i)
                if (i % 500000 == 0):
                    print(f"Counter: {i}")
                if (i < 10e38):
                    #print(line)
                    line_splitted = line.split()
                    instruction_type = int(line_splitted[1])  # tipo de instrucción: 0 = load, 1 = store
                    address_value = int(line_splitted[2], 16) # dirección
                    address_hex = hex(address_value)          # convertir direcc. a hex
                    instruction_quant = int(line_splitted[3]) # cantidad de instrucciones
                    #print(address_hex)

                    # aplicar mascaras para obtener las direcciones
                    block_number = (address_value & mask_block_offset)
                    index_number = (address_value & mask_index_bits) >> block_offset_bits
                    tag_number = (address_value & mask_tag_bits) >> (block_offset_bits + index_bits)
                    print(f"address_value: {address_hex}")
                    print(f"tag: {tag_number}")
                    print(f"index: {index_number}")
                    print(f"block: {block_number}")
                    #print("block: ", hex(block_number))
                    #print("index: ", hex(index_number))
                    #print("tag: ", hex(tag_number))

                    # empezar a llenar el cache
                    # 1. revisar que el elemento exista en algun way, viendo tag e index
                    # 2. si no existe y hay espacio en la cache, se mete la linea
                    # 3. si no existe y no hay espacio, se reemplaza
                    way_iterador = 0                # recore los ways ascendentemente
                    way_iterador_tag = 0
                    parar = False
                    parar1 = False

                    # Ciclo while para verificar si ya existe el elemento
                    while not parar1:
                        if (cache[index_number][way_iterador*linea ]) == tag_number:
                            parar = True
                            parar1 = True
                            print("Encontrado, hit")
                        else:
                            way_iterador = way_iterador + 1
                            if way_iterador >= way_size:
                                parar1 = True

                    way_iterador = 0
                    while not parar:

                        # si linea de cache esta vacia
                        #
                        if cache[index_number][way_iterador*linea + 1 : ((way_iterador + 1) * linea) - 1 ].all() == 0:
                            cache[index_number][way_iterador*linea] = tag_number        # se escribe tag en cache
                            cache[index_number][way_iterador*linea + 1: ((way_iterador + 1) * linea) - 1] = 1   # se escribe 1 en toda la linea
                            queue_LRU.append((index_number, way_iterador))  # se añade el elemento a la lista de LRU para el reemplazo
                            #print(f"linea puesta en {index_number}, way: {way_iterador}")
                            parar = True

                        else:
                            way_iterador = way_iterador + 1
                            # si iteramos en todos los ways y no hay espacio, hay que reemplazar
                            # reemplazamos el primer elemento de la lista queue_LRU, y luego lo borramos de la lista
                            if way_iterador >= way_size:
                                parar = True
                                way_iterador = 0
                                # reemplazo con la dirección dada por el primer elemento de queue_LRU
                                cache[(queue_LRU[0])[0]][(queue_LRU[0])[1] * linea] = tag_number
                                # cache[5][0 * 32 + 1 : ((0 + 1)*32 ) - 1] = cache[5][1 : 31]
                                cache[(queue_LRU[0])[0]][(queue_LRU[0])[1] * linea + 1: (((queue_LRU[0])[1] + 1) * block_number) - 1] = 1
                                #print(f"linea puesta en {(queue_LRU[0])[0]}, way: {(queue_LRU[0])[1]}")
                                queue_LRU.append(((queue_LRU[0])[0], (queue_LRU[0])[1]))    # pongo nueva escritura al final
                                queue_LRU.pop(0)                                            # borro primer elemento



                #print(queue_LRU)
                #print((queue_LRU[0])[0])

            for row1 in cache:
                # Convert each element to a string and join them with a space
                row_str = ' '.join(map(str, row1))

                # Write the row to the file followed by a newline
                logfile.write(row_str + '\n')







    return


if __name__ == '__main__':
    #especificaciones_cache = getValues()
    data = 32, 256, 4, 32768
    cache = buildCache(data)
    address_bits = tagBlockBits(data)
    way_size = 4
    processTrace(cache,data, address_bits, way_size)
    print(np.shape(cache))
    #print(data)
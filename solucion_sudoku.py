import time
import random
 
def encontrar_espacio_vacio(tablero): # Encuentra la primera celda vacía (0) en el tablero  
    for i in range(9): # Recorre las filas
        for j in range(9): # Recorre las columnas
            if tablero[i][j] == 0: # Si encuentra una celda vacía
                return i, j # Devuelve la posición (fila, columna)
    return None, None # Si no hay celdas vacías, devuelve None

def movimiento_valido(tablero, fila, col, num): # Verifica si se puede colocar un número en una celda
    for x in range(9):  # Verificar fila
        if tablero[fila][x] == num: # Si el número ya está en la fila
            return False # No se puede colocar
    
    for x in range(9): # Verificar columna
        if tablero[x][col] == num: # Si el número ya está en la columna
            return False # No se puede colocar
    
    # Verificar subgrilla 3x3
    fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3): # Recorre las filas de la subgrilla
        for j in range(3): # Recorre las columnas de la subgrilla
            if tablero[i + fila_inicial][j + col_inicial] == num: # Si el número ya está en la subgrilla
                return False # No se puede colocar
    return True # Si no se encontró ningún conflicto, se puede colocar el número

def impresion(tablero): # Imprime el tablero de Sudoku
    for fila in tablero: # Recorre cada fila del tablero
        print(fila) # Imprime la fila actual

def solucion1_FB(tablero, max_intentos=1000000): # Fuerza Bruta
    intentos = 0 # Contador de intentos

    while intentos < max_intentos: # Mientras no se alcance el número máximo de intentos
        nuevo_tablero = [fila[:] for fila in tablero]  # Copia del tablero original
        valido = True # Bandera para verificar si el tablero es válido

        while True: # Bucle para llenar el tablero
            fila, col = encontrar_espacio_vacio(nuevo_tablero)  # Busca la siguiente celda vacía
            if fila is None:  # Si no hay más espacios vacíos, terminamos
                return nuevo_tablero # Devolvemos el tablero lleno

            numeros = list(range(1, 10))  # Generamos números del 1 al 9
            random.shuffle(numeros)  # Mezclamos para probar combinaciones diferentes

            colocado = False # Bandera para verificar si se colocó un número
            for num in numeros: # Probar cada número en la celda vacía
                if movimiento_valido(nuevo_tablero, fila, col, num): # Verifica si el número es válido
                    nuevo_tablero[fila][col] = num  # Coloca el número en la celda
                    colocado = True # Marcamos que se colocó un número
                    break  # Pasamos a la siguiente celda

            if not colocado:  # Si no se pudo colocar un número válido, descartamos este intento
                valido = False # Marcamos que el tablero no es válido
                break # Salimos del bucle de llenado

        if valido: # Si logramos llenar el tablero sin conflictos
            return nuevo_tablero  # Si logramos llenar todo el tablero, lo devolvemos

        intentos += 1  # Contamos el intento fallido

    return "No hay solución posible"  # Si después de muchos intentos no encontramos solución

def solucion2_BT(tablero): # Backtracking
    # Backtracking sin Forward Checking
    def resolver(tablero): # Función recursiva para resolver el Sudoku
        fila, col = encontrar_espacio_vacio(tablero)    # Busca la siguiente celda vacía
        if fila is None: # Si no hay más espacios vacíos, terminamos
            return True # El tablero está completo
        
        for num in range(1, 10): # Probar números del 1 al 9
            if movimiento_valido(tablero, fila, col, num): # Verifica si el número es válido
                tablero[fila][col] = num # Coloca el número en la celda
                if resolver(tablero): # Llama recursivamente para resolver el resto del tablero
                    return True # Si se encontró una solución, devolvemos True
                tablero[fila][col] = 0  # Deshacer movimiento (backtrack)
        
        return False # Si no se encontró solución, devolvemos False
    
    if resolver(tablero): # Si logramos resolver el tablero
        return tablero # Devolvemos el tablero resuelto
    else: # Si no se encontró solución
        return "No hay solución" # Devolvemos un mensaje de error

def solucion3_BT_FC(tablero): 
    # Backtracking con Forward Checking
    def forward_check(tablero): # Función para verificar si el tablero es válido con Forward Checking
        for i in range(9):  # Recorre las filas
            for j in range(9): # Recorre las columnas
                if tablero[i][j] == 0:  # Si la celda está vacía
                    posibles = [x for x in range(1, 10) if movimiento_valido(tablero, i, j, x)] # Genera lista de números posibles
                    if len(posibles) == 0:  # Si no hay valores posibles
                        return False # No se puede continuar
        return True # Si hay al menos un número posible en cada celda vacía, es válido
    
    def resolver(tablero): # Función recursiva para resolver el Sudoku
        fila, col = encontrar_espacio_vacio(tablero) # Busca la siguiente celda vacía
        if fila is None: # Si no hay más espacios vacíos, terminamos
            return True    # El tablero está completo
        
        for num in range(1, 10): # Probar números del 1 al 9
            if movimiento_valido(tablero, fila, col, num): # Verifica si el número es válido
                tablero[fila][col] = num # Coloca el número en la celda
                if forward_check(tablero):  # Comprobar con Forward Checking
                    if resolver(tablero): # Llama recursivamente para resolver el resto del tablero
                        return True # Si se encontró una solución, devolvemos True
                tablero[fila][col] = 0  # Deshacer movimiento (backtrack)
        
        return False # Si no se encontró solución, devolvemos False
    
    if resolver(tablero): # Si logramos resolver el tablero
        return tablero # Devolvemos el tablero resuelto
    else: # Si no se encontró solución
        return "No hay solución" # Devolvemos un mensaje de error

if __name__ == "__main__": # Bloque principal para ejecutar el código
    tablero = [ # Tablero de Sudoku inicial
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]
    ] 
    
    # Imprimir tablero inicial
    print("Tablero inicial:")
    impresion(tablero) 
    
    # Medir el tiempo de ejecución para la solución seleccionada (switch-like)
    print("\nSeleccione la solución (1: Fuerza Bruta, 2: Backtracking, 3: Backtracking + Forward Checking): ")
    seleccion = int(input())  # Usamos input para seleccionar cuál algoritmo ejecutar
    # Validar la selección
    if seleccion == 1: 
        start_time = time.perf_counter() 
        print("\nSolución con Fuerza Bruta:")
        resultado_fb = solucion1_FB(tablero)
        if isinstance(resultado_fb, str):
            print(resultado_fb)
        else:
            impresion(resultado_fb)
        end_time = time.perf_counter()
        print(f"\nTiempo de ejecución para Fuerza Bruta: {end_time - start_time:.6f} segundos")
    
    elif seleccion == 2:
        start_time = time.perf_counter()
        print("\nSolución con Backtracking:")
        resultado_bt = solucion2_BT(tablero)
        if isinstance(resultado_bt, str):
            print(resultado_bt)
        else:
            impresion(resultado_bt)
        end_time = time.perf_counter()
        print(f"\nTiempo de ejecución para Backtracking: {end_time - start_time:.6f} segundos")
    
    elif seleccion == 3:
        start_time = time.perf_counter()
        print("\nSolución con Backtracking + Forward Checking:")
        resultado_bt_fc = solucion3_BT_FC(tablero)
        if isinstance(resultado_bt_fc, str):
            print(resultado_bt_fc)
        else:
            impresion(resultado_bt_fc)
        end_time = time.perf_counter()
        print(f"\nTiempo de ejecución para Backtracking + Forward Checking: {end_time - start_time:.6f} segundos")
    else:
        print("Selección no válida.")
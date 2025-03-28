import time
import random

def encontrar_espacio_vacio(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None, None

def movimiento_valido(tablero, fila, col, num):
    # Verificar fila
    for x in range(9):
        if tablero[fila][x] == num:
            return False
    
    # Verificar columna
    for x in range(9):
        if tablero[x][col] == num:
            return False
    
    # Verificar subgrilla 3x3
    fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[i + fila_inicial][j + col_inicial] == num:
                return False
    return True

def impresion(tablero):
    for fila in tablero:
        print(fila)

def solucion1_FB(tablero, max_intentos=1000000):
    intentos = 0

    while intentos < max_intentos:
        nuevo_tablero = [fila[:] for fila in tablero]  # Copia del tablero original
        valido = True

        while True:
            fila, col = encontrar_espacio_vacio(nuevo_tablero)  # Busca la siguiente celda vacía
            if fila is None:  # Si no hay más espacios vacíos, terminamos
                return nuevo_tablero

            numeros = list(range(1, 10))  # Generamos números del 1 al 9
            random.shuffle(numeros)  # Mezclamos para probar combinaciones diferentes

            colocado = False
            for num in numeros:
                if movimiento_valido(nuevo_tablero, fila, col, num):
                    nuevo_tablero[fila][col] = num
                    colocado = True
                    break  # Pasamos a la siguiente celda

            if not colocado:  # Si no se pudo colocar un número válido, descartamos este intento
                valido = False
                break

        if valido:
            return nuevo_tablero  # Si logramos llenar todo el tablero, lo devolvemos

        intentos += 1  # Contamos el intento fallido

    return "No hay solución posible"  # Si después de muchos intentos no encontramos solución

def solucion2_BT(tablero):
    # Backtracking sin Forward Checking
    def resolver(tablero):
        fila, col = encontrar_espacio_vacio(tablero)
        if fila is None:
            return True
        
        for num in range(1, 10):
            if movimiento_valido(tablero, fila, col, num):
                tablero[fila][col] = num
                if resolver(tablero):
                    return True
                tablero[fila][col] = 0  # Deshacer movimiento (backtrack)
        
        return False
    
    if resolver(tablero):
        return tablero
    else:
        return "No hay solución"

def solucion3_BT_FC(tablero):
    # Backtracking con Forward Checking
    def forward_check(tablero):
        for i in range(9):
            for j in range(9):
                if tablero[i][j] == 0:  # Si la celda está vacía
                    posibles = [x for x in range(1, 10) if movimiento_valido(tablero, i, j, x)]
                    if len(posibles) == 0:  # Si no hay valores posibles
                        return False
        return True
    
    def resolver(tablero):
        fila, col = encontrar_espacio_vacio(tablero)
        if fila is None:
            return True
        
        for num in range(1, 10):
            if movimiento_valido(tablero, fila, col, num):
                tablero[fila][col] = num
                if forward_check(tablero):  # Comprobar con Forward Checking
                    if resolver(tablero):
                        return True
                tablero[fila][col] = 0  # Deshacer movimiento (backtrack)
        
        return False
    
    if resolver(tablero):
        return tablero
    else:
        return "No hay solución"

if __name__ == "__main__":
    tablero = [
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
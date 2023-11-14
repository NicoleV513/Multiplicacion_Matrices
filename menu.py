import PySimpleGUI as sg
import pandas as pd
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#sg.theme('BlueMono')
sg.theme('LightPurple')

def crear_matriz_manual(tamaño):
    matriz = []
    layout = [
         [sg.Text('Ingresa los valores de la matriz a crear', justification='center')],
    ]

    for i in range(tamaño):
        row = []
        for j in range(tamaño):
            key = f'input_{i}_{j}'
            row.append(sg.InputText(key=key, size=(5, 1), justification='center'))
        layout.append(row)

    layout.append([sg.Button('Aceptar')])
    window = sg.Window('Ingresa los valores de la matriz', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Aceptar':
            try:
                matriz = [[float(values[f'input_{i}_{j}']) for j in range(tamaño)] for i in range(tamaño)]
                break
            except ValueError:
                sg.popup_error('Ingresa valores numéricos en todas las celdas')

    window.close()

    return matriz

def crear_matriz_automática(tamaño, Matriz):
    for Filas in range(tamaño): #0 -> 2 
        for Columnas in range(tamaño): # -> 3
            Matriz[Filas][Columnas]=random.randint(-10, 10)
            
    return Matriz

#Multiplicación Tradicional

def multiplicacion_tradicional(MatrizA,MatrizB):
    MatrizC =[]
    for i in range(tamaño):
        MatrizC.append([0]* tamaño)
    #Multiplicaciones por a y B
    for i in range(len(MatrizA)): #recorre filas
        for j in range(len(MatrizB[0])): #recorre columnas
            for k in range(len(MatrizB)):
                MatrizC[i][j] += MatrizA[i][k] * MatrizB[k][j]

    return MatrizC

#Método Strassen
def strassen_multiply(A, B):
    # ... (unchanged)
    def matrix_add(A, B):
     """Suma de matrices"""
    return [
        [A[i][j] + B[i][j] for j in range(len(A[i]))]
        for i in range(len(A))
    ]


def matrix_subtract(A, B):
    """Resta de matrices"""
    return [
        [A[i][j] - B[i][j] for j in range(len(A[i]))]
        for i in range(len(A))
    ]

def matrix_blocks(matrix):
    """Divide una matriz en bloques más pequeños"""
    n = len(matrix) // 2
    a11 = [row[:n] for row in matrix[:n]]
    a12 = [row[n:] for row in matrix[:n]]
    a21 = [row[:n] for row in matrix[n:]]
    a22 = [row[n:] for row in matrix[n:]]
    return a11, a12, a21, a22

def matrix_combine(a11, a12, a21, a22):
    """Combina bloques de matriz en una matriz completa"""
    n = len(a11)
    result = []
    for i in range(n):
        result.append(a11[i] + a12[i])
    for i in range(n):
        result.append(a21[i] + a22[i])
    return result


def mostrar_resultados_guardar_xlsx(MatrizA, MatrizB):

    # Medir el tiempo de ejecución de la multiplicación tradicional
    start_time_tradicional = time.time()
    MatrizC = multiplicacion_tradicional(MatrizA, MatrizB)
    elapsed_time_tradicional = time.time() - start_time_tradicional

    # Medir el tiempo de ejecución de la multiplicación Strassen
    start_time_strassen = time.time()
    MatrizD = strassen_multiply(MatrizA, MatrizB)
    elapsed_time_strassen = time.time() - start_time_strassen

    # Crear DataFrames de pandas para las matrices
    df_matriz_a = pd.DataFrame(MatrizA, columns=[f'A_{i+1}' for i in range(len(MatrizA[0]))])
    df_matriz_b = pd.DataFrame(MatrizB, columns=[f'B_{i+1}' for i in range(len(MatrizB[0]))])
    df_matriz_c = pd.DataFrame(MatrizC, columns=[f'C_{i+1}' for i in range(len(MatrizC[0]))])
    #df_matriz_d = pd.DataFrame(MatrizD, columns=[f'D_{i+1}' for i in range(len(MatrizD[0]))])

    # Guardar los DataFrames en un archivo Excel
    with pd.ExcelWriter('resultados_matrices.xlsx', engine='xlsxwriter') as writer:
        df_matriz_a.to_excel(writer, sheet_name='Matriz A', index=False)
        df_matriz_b.to_excel(writer, sheet_name='Matriz B', index=False)
        df_matriz_c.to_excel(writer, sheet_name='Resultado', index=False)

    sg.Popup(f'Tiempo Tradicional: {elapsed_time_tradicional:.6f} segundos\n'
             f'Tiempo Strassen: {elapsed_time_strassen:.6f} segundos\n'
             '\nResultados guardados en "resultados_matrices.xlsx"')

    # Generar gráfica de barras con los tiempos
    labels = ['Multiplicación Tradicional', 'Multiplicación Strassen']
    times = [elapsed_time_tradicional, elapsed_time_strassen]

    plt.plot(labels, times, marker='o', linestyle='-', color='b')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Comparación de Tiempos de Ejecución')

    fig_manager = plt.get_current_fig_manager()
    fig_manager.resize(800, 600)

    plt.show()


#menú principal

layout = [
    [sg.Text('¡Bienvenido! Por favor elige la opción que prefieras')],
    [sg.Text('1.Crear tu matriz')],
    [sg.Text('2.Crear matriz automáticamente')],
    [sg.Text('')],
    [sg.Text('Elige 1 o 2: '), sg.InputText(key="opcion")],
    [sg.Text('')],
    [sg.Text('Elige el tamaño de la Matriz a crear')],
    [sg.Text('# Filas y Columnas: '), sg.InputText(key="tamaño")],
    [sg.Text('')],
    [sg.Button('Continuar'), sg.Button('Salir')]
]

window = sg.Window('Multiplicación de Matrices', layout, margins=(10, 10), finalize=True)
window.set_min_size((100, 200))

while True:
    event, values = window.read()
    opcion = int(values["opcion"])
    tamaño = int(values["tamaño"])

    #Creación de la primera matriz cuadrada
    MatrizA=[]
    for i in range(tamaño):
        MatrizA.append([0] *tamaño)

    #Creación de la segunda matriz cuadrada
    MatrizB=[]
    for i in range(tamaño):
        MatrizB.append([0] *tamaño)

    if event == 'Continuar':
        if opcion == 1:
            MatrizA=crear_matriz_manual(tamaño)
            MatrizB=crear_matriz_manual(tamaño)
            # mostrar_matrices(MatrizA, MatrizB)
            # mostrar_resultados(MatrizA,MatrizB)
            mostrar_resultados_guardar_xlsx(MatrizA, MatrizB)
            

        elif  opcion == 2:
            MatrizA=crear_matriz_automática(tamaño,MatrizA)
            MatrizB=crear_matriz_automática(tamaño,MatrizB)
            # mostrar_matrices(MatrizA, MatrizB)
            # mostrar_resultados(MatrizA,MatrizB)
            mostrar_resultados_guardar_xlsx(MatrizA, MatrizB)

        else:
            sg.Popup('Opción Incorrecta')

    if event == "Salir" or event == sg.WIN_CLOSED:
        break

window.close()


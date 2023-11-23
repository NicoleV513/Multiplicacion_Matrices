#Importar librerias
import PySimpleGUI as sg
import pandas as pd
import random
import time
import numpy as np
import matplotlib.pyplot as plt

#sg.theme('BlueMono')
sg.theme('LightPurple')

#Crear la matriz de manera manual
def crear_matriz_manual(tamaño):
    matriz = []
    layout = [
         [sg.Text('Ingresa los valores de la matriz a crear', justification='center')],
    ]

    #Recibir los datos a través de interfaz
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
                #Pedir valores de la matriz 
                matriz = [[int(values[f'input_{i}_{j}']) for j in range(tamaño)] for i in range(tamaño)]
                break
            except ValueError:
                sg.popup_error('Ingresa valores numéricos en todas las celdas')

    window.close()

    return matriz

#Recibe valores de -100 a 100 para la creación de la matriz
def crear_matriz_automática(tamaño, Matriz):
    for Filas in range(tamaño): 
        for Columnas in range(tamaño): 
            Matriz[Filas][Columnas]=random.randint(-100, 100)
            
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
#Solo funciona para matrices que tienen por tamaño una potencia de 2
# def strassen(A,B):
#     A = np.array(A)
#     B = np.array(B)
#     n=len(A)

#     if n==1:
#         return A*B
#     else:
#         a11=A[:n//2,:n//2]
#         a12=A[:n//2,n//2:]
#         a21=A[n//2:,:n//2]
#         a22=A[n//2:,n//2:]
#         b11=B[:n//2,:n//2]
#         b12=B[:n//2,n//2:]
#         b21=B[n//2:,:n//2]
#         b22=B[n//2:,n//2:]

#         m1=strassen(a11+a22,b11+b22)
#         m2=strassen(a21+a22,b11)
#         m3=strassen(a11,b12-b22)
#         m4=strassen(a22,b21-b11)
#         m5=strassen(a11+a12,b22)
#         m6=strassen(a21-a11,b11+b12)
#         m7=strassen(a12-a22,b21+b22)

#         c11=m1+m4-m5+m7
#         c12=m3+m5
#         c21=m2+m4
#         c22=m1-m2+m3+m6

#         c=np.zeros((n,n))
#         c[:n//2,:n//2]=c11
#         c[:n//2,n//2:]=c12
#         c[n//2:,:n//2]=c21
#         c[n//2:,n//2:]=c11

#         return c

def multiplicacion_eficiente(matriz_a, matriz_b):
    #for _ in range(n), el guion bajo (_) se utiliza como una convención para indicar que el valor de la variable no se va a utilizar en el cuerpo del bucle.
    resultado = [[0] * len(matriz_b[0]) for _ in range(len(matriz_a))]

    for i in range(len(matriz_a)):
        for j in range(len(matriz_b[0])):
            resultado[i][j] = sum(matriz_a[i][k] * matriz_b[k][j] for k in range(len(matriz_b)))

    return resultado


def mostrar_resultados_guardar_xlsx(MatrizA, MatrizB):

    # Medir el tiempo de ejecución de la multiplicación tradicional
    start_time_tradicional = time.time()
    MatrizC = multiplicacion_tradicional(MatrizA, MatrizB)
    elapsed_time_tradicional = time.time() - start_time_tradicional

    # Medir el tiempo de ejecución de la multiplicación Strassen
    start_time_strassen = time.time()
    MatrizD = multiplicacion_eficiente(MatrizA, MatrizB)
    elapsed_time_strassen = time.time() - start_time_strassen

    # Crear DataFrames de pandas para las matrices
    df_matriz_a = pd.DataFrame(MatrizA, columns=[f'A_{i+1}' for i in range(len(MatrizA[0]))])
    df_matriz_b = pd.DataFrame(MatrizB, columns=[f'B_{i+1}' for i in range(len(MatrizB[0]))])
    df_matriz_c = pd.DataFrame(MatrizC, columns=[f'C_{i+1}' for i in range(len(MatrizC[0]))])
    df_matriz_d = pd.DataFrame(MatrizD, columns=[f'D_{i+1}' for i in range(len(MatrizD[0]))])

    # Guardar los DataFrames en un archivo Excel
    with pd.ExcelWriter('resultados_matrices.xlsx', engine='xlsxwriter') as writer:
        df_matriz_a.to_excel(writer, sheet_name='Matriz A', index=False)
        df_matriz_b.to_excel(writer, sheet_name='Matriz B', index=False)
        df_matriz_c.to_excel(writer, sheet_name='Resultado Tradicional', index=False)
        df_matriz_d.to_excel(writer, sheet_name='Resultado Eficiente', index=False)

    sg.Popup(f'Tiempo Tradicional: {elapsed_time_tradicional:.6f} segundos\n'
             f'Tiempo Eficiente: {elapsed_time_strassen:.6f} segundos\n'
             '\nResultados guardados en "resultados_matrices.xlsx"')

    # Generar gráfica de barras con los tiempos
    labels = ['Multiplicación Tradicional', 'Multiplicación Eficiente']
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
            mostrar_resultados_guardar_xlsx(MatrizA, MatrizB)
            

        elif  opcion == 2:
            MatrizA=crear_matriz_automática(tamaño,MatrizA)
            MatrizB=crear_matriz_automática(tamaño,MatrizB)
            mostrar_resultados_guardar_xlsx(MatrizA, MatrizB)

        else:
            sg.Popup('Opción Incorrecta')

    if event == "Salir" or event == sg.WIN_CLOSED:
        break

window.close()


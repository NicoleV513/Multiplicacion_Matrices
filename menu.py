import PySimpleGUI as sg
import random
import numpy as np

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

def mostrar_matrices(matriz1, matriz2):
    #Size(cango,altura)
    layout = [
        [sg.Text('Matriz A', size=(12, 1), justification='center'), sg.Text('Matriz B', size=(15, 1), justification='center')],
    ]

    # Agregar filas de ambas matrices
    for row1, row2 in zip(matriz1, matriz2):
        layout.append([sg.Text(str(row1), size=(15, 1)), sg.Text(str(row2), size=(15, 1))])

    layout.append([sg.Button('Continuar')])

    window = sg.Window('Matrices en PySimpleGUI', layout)
    while True:
         event, values = window.read()
         if event == sg.WINDOW_CLOSED or event == 'Continuar':
             sg.Popup('Multipliquemos!')
             break

    window.close()

def mostrar_resultados(MatrizA,MatrizB):
    #Size(cango,altura)
    layout = [
        [sg.Text('Matriz Resultante', size=(12, 1), justification='center')],
    ]

    MatrizC=multiplicacion_tradicional(MatrizA,MatrizB)

    # Agregar filas de ambas matrices
    for row1 in zip(MatrizC):
        layout.append([sg.Text(str(row1), size=(15, 1))])

    layout.append([sg.Button('Cerrar')])

    window = sg.Window('Matrices en PySimpleGUI', layout)
    while True:
         event, values = window.read()
         if event == sg.WINDOW_CLOSED or event == 'Cerrar':
             sg.Popup('Vuelve Pronto!')
             break

    window.close()


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

window = sg.Window('Multiplicación de Matrices', layout, margins=(10, 10))

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
            mostrar_matrices(MatrizA, MatrizB)
            mostrar_resultados(MatrizA,MatrizB)

        elif  opcion == 2:
            MatrizA=crear_matriz_automática(tamaño,MatrizA)
            MatrizB=crear_matriz_automática(tamaño,MatrizB)
            mostrar_matrices(MatrizA, MatrizB)
            mostrar_resultados(MatrizA,MatrizB)

        else:
            sg.Popup('Opción Incorrecta')

    if event == "Salir" or event == sg.WIN_CLOSED:
        break

window.close()


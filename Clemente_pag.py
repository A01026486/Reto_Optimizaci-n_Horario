from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum, value
import streamlit as st
import pandas as pd

profesores = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
materias = ['k', 'j', 'o', 'r', 'p', 'm', 'n', 's', 'q']
horarios = [1, 2, 3, 4, 5, 6, 7, 8, 9]
salones = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

materias_profesor = {
    'A':['j', 's', 'k'], 
    'B':['o', 'm'], 
    'C':['r', 'n', 's'], 
    'D':['p', 's', 'q'], 
    'E':['j', 'o', 'n'],
    'F':['o', 'r', 'q'],
    'G':['r', 'p', 'k'],
    'H':['p', 'j', 'm'],
    'I':['j', 'o', 'r']     
}

disponibilidad_horario = {
    'A':[1, 2, 3], 
    'B':[2, 4, 6], 
    'C':[3, 4, 5], 
    'D':[6, 8, 9], 
    'E':[9, 8, 6],
    'F':[1, 3, 5],
    'G':[4, 6, 8],
    'H':[1, 3, 6],
    'I':[3, 6, 7]     
}

costos_profesor = {
    'A':10, 
    'B':20, 
    'C':20, 
    'D':10, 
    'E':20,
    'F':10,
    'G':10,
    'H':20,
    'I':20     
}

costos_materia = {
    'k':10, 
    'j':5, 
    'o':5, 
    'r':5, 
    'p':10,
    'm':10,
    'n':5,
    's':5,
    'q':5     
}

costos_horario = {
    1:20,
    2:20,
    3:20,
    4:18,
    5:18,
    6:18,
    7:16,
    8:16,
    9:16
}

costos_salon = {
    'a':50, 
    'b':50, 
    'c':40, 
    'd':40, 
    'e':50,
    'f':50,
    'g':40,
    'h':40,
    'i':50  
}

def profesor_disponible(profesor, horario):
    return horario in disponibilidad_horario[profesor]

def profesor_puede_impartir_materia(profesor, materia):
    return materia in materias_profesor[profesor]


# Crea el problema de optimización
prob = LpProblem("Asignación de horarios", LpMinimize)

# Crea las variables de decisión
x = LpVariable.dicts("x", ((profesor, materia, horario, salon) for profesor in profesores for materia in materias for horario in horarios for salon in salones), cat='Binary')

costo_total = lpSum([x[profesor, materia, horario, salon] * (costos_profesor[profesor] + costos_materia[materia] + costos_horario[horario] + costos_salon[salon]) for profesor in profesores for materia in materias for horario in horarios for salon in salones])
costo_total = costo_total * 1000

prob += costo_total

# Cada materia debe ser asignada exactamente una vez
for materia in materias:
    prob += lpSum(x[profesor, materia, horario, salon] for profesor in profesores for horario in horarios for salon in salones) == 1

# Un profesor no puede enseñar más de una materia al mismo tiempo
for profesor in profesores:
    for horario in horarios:
        prob += lpSum(x[profesor, materia, horario, salon] for materia in materias for salon in salones) <= 1

# Un salón no puede ser utilizado por más de una materia al mismo tiempo
for salon in salones:
    for horario in horarios:
        prob += lpSum(x[profesor, materia, horario, salon] for profesor in profesores for materia in materias) <= 1

# Las materias solo pueden ser asignadas a profesores que pueden enseñarlas y a horarios en los que estén disponibles
for profesor in profesores:
    for materia in materias:
        for horario in horarios:
            for salon in salones:
                if not profesor_puede_impartir_materia(profesor, materia) or not profesor_disponible(profesor, horario):
                    prob += x[profesor, materia, horario, salon] == 0

prob.msg = 1
status = prob.solve()

if LpStatus[status] == 'Optimal':
    asignaciones = [(profesor, materia, horario, salon) for profesor in profesores for materia in materias for horario in horarios for salon in salones if x[profesor, materia, horario, salon].value() == 1]

    for asignacion in asignaciones:
        profesor, materia, horario, salon = asignacion
        print(f"{profesor} imparte {materia} en el horario {horario} en el salón {salon}")

    print(f"Costo total: {value(costo_total)}")
else:
    print("No se encontró una solución óptima.")

st.set_page_config(
    page_title='Horario Óptimo',
    layout='wide',
)

st.title("Calculadora para optimizar horarios")

table1 = {'Profesores': {0: 'A',
  1: 'B',
  2: 'C',
  3: 'D',
  4: 'E',
  5: 'F',
  6: 'G',
  7: 'H',
  8: 'I'},
 'Materias': {0: 'k',
  1: 'j',
  2: 'o',
  3: 'r',
  4: 'p',
  5: 'm',
  6: 'n',
  7: 's',
  8: 'q'},
 'Horarios': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9},
 'Salones': {0: 'a',
  1: 'b',
  2: 'c',
  3: 'd',
  4: 'e',
  5: 'f',
  6: 'g',
  7: 'h',
  8: 'i'},
 'Materias que puede dar cada profesor': {0: 'jsk',
  1: 'om',
  2: 'rns',
  3: 'psq',
  4: 'jon',
  5: 'orq',
  6: 'rpk',
  7: 'pjm',
  8: 'jor'},
 'Disponibilidad de horario de cada profesor': {0: 123,
  1: 246,
  2: 345,
  3: 689,
  4: 986,
  5: 135,
  6: 468,
  7: 136,
  8: 367},
 'Costos Profesores': {0: 10,
  1: 20,
  2: 20,
  3: 10,
  4: 20,
  5: 10,
  6: 10,
  7: 20,
  8: 20},
 'Costos Materias': {0: 10, 1: 5, 2: 5, 3: 5, 4: 10, 5: 10, 6: 5, 7: 5, 8: 5},
 'Costos Horarios': {0: 20,
  1: 20,
  2: 20,
  3: 18,
  4: 18,
  5: 18,
  6: 16,
  7: 16,
  8: 16},
 'Costos Salones': {0: 50,
  1: 50,
  2: 40,
  3: 40,
  4: 50,
  5: 50,
  6: 40,
  7: 40,
  8: 50}}

df1 = pd.DataFrame(table1)

st.markdown("Esta calculadora sirve para optimizar horarios. Se usó la librería PuLP en Python")


st.header("Restricciones")
horario = df1
st.write(horario)

st.header("Horario óptimo")
if LpStatus[status] == 'Optimal':
    dic = {'Materia': [], 'Profesor': [], 'Horario': [], 'Salón': []}
    asignaciones = [(profesor, materia, horario, salon) for profesor in profesores for materia in materias for horario in horarios for salon in salones if x[profesor, materia, horario, salon].value() == 1]

    for asignacion in asignaciones:
        profesor, materia, horario, salon = asignacion
        dic['Materia'].append(materia)
        dic['Profesor'].append(profesor)
        dic['Horario'].append(horario)
        dic['Salón'].append(salon)

    df = pd.DataFrame(dic)
    st.write(df)

    st.write(f"Costo total: {value(costo_total)*1000:,}")
else:
    print("No se encontró una solución óptima.")
import random
import csv

# Algoritmos
# 0.2(C1) + 0.2(C2) + 0.2(Ex1) + 0.2(Ex2) + 0.1(P1) + 0.1(P2)
# Notas = [EC1, EC2, Ex1, Ex2, Pr1, Pr2, Promedio]
# Margenes = [Parecido, peor, mejor]
# curso_por_ciclo = [2018-2, 2019-1, 2019-2]
NOTAS = []
PORCENTAJES = []
CICLOS = 1
ALUMNOS_POR_CICLO = 40
NUMERO_DE_ALUMNOS = CICLOS*ALUMNOS_POR_CICLO
NOTA_MINIMA = 10.5
NOTAS_POR_CICLO = []
real0 = [15, 15, 2, 6, 14, 14]
real1 = [15, 10, 8, 12, 15, 15]
real2 = [16, 12, 13, 12, 18, 16]
real3 = [18, 17, 11, 13, 19, 17]
real4 = [18, 15, 14, 17, 18, 16]
real5 = [15, 12, 15, 18, 16, 14]
real6 = [18, 13, 12, 13, 15, 14]
alumnos = [real0, real1, real2, real3 , real4, real5, real6]
margenes = [[-1,+2],[-2, +1],[-1,+1],[-5, -2],[2, 3]]


def getPercentages():
  NOTAS.append(int(input("Ingrese el numero de notas en el curso de acuerdo a Intranet\nNumero: ")))
  print("Ingrese el peso de las notas en formato decimal. (Si vale 10%, colocar 0.1)")
  for i in range(NOTAS[0]):
    print("Nota",i+1,end = ": ")
    PORCENTAJES.append(float(input()))

def promedio(notas):
  prom = 0
  for i in range(NOTAS[0]):
    prom += PORCENTAJES[i]*notas[i]
  return prom

def desdeExamen(notas, numero):
  duplicado = notas.copy()
  for i in range(numero):
    duplicado[i] = 0;
  return promedio(duplicado)

def hastaExamen(notas, numero):
  duplicado = [0,0,0,0,0,0,0]
  for i in range(numero):
    duplicado[i] = notas[i];
  return promedio(duplicado)

def produceCSV(file_name, alumnos):
  headers = []
  for i in range(NOTAS[0]):
    headers.append("Nota"+str(i+1))
  headers.append("Promedio")
  with open(file_name, mode='w') as gradesfile:
    writer = csv.writer(gradesfile, delimiter=',')
    writer.writerow(headers)
    for alumno in alumnos:
      writer.writerow(alumno)
def produceXLSX():
  print("boop")

def nuevo_estudiante():
  notas = []
  referencia = random.choice(alumnos)
  calidad = random.choice(margenes)
  for nota in referencia:
    numero = nota + random.randint(calidad[0], calidad[1])
    if numero > 20:
      numero = 20 - (random.randint(1,3))
    elif numero < 0:
      numero = 0 + (random.randint(1,3))
    notas.append(numero)
  notas[-1] = promedio(notas)
  return notas

def crearData(generate=False):
  for alumno in alumnos:
    alumno.append(promedio(alumno))
  for i in range(CICLOS):
    alumnos_de_curso = []
    for j in range(ALUMNOS_POR_CICLO-1):
      alumnos_de_curso.append(nuevo_estudiante())
    if (generate):
      produceCSV("CSVs/alumnos-ciclo"+str(i+1)+".csv",alumnos_de_curso)
    NOTAS_POR_CICLO.append(alumnos_de_curso)

def displayData():
  for i in NOTAS_POR_CICLO:
    print("NUEVO CICLO")
    for j in i:
      print(j)

## Estimate final grades and probabilities ---------------------
def getStudentGrades():
  grades = []
  print("Ingrese el numero de notas del estudiante")
  num = int(input("Numero de notas: "))
  while (num < 1 or num > NOTAS[0]):
    print("Ingrese un numero dentro del numero de notas del curso")
    num = int(input("Numero de notas: "))
  for i in range(num):
    print("Ingrese nota", i + 1, "de libretas")
    grades.append(int(input()))
  return grades

def parseStudentGrades(file_name):
  all_grades = []
  with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
          if(len(row) < 1 or len(row) > NOTAS[0]):
            raise Exception("Numero de notas incongruente en linea", line_count+1)
          grades=[]
          if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
          else:
            for grade in row:
              grades.append(int(grade))
            line_count += 1
            print(f'Processed {line_count} lines.')
            all_grades.append(grades)
  return all_grades

def chances(needed_grade, until):
  cont = 0
  # print(NOTAS_POR_CICLO)
  for i in NOTAS_POR_CICLO:
    for j in i:
      # print("Array analizing is ", j)
      nota = desdeExamen(j, until)
      # print(nota)
      if(nota >= needed_grade):
        cont += 1
        #print(cont, end=", ")
  return cont

def getRate(notas):
  current_grade = hastaExamen(notas, len(notas))
  needed_grade = NOTA_MINIMA - current_grade
  print("Needed grade is", needed_grade)
  return chances(needed_grade, len(notas))/NUMERO_DE_ALUMNOS

def run():
    getPercentages()
    crearData()
    displayData()
    print("Ingrese la opcion de prediccion (1 o 2): \n1) Nota singular\n2) CSV de notas\n")
    opcion = input("")
    if (opcion == "1"):
      grades = getStudentGrades()
      print(getRate(grades))
    else:
      rates = []
      file_name = input("Ingrese nombre de archivo CSV: ")
      all_grades = parseStudentGrades(file_name)
      for student in all_grades:
        print(getRate(student))

run()

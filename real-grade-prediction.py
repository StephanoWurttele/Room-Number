import random
import csv
import xlsxwriter
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pandas as pd

# Algoritmos
# 0.2(C1) + 0.2(C2) + 0.2(Ex1) + 0.2(Ex2) + 0.1(P1) + 0.1(P2)
# Notas = [EC1, EC2, Ex1, Ex2, Pr1, Pr2, Promedio]
# Margenes = [Parecido, peor, mejor]
# curso_por_ciclo = [2018-2, 2019-1, 2019-2]
CURSO = []
NOTAS = []
PORCENTAJES = []
CICLOS = 5
ALUMNOS_POR_CICLO = 50
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
  CURSO.append(input("Ingrese nombre del curso"))
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
  with open(file_name, mode='w') as gradesfile:
    writer = csv.writer(gradesfile, delimiter=',')
    writer.writerow(headers)
    for alumno in alumnos:
      writer.writerow(alumno[0:-3])

def produceXLSX(file_name, alumnos):
  headers = []
  aprobados = 0
  for i in range(NOTAS[0]):
    headers.append("Nota"+str(i+1))
  headers.append("Probabilidad")
  book = xlsxwriter.Workbook(file_name)
  sheet = book.add_worksheet()
  hformat = book.add_format({'bg_color':'#FFEFD5'})
  passformat = book.add_format({'bg_color':'#5DE95D'})
  failformat = book.add_format({'bg_color':'#EF5050'})
  for i in range(len(headers)):
    sheet.write(0, i, headers[i], hformat)
  row=1
  col=0
  for grades in alumnos:
    diferencia = NOTAS[0] - len(grades)
    for i in range(len(grades)):
      sheet.write(row, i, grades[i])
    for j in range(i,NOTAS[0]):
      sheet.write(row,j, "?")
    if(grades[-1] > 0.5):
      aprobados += 1
      sheet.write(row, j+1, grades[-1], passformat)
    else:
      sheet.write(row, j+1, grades[-1], failformat)
    row += 1
  finalformat = book.add_format({'bg_color':'#B0C4DE', 'bold': True})
  sheet.write(row,0  ,"Aprobados", finalformat)
  for i in range(1,j+1):
    sheet.write(row, i ,"", finalformat)
  sheet.write(row,j+1,aprobados, finalformat)
  print("\n\nArchivo guardado como: " + file_name)
  book.close()

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
    for j in range(ALUMNOS_POR_CICLO):
      alumnos_de_curso.append(nuevo_estudiante())
    if (generate):
      produceCSV("CSVs/alumnos-"+CURSO[0]+"-mediociclo"+str(i+1)+".csv",alumnos_de_curso)
    NOTAS_POR_CICLO.append(alumnos_de_curso)

def parseData(file_name):
  with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        grades_row = 0
        grades=[]
        previo = ""
        for row in csv_reader:
          print(f'Column names are {", ".join(row)}')
          for i in range(len(row)):
            if(row[i] == "PUNTAJE"):
              grades_row = i
              break
          line_count += 1
          break
        for row in csv_reader:
          nombre = row[0]
          if(nombre == previo):
            if(row[grades_row].isnumeric()):
              grades.append(row[grades_row])
          else:
            previo = nombre
            NOTAS_POR_CICLO.append(grades)
            grades = []
            if(row[grades_row].isnumeric()):
              grades.append(row[grades_row])
          line_count += 1
        NOTAS_POR_CICLO.append(grades)
        del NOTAS_POR_CICLO[0]


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
          grades=[]
          if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
          else:
            for grade in row:
              grades.append(int(grade))
            line_count += 1
            all_grades.append(grades)
  return all_grades




def chances(needed_grade, until):
  cont = 0
  # print(NOTAS_POR_CICLO)
  for ciclo in NOTAS_POR_CICLO:
    for nota in ciclo:
      # print("Array analizing is ", j)
      achieved = desdeExamen(nota, until)
      # print(nota)
      if(achieved >= needed_grade):
        cont += 1
        #print(cont, end=", ")
  return cont

def chances2(needed_grade, until):
  achieved = []
  for ciclo in NOTAS_POR_CICLO:
    for nota in ciclo:
      single_achieved = desdeExamen(nota, until)
      if(single_achieved >= needed_grade):
        achieved.append(single_achieved)
      #achieved.append(desdeExamen(nota, until))
  mean = statistics.mean(achieved)
  stdv = statistics.stdev(achieved)
  print("Max = ", max(achieved))
  print("Min = ", min(achieved))
  print("Mean = ", mean)
  print("DV = ", stdv)
  data1 = np.random.normal(loc = mean, scale = stdv, size=100)
  fig, axs = plt.subplots(figsize = (10,5))
  axs.hist(achieved, bins = 25)
  axs.set_title("Histogram")
  plt.show()




def getRate(notas):
  current_grade = hastaExamen(notas, len(notas))
  needed_grade = NOTA_MINIMA - current_grade
  #chances2(needed_grade, len(notas))
  #print("Needed grade is", needed_grade)
  return chances(needed_grade, len(notas))/NUMERO_DE_ALUMNOS

def run():
    # getPercentages()
    parseData("./CSVs/Data_mini.csv")
    print(NOTAS_POR_CICLO)
    # crearData()
    # print("Ingrese la opcion de prediccion (1 o 2): \n1) Nota singular\n2) CSV de notas\n")
    # opcion = input("")
    # if (opcion == "1"):
    #   grades = getStudentGrades()
    #   print(getRate(grades))
    # else:
    #   rates = []
    #   file_name = input("Ingrese nombre de archivo CSV: ")
    #   all_grades = parseStudentGrades(file_name)
    #   rate = getRate(all_grades[0])
    #   for student in all_grades:
    #     rate = getRate(student)
    #     student.append(rate)
    #     print(rate)
    #   #produceXLSX("prediccion_"+CURSO[0]+".xlsx", all_grades)

run()

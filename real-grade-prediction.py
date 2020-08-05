import random
import math
import csv
import xlsxwriter
import matplotlib.pyplot as plt
import statistics
import scipy.stats
import numpy as np
CURSO = []
NOTAS = []
RATIO = []
TOTAL = []
MAX_POR_SALON = []
PORCENTAJES = []
NOTA_MINIMA = 10.5
HISTORIAL_NOTAS = []
DISTRIBUCIONES = {}
PRODUCIDO = []

def obtenerPorcentajes():
  CURSO.append(input("Ingrese nombre del curso"))
  MAX_POR_SALON.append(int(input("Numero de alumnos por sección en el curso:")))
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
      writer.writerow(alumno[0:-1])

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
    if(grades[-1] > 0.74):
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
  row+=1
  sheet.write(row,0  ,"Reprobados", finalformat)
  for i in range(1,j+1):
    sheet.write(row, i ,"", finalformat)
  sheet.write(row,j+1,row-aprobados-2, finalformat)
  row+=2
  sheet.write(row,0 ,"Habiles", finalformat)
  sheet.write(row,1 ,"Salones", finalformat)
  row+=1
  sheet.write(row,0 , TOTAL[1]-TOTAL[0], finalformat)
  print("----------------------------------------------------")
  print(TOTAL[1])
  print(TOTAL[0])
  sheet.write(row,1 , (TOTAL[1]-TOTAL[0])*RATIO[0]/MAX_POR_SALON[0], finalformat)
  print("\n\nArchivo guardado como: " + file_name)
  book.close()

def parseHabiles(file_name):
  rat = 0
  line_count = 0
  with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      if(line_count == 0):
        print(f'Column names are {", ".join(row)}')
      else:
        print(row[2])
        print(row[1])
        print(int(row[2])/int(row[1]))
        rat += int(row[2])/int(row[1])
      line_count += 1
  print("line count - 1 = ", (line_count-1))
  RATIO.append(rat/(line_count-1))

def parseData(file_name, all):
  with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    aprobados = 0
    reprobados = 0
    retirados = 0
    line_count = 1
    grades_row = 0
    grades=[]
    temp = []
    previo = ""
    guide = 2
    for row in csv_reader:
      print(f'Column names are {", ".join(row)}')
      for i in range(len(row)):
        if(row[i] == "PUNTAJE"):
          grades_row = i
          break
      line_count += 1
      break
    for row in csv_reader:
      line_count += 1
      nombre = row[0]
      if(nombre == previo):
        if(row[grades_row].isnumeric()):
          if(guide%2 == 0 or all):
            grades.insert(0,int(row[grades_row]))
            if(all):
              temp.insert(0,int(row[grades_row]))
          else:
            temp.insert(0,int(row[grades_row]))
          guide += 1
          #print("graded person is", row[1])
      else:
        previo = nombre
        if(guide != 0):
          #print("grades", grades, "\n\n")
          #print("guide", guide)
          #print("person is", row[1])
          #print("line", line_count)
          guide = 0
          HISTORIAL_NOTAS.append(grades)
          PRODUCIDO.append(temp)
        grades = []
        temp = []
        #print("Gonna append average", row[grades_row])
        if(row[grades_row].isnumeric()):
          grades.insert(0,int(row[grades_row]))
          if(int(row[grades_row]) > 10.5):
            aprobados += 1
          else:
            reprobados += 1
        else:
          retirados += 1
    HISTORIAL_NOTAS.append(grades)
    del HISTORIAL_NOTAS[0]
    
    del PRODUCIDO[0]
    print("APROBARON ", aprobados, " ALUMNOS")
    print("REPROBARON ", reprobados, " ALUMNOS")
    print("RETIRADOS ", retirados, " ALUMNOS")
    print(TOTAL)
    TOTAL.append(aprobados)
    print(TOTAL)

def displayData():
  for i in HISTORIAL_NOTAS:
    print("NUEVO CICLO")
    for j in i:
      print(j)

## Estimate final grades and probabilities ---------------------
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
          if(grade.isnumeric()):
            grades.append(int(grade))
        line_count += 1
        all_grades.append(grades)
  return all_grades

def chances(needed_grade, until):
  if(until not in DISTRIBUCIONES):
    achieved = []
    for nota in HISTORIAL_NOTAS:
      single_achieved = desdeExamen(nota, until)
      achieved.append(single_achieved)
      #achieved.append(desdeExamen(nota, until))
    mean = statistics.mean(achieved)
    stdv = statistics.stdev(achieved)
    nd = scipy.stats.norm(mean, stdv)
    DISTRIBUCIONES[until] = nd
  distribucion = DISTRIBUCIONES[until]
  prob = 1-distribucion.cdf(needed_grade)
  # data1 = np.random.normal(loc = mean, scale = stdv, size=1)
  # fig, axs = plt.subplots(figsize = (10,5))
  # axs.hist(achieved, bins = 20)
  # axs.set_title("Histogram")
  # plt.show()
  return prob

def getRate(notas):
  current_grade = hastaExamen(notas, len(notas))
  needed_grade = NOTA_MINIMA - current_grade
  return chances(needed_grade, len(notas))
  #return chances(needed_grade, len(notas))/NUMERO_DE_ALUMNOS

def run():
    obtenerPorcentajes()
    parsing_file = "Estadistica_2019_1"
    parsing_habiles = "Parsing_h4b1l3s"
    all = False
    new_parse = input("¿Va a ingresar datos nuevos con los que hacer el análisis? Recuerde que tiene que usar el formato definido y estar dentro de la carpeta 'CSVs'. (y/n) ") == "y"
    if new_parse:
      parsing_file = input("Ingrese nombre del archivo con datos para parsear: ")
      all = input("La data contiene datos de semana intermedia? y/n ") == "n"
      parsing_habiles = input("Ingrese nombre de archivo con datos de alumnos habiles: ")
    
    
    parseData("./CSVs/" + parsing_file+".csv", all)
    parseHabiles("./CSVs/" + parsing_habiles+".csv")
    produceCSV("CSVs/test_Arte_2019_1.csv", PRODUCIDO)

    total = int(input("Ingrese el número total de alumnos habilitados para el actual ciclo: "))
    TOTAL.append(total)
    TOTAL[1] += int(input("Ingrese el numero aproximado de alumnos que estaran habilitados el siguiente ciclo"))
    file_name = input("Ingrese nombre de archivo CSV: ")
    all_grades = parseStudentGrades("CSVs/"+file_name+".csv")
    for student in all_grades:
      rate = getRate(student)
      student.append(rate)
    produceXLSX("prediccion_"+file_name+".xlsx", all_grades)

run()

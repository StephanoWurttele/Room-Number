from tkinter import *
import random
import math
import csv
import xlsxwriter
import matplotlib.pyplot as plt
import statistics
import scipy.stats
import numpy as np
NOTAS = []
RATIO = []
TOTAL = []
MAX_POR_SALON = []
PORCENTAJES = []
NOTA_MINIMA = 10.5
HISTORIAL_NOTAS = []
DISTRIBUCIONES = {}
PRODUCIDO = []
PARSING_FILE = ["Estadistica_2019_1"]
PARSING_HABILES = ["Parsing_h4b1l3s"]
ALL = [False]

def obtenerPorcentajes():
  MAX_POR_SALON.append(int(maxStudents.get()))
  NOTAS.append(int(numberGrades.get()))
  for i in range(len(notasInput)):
    PORCENTAJES.append(float(notasInput[i][1].get()))

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
  duplicado = []
  for i in range(NOTAS[0]):
    duplicado.append(0)
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
  sheet.write(row,0 , TOTAL[1]-aprobados, finalformat)
  sheet.write(row,1 , (TOTAL[1]-aprobados)*RATIO[0]/MAX_POR_SALON[0], finalformat)
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
        rat += int(row[2])/int(row[1])
      line_count += 1
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
      else:
        previo = nombre
        if(guide != 0):
          guide = 0
          HISTORIAL_NOTAS.append(grades)
          PRODUCIDO.append(temp)
        grades = []
        temp = []
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
    TOTAL.append(aprobados)

## Estimate final grades and probabilities ---------------------
def parseStudentGrades(file_name):
  all_grades = []
  with open(file_name) as csv_file2:
    csv_reader2 = csv.reader(csv_file2, delimiter=',')
    line_count = 0
    for row in csv_reader2:
      grades=[]
      if line_count == 0:
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
  return prob

def getRate(notas):
  current_grade = hastaExamen(notas, len(notas))
  needed_grade = NOTA_MINIMA - current_grade
  return chances(needed_grade, len(notas))
  #return chances(needed_grade, len(notas))/NUMERO_DE_ALUMNOS

def parse():
    PARSING_FILE[0] = data_file_name.get()
    ALL[0] = var.get() == 0
    PARSING_HABILES[0] = habiles_file_name.get()

def run():
    obtenerPorcentajes()
    parseData("./CSVs/" + PARSING_FILE[0] + ".csv", ALL[0])
    parseHabiles("./CSVs/" + PARSING_HABILES[0] +".csv")
    # produceCSV("CSVs/test_Estadistica_2019_1.csv", PRODUCIDO)

    TOTAL.append(int(numberHabiles.get()))
    TOTAL[1] += int(numberNuevos.get())
    file_name = currentGrades.get()
    all_grades = parseStudentGrades("CSVs/"+file_name+".csv")
    for student in all_grades:
      rate = getRate(student)
      student.append(rate)
    produceXLSX("prediccion_"+file_name+"GUI.xlsx", all_grades)

def parseAndClose():
  parse()
  top.destroy()

def openParse():
  global data_file_name
  global habiles_file_name
  global var
  global top
  top = Toplevel()
  top.title("Parseo")
  top.geometry("500x200")
  data_text = Label(top, text="Nombre de archivo con data historica: ")
  var = IntVar()
  c = Checkbutton(top, text="¿Data contiene datos intermedios de ciclo?", variable=var)
  c.deselect()
  data_file_name = Entry(top)
  habiles_text = Label(top, text="Nombre de archivo con alumnos habiles: ")
  habiles_file_name = Entry(top)
  submit = Button(top, text="Submit", command=parseAndClose)
  data_text.pack()
  c.pack()
  data_file_name.pack()
  habiles_text.pack()
  habiles_file_name.pack()
  submit.pack()

def showSubmit():
  habiles_text.pack_forget()
  nuevos_text.pack_forget()
  mensaje_nuevos.pack_forget()
  mensaje_habiles.pack_forget()
  numberNuevos.pack_forget()
  numberHabiles.pack_forget()
  submit.pack_forget()
  habiles_text.pack(pady=(20,5))
  numberHabiles.pack()
  mensaje_habiles.pack()
  nuevos_text.pack(pady=(20,5))
  numberNuevos.pack()
  mensaje_nuevos.pack()
  submit.pack()
  temp = True
  x = 0
  for i in notasInputVars:
    if(i[1].cget("text") != " "):
      temp = False
      break
    x+=float(i[0].get())
  if x != 1:
    temp = False
  if(mensaje_notas.cget("text") == " " and mensaje_alumnos.cget("text") == " " and temp and mensaje_nuevos.cget("text") == " " and mensaje_habiles.cget("text") == " "):
    submit["state"] = "normal"
  else:
    submit["state"] = "disabled"

def percentageCheck():
    for i in notasInputVars:
      try:
        float(i[0].get())
        if(i[0].get().isdigit()):
          i[1].config(text="Por favor, ingrese un numero decimal en el porcentaje de nota")
        else:
          i[1].config(text=" ")
      except ValueError:
        i[1].config(text="Por favor, ingrese un numero decimal en el porcentaje de nota")
    showSubmit()

def habilesNumber():
  try:
    int(sv_habiles.get())
    mensaje_habiles.config(text=" ")
  except ValueError:
    mensaje_habiles.config(text="Por favor, ingrese un numero en el numero de alumnos por salon")
  showSubmit()

def nuevosNumber():
  try:
    int(sv_nuevos.get())
    mensaje_nuevos.config(text=" ")
  except ValueError:
    mensaje_nuevos.config(text="Por favor, ingrese un numero en el numero de alumnos por salon")
  showSubmit()

def studNumber():
  try:
    int(sv_alumnos.get())
    mensaje_alumnos.config(text=" ")
  except ValueError:
    mensaje_alumnos.config(text="Por favor, ingrese un numero en el numero de alumnos por salon")
  showSubmit()

def gradesNumber():
  try:
    mensaje_notas.config(text=" ")
    for i in notasInput:
      for j in i:
        j.pack_forget()
    for i in notasInputVars:
      i[1].pack_forget()

    notasInput.clear()
    notasInputVars.clear()
    for i in range(int(sv_grades.get())):
      sv_temp = StringVar()
      sv_temp.trace("w", lambda name, index, mode, sv_temp=sv_temp: percentageCheck())
      mensaje_temp = Label(top, text="")
      notasInputVars.append([sv_temp, mensaje_temp])

      temp1 = Label(top, text="Nota"+str(i+1)+":")
      temp2 = Entry(top, textvariable = notasInputVars[i][0])
      temp3 = [temp1, temp2]
      notasInput.append(temp3)
    for i in range(len(notasInput)):
        notasInput[i][0].pack()
        notasInput[i][1].pack()
        notasInputVars[i][1].pack()
  except ValueError:
    mensaje_notas.config(text="Por favor, ingrese un numero en el numero de notas")
  showSubmit()

def executeAndClose():
  run()
  top.destroy()

def openEjecutar():
  global habiles_text
  global nuevos_text
  global currentGrades
  global maxStudents
  global numberGrades
  global numberHabiles
  global numberNuevos
  global sv_grades
  global sv_alumnos
  global sv_nuevos
  global sv_habiles
  global top
  global mensaje_notas
  global mensaje_alumnos
  global mensaje_nuevos
  global mensaje_habiles
  global notasInputVars
  global notasInput
  global submit
  notasInput=[]
  notasInputVars=[]
  top = Toplevel()
  top.title("Run data")
  top.geometry("1000x700")
  scroll = Scrollbar(top, orient=VERTICAL)
  scroll.pack(side=RIGHT, fill=Y)

  course_text = Label(top, text="Nombre de archivo con notas: ")
  currentGrades = Entry(top)

  sv_alumnos = StringVar()
  sv_alumnos.trace("w", lambda name, index, mode, sv_alumnos=sv_alumnos: studNumber())
  maxstudents_text = Label(top, text="Número maximo de alumnos por salon: ")
  maxStudents = Entry(top, textvariable = sv_alumnos)
  mensaje_alumnos = Label(top, text="")

  sv_grades = StringVar()
  sv_grades.trace("w", lambda name, index, mode, sv_grades=sv_grades: gradesNumber())
  number_text = Label(top, text="Número de notas de curso: ")
  numberGrades = Entry(top, textvariable = sv_grades)
  mensaje_notas = Label(top, text="")

  sv_habiles = StringVar()
  sv_habiles.trace("w", lambda name, index, mode, sv_habiles=sv_habiles: habilesNumber())
  habiles_text = Label(top, text="Número de alumnos hábiles este ciclo: ")
  numberHabiles = Entry(top, textvariable = sv_habiles)
  mensaje_habiles = Label(top, text="")

  sv_nuevos = StringVar()
  sv_nuevos.trace("w", lambda name, index, mode, sv_nuevos=sv_nuevos: nuevosNumber())
  nuevos_text = Label(top, text="Número de alumnos nuevos para el siguiente ciclo: ")
  numberNuevos = Entry(top, textvariable = sv_nuevos)
  mensaje_nuevos = Label(top, text="")

  submit = Button(top, text="Submit", command=executeAndClose, state=DISABLED)

  course_text.pack(pady=(20,5))
  currentGrades.pack()

  maxstudents_text.pack(pady=(20,5))
  maxStudents.pack()
  mensaje_alumnos.pack()

  number_text.pack(pady=(20,5))
  numberGrades.pack()
  mensaje_notas.pack()
  
  habiles_text.pack(pady=(20,5))
  numberHabiles.pack()
  mensaje_habiles.pack()

  nuevos_text.pack(pady=(20,5))
  numberNuevos.pack()
  mensaje_nuevos.pack()

  submit.pack()

BGCOLOR = "#EFF0F1"
root = Tk()
root.configure(background=BGCOLOR)
root.geometry("500x200")

title = Label(root, text="Prediccion de salones", bg=BGCOLOR)
parsear = Button(root, text = "Ingresar nuevos datos para sistema", command = openParse)
ejecutar = Button(root, text = "Correr prediccion", command=openEjecutar)

title.pack()
parsear.pack(expand = 1)
ejecutar.pack(expand = 1)

mainloop()
#run()

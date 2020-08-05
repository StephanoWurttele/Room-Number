import csv


def parseData(input, output):
  with open(output, mode='w') as gradesfile:
    writer = csv.writer(gradesfile, delimiter=',')
    with open(input) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 1
      average_row = 0
      average_row = 0
      previo = ""
      nombre = ""
      pendiente = []
      for row in csv_reader:
        print(f'Column names are {", ".join(row)}')
        writer.writerow(row)
        for i in range(len(row)):
          if(row[i] == "PUNTAJE"):
            grades_row = i
          else:
            if(row[i] == "PROMEDIO FINAL"):
              average_row = i
        line_count += 1
        break
      for row in csv_reader:
        line_count += 1
        nombre = row[0]
        if(nombre == previo):
          if(changed):
            temp = row.copy()
            temp[grades_row] = promedio
            writer.writerow(temp)
            print(temp)
            writer.writerow(pendiente)
            changed = False
          if (row[grades_row] == "NP"):
            row[grades_row] = 0
          writer.writerow(row)
          print(row)
        else:
          pendiente = row.copy()
          if (pendiente[grades_row] == "NP"):
            pendiente[grades_row] = 0
          promedio = row[average_row]
          changed = True
          previo = row[0]

parseData("./CSVs/raw_arte.csv", "./CSVs/Arte_2019_1.csv")
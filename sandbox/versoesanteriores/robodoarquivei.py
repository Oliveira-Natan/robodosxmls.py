import os.path
import shutil
import pandas as pd
from datetime import datetime
import csv

source_of_files = r'C:\Users\felipe.rosa\Desktop\teste\source_of_files'
report_file = r'C:\Users\felipe.rosa\Desktop\teste\report'
files_destiny = r'C:\Users\felipe.rosa\Desktop\teste\destino'

# defining year, month and day
currentDay = datetime.now().day
if currentDay < 10:
    currentDay = '0' + str(currentDay)
else:
    currentDay = str(currentDay)

currentMonth = datetime.now().month
if currentMonth < 10:
    currentMonth = '0' + str(currentMonth)
else:
    currentMonth = str(currentMonth)

currentYear = datetime.now().year

# check and create new report
report_name = '\\robodoarquivei_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
try:
    df = pd.read_csv(report_file + report_name, header=None)
    file_names_report = df[0].to_list()
except:
    with open(report_file + report_name, 'w') as new_report:
        csv.writer(new_report)
    file_names_report = []

# for each file in source_of_files, if not  in file_names_report, copy and update report
for file in os.listdir(source_of_files):
    if file not in file_names_report:
        print('file not found: ', file)

        shutil.copy(source_of_files + '\\' + file, files_destiny)

        with open(report_file + report_name, "a") as report:
            report.write(file + '\n')
            report.close()
            print('added to report: ', file)
    else:
        print('found: ', file)

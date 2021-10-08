from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
import shutil
import pandas as pd
from datetime import datetime
import csv

source_of_files = r'F:\CentralDeNotas'
report_folder = r'F:\robodepdfs\reports'
path_temp_original = r'F:\robodepdfs\temp_original2'
path_temp_unificado = r'F:\robodepdfs\temp_unificados2'

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

# check and create new report for progress
report_name = '\\robodospdfs_2_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
try:
    df = pd.read_csv(report_folder + report_name, header=None)
    file_names_report = df[0].to_list()
except:
    with open(report_folder + report_name, 'w') as new_report:
        csv.writer(new_report)
    file_names_report = []

# check and create new report for error
report_error_name = '\\erros_do_robodospdfs_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
try:
    checking_report_error = pd.read_csv(report_folder + report_error_name, header=None)
except:
    with open(report_folder + report_error_name, 'w') as new_report_error:
        csv.writer(new_report_error)

# getting folders names on CentraldeNotas
source_of_files_year = source_of_files + '\\' + str(currentYear)  #..\CentraldeNotas\\2021\\Empresa01\\08'
paths_centraldenotas = [f.path + '\\' + str(currentMonth) for f in os.scandir(source_of_files_year) if f.is_dir()]  # listing folders names
print(paths_centraldenotas)

for path_centraldenotas in paths_centraldenotas:  # accessing each folder on CentraldeNotas
    for file in os.listdir(path_centraldenotas):  # getting files names on folder
        checking_erro_from_temp_original_to_temp_unificado = 0
        file_path = path_centraldenotas + "\\" + file  # creating file path for current file
        if file_path not in file_names_report:  # check if file path not is on the report
            if file.endswith(".pdf"):  # check if it is a pdf

                try:  # copy file from CentraldeNotas to temp_original
                    shutil.copy(file_path, path_temp_original)  # copying pdfs from CentraldeNotas to temp_original
                    print('copied from central_de_notas to temp_original: ', file)

                    with open(report_folder + report_name, "a") as report:  # include copied file on report
                        report.write(file_path + '\n')
                        report.close()
                        print('added to report: ', file)
                    
                    try:
                        # copying pdfs from temp_original to temp_unificados splitting if more than 01 page
                        for file_in_original in os.listdir(path_temp_original):  # on temp_original
                            if file_in_original.endswith(".pdf"):  # if file ends with .pdf
                                path_original_and_filename = os.path.join(path_temp_original, file_in_original)  # creating file path
                                with open(path_original_and_filename, 'rb') as pdf_file:  # read file as pdf_file
                                    pdf = PdfFileReader(pdf_file)
                                    number_of_pages = pdf.getNumPages()  # get number of pages from pdf
                                    if number_of_pages > 1:  # if more than 01 page, then try to split and delete original from temp_original
                                        try:
                                            file_base_name = file_in_original.replace('.pdf', '')  # getting pdf name
                                            pdf = PdfFileReader(path_original_and_filename)
                                            for page_number in range(pdf.getNumPages()):  # for each page of this pdf
                                                pdfWriter = PdfFileWriter()
                                                pdfWriter.addPage(pdf.getPage(page_number))

                                                with open(os.path.join(path_temp_unificado, '{0}_page{1}.pdf'.format(file_base_name, page_number + 1)), 'wb') as new_pdf:  # save new pdf for this page
                                                    pdfWriter.write(new_pdf)
                                                    new_pdf.close()
                                                    print('copied from temp_original to temp_unificados: ', path_temp_unificado, '{0}_page{1}.pdf'.format(file_base_name, page_number + 1))
                                            pdf_file.close()
                                            os.remove(path_original_and_filename)
                                        except:
                                            with open(report_folder + report_error_name, "a") as report_error:  # save error on relatorio_de_erros_dos_pdfs
                                                report_error.write(str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original + '\n')
                                                report_error.close()
                                            checking_erro_from_temp_original_to_temp_unificado += 1
                                            print('erro1')
                                            pass
                                    # if do not have more than 01 page, then move file from temp_original to temp_unificados
                                    else:  # if do not have more than 01 page, then move file from temp_original to temp_unificados
                                        try:
                                            pdf_file.close()
                                            shutil.copy(
                                                os.path.join(path_temp_original, file),
                                                os.path.join(path_temp_unificado, file))
                                            print(path_temp_unificado)
                                            print(file)
                                            print('moved from temp_original to temp_unificados: ', path_temp_unificado + file)
                                        except:
                                            with open(report_folder + report_error_name,
                                                      "a") as report_error:  # save error on relatorio_de_erros_dos_pdfs
                                                report_error.write(
                                                    str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original + '\n')
                                                report_error.close()
                                            checking_erro_from_temp_original_to_temp_unificado +=1
                                            print('erro2')
                                            pass
                    except:
                        with open(report_folder + report_error_name, "a") as report_error:  # save error on relatorio_de_erros_dos_pdfs
                            report_error.write(
                                str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original + '\n')
                            report_error.close()
                        checking_erro_from_temp_original_to_temp_unificado += 1
                        print('erro3')
                        pass
                except:
                    with open(report_folder + report_error_name, "a") as report_error:
                        report_error.write(str(datetime.now()) + "," + 'error on copy from central_de_notas to temp_original: ' + file_path + '\n')
                        report_error.close()
                    pass
        else:
            print('already copied: ', file_path)

        if checking_erro_from_temp_original_to_temp_unificado != 0:
            print('o erro foi detectado')
            # removing file from temp_original, so we can try again later
            with open(report_folder + report_name, "r") as text:
                text = ''.join([i for i in text])
                text = text.replace(file_path, "")

            with open(report_folder + report_name, "w") as x:
                x.writelines(text)
                x.close()
            os.remove(path_original_and_filename)
            print('reverted copy from CentraldeNotas to temp_original: ', file_path)

# import os
# os.startfile("C:\Documents and Settings\flow_model\flow.exe")
# source_of_files = r'C:\Users\felipe.rosa\Desktop\CentraldeNotas02'
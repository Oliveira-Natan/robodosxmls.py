from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
import shutil
import pandas as pd
from datetime import datetime
import csv

def creatingReports(currentDay, currentMonth, currentYear, report_folder, path_temp_original, path_temp_unificado, report_error_name):
    # check and create new report for progress
    # report_name = '\\robodeunificar_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
    # try:
    #     df = pd.read_csv(report_folder + report_name, header=None)
    #     file_names_report = df[0].to_list()
    # except:
    #     with open(report_folder + report_name, 'w') as new_report:
    #         csv.writer(new_report)
    #     file_names_report = []

    # check and create new report for error
    try:
        checking_report_error = pd.read_csv(report_folder + report_error_name, header=None)
    except:
        with open(report_folder + report_error_name, 'w') as new_report_error:
            csv.writer(new_report_error)

def individualizandoArquivos(currentDay, currentMonth, currentYear, report_folder, path_temp_original, path_temp_unificado, report_error_name):
    report_name = '\\robodeunificar_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
    try:
        df = pd.read_csv(report_folder + report_name, header=None)
        file_names_report = df[0].to_list()
    except:
        file_names_report = []

    for file_in_original in os.listdir(path_temp_original):  # on for each file on temp_original
        checking_erro_from_temp_original_to_temp_unificado = 0
        if file_in_original not in file_names_report:  # if not in list of unificado
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
                            with open(report_folder + report_name, "a") as report:  # include copied file on report
                                report.write(file_in_original + '\n')
                                report.close()
                                print('added to report: ', file_in_original)
                            os.remove(path_original_and_filename)
                        except:
                            with open(report_folder + report_error_name, "a") as report_error:  # save error on relatorio_de_erros_dos_pdfs
                                report_error.write(
                                    str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original + '\n')
                                report_error.close()
                            checking_erro_from_temp_original_to_temp_unificado += 1
                            print('erro1')
                            pass
                    # if do not have more than 01 page, then move file from temp_original to temp_unificados
                    else:  # if do not have more than 01 page, then move file from temp_original to temp_unificados
                        try:
                            pdf_file.close()
                            shutil.copy(
                                os.path.join(path_temp_original, file_in_original),
                                os.path.join(path_temp_unificado, file_in_original))
                            print('moved from temp_original to temp_unificados: ', file_in_original)
                        except:
                            with open(report_folder + report_error_name, "a") as report_error:  # save error on relatorio_de_erros_dos_pdfs
                                report_error.write(str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original + '\n')
                                report_error.close()
                            checking_erro_from_temp_original_to_temp_unificado += 1
                            print('erro2')
                            pass
                    if checking_erro_from_temp_original_to_temp_unificado != 0:
                        print('erro identificado durante o processo')
                        with open(report_folder + report_name, "r") as text:
                            text = ''.join([i for i in text])
                            text = text.replace(file_in_original, "")

                        with open(report_folder + report_name, "w") as x:
                            x.writelines(text)
                            x.close()

if __name__ == '__main__':
    report_folder = r'C:\Users\felipe.rosa\Desktop\New folder\reports'
    path_temp_original = r'C:\Users\felipe.rosa\Desktop\New folder\temp_original'
    path_temp_unificado = r'C:\Users\felipe.rosa\Desktop\New folder\temp_unificados'

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

    report_error_name = '\\erros_do_robodeunificar_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
    # creatingReports(currentDay, currentMonth, currentYear, report_folder, path_temp_original, path_temp_unificado, report_error_name)
    individualizandoArquivos(currentDay, currentMonth, currentYear, report_folder, path_temp_original, path_temp_unificado, report_error_name)
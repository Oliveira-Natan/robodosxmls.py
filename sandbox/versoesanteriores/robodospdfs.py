import time
from datetime import datetime
import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter

import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# path to pdf
path_centraldenotas = 'F:\CentralDeNotas\Modelo\\' + str(currentYear) + '\\' + str(currentMonth) + '\\' + str(currentDay) + '\\'
path_temp_original = 'F:\\robodepdfs\\temp_original\\'
path_temp_unificado = 'F:\\robodepdfs\\temp_unificados\\'
path_temp_unificado_enviados = 'F:\\robodepdfs\\temp_unificados_enviados\\'
path_relatorio_de_erros = 'F:\\robodepdfs\\relatorio_de_erros\\'


sender_email = "impostosretidos@mcsmarkup.com.br"
receiver_email = "felipe.rosa@mcsmarkup.com.br"
password = '50MCS14p@dr@o'

# copying pdfs from central de notas to temp_original
for file in os.listdir(path_centraldenotas):
    if file.endswith(".pdf"):
        try:
            path_centraldenotas_and_filename = os.path.join(path_centraldenotas, file)
            shutil.copy(path_centraldenotas_and_filename, path_temp_original)
            print('copied from central_de_notas to temp_original: ', path_temp_original, file)
        except:
            relatorio_de_erros = open(path_relatorio_de_erros, "a")
            relatorio_de_erros.write('\nerror on copy from central_de_notas to temp_original: ', path_temp_original, file)
            relatorio_de_erros.close()

        # copying pdfs from temp_original to temp_unificados splitting if more than 01 page
        for file_in_original in os.listdir(path_temp_original):
            if file_in_original.endswith(".pdf"):
                path_original_and_filename = os.path.join(path_temp_original, file_in_original)
                with open(path_original_and_filename, 'rb') as f1:
                    pdf = PdfFileReader(f1)
                    number_of_pages = pdf.getNumPages()
                    # print(file_in_original)
                    # print(number_of_pages)

# splitting pdf if more than 01 page
                    if number_of_pages > 1:
                        try:
                            file_base_name = file_in_original.replace('.pdf', '')
                            pdf = PdfFileReader(path_original_and_filename)

                            for page_number in range(pdf.getNumPages()):
                                pdfWriter = PdfFileWriter()
                                pdfWriter.addPage(pdf.getPage(page_number))

                                with open(os.path.join(path_temp_unificado, '{0}_page{1}.pdf'.format(file_base_name, page_number+1)),'wb') as f:
                                    pdfWriter.write(f)
                                    f.close()
                                    print('copied from temp_original to temp_unificados: ', path_temp_unificado, '{0}_page{1}.pdf'.format(file_base_name, page_number+1))

                                    subject = '{0}_page{1}.pdf'.format(file_base_name, page_number+1)
                                    body = ""

                                    # Create a multipart message and set headers
                                    message = MIMEMultipart()
                                    message["From"] = sender_email
                                    message["To"] = receiver_email
                                    message["Subject"] = subject

                                    # Add body to email
                                    message.attach(MIMEText(body, "plain"))

                                    filename = os.path.join(path_temp_unificado, '{0}_page{1}.pdf'.format(file_base_name, page_number+1))  # In same directory as script

                                    # Open PDF file in binary mode
                                    with open(str(filename), "rb") as attachment:
                                        # Add file as application/octet-stream
                                        # Email client can usually download this automatically as attachment
                                        part = MIMEBase("application", "octet-stream")
                                        part.set_payload(attachment.read())

                                    # Encode file in ASCII characters to send by email
                                    encoders.encode_base64(part)

                                    # Add header as key/value pair to attachment part
                                    part.add_header(
                                        "Content-Disposition",
                                        f"attachment; filename= {filename}",
                                    )

                                    # Add attachment to message and convert message to string
                                    message.attach(part)
                                    text = message.as_string()

                                    # Log in to server using secure context and send email
                                    context = ssl.create_default_context()
                                    with smtplib.SMTP("smtp.office365.com", 587) as server:
                                        server.starttls(context=context)
                                        server.login(sender_email, password)
                                        server.sendmail(sender_email, receiver_email, text)
                                    print('{0}_page{1}.pdf'.format(file_base_name, page_number+1), 'enviado por email')
                                    shutil.move(filename, path_temp_unificado_enviados)

                            f1.close()
                            os.remove(path_original_and_filename)

                        except:
                            relatorio_de_erros = open(path_relatorio_de_erros + 'relatorio_de_erros.txt', "a")
                            relatorio_de_erros.write('\n' + str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original)
                            relatorio_de_erros.close()
                            pass
                    else:
                        try:
                            shutil.copy(path_original_and_filename, path_temp_unificado)
                            print('copied from temp_original to temp_unificados: ', path_temp_unificado + file_in_original)
                            f1.close()
                            os.remove(path_original_and_filename)

                            subject = file_in_original
                            body = ""

                            # Create a multipart message and set headers
                            message = MIMEMultipart()
                            message["From"] = sender_email
                            message["To"] = receiver_email
                            message["Subject"] = subject

                            # Add body to email
                            message.attach(MIMEText(body, "plain"))

                            filename = os.path.join(path_temp_unificado + file_in_original)  # In same directory as script

                            # Open PDF file in binary mode
                            with open(filename, "rb") as attachment:
                                # Add file as application/octet-stream
                                # Email client can usually download this automatically as attachment
                                part = MIMEBase("application", "octet-stream")
                                part.set_payload(attachment.read())

                            # Encode file in ASCII characters to send by email
                            encoders.encode_base64(part)

                            # Add header as key/value pair to attachment part
                            part.add_header(
                                "Content-Disposition",
                                f"attachment; filename= {filename}",
                            )

                            # Add attachment to message and convert message to string
                            message.attach(part)
                            text = message.as_string()

                            # Log in to server using secure context and send email
                            context = ssl.create_default_context()
                            with smtplib.SMTP("smtp.office365.com", 587) as server:
                                server.starttls(context=context)
                                server.login(sender_email, password)
                                server.sendmail(sender_email, receiver_email, text)
                            print(file_in_original, 'enviado por email')
                            shutil.move(filename, path_temp_unificado_enviados)
                        except:
                            relatorio_de_erros = open(path_relatorio_de_erros + 'relatorio_de_erros.txt', "a")
                            relatorio_de_erros.write('\n' + str(datetime.now()) + "," + 'error on copy temp_original to temp_unificados' + "," + path_temp_unificado + file_in_original)
                            relatorio_de_erros.close()
                            pass

# Criar função de enviar erro para  email

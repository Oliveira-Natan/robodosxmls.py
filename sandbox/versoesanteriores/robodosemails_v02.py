from datetime import datetime
import os
import shutil
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


path_temp_unificado = 'F:\\robodepdfs\\temp_unificados\\'
path_temp_unificado_enviados = 'F:\\robodepdfs\\temp_unificados_enviados\\'
path_relatorio_de_erros = 'F:\\robodepdfs\\relatorio_de_erros\\'
sender_email = "impostosretidos@mcsmarkup.com.br"
receiver_email = "nfse@cloudfiscal.com"
password = '50MCS14p@dr@o'

for file in os.listdir(path_temp_unificado):
    if file.endswith(".pdf"):
        try:
            path_temp_unificado_and_filename = os.path.join(path_temp_unificado, file)
            file_base_name = file.replace('.pdf', '')

            subject = file_base_name
            body = ""
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # Add body to email
            message.attach(MIMEText(body, "plain"))

            # Open PDF file in binary mode
            with open(str(path_temp_unificado_and_filename), "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file}",
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
            print('enviado por email: ', file_base_name)
            shutil.move(path_temp_unificado_and_filename, os.path.join(path_temp_unificado_enviados, file))
        except:
            relatorio_de_erros = open(path_relatorio_de_erros + 'relatorio_de_erros_de_envio.txt', "a")
            relatorio_de_erros.write('\n' + str(datetime.now()) + "," + 'error while sending file' + "," + file)
            print('\n' + str(datetime.now()) + "," + 'error while sending file' + "," + file)
            relatorio_de_erros.close()
            pass



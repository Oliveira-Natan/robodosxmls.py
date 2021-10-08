from datetime import datetime
import os
import shutil
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

start = datetime.now()
def uploadingReport(action_list, reportrobodosemails):
    robo_data = pd.read_csv(path_report + reportrobodosemails)

    # appending action to reportdosrobos
    action_list = pd.Series(action_list, index=robo_data.columns)
    robo_data = robo_data.append(action_list, ignore_index=True)
    robo_data.to_csv(path_report + reportrobodosemails, index=False)
    robo_data = pd.read_csv(path_report + reportrobodosemails)

def uploadingReportError(action_list, reportdosrobos_erros):
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)  # lendo o csv de erros no formato de df

    # appending error to reportdosrobos_erros
    action_list = pd.Series(action_list, index=robo_data_error.columns)
    robo_data_error = robo_data_error.append(action_list, ignore_index=True)  # incluindo novo erro no csv de erros
    robo_data_error.to_csv(path_report + reportdosrobos_erros, index=False)  # salvando DF de erro em CSV
    # robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

def enviarEmail(file, path_temp_individualizado, sender_email, receiver_email, password):
    if file.endswith(".pdf"):
        path_temp_unificado_and_filename = os.path.join(path_temp_individualizado, file)
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

        # movendo arquivo enviado de individualizado para enviados
        shutil.move(path_temp_unificado_and_filename, os.path.join(path_temp_individualizados_enviados, file))

def enviarEmaildeNovosarquivos(lista_de_xmls_enviados, sender_email, analista_de_retenção_email, password):
    port = 587  # For SSL
    smtp_server = "smtp.office365.com"
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = analista_de_retenção_email
    message["Subject"] = "Novos XMLs no CloudFiscal"

    # Create the plain-text of your message
    quantidade_de_xmls_enviados = len(lista_de_xmls_enviados)
    user = analista_de_retenção_email.split('.')[0].capitalize()

    body = "Olá, {}.".format(user) + \
           ("\n\nO seguinte XML acabou de ser enviado para o CloudFiscal:\n\n"
            if quantidade_de_xmls_enviados <= 1
            else
            "\n\n{} XMLs acabaram de ser enviados para o CloudFiscal e seus nomes são:\n\n".format(
                quantidade_de_xmls_enviados)) + \
           "".join(str(xml_enviado) + '\n' for xml_enviado in lista_de_xmls_enviados) + \
           "\nAtenciosamente, \nRobodosEmails \nSquad de Inovação"

    # Turn these into plain/html MIMEText objects
    body = MIMEText(body, "plain")

    # Add plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, analista_de_retenção_email, message.as_string())

    return 'Upload para o CloudFiscal informado ao analista de retenção'


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

# main paths

# path_report = r"C:\Users\felipe.rosa\Desktop\New folder\report"
# path_temp_original = r'C:\Users\felipe.rosa\Desktop\New folder\temp_original'
# path_temp_individualizados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados'
# path_temp_individualizados_enviados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados_enviados'

path_centraldenotas = r'F:\CentralDeNotas'
path_report = r"F:\robodepdfs\reports"
path_temp_original = r'F:\robodepdfs\temp_original'
path_temp_individualizados = r'F:\robodepdfs\temp_individualizados'
path_temp_individualizados_enviados = r'F:\robodepdfs\temp_individualizados_enviados'
path_arquivei = r'F:\Fiscal\Clientes Fiscal\Arquivei - Armazenamento de XML'
path_cloudFiscal = r'F:\Impostos Retidos\Conversor FIT'

# reports names
reportrobodeindividualizacao = '\\robodeindividualizacao_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportdosrobos_erros = '\\errosdosrobos_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodospdfs = '\\robodospdfs_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodosemails = '\\robodosemails_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodoarquivei = '\\robodoarquivei_' + str(currentYear) + '_' + str(currentMonth) + '.csv'

# sender_email = "impostosretidos@mcsmarkup.com.br"
# password = '50MCS14p@dr@o'

sender_email = "mcstools.resumocfop@outlook.com"
password = "markuptools@2021"

receiver_email = "nfse@cloudfiscal.com"

analista_de_retenção_email = "natan.oliveira@mcsmarkup.com.br"

# start process
# if len(os.listdir(path_temp_individualizados)) != 0:
#     lista_de_xmls_enviados = []
#     for file in os.listdir(path_temp_individualizados):
#         # try:
#         enviarEmail(file, path_temp_individualizados, sender_email, receiver_email, password)
#         action_list = [datetime.now(), 'robodosemails', 'temp_individualizados to temp_individualizados_enviados',
#                        path_temp_individualizados + "\\" + file]
#         uploadingReport(action_list, reportrobodosemails)
#         print('Report do Robo dos Emails atualizado com sucesso')
#         lista_de_xmls_enviados.append(file)
#     # except:
#     #     action_list = [datetime.now(), 'robodosemails', 'ERROR: temp_individualizados to temp_individualizados_enviados', path_temp_individualizados + "\\" + file]
#     #     uploadingReportError(action_list, reportdosrobos_erros)
#     #     print('ERROR: Report de erro dos robos atualizado com sucesso')
#     enviarEmaildeNovosarquivos = enviarEmaildeNovosarquivos(lista_de_xmls_enviados, sender_email,
#                                                             analista_de_retenção_email, password)
#     print(enviarEmaildeNovosarquivos)

# try:
if len(os.listdir(path_temp_individualizados)) != 0:
    lista_de_xmls_enviados = []
    for file in os.listdir(path_temp_individualizados):
        # try:
        enviarEmail(file, path_temp_individualizados, sender_email, receiver_email, password)
        action_list = [datetime.now(), 'robodosemails', 'temp_individualizados to temp_individualizados_enviados',
                       path_temp_individualizados + "\\" + file]
        uploadingReport(action_list, reportrobodosemails)
        print('Report do Robo dos Emails atualizado com sucesso')
        lista_de_xmls_enviados.append(file)
        # except:
        #     action_list = [datetime.now(), 'robodosemails', 'ERROR: temp_individualizados to temp_individualizados_enviados', path_temp_individualizados + "\\" + file]
        #     uploadingReportError(action_list, reportdosrobos_erros)
        #     print('ERROR: Report de erro dos robos atualizado com sucesso')
    enviarEmaildeNovosarquivos = enviarEmaildeNovosarquivos(lista_de_xmls_enviados, sender_email,
                                                            analista_de_retenção_email, password)
    print(enviarEmaildeNovosarquivos)
else:
    print('Não há arquivos novos a serem enviados')
# except:
#     action_list = [datetime.now(), 'robodosemails', 'ERROR: problemas ao processar o robo de envio', path_temp_individualizados_enviados]
#     uploadingReportError(action_list, reportdosrobos_erros)
#     print('ERROR: Report de erro dos robos atualizado com sucesso (problemas ao processar o robo de envio)')

end = datetime.now()
print(end-start)

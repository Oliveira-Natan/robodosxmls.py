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
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

    # appending error to reportdosrobos_erros
    action_list = pd.Series(action_list, index=robo_data_error.columns)
    robo_data_error = robo_data_error.append(action_list, ignore_index=True)
    robo_data_error.to_csv(path_report + reportdosrobos_erros, index=False)
    robo_data_error = pd.read_csv(path_report + reportdosrobos_erros)

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
        shutil.move(path_temp_unificado_and_filename, os.path.join(path_temp_individualizados_enviados, file))


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
path_report = r"C:\Users\felipe.rosa\Desktop\New folder\report"
path_centraldenotas = r'C:\Users\felipe.rosa\Desktop\centraldenotas'
path_temp_original = r'C:\Users\felipe.rosa\Desktop\New folder\temp_original'
path_temp_individualizados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados'
path_temp_individualizados_enviados = r'C:\Users\felipe.rosa\Desktop\New folder\temp_individualizados_enviados'
path_arquivei = r'C:\Users\felipe.rosa\Desktop\arquivei'
path_cloudFiscal = r'C:\Users\felipe.rosa\Desktop\cloudfiscal_fit'

# reports names
reportrobodeindividualizacao = '\\robodeindividualizacao_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportdosrobos_erros = '\\errosdosrobos_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodospdfs = '\\robodospdfs_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodosemails = '\\robodosemails_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
reportrobodoarquivei = '\\robodoarquivei_' + str(currentYear) + '_' + str(currentMonth) + '.csv'
sender_email = "impostosretidos@mcsmarkup.com.br"
# receiver_email = "nfse@cloudfiscal.com"
receiver_email = "felipe.rosa@mcsmarkup.com.br"  # e-mail for testing
password = '50MCS14p@dr@o'

# start process
for file in os.listdir(path_temp_individualizados):
    try:
        enviarEmail(file, path_temp_individualizados, sender_email, receiver_email, password)
        action_list = [datetime.now(), 'robodosemails', 'temp_individualizados to temp_individualizados_enviados', path_temp_individualizados + "\\" + file]
        uploadingReport(action_list, reportrobodosemails)
        print('Report do Robo dos Emails atualizado com sucesso')
    except:
        action_list = [datetime.now(), 'robodosemails', 'ERROR: temp_individualizados to temp_individualizados_enviados', path_temp_individualizados + "\\" + file]
        uploadingReportError(action_list, reportdosrobos_erros)
        print('ERROR: Report de erro dos robos atualizado com sucesso')

end = datetime.now()
print(end-start)

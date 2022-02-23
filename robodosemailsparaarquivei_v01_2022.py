import time

from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
import shutil
from datetime import datetime
import pandas as pd
import win32api
from subprocess import call
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from os import listdir
from smtplib import SMTP
import shutil
import ssl
from string import Template
import getpass

start = datetime.now()
EMAIL_REMETENTE = "impostosretidos@mcsmarkup.com.br"
SENHA_REMETENTE = "50MCS14p@dr@o"
EMAIL_DESTINATARIO = "mcsmarkup@ocr.arquivei.com.br"
EMAIL_ANALISTA = "natan.oliveira@mcsmarkup.com.br"

def listardiretorios(path):
    listadediretorios = []
    print('Iniciando listagem de diretorios')
    for root, dirs, files in os.walk(path):  # PARA cada raiz, diretorio, NO arvore gerada a partir do diretorio da central de notas
        root_sem_prefixo = root.replace(str(path), "")
        for dir in dirs:  # PARA cada diretorio na lista de diretorios
            listadediretorios.append(os.path.join(root_sem_prefixo, dir))  # raiz do diretorio + diretorio
    return listadediretorios

def diretoriosparacriar(diretorios_do_path_origem_atual, diretorios_da_path_destino_atual):
    print('Iniciando criacao diretorios_da_path_destino_atual')
    diretorios_para_criar_list = []
    for item in diretorios_do_path_origem_atual:
        if item not in diretorios_da_path_destino_atual:
            # print('criar diretorio: ', item)
            diretorios_para_criar_list.append(item)
    print('total de diretorios_para_criar_na_fase_atual: ', len(diretorios_para_criar_list))
    return diretorios_para_criar_list

def criardiretorios(path_destino_atual, diretoriosparacriar_list):
    for diretoriosparacriar in diretoriosparacriar_list:
        nome_do_novo_diretorio = path_destino_atual + "\\" + diretoriosparacriar
        os.makedirs(nome_do_novo_diretorio)
        print('Criado o diretorio: ', nome_do_novo_diretorio)

def listaarquivosjaprocessadosnafaseatual(reportdafaseatual):
    print('Iniciando listagem de listaarquivosjaprocessadosnafaseatual')
    df = pd.read_csv(reportdafaseatual)
    arquivosjaprocessadosnafaseatual_list = df['path'].to_list()  # quero a coluna do report onde registrei a origem do que já copiei da central de notas
    print('total de listaarquivosjaprocessadosnafaseatual: ', len(arquivosjaprocessadosnafaseatual_list))
    return arquivosjaprocessadosnafaseatual_list

def listaarquivosprocessadosnafaseanterior(reportdafaseanterior):
    print('Iniciando listagem de listaarquivosprocessadosnafaseanterior')
    df = pd.read_csv(reportdafaseanterior)
    arquivosprocessadosnafaseanterior_list = df.loc[:, ['id', 'serie', 'destiny']].values.tolist()  # quero a coluna do report do onedrive onde registrei o destino da copia na central
    print('total de listaarquivosprocessadosnafaseanterior: ', len(arquivosprocessadosnafaseanterior_list))
    return arquivosprocessadosnafaseanterior_list

def listaarquivosparaprocessarnafaseatual(arquivosprocessadosnafaseanterior_list, arquivosjaprocessadosnafaseatual_list, path_origem_atual, path_destino_atual):
    print('Iniciando listagem de listaarquivosparaprocessarnafaseatual')
    path_files_to_copy = []
    for id, serie, item in arquivosprocessadosnafaseanterior_list:
        if item not in arquivosjaprocessadosnafaseatual_list:
            path_files_to_copy.append([id, serie, item, item.replace('temp_individualizados', 'temp_enviados')]) # id, origem, destino
    print('total de listaarquivosparaprocessarnafaseatual: ', len(path_files_to_copy))
    return path_files_to_copy

def processamento(origem, destino):
    shutil.copy(origem, destino)  # copiando pdfs do individualizado para enviados

def enviar_email(origem, destino, path_destino_atual, id, serie, tentativa):
    print(tentativa)
    nome_arquivo = origem.split('\\')[-1]
    if not nome_arquivo.replace("PDF", "pdf").endswith(".pdf"):
        return

    assunto_email = str(id) + "|" + str(serie) + "|" + nome_arquivo.replace(".pdf", "").replace(".PDF", "")
    caminho_arquivo = origem
    with open(caminho_arquivo, "rb") as anexo:
        pdf = MIMEApplication(anexo.read(), _subtype="pdf")
        pdf.add_header(
            "content-disposition",
            "attachment",
            filename=nome_arquivo,
        )

    email = MIMEMultipart(_subparts=(MIMEText("", _charset="UTF-8"), pdf))
    email["From"] = EMAIL_REMETENTE
    email["To"] = EMAIL_DESTINATARIO
    email["Subject"] = assunto_email

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with SMTP("smtp.office365.com", 587) as server:
        server.starttls(context=context)
        server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, email.as_string())
    print(f"enviado por email: {assunto_email}")
    return assunto_email


def enviar_email_novos_arquivos(arquivos):
    if len(arquivos) == 0:
        print("Nenhum arquivo foi processado")
        return

    template = None
    nome_template = "plural" if len(arquivos) > 1 else "singular"
    arquivo_template = f"envio_arquivei_{nome_template}.txt"
    caminho_tempalte = Path("mcstoolsretencoes/templates") / arquivo_template
    with open(caminho_tempalte) as template_file:
        template = Template(template_file.read())

    if template is None:
        print("Erro ao ler o template de email")
        return

    nome = EMAIL_ANALISTA.split(".")[0].capitalize()
    corpo_email = template.substitute(
        NOME=nome,
        ARQUIVOS="\n".join(arquivos),
        QTD=len(arquivos),
    )
    email = MIMEMultipart()
    email["From"] = EMAIL_REMETENTE
    email["To"] = EMAIL_ANALISTA
    email["Subject"] = "Novos PDF's enviados Arquivei"
    email.attach(MIMEText(corpo_email, _charset="UTF-8"))

    context = ssl.create_default_context()
    with SMTP("smtp.office365.com", 587) as server:
        server.starttls(context=context)
        server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        server.sendmail(EMAIL_REMETENTE, EMAIL_ANALISTA, email.as_string())
    print("Envio informado ao {}".format(nome))

def uploadingReport(action_list, reportdafaseatual):
    robo_data = pd.read_csv(reportdafaseatual)
    action_list = pd.Series(action_list, index=robo_data.columns)  # convertendo lista de acao em serie
    robo_data = robo_data.append(action_list, ignore_index=True)  # appending serie no report
    robo_data.to_csv(reportdafaseatual, index=False)  # salvando report

def uploadingReportError(action_list, reportdosrobos_erros):
    robo_data_error = pd.read_csv(reportdosrobos_erros)
    action_list = pd.Series(action_list, index=robo_data_error.columns)  # convertendo lista de acao em serie
    robo_data_error = robo_data_error.append(action_list, ignore_index=True)  # appending serie no report
    robo_data_error.to_csv(reportdosrobos_erros, index=False)  # salvando report
    time.sleep(1)

# path and reports names
username = getpass.getuser()
onedrive_path = r'C:\Users\{}\OneDrive - MCS MARKUP AUDITORIA E CONSULTORIA EMPRESARIAL LTDA\CentraldeNotas'.format(username)
robo_path = r'C:\Users\{}\Desktop\rede\robodepdfs'.format(username)

centraldosrobos_path = r'{}\centraldosrobos'.format(robo_path)
temp_original_path = r'{}\temp_original'.format(robo_path)
temp_individualizados_path = r'{}\temp_individualizados'.format(robo_path)
temp_enviados_path = r'{}\temp_enviados'.format(robo_path)

reportdosrobos_erros = r'{}\reports\errosdosrobos.csv'.format(robo_path)
report_robodoonedrive = r'{}\reports\robodoonedrive.csv'.format(robo_path)
report_robodospdfs = r'{}\reports\robodospdfs.csv'.format(robo_path)
report_robodeindividualizacao = r'{}\reports\robodeindividualizacao.csv'.format(robo_path)
report_robodosemailsparaarquivei = r'{}\reports\robodosemails.csv'.format(robo_path)

reportdafaseanterior = report_robodeindividualizacao
reportdafaseatual = report_robodosemailsparaarquivei
path_origem_atual = temp_individualizados_path
path_destino_atual = temp_enviados_path

## TRATAMENTO DE FOLDERS: clonando estrutura da fase anterior para a fase atual
diretorios_do_path_origem_atual = listardiretorios(path_origem_atual)  # listar estrutura de pasta da fase anterior
diretorios_da_path_destino_atual = listardiretorios(path_destino_atual)  # listar estrutura de pasta da fase atual
diretoriosparacriar_list = diretoriosparacriar(diretorios_do_path_origem_atual, diretorios_da_path_destino_atual)  # identifica novas pastas na estrutura atual
if diretoriosparacriar_list != 0:
    criardiretorios(path_destino_atual, diretoriosparacriar_list)  # cria novas pastas na estrutura atual

## TRATAMENTO DE ARQUIVOS
print('----------')
arquivosjaprocessadosnafaseatual_list = listaarquivosjaprocessadosnafaseatual(reportdafaseatual)  # lista arquivosjaprocessadosnafaseatual
print('----------')
arquivosprocessadosnafaseanterior_list = listaarquivosprocessadosnafaseanterior(reportdafaseanterior)  # listar arquivosprocessadosnafaseanterior
print('----------')
arquivosparaprocessarnafaseatual_list = listaarquivosparaprocessarnafaseatual(arquivosprocessadosnafaseanterior_list, arquivosjaprocessadosnafaseatual_list, path_origem_atual, path_destino_atual)  # listar arquivosparaprocessarnafaseatual

n = 0
e = 0
pdfs_enviados_list = []
if len(arquivosparaprocessarnafaseatual_list) > 0:
    # iniciar copia
    for id, serie, origem, destino in arquivosparaprocessarnafaseatual_list:
        if "\\?\\" in origem:
            origem = origem.replace("\\?\\", "").replace("\\\\", "\\")

        if "\\?\\" in destino:
            destino = destino.replace("\\?\\", "").replace("\\\\", "\\")
        origem = robo_path + origem
        destino = robo_path + destino
        try:
            assunto_email = enviar_email(origem, destino, path_destino_atual, id, serie, 'tentativa01')  # copiando arquivos (arquivosparaprocessarnafaseatual) da central dos robos para a temp_original (path_destino_atual)
            processamento(origem, destino)  # copiando arquivos (arquivosparaprocessarnafaseatual) da central dos robos para a temp_original (path_destino_atual)
            action_list = [id, serie, datetime.now(), 'robodosemails', 'individualizados to enviados', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
            uploadingReport(action_list, reportdafaseatual)
            pdfs_enviados_list.append(assunto_email)
            print(n, 'Processado item: ', id, 'serie: ', serie)
            n += 1
        except:
            try:  # TENTANDO NOVAMENTE, MAS COM REDUCAO DO NOME DO DIRETORIO
                assunto_email = enviar_email("\\\\?\\" + origem, "\\\\?\\" + destino, path_destino_atual, id, serie, 'tentativa02')  # copiando arquivos (arquivosparaprocessarnafaseatual) da central dos robos para a temp_original (path_destino_atual)
                processamento("\\\\?\\" + origem, "\\\\?\\" + destino)
                action_list = [id, serie, datetime.now(), 'robodosemails', 'individualizados to enviados', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
                uploadingReport(action_list, reportdafaseatual)
                pdfs_enviados_list.append(assunto_email)
                print(n, 'Processado item: ', id, 'serie: ', serie)
                n += 1
            except:
                try:  # TENTANDO NOVAMENTE, MAS COM OUTRA TECNICA DE REDUCAO DO NOME DO DIRETORIO
                    destino_curto = os.path.dirname(os.path.abspath(destino))  # pega o diretorio do arquivo, sem o nome
                    destino_curto = win32api.GetShortPathName(destino_curto)  # deixa o diretorio do arquivo menor

                    filename = origem.split('\\')[-1]  # pega o nome do arquivo
                    origem_curto = os.path.dirname(os.path.abspath(origem))  # pega o diretorio do arquivo, sem o nome
                    origem_curto = win32api.GetShortPathName(origem_curto)  # deixa o diretorio do arquivo menor
                    origem_curto = origem_curto + '\\' + filename  # remonta a origem: diretorio menor + nome do arquivo

                    assunto_email = enviar_email("\\\\?\\" + origem_curto, "\\\\?\\" + destino_curto, path_destino_atual, id, serie, 'tentativa03')  # copiando arquivos (arquivosparaprocessarnafaseatual) da central dos robos para a temp_original (path_destino_atual)
                    processamento("\\\\?\\" + origem_curto, "\\\\?\\" + destino_curto)

                    action_list = [id, serie, datetime.now(), 'robodosemails', 'individualizados to enviados', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
                    uploadingReport(action_list, reportdafaseatual)
                    pdfs_enviados_list.append(assunto_email)
                    print(n, 'Processado item: ', id, 'serie: ', serie)
                    n += 1
                except:
                    action_list = [id, serie, datetime.now(), 'robodosemails', 'ERROR: individualizados to enviados', origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"), destino.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\")]
                    uploadingReportError(action_list, reportdosrobos_erros)
                    print('ERROR: Report de erro dos robos atualizado com sucesso: ', str(id) + "|" + str(serie), "diretorio: ", origem.replace(robo_path, '').replace("\\?\\", "").replace("\\\\", "\\"))
                    e += 1
    enviar_email_novos_arquivos(pdfs_enviados_list)
else:
    print('Não há arquivos novos a serem copiados')
print('Total de arquivos na central conforme reportdorobodoonedrive: ', len(arquivosparaprocessarnafaseatual_list))
print('Total de arquivos antigos no report: ', len(arquivosjaprocessadosnafaseatual_list))
print('Total de arquivos novos copiados para o report: ', n)
print('Total de erros: ', e)
end = datetime.now()
print('Time running: ', end-start)


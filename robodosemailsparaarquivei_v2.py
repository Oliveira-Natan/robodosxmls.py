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

from mcstoolsretencoes.utils.diretorio import Diretorio
from mcstoolsretencoes.utils.relatorio import Relatorio, NomeRobo


EMAIL_REMETENTE = "impostosretidos@mcsmarkup.com.br"
SENHA_REMETENTE = "50MCS14p@dr@o"
EMAIL_DESTINATARIO = "mcsmarkup@ocr.arquivei.com.br"
EMAIL_ANALISTA = "natan.oliveira@mcsmarkup.com.br"


def enviar_email(nome_arquivo):
    if not nome_arquivo.replace("PDF", "pdf").endswith(".pdf"):
        return

    assunto_email = nome_arquivo.replace(".pdf", "")
    caminho_arquivo = Path(Diretorio.TEMP_INDIVIDUALIZADOS) / nome_arquivo
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
    # fmt: off
    destino_arquivo = Path(Diretorio.TEMP_INDIVIDUALIZADOS_ENVIADOS_ARQUIVEI) / nome_arquivo
    shutil.move(caminho_arquivo, destino_arquivo)


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


def run():
    if len(listdir(Diretorio.TEMP_INDIVIDUALIZADOS)) == 0:
        print("Não há arquivos para enviar")
        return

    lista_de_xmls_enviados = []
    relatorio_envio = Relatorio(
        diretorio_envios=Diretorio.TEMP_INDIVIDUALIZADOS,
        arquivo=NomeRobo.ROBO_EMAILS_ARQUIVEI,
        nome_robo="robodosemailsparaarquivei",
        acao="temp_individualizados to temp_individualizados_enviados_arquivei",
    )
    relatorio_erro = Relatorio(
        diretorio_envios=Diretorio.TEMP_INDIVIDUALIZADOS,
        arquivo=NomeRobo.ROBO_ERROS,
        nome_robo="robodosemails",
        acao="ERROR: temp_individualizados to temp_individualizados_enviados_arquivei",
    )
    for arquivo in listdir(Diretorio.TEMP_INDIVIDUALIZADOS):
        try:
            enviar_email(arquivo)
            relatorio_envio.registrar(arquivo)
            lista_de_xmls_enviados.append(arquivo)
        except:
            relatorio_erro.registrar(arquivo)
    enviar_email_novos_arquivos(lista_de_xmls_enviados)


if __name__ == "__main__":
    start = datetime.now()
    run()
    end = datetime.now()
    print(f"Tempo de execução: {end - start}")

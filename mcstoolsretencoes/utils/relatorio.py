from datetime import datetime
from pathlib import Path
from os.path import isfile

from pandas import DataFrame


BASE_DIR = Path(r"F:\robodepdfs\reports")


class NomeRobo:
    ROBO_INDIVIDUALIZACAO = "robodeindividualizacao"
    ROBO_ERROS = "errosdosrobos"
    ROBO_PDF = "robodospdfs"
    ROBO_EMAILS = "robodosemails"
    ROBO_EMAILS_ARQUIVEI = "robodosemailsarquivei"
    ROBO_DO_ARQUIVEI = "robodoarquivei"


class Relatorio:
    def __init__(
        self,
        diretorio_envios: str,
        arquivo: str,
        nome_robo: str,
        acao: str,
    ):
        data = datetime.now()
        self.ano = data.year
        self.mes = f"{data.month:01}"
        self.diretorio = BASE_DIR
        self.diretorio_envios = diretorio_envios
        self.arquivo = self._gerar_arquivo(arquivo)
        self.nome_robo = nome_robo
        self.acao = acao

    def _gerar_arquivo(self, nome):
        arquivo = f"{nome}_{self.ano}_{self.mes}.csv"
        path_arquivo = Path(self.diretorio) / arquivo
        if isfile(path_arquivo) is False:
            msg = (
                f"Criando arquivo {arquivo} para o robo {self.nome_robo} "
                "para a data de {self.ano}-{self.mes}..."
            )
            with open(path_arquivo, "w") as arquivo:
                arquivo.write("time,nomedorobo,acao,path\n")
        return path_arquivo

    def registrar(self, nome_arquivo: str):
        dados = [
            datetime.now(),
            self.nome_robo,
            self.acao,
            Path(self.diretorio_envios) / nome_arquivo,
        ]
        DataFrame([dados]).to_csv(
            self.arquivo,
            mode="a",
            header=False,
            index=False,
        )

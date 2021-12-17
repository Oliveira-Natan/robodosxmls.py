from datetime import datetime
from enum import Enum
from pathlib import Path

from pandas import Series, read_csv


class ArquivoRelatorio(Enum):
    ROBO_INDIVIDUALIZACAO = "robodeindividualizacao"
    ROBO_ERROS = "errosdosrobos"
    ROBO_PDF = "robodospdfs"
    ROBO_EMAILS = "robodosemails"
    ROBO_EMAILS_ARQUIVEI = "robodosemailsarquivei"
    ROBO_DO_ARQUIVEI = "robodoarquivei"


class Relatorio:
    BASE_DIR = r"F:\robodepdfs\reports"

    def __init__(
        self,
        diretorio: str,
        arquivo_sucesso: str,
        arquivo_erro: str,
        rotina_sucesso: str,
        rotina_erro: str,
        acao_sucesso: str,
        acao_erro: str,
    ):
        data = datetime.now()
        self.ano = data.year
        self.mes = f"{data.month:01}"
        self.diretorio = diretorio
        self.arquivo_sucesso = self._gerar_nome_arquivo(arquivo_sucesso)
        self.arquivo_erro = self._gerar_nome_arquivo(arquivo_erro)
        self.rotina_sucesso = rotina_sucesso
        self.rotina_erro = rotina_erro
        self.acao_sucesso = acao_sucesso
        self.acao_erro = acao_erro

    def _gerar_nome_arquivo(self, nome):
        arquivo = f"\\{nome}_{self.ano}_{self.mes}.csv"
        return Path(self.BASE_DIR) / arquivo

    def registrar_envio(self, arquivo):
        dados = Series(
            datetime.now(),
            self.rotina_sucesso,
            self.acao_sucesso,
            arquivo,
        )
        dados.to_csv(self.arquivo_sucesso, mode="a", header=False)

    def registrar_erro(self, arquivo):
        dados = Series(
            datetime.now(),
            self.rotina_sucesso,
            self.acao_sucesso,
            arquivo,
        )
        dados.to_csv(self.arquivo_erro, mode="a", header=False)

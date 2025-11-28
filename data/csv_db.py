import os
import csv
from datetime import datetime
from typing import Optional

from ouvidoria import Pessoa, Solicitacao, Sugestao, Reclamacao, Denuncia


class CSVDatabase:
    """Classe simples para persistir registros em CSV dentro da pasta `data/`.

    Arquivos gerados:
    - `data/users.csv` - armazena registros de usuários (nome, cpf, senha, criado_em)
    - `data/solicitacoes.csv` - armazena solicitações (data, hora, endereco, cpf, nome, tipo_codigo, tipo_texto, salvo_em)

    Uso:
        db = CSVDatabase()
        db.save_user(pessoa)
        db.save_solicitacao(solicitacao, tipo_codigo)
    """

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.dirname(__file__)
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.users_file = os.path.join(self.data_dir, "users.csv")
        self.solicitacoes_file = os.path.join(self.data_dir, "solicitacoes.csv")
        self._ensure_headers()

    def _ensure_headers(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["nome", "cpf", "senha", "criado_em"])

        if not os.path.exists(self.solicitacoes_file):
            with open(self.solicitacoes_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "data_ocorrencia",
                    "hora_ocorrencia",
                    "endereco",
                    "usuario_cpf",
                    "usuario_nome",
                    "tipo_codigo",
                    "tipo_texto",
                    "salvo_em",
                ])

    def save_user(self, pessoa: Pessoa) -> None:
        """Adiciona um usuário ao CSV `users.csv` (append)."""
        with open(self.users_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                pessoa.get_nome(),
                getattr(pessoa, "_Pessoa__cpf", ""),
                getattr(pessoa, "_Pessoa__senha", ""),
                datetime.utcnow().isoformat(),
            ])

    def save_solicitacao(self, solicitacao: Solicitacao, tipo_codigo: int) -> None:
        """Adiciona uma solicitação ao CSV `solicitacoes.csv` (append)."""
        tipo_texto = ""
        if isinstance(solicitacao, Solicitacao):
            tipo_texto = solicitacao.lista_solicitacoes.get(tipo_codigo, "")

        usuario = getattr(solicitacao, "usuario", None)
        usuario_cpf = getattr(usuario, "_Pessoa__cpf", "") if usuario else ""
        usuario_nome = usuario.get_nome() if usuario and hasattr(usuario, "get_nome") else ""

        with open(self.solicitacoes_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                getattr(solicitacao, "data", ""),
                getattr(solicitacao, "hora", ""),
                getattr(solicitacao, "endereco", ""),
                usuario_cpf,
                usuario_nome,
                tipo_codigo,
                tipo_texto,
                datetime.utcnow().isoformat(),
            ])

    # métodos utilitários adicionais podem ser adicionados conforme necessário


if __name__ == "__main__":
    db = CSVDatabase()
    # quick smoke test
    p = Pessoa("Teste", "00000000000", "senha")
    db.save_user(p)
    s = Solicitacao("01/01/2025", "12:00", "Rua Teste", p)
    db.save_solicitacao(s, 1)

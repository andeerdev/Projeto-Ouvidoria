import string
import datetime
from typing import Dict


class Pessoa:
    __nome: str
    __cpf: str
    __senha: str

    def __init__(self, nome: str, cpf: str, senha: str):
        self.__nome = nome
        self.__cpf = cpf
        self.__senha = senha

    def __str__(self):
        info = (
            f"Nome: {self.__nome}\n" f"CPF: {self.__cpf}\n" f"Senha: {self.__senha}\n"
        )
        return info

    def verificar_senha(self, senha: str) -> bool:
        return self.__senha == senha
    
    def get_nome(self):
        return self.__nome

    def __repr__(self):
        return (
            f"Pessoa(nome='{self.__nome}', Senha='{self.__senha}', CPF='{self.__cpf}')"
        )


class SistemaOuvidoria:
    def __init__(self):
        self.pessoas_cadastradas = []
        self.ocorrencias = []


class Ocorrencia:
    data: string
    hora: datetime
    endereco: str
    usuario: Pessoa

    def __init__(self, data, hora, endereco, usuario):
        self.data = data
        self.hora = hora
        self.endereco = endereco
        self.usuario = usuario

    def __str__(self):
        info = (
            f"Usuario: {self.usuario}\n"
            f"Data: {self.data}\n"
            f"Endereco: {self.endereco}\n"
            f"Horario do ocorrido: {self.hora}"
        )
        return info


class Solicitacao(Ocorrencia):
    
    lista_solicitacoes = {
        1: "Cortar grama",
        2: "Trocar luz",
        3: "Podar árvore",
        4: "Tapa buraco",
        5: "Limpeza de bueiro",
    }
    
    solicitacao_selecioda: int 

    def __init__(self, data, hora, endereco, usuario: Pessoa):
        super().__init__(data, hora, endereco, usuario)
        pass 

    def registrar_solicitacao(self, tipo: int):
        if tipo in self.lista_solicitacoes:
            return f"Solicitacao registrada: {self.lista_solicitacoes[tipo]}"
        else:
            return "Tipo de solicitacao invalido!"


class Sugestao(Ocorrencia):

    def __init__(self, data, hora, endereco, usuario: Pessoa, descricao: str):
        super().__init__(data, hora, endereco, usuario)
        self.descricao = descricao

    def registrar_sugestao(self):
        return f"Sugestão registrada com sucesso: {self.descricao}"

    def __str__(self):
        info = (
            f"--- Sugestão ---\n"
            f"{super().__str__()}\n"
            f"Descrição: {self.descricao}"
        )
        return info


class Reclamacao(Ocorrencia):
    niveis_reclamacao: Dict[int, str]

    def __init__(
        self, data, hora, endereco, usuario: Pessoa, descricao: str, nivel: int = 1
    ):
        super().__init__(data, hora, endereco, usuario)
        self.descricao = descricao
        self.niveis_reclamacao = {
            1: "Baixa prioridade",
            2: "Média prioridade",
            3: "Alta prioridade",
        }
        self.nivel = nivel

    def registrar_reclamacao(self):
        prioridade = self.niveis_reclamacao.get(self.nivel, "Desconhecida")
        return (
            f"Reclamação registrada com sucesso!\n"
            f"Prioridade: {prioridade}\n"
            f"Descrição: {self.descricao}"
        )

    def __str__(self):
        info = (
            f"--- Reclamação ---\n"
            f"{super().__str__()}\n"
            f"Nível: {self.nivel}\n"
            f"Descrição: {self.descricao}"
        )
        return info


class Denuncia(Ocorrencia):
    def __init__(
        self,
        data,
        hora,
        endereco,
        usuario: Pessoa,
        descricao: str,
        anonima: bool = False,
    ):
        super().__init__(data, hora, endereco, usuario)
        self.descricao = descricao
        self.anonima = anonima

    def registrar_denuncia(self):
        if self.anonima:
            return f"Denuncia anonima registrada com sucesso: {self.descricao}"
        else:
            return (
                f"Denuncia registrada com sucesso por {self.usuario.get_nome()}: {self.descricao}"
            )

    def __str__(self):
        info = (
            f"--- Denuncia ---\n"
            f"{super().__str__()}\n"
            f"Anonima: {'Sim' if self.anonima else 'Não'}\n"
            f"Descrição: {self.descricao}"
        )
        return info
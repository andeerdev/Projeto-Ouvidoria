from ouvidoria import *


def ocorrencia():
    print("=== REGISTRAR OCORRÊNCIA ===")
    nome = input("Seu nome: ").strip()
    cpf = input("Seu CPF: ").strip()
    senha = input("Sua senha: ").strip()
    usuario_base = Pessoa(nome, cpf, senha)

    while True:
        print("\n--- Menu de Ocorrências ---")
        print("1 - Solicitação")
        print("2 - Sugestão")
        print("3 - Reclamação")
        print("4 - Denúncia")
        print("0 - Sair")
        escolha = input("Escolha o tipo (0-4): ").strip()

        if escolha == "0":
            print("Saindo do menu de ocorrências.")
            break

        data = input("Data (ex: 07/11/2025): ").strip()
        hora = input("Hora (ex: 14:30): ").strip()
        endereco = input("Endereço: ").strip()

        if escolha == "1":
            usuario = usuario_base
            solicitacao = Solicitacao(data, hora, endereco, usuario)
            print("Tipos de solicitação:")
            for cod, desc in solicitacao.lista_solicitacoes.items():
                print(f"{cod} - {desc}")
            try:
                tipo = int(input("Informe o código da solicitação: ").strip())
            except ValueError:
                print("Código inválido.")
                continue
            print(solicitacao.registrar_solicitacao(tipo))

        elif escolha == "2":
            usuario = usuario_base
            descricao = input("Descreva sua sugestão: ").strip()
            sugestao = Sugestao(data, hora, endereco, usuario, descricao)
            print(sugestao.registrar_sugestao())

        elif escolha == "3":
            usuario = usuario_base
            descricao = input("Descreva sua reclamação: ").strip()
            try:
                nivel = int(input("Nível (1=Baixa, 2=Média, 3=Alta): ").strip())
            except ValueError:
                nivel = 1
            reclamacao = Reclamacao(data, hora, endereco, usuario, descricao, nivel)
            print(reclamacao.registrar_reclamacao())

        elif escolha == "4":
            usuario = usuario_base
            descricao = input("Descreva sua denúncia: ").strip()
            anon = input("Deseja anonimato? (s/n): ").strip().lower() == "s"
            if anon == 's':
                anon = True
            else:
                anon = False
            denuncia = Denuncia(data, hora, endereco, usuario, descricao, anon)
            print(denuncia.registleorar_denuncia())

        else:
            print("Opção inválida.")

        print("\nVoltando ao menu de ocorrências...")


if __name__ == "__main__":
    # Pergunta se o usuário deseja usar a interface gráfica (GUI) ou a interface de texto (CLI).
    escolha_interacao = input("Deseja abrir a interface gráfica? (s/n): ").strip().lower()
    if escolha_interacao == "s":
        try:
            from interface import OuvidoriaApp

            app = OuvidoriaApp()
            app.run()
        except Exception as e:
            print("Falha ao iniciar a interface gráfica:", e)
            print("Caindo para modo texto.")
            ocorrencia()
    else:
        ocorrencia()

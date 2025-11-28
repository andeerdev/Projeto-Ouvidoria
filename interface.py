import tkinter as tk
from tkinter import ttk, messagebox
from ouvidoria import Pessoa, Solicitacao, Sugestao, Reclamacao, Denuncia
from data.csv_db import CSVDatabase


class OuvidoriaApp:
    """Aplicação GUI orientada a objeto para a Ouvidoria."""

    def __init__(self, title: str = "Ouvidoria", size: str = "350x500"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)
        # instância do "banco de dados" CSV
        try:
            self.db = CSVDatabase()
        except Exception:
            self.db = None
        self.mostrar_tela_login()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- Lógica de ações ---
    def logar(self, nome_entry, cpf_entry, senha_entry):
        nome = nome_entry.get()
        cpf = cpf_entry.get()
        senha = senha_entry.get()

        if not all([nome, cpf, senha]):
            messagebox.showwarning("Erro", "Preencha todos os campos para entrar.")
            return

        usuario_logado = Pessoa(nome, cpf, senha)
        # salva cadastro no CSV (se o DB estiver disponível)
        if getattr(self, "db", None) is not None:
            try:
                self.db.save_user(usuario_logado)
            except Exception:
                pass

        self.mostrar_tela_menu(usuario_logado)

    def registrar_solicitacao(
        self, usuario, data_entry, hora_entry, endereco_entry, combo, mapa_solicitacoes
    ):
        try:
            data = data_entry.get()
            hora = hora_entry.get()
            endereco = endereco_entry.get()
            tipo_selecionado_texto = combo.get()

            if not all([data, hora, endereco, tipo_selecionado_texto]):
                messagebox.showwarning("Erro", "Preencha todos os campos.")
                return

            tipo_codigo = None
            for codigo, texto in mapa_solicitacoes.items():
                if texto == tipo_selecionado_texto:
                    tipo_codigo = codigo
                    break

            if tipo_codigo is None:
                messagebox.showerror("Erro", "Tipo de solicitação inválido.")
                return

            sol = Solicitacao(data, hora, endereco, usuario)
            resultado = sol.registrar_solicitacao(tipo_codigo)

            # salva a solicitação no CSV (se o DB estiver disponível)
            if getattr(self, "db", None) is not None:
                try:
                    self.db.save_solicitacao(sol, tipo_codigo)
                except Exception:
                    pass

            messagebox.showinfo("Sucesso!", resultado)
            self.mostrar_tela_menu(usuario)

        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def registrar_sugestao(
        self, usuario, data_entry, hora_entry, endereco_entry, descricao_entry
    ):
        try:
            data = data_entry.get()
            hora = hora_entry.get()
            endereco = endereco_entry.get()
            descricao = descricao_entry.get("1.0", "end").strip()

            if not all([data, hora, endereco, descricao]):
                messagebox.showwarning("Erro", "Preencha todos os campos.")
                return

            sug = Sugestao(data, hora, endereco, usuario, descricao)
            resultado = sug.registrar_sugestao()

            if getattr(self, "db", None) is not None:
                try:
                    self.db.save_sugestao(sug)
                except Exception:
                    pass

            messagebox.showinfo("Sucesso!", resultado)
            self.mostrar_tela_menu(usuario)

        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def registrar_reclamacao(
        self,
        usuario,
        data_entry,
        hora_entry,
        endereco_entry,
        descricao_entry,
        nivel_combo,
    ):
        try:
            data = data_entry.get()
            hora = hora_entry.get()
            endereco = endereco_entry.get()
            descricao = descricao_entry.get("1.0", "end").strip()
            nivel_text = nivel_combo.get()

            if not all([data, hora, endereco, descricao, nivel_text]):
                messagebox.showwarning("Erro", "Preencha todos os campos.")
                return

            try:
                nivel = int(nivel_text.split(" - ")[0])
            except Exception:
                nivel = 1

            rec = Reclamacao(data, hora, endereco, usuario, descricao, nivel)
            resultado = rec.registrar_reclamacao()

            if getattr(self, "db", None) is not None:
                try:
                    self.db.save_reclamacao(rec)
                except Exception:
                    pass

            messagebox.showinfo("Sucesso!", resultado)
            self.mostrar_tela_menu(usuario)

        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def registrar_denuncia(
        self,
        usuario,
        data_entry,
        hora_entry,
        endereco_entry,
        descricao_entry,
        anonima_var,
    ):
        try:
            data = data_entry.get()
            hora = hora_entry.get()
            endereco = endereco_entry.get()
            descricao = descricao_entry.get("1.0", "end").strip()
            anonima = bool(anonima_var.get())

            if not all([data, hora, endereco, descricao]):
                messagebox.showwarning("Erro", "Preencha todos os campos.")
                return

            den = Denuncia(data, hora, endereco, usuario, descricao, anonima)
            resultado = den.registrar_denuncia()

            if getattr(self, "db", None) is not None:
                try:
                    self.db.save_denuncia(den)
                except Exception:
                    pass

            messagebox.showinfo("Sucesso!", resultado)
            self.mostrar_tela_menu(usuario)

        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    # --- Telas da aplicação ---
    def mostrar_tela_login(self):
        self.limpar_tela()

        frame_login = ttk.Frame(self.root, padding=20)
        frame_login.pack(expand=True)

        ttk.Label(frame_login, text="Ouvidoria", font=("Helvetica", 16, "bold")).pack(
            pady=10
        )
        ttk.Label(frame_login, text="Faça seu login para continuar").pack(pady=(0, 20))

        ttk.Label(frame_login, text="Nome:").pack()
        entry_nome = ttk.Entry(frame_login, width=40)
        entry_nome.pack()

        ttk.Label(frame_login, text="CPF:").pack(pady=(10, 0))
        entry_cpf = ttk.Entry(frame_login, width=40)
        entry_cpf.pack()

        ttk.Label(frame_login, text="Senha:").pack(pady=(10, 0))
        entry_senha = ttk.Entry(frame_login, width=40, show="*")
        entry_senha.pack()

        btn_entrar = ttk.Button(
            frame_login,
            text="Entrar",
            command=lambda: self.logar(entry_nome, entry_cpf, entry_senha),
        )
        btn_entrar.pack(pady=20, ipady=10, fill="x")

    def mostrar_tela_menu(self, usuario: Pessoa):
        self.limpar_tela()

        frame_menu = ttk.Frame(self.root, padding=20)
        frame_menu.pack(expand=True, fill="both")

        # assume que Pessoa possui método get_nome(); se for diferente, adapte
        nome_display = (
            usuario.get_nome()
            if hasattr(usuario, "get_nome")
            else getattr(usuario, "nome", "Usuário")
        )

        ttk.Label(
            frame_menu, text=f"Olá, {nome_display}!", font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        ttk.Label(frame_menu, text="Escolha o tipo de ocorrência:").pack(pady=(0, 20))

        btn_solicitacao = ttk.Button(
            frame_menu,
            text="1 - Solicitação",
            command=lambda: self.mostrar_tela_solicitacao(usuario),
        )
        btn_solicitacao.pack(pady=5, ipady=10, fill="x")
        btn_sugestao = ttk.Button(
            frame_menu,
            text="2 - Sugestão",
            command=lambda: self.mostrar_tela_sugestao(usuario),
        )
        btn_sugestao.pack(pady=5, ipady=10, fill="x")
        btn_reclamacao = ttk.Button(
            frame_menu,
            text="3 - Reclamação",
            command=lambda: self.mostrar_tela_reclamacao(usuario),
        )
        btn_reclamacao.pack(pady=5, ipady=10, fill="x")
        btn_denuncia = ttk.Button(
            frame_menu,
            text="4 - Denúncia",
            command=lambda: self.mostrar_tela_denuncia(usuario),
        )
        btn_denuncia.pack(pady=5, ipady=10, fill="x")

        btn_sair = ttk.Button(
            frame_menu,
            text="0 - Sair (Voltar ao Login)",
            command=self.mostrar_tela_login,
        )
        btn_sair.pack(pady=(20, 0))

    def mostrar_tela_solicitacao(self, usuario: Pessoa):
        self.limpar_tela()

        frame_form = ttk.Frame(self.root, padding=20)
        frame_form.pack(expand=True, fill="both")

        ttk.Label(
            frame_form, text="Registrar Solicitação", font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        ttk.Label(frame_form, text="Data (ex: 01/01/2025):").pack()
        entry_data = ttk.Entry(frame_form, width=40)
        entry_data.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Hora (ex: 12:30):").pack()
        entry_hora = ttk.Entry(frame_form, width=40)
        entry_hora.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Endereço:").pack()
        entry_endereco = ttk.Entry(frame_form, width=40)
        entry_endereco.pack(pady=(0, 10))

        ttk.Label(
            frame_form, text="Escolha o tipo de solicitação:", font=("", 10, "bold")
        ).pack(pady=(10, 5))
        mapa_solicitacoes = getattr(Solicitacao, "lista_solicitacoes", {})
        opcoes = list(mapa_solicitacoes.values())

        combo_solicitacoes = ttk.Combobox(
            frame_form, values=opcoes, state="readonly", width=38
        )
        combo_solicitacoes.pack(pady=(0, 20))

        btn_registrar = ttk.Button(
            frame_form,
            text="Registrar Solicitação",
            command=lambda: self.registrar_solicitacao(
                usuario,
                entry_data,
                entry_hora,
                entry_endereco,
                combo_solicitacoes,
                mapa_solicitacoes,
            ),
        )
        btn_registrar.pack(ipady=10, fill="x")

        btn_voltar = ttk.Button(
            frame_form,
            text="Voltar ao Menu",
            command=lambda: self.mostrar_tela_menu(usuario),
        )
        btn_voltar.pack(pady=10)

    def mostrar_tela_sugestao(self, usuario: Pessoa):
        self.limpar_tela()

        frame_form = ttk.Frame(self.root, padding=20)
        frame_form.pack(expand=True, fill="both")

        ttk.Label(
            frame_form, text="Registrar Sugestão", font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        ttk.Label(frame_form, text="Data (ex: 01/01/2025):").pack()
        entry_data = ttk.Entry(frame_form, width=40)
        entry_data.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Hora (ex: 12:30):").pack()
        entry_hora = ttk.Entry(frame_form, width=40)
        entry_hora.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Endereço:").pack()
        entry_endereco = ttk.Entry(frame_form, width=40)
        entry_endereco.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Descrição:").pack()
        text_descricao = tk.Text(frame_form, width=40, height=6)
        text_descricao.pack(pady=(0, 10))

        btn_registrar = ttk.Button(
            frame_form,
            text="Registrar Sugestão",
            command=lambda: self.registrar_sugestao(
                usuario, entry_data, entry_hora, entry_endereco, text_descricao
            ),
        )
        btn_registrar.pack(ipady=10, fill="x")

        btn_voltar = ttk.Button(
            frame_form,
            text="Voltar ao Menu",
            command=lambda: self.mostrar_tela_menu(usuario),
        )
        btn_voltar.pack(pady=10)

    def mostrar_tela_reclamacao(self, usuario: Pessoa):
        self.limpar_tela()

        frame_form = ttk.Frame(self.root, padding=20)
        frame_form.pack(expand=True, fill="both")

        ttk.Label(
            frame_form, text="Registrar Reclamação", font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        ttk.Label(frame_form, text="Data (ex: 01/01/2025):").pack()
        entry_data = ttk.Entry(frame_form, width=40)
        entry_data.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Hora (ex: 12:30):").pack()
        entry_hora = ttk.Entry(frame_form, width=40)
        entry_hora.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Endereço:").pack()
        entry_endereco = ttk.Entry(frame_form, width=40)
        entry_endereco.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Descrição:").pack()
        text_descricao = tk.Text(frame_form, width=40, height=6)
        text_descricao.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Nível de prioridade:").pack()
        niveis = [
            f"{k} - {v}"
            for k, v in getattr(
                Reclamacao,
                "niveis_reclamacao",
                {1: "Baixa prioridade", 2: "Média prioridade", 3: "Alta prioridade"},
            ).items()
        ]
        if not niveis:
            niveis = [
                "1 - Baixa prioridade",
                "2 - Média prioridade",
                "3 - Alta prioridade",
            ]

        combo_nivel = ttk.Combobox(
            frame_form, values=niveis, state="readonly", width=38
        )
        combo_nivel.pack(pady=(0, 10))

        btn_registrar = ttk.Button(
            frame_form,
            text="Registrar Reclamação",
            command=lambda: self.registrar_reclamacao(
                usuario,
                entry_data,
                entry_hora,
                entry_endereco,
                text_descricao,
                combo_nivel,
            ),
        )
        btn_registrar.pack(ipady=10, fill="x")

        btn_voltar = ttk.Button(
            frame_form,
            text="Voltar ao Menu",
            command=lambda: self.mostrar_tela_menu(usuario),
        )
        btn_voltar.pack(pady=10)

    def mostrar_tela_denuncia(self, usuario: Pessoa):
        self.limpar_tela()

        frame_form = ttk.Frame(self.root, padding=20)
        frame_form.pack(expand=True, fill="both")

        ttk.Label(
            frame_form, text="Registrar Denúncia", font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        ttk.Label(frame_form, text="Data (ex: 01/01/2025):").pack()
        entry_data = ttk.Entry(frame_form, width=40)
        entry_data.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Hora (ex: 12:30):").pack()
        entry_hora = ttk.Entry(frame_form, width=40)
        entry_hora.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Endereço:").pack()
        entry_endereco = ttk.Entry(frame_form, width=40)
        entry_endereco.pack(pady=(0, 10))

        ttk.Label(frame_form, text="Descrição:").pack()
        text_descricao = tk.Text(frame_form, width=40, height=6)
        text_descricao.pack(pady=(0, 10))

        anonima_var = tk.IntVar(value=0)
        chk_anonima = ttk.Checkbutton(
            frame_form, text="Enviar anonimamente", variable=anonima_var
        )
        chk_anonima.pack(pady=(0, 10))

        btn_registrar = ttk.Button(
            frame_form,
            text="Registrar Denúncia",
            command=lambda: self.registrar_denuncia(
                usuario,
                entry_data,
                entry_hora,
                entry_endereco,
                text_descricao,
                anonima_var,
            ),
        )
        btn_registrar.pack(ipady=10, fill="x")

        btn_voltar = ttk.Button(
            frame_form,
            text="Voltar ao Menu",
            command=lambda: self.mostrar_tela_menu(usuario),
        )
        btn_voltar.pack(pady=10)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = OuvidoriaApp()
    app.run()

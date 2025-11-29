**Projeto: Ouvidoria**

- **Descrição:**: Pequeno sistema de ouvidoria que permite registrar ocorrências (Solicitação, Sugestão, Reclamação, Denúncia). Possui interface gráfica baseada em `tkinter` e uma interface de texto (CLI). Os dados são armazenados em CSV na pasta `data/`.

**Estrutura do Projeto**
- **`interface.py`**: Classe `OuvidoriaApp` — Interface orientada a objetos (Tkinter).
- **`main.py`**: Entry-point; oferece opção de iniciar interface ou pelo terminal.
- **`ouvidoria.py`**: Modelos de domínio (classes `Pessoa`, `Ocorrencia`, `Solicitacao`, `Sugestao`, `Reclamacao`, `Denuncia`).
- **`data/csv_db.py`**: Classe `CSVDatabase` para armazenamento simples em CSV.
- **`data/`**: Pasta que armazena os CSVs gerados (`users.csv`, `solicitacoes.csv`).

**Principais Classes**
- **`Pessoa`**: representa o usuário (nome, CPF, senha).
- **`Ocorrencia` e subclasses**: modelos das ocorrências.
- **`OuvidoriaApp`**: controla telas e ações da interface.
- **`CSVDatabase`**: cria/atualiza `users.csv` e `solicitacoes.csv`.

**Como executar**
- Requisitos mínimos:
  - **Python:** 3.8+ (testado em 3.11/3.13)

- Abrir a aplicação (GUI ou CLI):

  Em PowerShell, na raiz do projeto:
  ```powershell
  python .\main.py
  ```
  - Responda `s` para abrir a interface gráfica (GUI).
  - Responda `n` para usar a interface de texto (CLI).

- Abrir somente a GUI (opcional):
  ```powershell
  python .\interface.py
  ```

**Persistência (CSV)**
- Os arquivos são criados automaticamente dentro de `data/`:
  - `data/users.csv` — colunas: `nome`, `cpf`, `senha`, `criado_em` (ISO UTC).
  - `data/solicitacoes.csv` — colunas: `data_ocorrencia`, `hora_ocorrencia`, `endereco`, `usuario_cpf`, `usuario_nome`, `tipo_codigo`, `tipo_texto`, `salvo_em`.

---

Feito por:
Anderson Freitas - afreitas@unisantos.br  
Leonardo Mastros - leonardomastros@unisantos.br  
Lucas Farah - farah@unisantos.br

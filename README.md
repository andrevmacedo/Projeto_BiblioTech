# 📚 Bibliotech — Sistema de Gerenciamento de Biblioteca em Python

Projeto educacional desenvolvido para praticar **Python**, **Programação Orientada a Objetos (POO)**, **Estruturas de Dados** e integração com banco de dados **SQLite**.

---

## 📝 Descrição

O **Bibliotech** é um sistema de gerenciamento de biblioteca desenvolvido em Python com integração ao banco de dados SQLite.  

O projeto foi construído com foco na aplicação de conceitos fundamentais de desenvolvimento de software, como **POO**, **modularização**, **manipulação de estruturas de dados** e **regras de negócio**.

A aplicação simula o funcionamento de uma biblioteca real, permitindo o controle de livros, usuários e empréstimos, além de automatizar processos como verificação de atrasos e controle de disponibilidade.

---

## 🧠 Conceitos Aplicados

### 🔹 Programação Orientada a Objetos (POO)
- Organização do sistema em **classes e métodos**
- Separação de responsabilidades entre módulos
- Encapsulamento de dados e comportamentos
- Uso de métodos de classe (`@classmethod`) para operações controladas

---

### 🔹 Estruturas de Dados
- Manipulação de **listas** para exibição e processamento de registros
- Uso de **tuplas** para representar dados retornados do banco
- Iteração e validação de dados com base em coleções
- Controle de fluxo com base em estruturas iteráveis

---

### 🔹 Banco de Dados e SQL
- Integração com **SQLite**
- Uso de consultas com:
  - `JOIN`
  - `GROUP BY`
  - `ORDER BY`
  - `COUNT`
- Manipulação de dados com `INSERT`, `UPDATE` e `SELECT`

---

### 🔹 Regras de Negócio
- Controle de disponibilidade de livros
- Bloqueio de usuários com pendências
- Atualização automática de empréstimos atrasados
- Validação de operações antes da execução

---

## ⚙️ Funcionalidades

- Cadastro, consulta, atualização e exclusão de livros  
- Gerenciamento de usuários (ativação e desativação de contas)  
- Registro de empréstimos e devoluções com controle de estoque  
- Atualização automática de status (empréstimos atrasados)  
- Bloqueio de usuários com pendências  
- Consultas e relatórios (histórico, livros mais emprestados, indisponíveis, etc.)  

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**  
- **SQLite3**  
- Biblioteca `datetime`  
- SQL estruturado para manipulação e análise de dados  

---

## ▶️ Como Executar o Projeto

1. Certifique-se de ter o **Python 3** instalado.

2. Clone o repositório:
```bash
git clone https://github.com/andrevmacedo/bibliotech.git

3. No arquivo principal do projeto, ajuste o caminho do banco de dados para um diretório válido em sua máquina:
   caminho = "C:/Users/.../dbExercicio.db"
⚠️ É importante informar corretamente o caminho onde o arquivo .db será criado ou acessado, caso contrário o sistema não conseguirá se conectar ao banco de dados.

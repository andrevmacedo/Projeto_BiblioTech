import sqlite3
import warnings
from datetime import date,timedelta
warnings.filterwarnings('ignore', 
    message='The default date adapter is deprecated')

class SQL:
    caminhodb = "C:/Users/André Vítor/Desktop/Modularização.py/dbExercicio.db"
    conn = None
    cursor = None
    def __init__(self):
        pass
    @classmethod
    def ConectarBanco (cls):
        try:
            cls.conn = sqlite3.connect(cls.caminhodb)
            cls.cursor = cls.conn.cursor()
            return True
        except sqlite3.Error as erro:
            return erro
    @classmethod
    def ConsultarCategorias (cls):
        cls.cursor.execute('''
                   select distinct categoria
                   from livro
                   ''') #DISTINCT TIRA LINHAS DUPLICADAS
        return cls.cursor.fetchall()
    @classmethod
    def ConsultarLivrosPorCategoria (cls,dado):
        cls.cursor.execute("select * from livro where categoria = ?",(dado,))
        return cls.cursor.fetchall()
    @classmethod
    def ConsultarMaisEmprestados (cls):
        cls.cursor.execute('''
                   select count(emprestimos.id_livro),emprestimos.id_livro,livro.titulo,livro.autor,livro.categoria,livro.ano_publicacao
                   from emprestimos
                   inner join livro on livro.id_livro = emprestimos.id_livro
                   group by emprestimos.id_livro
                   order by count(*) desc
                   limit 3
                   ''')
        #SELECIONA A COLUNA id_livro E CONTA, AGRUPA TODAS AS LINHAS QUE O ID SE REPETE, ORDENA A CONTAGEM EM DESC (MAIOR PRO MENOR) E LIMITA ATÉ 3
        return cls.cursor.fetchall()
    @classmethod
    def ConsultarIndisponibilidade (cls):
        cls.cursor.execute("select * from livro where quantidade_disponivel = 0")
        return cls.cursor.fetchall()
    @classmethod
    def ConsultarStatusUsuarios (cls):
        cls.cursor.execute('''select * from usuario 
                           order by status desc''')
        return cls.cursor.fetchall()
    @classmethod
    def ConsultarEmprestimos (cls):
        cls.cursor.execute('''select emprestimos.id_emprestimo,emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.data_devolucao_real,emprestimos.status
                            from emprestimos
                            inner join livro on livro.id_livro = emprestimos.id_livro
                            inner join usuario on usuario.id_usuario = emprestimos.id_usuario
                            order by emprestimos.status desc''')
        return cls.cursor.fetchall()
        
def ListarPorCategoria(): #✅
    dados = SQL.ConsultarCategorias()
    if dados:
        n=0
        for categorias, in dados:
            n=n+1
            print(f"{n}. {categorias}")
        op = input("Digite a opção desejada: ")
        livros = SQL.ConsultarLivrosPorCategoria(op)
        if livros:
            MostrarLivros(livros)
            return True
        else:
            return False
    else:
        return False    
def LivrosMaisEmprestados(): #✅
    dados = SQL.ConsultarMaisEmprestados()
    if dados:
        MostarIncidenciaLivros(dados)
        return True
    else:
        return False
def LivrosIndisponiveis(): #✅
    dados = SQL.ConsultarIndisponibilidade()
    if dados:
        MostrarLivros(dados)
        return True
    else:
        return False
def StatusUsuarios(): #✅
    dados = SQL.ConsultarStatusUsuarios()
    if dados:
        MostrarUsuarios(dados)
        return True
    else:
        return False
def Relatorios(): #✅
    dados = SQL.ConsultarEmprestimos()
    if dados: 
        MostrarRelatorios(dados)
        return True
    else:
        return False

def MostrarLivros(livros):
    print(f"{len(livros)} Resultados Encontrados!")
    for id,titulo,autor,categoria,publicacao,total,disponivel in livros:
        print(f'''
                ID do Livro = {id}
                Titulo = {titulo}
                Autor = {autor}
                Categoria = {categoria}
                Ano de publicação = {publicacao}
                Quantidade Total = {total}
                Quantidade Disponivel = {disponivel}
                ''')
def MostarIncidenciaLivros(dados):
    print(f"{len(dados)} Resultados Encontrados!")
    for rep,id,titulo,autor,categoria,ano in dados:
        print(f'''
                Incidência: {rep}
                ID do Livro: {id}
                Título: {titulo}
                Autor: {autor}
                Categoria: {categoria}
                Ano de publicação: {ano}
                ''')
def MostrarUsuarios(dados):
    for id,nome,email,telefone,status in dados:
        if status == 1:
            condicao = "Ativa"
        else:
            condicao = "Inativa"
        print(f'''
            ID do Usuário = {id}
            Nome = {nome}
            Email = {email}
            Telefone = {telefone}
            Status da Conta = {condicao}
            ''')
def MostrarRelatorios(dados):
    for idemprestimo,idlivro,idusuario,titulo,nome,emprestimo,prev,real,status in dados:
        print(f'''
                ID do Empréstimo = {idemprestimo}
                Livro = {titulo}
                Usuário = {nome}
                Data de empréstimo = {emprestimo}
                Data de devolução prevista = {prev}
                Status = {status}
                ''')

def MenuConsultas():
    conexao = SQL.ConectarBanco()
    if conexao == True:
        pass
    else:
        print(f"Erro ao conectar no Banco, erro: {conexao}")
        return
    while True:
        print('''
          1 - Listar livros por categoria
          2 - Listar livros mais emprestados
          3 - Contar livros indisponíveis
          4 - Contar usuários cadastrados
          5 - Relatório geral de empréstimos
          0 - Voltar ao menu principal
          ''')
        op = int(input("Digite a opção desejada: "))
        match op:
            case 0:
                return
            case 1:
                if not ListarPorCategoria():
                    print("Resultados NÃO Encontrados!")
            case 2:
                if not LivrosMaisEmprestados():
                    print("Resultados NÃO Encontrados!")
            case 3:
                if not LivrosIndisponiveis():
                    print("TODOS livros estão disponíveis!")
            case 4:
                if not StatusUsuarios():
                    print("Nenhum usuário encontrado!")
            case 5:
                if not Relatorios():
                    print("Nenhum resultado encontrado!")
            case _:
                print("Opção Inválida!")
def Main():
    MenuConsultas()
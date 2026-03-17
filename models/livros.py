import sqlite3
import warnings
warnings.filterwarnings('ignore', 
    message='The default date adapter is deprecated')

class Livros:
    def __init__(self,titulo,autor,categoria,publi,total,disp):
        self._titulo = titulo
        self._autor = autor
        self._categoria = categoria
        self._publi = publi
        self._total = total
        self._disp = disp
    @classmethod
    def VerificarDisponibilidade(cls,qtd_disponivel,qtd_total):
        if qtd_disponivel > qtd_total:
            return False
        else:
            return True    
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
    def CadastrarLivroBanco (cls,livro):
        try:
            cls.conn.execute('''
                    insert into livro values (?,?,?,?,?,?,?)
                    ''',(None,livro._titulo,livro._autor,livro._categoria,livro._publi,livro._total,livro._disp))
            cls.conn.commit()
            return True
        except sqlite3.Error as erro:
            return erro
    @classmethod
    def BuscarLivro (cls,coluna,dado):
        sql = (f"select * from livro where {coluna} = ?")
        cls.cursor.execute (sql,(dado,))
        return cls.cursor.fetchone()
    @classmethod
    def AlterarDadosLivro (cls,title,alterar,coluna,calc_disp,calc_total):
        sql = (f'''
                update livro
                set {coluna} = ?
                where titulo = ?
            ''')
        if coluna == "quantidade_disponivel":
            cls.conn.execute(sql,(calc_disp,title))
            cls.conn.execute('''
                        update livro
                        set quantidade_total = ?
                        where titulo = ?
                        ''',(calc_total,title))
            cls.conn.commit()
        else:
            cls.conn.execute(sql,(alterar,title))
            cls.conn.commit()
    @classmethod
    def BuscarTodosLivros (cls):
        cls.cursor.execute("select * from livro")
        return cls.cursor.fetchall()
    @classmethod
    def BuscarLivrosIndisponiveis (cls):
        cls.cursor.execute("select * from livro where quantidade_disponivel = 0")
        return cls.cursor.fetchall()
    @classmethod
    def ExcluirLivroBanco (cls,dado):
        cls.conn.execute("delete from livro where id_livro = ?",(dado,))
        cls.conn.commit()

def MenuLivros():
    conexao = SQL.ConectarBanco()
    if conexao == True:
        pass
    else:
        print(f"Erro ao conectar no Banco, erro: {conexao}")
        return
    while True:
        print('''
            1 - Cadastrar novo livro
            2 - Atualizar dados de um livro
            3 - Consultar livro por ID
            4 - Consultar livros por título
            5 - Listar todos os livros
            6 - Listar livros indisponíveis
            7 - Excluir livro
            0 - Voltar ao menu principal
            ''')
        op = int(input("Digite uma opção: "))
        match op:
            case 0:
                return
            case 1:
                livro = CadastrarLivro()
                if not livro:
                    print("Livro já cadastrado no banco!")
                else:
                    banco = SQL.CadastrarLivroBanco(livro)
                    if banco == True:
                        print("Livro cadastrado com Sucesso!")
                    else: 
                        print(f"Erro ao Cadastrar! Erro: {banco}")
            case 2:
                atualizar = AtualizarLivro()
                if atualizar:
                    print("Livro encontrado e atualizado com sucesso!")
                else:
                    print("Livro NÃO encontrado ou operação cancelada.")
            case 3:
                busca = BuscarLivroID()
                if not busca:
                    print("Livro NÃO encontrado!")
            case 4:
                busca = BuscarLivroTitulo()
                if not busca:
                    print("Livro NÃO encontrado!")
            case 5:
                busca = ListarTodosLivros()
                if not busca:
                    print("Livro(s) NÃO encontrado(s)!")
            case 6:
                busca = ListarLivrosIndisponiveis()
                if not busca:
                    print("Livro(s) NÃO encontrado(s)!")
            case 7:
                busca = ExcluirLivro()
                if busca:
                    print("Livro excluído com sucesso!")
                else:
                    print("Impossível completar operação!")
            case _:
                print("Opção Inválida!")
def CadastrarLivro(): #✅
    titulo = input("Digite o título do livro: ")
    livro_banco = SQL.BuscarLivro("titulo",titulo)
    if livro_banco:
        return False
    else:
        autor = input("Digite o autor do livro: ")
        categoria = input("Digite a categoria do livro: ")
        publicacao = input("Digite o ano de publicação(yyyy-mm-dd): ")
        quantidade_total = int(input("Digite a quantidade de livros adquiridos: "))
        quantidade_dis = int(input("Digite a quantidade de livros disponíveis: "))
        verify = Livros.VerificarDisponibilidade(quantidade_dis,quantidade_total)
        while not verify:
            quantidade_dis = int(input("Digite a quantidade de livros disponíveis: "))
            verify = Livros.VerificarDisponibilidade(quantidade_dis,quantidade_total)
        livro = Livros(titulo,autor,categoria,publicacao,quantidade_total,quantidade_dis)
        return livro
def AtualizarLivro(): #✅
    title = input("Digite o nome do livro que dejesa alterar: ")
    livro = SQL.BuscarLivro("titulo",title)
    if livro:
        print('''
            1. Título
            2. Autor
            3. Categoria
            4. Ano de Publicação
            5. Quantidade Total
            6. Quantidade Disponível
            ''')
        op = int(input("O que deseja alterar: "))
        match op:
            case 1:
                alterar = input("Digite o novo título: ")
                coluna = "titulo"
                SQL.AlterarDadosLivro(title,alterar,coluna,None,None)
            case 2:
                alterar = input("Digite o novo autor: ")
                coluna = "autor"
                SQL.AlterarDadosLivro(title,alterar,coluna,None,None)
            case 3:
                alterar = input("Digite a nova categoria: ")
                coluna = "categoria"
                SQL.AlterarDadosLivro(title,alterar,coluna,None,None)
            case 4:
                alterar = input("Digite a nova data de ppublicação(yyyy-mm-dd): ")
                coluna = "ano_publicacao"
                SQL.AlterarDadosLivro(title,alterar,coluna,None,None)
            case 5:
                alterar = int(input("Digite a nova quantidade total: "))
                qtd_total = livro[5]
                while alterar < qtd_total:
                    alterar = int(input("""Digite a nova quantidade total: 
                            Qtd. não deve ser menor que o valor atual! """))
                coluna = "quantidade_total"
                SQL.AlterarDadosLivro(title,alterar,coluna,None,None)
            case 6:
                qtd_total = livro[5]
                qtd_disp = livro[6]
                alterar = int(input('''
                            Digite a nova quantidade disponível: 
                            OBS: Será incrementada ao valor já existente! '''))
                while qtd_total < alterar:
                    alterar = int(input('''
                            Digite a nova quantidade disponível: 
                            OBS: Será incrementada ao valor já existente! '''))
                coluna = "quantidade_disponivel"
                calc_disp = qtd_disp + alterar
                calc_total = qtd_total - alterar
                SQL.AlterarDadosLivro(title,alterar,coluna,calc_disp,calc_total)
            case _:
                return False
        return True
    else:
        return False
def BuscarLivroID(): #✅
    id = int(input("Digite o ID do livro que deseja buscar: "))
    resultado = SQL.BuscarLivro("id_livro",id)
    if resultado:
        MostrarLivros(resultado)
        return True
    else:
        return False
def BuscarLivroTitulo(): #✅
    title = input("Digite o TÍTULO do livro que deseja buscar: ")
    resultado = SQL.BuscarLivro("titulo",title)
    if resultado:
        MostrarLivros(resultado)
        return True
    else:
        return False
def ListarTodosLivros(): #✅
    resultado = SQL.BuscarTodosLivros()
    if resultado:
        MostrarLivrosListados(resultado)
        return True
    else: 
        return False
def ListarLivrosIndisponiveis(): #✅
    resultado = SQL.BuscarLivrosIndisponiveis()
    if resultado:
        MostrarLivrosListados(resultado)
        return True
    else:
        return False
def ExcluirLivro(): #✅
    id = int(input("Digite o ID do livro que deseja excluir: "))
    resultado = SQL.BuscarLivro("id_livro",id)
    if resultado:
        MostrarLivros(resultado)
        op = input("Deseja exlcuir este livro (sim ou não): ").lower()
        if op == "sim":
            SQL.ExcluirLivroBanco(id)
            return True
        else:
            return False
    else:
        return False
    
def MostrarLivros(resultado):
    print(f'''
                Aqui está o resultado:
                ID do livro = {resultado[0]}
                Titulo = {resultado[1]}
                Autor = {resultado[2]}
                Categoria = {resultado[3]}
                Ano de Publicação = {resultado[4]}
                Quantidade Total = {resultado[5]}
                Quantidade Disponível = {resultado[6]}
                ''')
def MostrarLivrosListados(resultado):
    for id,titulo,autor,categoria,publi,total,dis in resultado:
                print(f'''
                ID do livro = {id}
                Titulo = {titulo}
                Autor = {autor}
                Categoria = {categoria}
                Ano de Publicação = {publi}
                Quantidade Total = {total}
                Quantidade Disponível = {dis}
                ''')

def Main():
    MenuLivros()

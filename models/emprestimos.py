import sqlite3
import warnings
from datetime import date,timedelta
warnings.filterwarnings('ignore', 
    message='The default date adapter is deprecated')

class Emprestimos:
    emprestimo = date.today()
    data_devolucao = emprestimo + timedelta(days=7) #ADICIONA 7 DIAS A PARTIR DE HOJE
    def __init__(self,idlivro,idusuario,data_emprestimo,data_prevista,devolucao,status):
        self._idlivro = idlivro
        self._idusuario = idusuario
        self._data_emprestimo = self.emprestimo
        self._data_prevista = self.data_devolucao
        self._devolucao = None
        self._status = "Aberto"
    @classmethod
    def set_DataDevolucao (cls):
        devolucao = date.today()
        return devolucao
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
    def BuscarDadosUsuario (cls,dado):
        sql = (f"select * from usuario where id_usuario = ? and status = 1")
        cls.cursor.execute(sql,(dado,))
        return cls.cursor.fetchone()  
    @classmethod
    def BuscarPendenciasUsuario (cls,dado):
        sql = (f"select * from emprestimos where id_usuario = ? and status = 'Atrasado'")
        cls.cursor.execute(sql,(dado,))
        return cls.cursor.fetchone()  
    @classmethod
    def BuscarDisponibilidadeLivro (cls,dado):
        sql = (f"select * from livro where id_livro = ? and quantidade_disponivel > 0")
        cls.cursor.execute(sql,(dado,))
        return cls.cursor.fetchone() 
    @classmethod
    def AlterarQtdDispLivro (cls,qtd_disponivel,idlivro):
        cls.conn.execute('''
                            update livro 
                            set quantidade_disponivel = ?
                            where id_livro = ?
                            ''',(qtd_disponivel,idlivro))
        cls.conn.commit()
    @classmethod
    def RegistrarEmprestimo (cls,emprestimo):
        cls.conn.execute('''
                    insert into emprestimos values (?,?,?,?,?,?,?)
                        ''',(None,emprestimo._idlivro,emprestimo._idusuario,emprestimo._data_emprestimo,emprestimo._data_prevista,emprestimo._devolucao,emprestimo._status))
        cls.conn.commit()
    @classmethod
    def BuscarDadosEmprestimo (cls,coluna,id):
        sql = (f'''
                   select emprestimos.id_emprestimo,emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.status
                   from emprestimos
                   inner join usuario on usuario.id_usuario = emprestimos.id_usuario
                   inner join livro on livro.id_livro = emprestimos.id_livro
                   where emprestimos.status = 'Aberto' and {coluna} = ?
                   ''')
        cls.cursor.execute(sql,(id,))
        return cls.cursor.fetchall()
    @classmethod
    def DevolverLivro (cls,devolucao,id):
        cls.conn.execute('''
                             update emprestimos
                             set data_devolucao_real = ?, status = 'Devolvido'
                             where id_emprestimo = ?
                             ''',(devolucao,id))
        cls.conn.commit()
    @classmethod
    def DevolverQtdDisponivel (cls,livro):
        cls.conn.execute('''
                            update livro
                            set quantidade_disponivel = quantidade_disponivel + 1
                            where id_livro = ?
                            ''',(livro,))
        cls.conn.commit()
    @classmethod
    def BuscarPorStatus (cls,status):
        sql = (f'''
            select emprestimos.id_emprestimo,emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.status
            from emprestimos
            inner join usuario on usuario.id_usuario = emprestimos.id_usuario
            inner join livro on livro.id_livro = emprestimos.id_livro
            where emprestimos.status = ?
               ''')
        cls.cursor.execute(sql,(status,))
        return cls.cursor.fetchall()
    @classmethod
    def BuscarHistorico (cls,coluna,id):
        try:
            sql = (f'''
                    select emprestimos.id_emprestimo,emprestimos.id_livro,emprestimos.id_usuario,livro.titulo,usuario.nome,emprestimos.data_emprestimo,emprestimos.data_devolucao_prevista,emprestimos.status
                    from emprestimos
                    inner join livro on livro.id_livro = emprestimos.id_livro
                    inner join usuario on usuario.id_usuario = emprestimos.id_usuario
                    where {coluna} = ?
                    ''')
            cls.cursor.execute(sql,(id,))
            return cls.cursor.fetchall()
        except sqlite3.Error as erro:
            return erro

def RealizarEmprestimo(): #✅
    idusuario = int(input("Digite o ID do usuário: "))
    dados_usuario = SQL.BuscarDadosUsuario(idusuario)
    if dados_usuario:
        pendencias = SQL.BuscarPendenciasUsuario(idusuario)
        if pendencias:
            return False
        else:
            idlivro = int(input("Digite o ID do livro: "))
            dados_livro = SQL.BuscarDisponibilidadeLivro(idlivro)
            if dados_livro:
                emprestimo = Emprestimos(idlivro,idusuario,None,None,None,None)
                qtd_disponivel = dados_livro[6] - 1
                SQL.AlterarQtdDispLivro(qtd_disponivel,idlivro)
                return emprestimo
            else:
                return False
    else:
        return False
def RealizarDevolucao(): #✅
    op = int(input('''
            1. ID de Empréstimo
            2. ID do Usuário
            Indique a opção desejada: '''))
    match op:
        case 1:
            coluna = "emprestimos.id_emprestimo"
            id = int(input("Digite o PROTOCOLO/ID de empréstimo: "))
            dados = SQL.BuscarDadosEmprestimo(coluna,id)
            if dados:
                registro = MostrarEmprestimos(dados)
                devolucao = Emprestimos.set_DataDevolucao()
                SQL.DevolverLivro(devolucao,id)
                SQL.DevolverQtdDisponivel(registro)
                return True
            else:
                return False
        case 2:
            coluna = "emprestimos.id_usuario"
            id = int(input("Digite o ID do Usuário: "))
            dados = SQL.BuscarDadosEmprestimo(coluna,id)
            if dados:
                registro = MostrarEmprestimos(dados)
                devolucao = Emprestimos.set_DataDevolucao()
                emprestimo = int(input("Digite o ID que deseja devolver: "))
                while not ObterIDEmprestimo(dados,emprestimo):
                    emprestimo = int(input("Digite um ID válido: "))
                SQL.DevolverLivro(devolucao,emprestimo)
                SQL.DevolverQtdDisponivel(registro)
                return True
            else:
                return False
        case _:
            print("Opção Inválida!")
def MostrarEmprestimos(dados): #✅
    print(f"{len(dados)} Resultados Encontrados!")
    for idemprestimo,idlivro,idusuario,titulo,nome,data,devolucao,status in dados:
        print(f'''
            ID Empréstimo: {idemprestimo}
            Título do Livro: {titulo}
            Usuário: {nome}
            Empréstimo: {data}
            Devolução Prevista: {devolucao}
            Status: {status}
              ''')
    return idlivro
def ObterIDEmprestimo(dados,emprestimo): #✅
    for idemprestimo,idlivro,idusuario,titulo,nome,data,devolucao,status in dados:
        if emprestimo == idemprestimo:
            return idlivro
    return None
def ConsultarEmprestimos(): #✅
    coluna = "emprestimos.id_emprestimo"
    id = int(input("Digite o ID do empréstimo que deseja buscar: "))
    dados = SQL.BuscarHistorico(coluna,id)
    print(dados)
    if dados:
        MostrarEmprestimos(dados)
        return True
    else:
        return False
def EmprestimosStatus(dado): #✅
    busca = SQL.BuscarPorStatus(dado)
    for emprestimo,livro,usuario,titulo,nome,data,devolucao,status in busca:
        print(f'''
          ID do Empréstimo = {emprestimo}
          Livro = {titulo}
          Usuário = {nome}
          Data de Empréstimo = {data}
          Data de Devolução Prevista = {devolucao}
          Status = {status}
          ''')
def HistoricoUsuario(): #✅
    coluna = "emprestimos.id_usuario"
    id = int(input("Digite o ID de usuário desejado: "))
    dados = SQL.BuscarHistorico(coluna,id)
    if dados:
        MostrarEmprestimos(dados)
        return True
    else:
        return False
def MenuEmprestimos():
    conexao = SQL.ConectarBanco()
    if conexao == True:
        pass
    else:
        print(f"Erro ao conectar no Banco, erro: {conexao}")
        return
    while True:
        print('''
        1 - Realizar novo empréstimo
        2 - Registrar devolução
        3 - Consultar empréstimo por ID
        4 - Listar empréstimos em aberto
        5 - Listar empréstimos atrasados
        6 - Histórico de empréstimos por usuário
        0 - Voltar ao menu principal
          ''')
        op = int(input("Digite a opção desejada: "))
        match op:
            case 0:
                return
            case 1:
                emprestimo = RealizarEmprestimo()
                if emprestimo:
                    SQL.RegistrarEmprestimo(emprestimo)
                    print("Empréstimo Registrado com Sucesso!")
                else:
                    print("Operação Encerrada\nPendencia ou Erros Encontrados!")
            case 2:
                if RealizarDevolucao():
                    print("Devolução Realizada com Sucesso!")
                else:
                    print("Erro ao Realizar Devolução!")
            case 3:
                if not ConsultarEmprestimos():
                    print("Empréstimo não Encontrado!")
            case 4:
                dado = 'Aberto'
                EmprestimosStatus(dado)
            case 5:
                dado = 'Atrasado'
                EmprestimosStatus(dado)
            case 6:
                if not HistoricoUsuario():
                    print("Usuário não Realizou Nenhum Empréstimo!")
            case _:
                print("Opção Inválida!")
    
def Main():
    MenuEmprestimos()
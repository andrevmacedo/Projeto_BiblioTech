import sqlite3
import warnings
warnings.filterwarnings('ignore', 
    message='The default date adapter is deprecated')

class Usuarios:
    def __init__(self,nome,email,telefone):
        self._nome = nome
        self._email = email
        self._telefone = telefone
    @classmethod
    def VerificarEmail (cls,email):
        if "@" not in email:
            return False
        else:
            return True
    @classmethod
    def VerificarTelefone (cls,telefone):
        if len(telefone) == 11:
            return True
        else:
            return False
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
    def BuscarDados (cls,coluna,dado):
        sql = (f"select * from usuario where {coluna} = ?")
        cls.cursor.execute(sql,(dado,))
        return cls.cursor.fetchone()
    @classmethod
    def CadastrarUsuarioBanco (cls,usuario):
        cls.conn.execute ('''
                insert into usuario values (?,?,?,?,?)
                          ''',(None,usuario._nome,usuario._email,usuario._telefone,1))
        cls.conn.commit()
    @classmethod
    def AlterarDadosUsuario (cls,coluna,alterar,id):
        sql = (f'''
            update usuario
            set {coluna} = ?
            where id_usuario = ?
               ''')
        cls.conn.execute(sql,(alterar,id))
        cls.conn.commit()
    @classmethod
    def ListarAtivos (cls):
        cls.cursor.execute("select * from usuario where status = 1")
        return cls.cursor.fetchall()
    @classmethod
    def ListarUsuarios (cls):
        cls.cursor.execute("select * from usuario")
        return cls.cursor.fetchall()
    @classmethod
    def ExcluirUsuarioBanco (cls,id):
        cls.conn.execute("delete from usuario where id_usuario = ?",(id,))
        cls.conn.commit()

def CadastrarUsuario(): #✅
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o email do usuário: ")
    while not Usuarios.VerificarEmail(email):
        email = input("Digite o email do usuário\nDeve conter o *@*: ")
        Usuarios.VerificarEmail(email)
    telefone = input("Digite o telefone do usuário(ddd + 9 dígitos): ")
    while not Usuarios.VerificarTelefone(telefone):
        telefone = input("Digite o telefone do usuário(ddd + 9 dígitos): ")
        Usuarios.VerificarTelefone(telefone)
    if SQL.BuscarDados("telefone",telefone):
        return None
    else:
        usuario = Usuarios(nome,email,telefone)
        return usuario
def AtualizarUsuario(): #✅
    id = int(input("Digite o ID do perfil que deseja alterar: "))
    dados = SQL.BuscarDados("id_usuario",id)
    if dados:
        op = int(input('''
                    1. Nome
                    2. Email
                    3. Telefone
                    4. Status
                    O que deseja alterar: '''))
        match op:
            case 1:
                alterar = input("Digite o novo nome: ") 
                coluna = "nome"
                SQL.AlterarDadosUsuario(coluna,alterar,id)
            case 2:
                alterar = input("Digite o novo email: ")
                coluna = "email"
                while not Usuarios.VerificarEmail(alterar):
                    alterar = input("Digite o novo email: ")
                    Usuarios.VerificarEmail(alterar)
                SQL.AlterarDadosUsuario(coluna,alterar,id)
            case 3:
                alterar = input("Digite o novo telefone: ")
                coluna = "telefone"
                while not Usuarios.VerificarTelefone(alterar):
                    alterar = input("Digite o novo telefone: ")
                    Usuarios.VerificarTelefone(alterar)
                SQL.AlterarDadosUsuario(coluna,alterar,id)    
            case 4:
                status = dados[4]
                coluna = "status"
                if status == 1:
                    alterar = int(input('''
                                Deseja alterar o estado da conta?
                                1. Sim
                                2. Não: '''))
                    if alterar == 1:
                        SQL.AlterarDadosUsuario(coluna,0,id)
                    else:
                        return False
                elif status == 0:
                    alterar = int(input('''
                                Deseja alterar o estado da conta?
                                1. Sim
                                2. Não: '''))
                    if alterar == 1:
                        SQL.AlterarDadosUsuario(coluna,1,id)
                    else:
                        return False
                else:
                    return False
            case 5:
                return False
            case _:
                return False
        return True
    else:
        return False
def ConsultarID(): #✅
    id = int(input("Digite o ID que deseja buscar: "))
    coluna = "id_usuario"
    dados = SQL.BuscarDados(coluna,id)
    if dados:
        MostrarUsuarios(dados)
        return True
    else:
        return False
def ConsultarNome(): #✅
    nome = input("Digite o nome que deve buscar: ")
    coluna = "nome"
    dados = SQL.BuscarDados(coluna,nome)
    if dados:
        MostrarUsuarios(dados)
        return True
    else:
        return False
def ListarUsuariosAtivos(): #✅
    dados = SQL.ListarAtivos()
    if dados:
        MostrarUsuariosListados(dados)
        return True
    else:
        return False
def ListarTodosUsuarios(): #✅
    dados = SQL.ListarUsuarios()
    if dados:
        MostrarUsuariosListados(dados)
        return True
    else:
        return False
def ExcluirUsuario(): #✅
    id = int(input("Digite o ID do usuário que deseja excluir: "))
    dados = SQL.BuscarDados("id_usuario",id)
    if dados:
        MostrarUsuarios(dados)
        op = input("Deseja exlcuir este usuário (sim ou não): ").lower()
        if op == "sim":
            SQL.ExcluirUsuarioBanco(id)
            return True
        else:
            return False
    else:
        return False
def MostrarUsuarios(dados):
    print(f'''
        ID do Usuário = {dados[0]}
        Nome = {dados[1]}
        Email = {dados[2]}
        Telefone = {dados[3]}
        Status da Conta = {dados[4]}
        ''')
def MostrarUsuariosListados(dados):
    for id,nome,email,telefone,status in dados:
        print(f'''
            ID do Usuário = {id}
            Nome = {nome}
            Email = {email}
            Telefone = {telefone}
            Status da Conta = {status}
            ''')
def MenuUsuarios():
    conexao = SQL.ConectarBanco()
    if conexao == True:
        pass
    else:
        print(f"Erro ao conectar no Banco, erro: {conexao}")
        return
    while True:
        print('''
            1 - Cadastrar novo usuário
            2 - Atualizar dados do usuário
            3 - Consultar usuário por ID
            4 - Consultar usuário por nome
            5 - Listar usuários ativos
            6 - Listar todos os usuários
            7 - Excluir usuário
            0 - Voltar ao menu principal
            ''')
        op = int(input("Digite a opção desejada: "))
        match op:
            case 0:
                return
            case 1:
                usuario = CadastrarUsuario()
                if usuario:
                    SQL.CadastrarUsuarioBanco(usuario)
                    print("Usuário Cadastrado com Sucesso!")
                else:
                    print("Telefone já cadastrado!")
            case 2:
                alteracao = AtualizarUsuario()
                if alteracao:
                    print("Alteração Realizada com Sucesso!")
                else:
                    print("Operação Cancelada ou ID não encontrado!")
            case 3:
                consulta = ConsultarID()
                if not consulta:
                    print("Usuário não encontrado!")
            case 4:
                consulta = ConsultarNome()
                if not consulta:
                    print("Usuário não encontrado!")
            case 5: 
                dados = ListarUsuariosAtivos()
                if not dados:
                    print("Nenhum Usuário encontrado!")
            case 6:
                dados = ListarTodosUsuarios()
                if not dados:
                    print("Nenhum Usuário encontrado!")
            case 7:
                if ExcluirUsuario():
                    print("Usuário excluído com Sucesso!")
                else:
                    print("Operação Cancelada ou ID não encontrado!")
            case _:
                print("Opção Inválida!")
def Main():
    MenuUsuarios()
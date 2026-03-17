import sqlite3
import warnings
from datetime import date,timedelta
warnings.filterwarnings('ignore', 
    message='The default date adapter is deprecated')

class Regras:
    dia_atual = date.today()
    def __init__(self):
        pass
    @classmethod
    def CalculoDatas (cls,datas):
        emprestimo = date.fromisoformat(datas)
        diferenca = (cls.dia_atual-emprestimo).days
        if diferenca > 7:
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
    def ConsultarEmprestimosAbertos (cls):
        cls.cursor.execute("select * from emprestimos where status = 'Aberto'")
        return cls.cursor.fetchall()
    @classmethod
    def AtualizarSistema (cls,id):
        cls.conn.execute('''
                             update emprestimos
                             set status = 'Atrasado'
                             where id_emprestimo = ?
                             ''',(id,))
        cls.conn.commit()
        
def GerenciarAtrasos():
    conexao = SQL.ConectarBanco()
    if conexao == True:
        pass
    else:
        print(f"Erro ao conectar no Banco, erro: {conexao}")
        return
    dados = SQL.ConsultarEmprestimosAbertos()
    if dados:
        for id, livro, usuario, emprestimo, prevista, real, status in dados:
            verify = Regras.CalculoDatas(emprestimo)
            if verify:
                SQL.AtualizarSistema(id)
    else:
        return
def Main():
    GerenciarAtrasos()
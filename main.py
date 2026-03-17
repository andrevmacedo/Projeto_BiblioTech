from models import emprestimos,livros,usuarios
from repository import consultas
from services import regras
def Main():
    while True:
        regras.Main()
        print('''
          !Bem - Vindo ao Sistema Bibliotech!
          1. Gerenciar Livros 
          2. Gerenciar Usuarios 
          3. Empréstimos 
          4. Consultas e Relatórios 
          0. Sair
          ''')
        op = int(input("Digite uma opção: "))
        match op:
            case 0:
                break
            case 1:
                livros.Main()
            case 2:
                usuarios.Main()
            case 3:
                emprestimos.Main()
            case 4:
                consultas.Main()
            case _:
                print("Opção Inválida!")
Main()
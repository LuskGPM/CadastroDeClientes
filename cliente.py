from datetime import datetime
import sqlite3


class Painel:
    def __init__(self, password: str, user: str):
        self.entrada_user = user.strip()  # Usuário fornecido pelo usuário
        self.entrada_password = password.strip()  # Senha fornecida pelo usuário
        self.__password = '123456'  # Senha padrão para autenticação
        self.__user = 'root'  # Usuário padrão para autenticação
        self.con = sqlite3.connect("Cadastro.db")  # Conexão com o banco de dados SQLite
        self.cursor = self.con.cursor()  # Cursor para executar comandos SQL
        self.dados = []  # Lista para armazenar dados temporariamente
        self.__logar_painel()  # Método para validar login

    def __logar_painel(self):
        # Valida as credenciais do usuário
        if self.entrada_user == self.__user and self.entrada_password == self.__password:
            print('Logado com sucesso!')
            return
        else:
            print('Usuário ou senha incorretos, fechando o programa...')
            self.con.close()
            quit()

    @staticmethod
    def __tamanho_painel() -> int:
        # Retorna o tamanho do painel para formatação de texto
        return 80

    @staticmethod
    def __validar_entrada(entrada: str):
        # Valida a entrada do usuário para garantir que seja um número inteiro
        while True:
            try:
                valor = int(input(entrada))
                return int(valor)
            except ValueError:
                print('Digite um número inteiro válido')

    def __validar_opcoes(self, valor):
        # Valida a opção escolhida pelo usuário no painel
        while True:
            if 1 <= valor <= 4:
                return int(valor)
            else:
                print('Digite um valor correspondente às opções acima')
                valor = self.__validar_entrada('Sua opção: ')

    @staticmethod
    def __validar_tamanho_cpf(cpf: str):
        # Valida que o CPF tenha exatamente 11 dígitos
        while True:
            if len(cpf) == 11:
                return cpf
            else:
                print(f'Seu CPF possuí {len(cpf)} dígitos, tenha certeza de ter digitado apenas os 11 dígitos '
                      f'corretamente')
                cpf = str(input('CPF: ')).replace('.', '').replace('-', '')

    def __validar_id_in_dados(self, valor) -> bool:
        # Verifica se o ID existe na lista de dados
        id_list = list()
        dados_id = self.cursor.execute('SELECT id FROM clientes')
        for i in dados_id:
            id_list.append(i[0])
        if valor in id_list:
            return True
        else:
            return False

    def __confirmar_delete(self, acesso: bool = False):
        # Confirma a ação de deletar um cliente após validação de senha
        self.acesso = acesso
        password_for_delete = str(input('Digite a senha para excluir: '))
        if password_for_delete == self.__password:
            self.acesso = True
            input('Enter para continuar...')
        else:
            self.acesso = False
            print('Senha incorreta')

    def exibir_painel(self):
        # Exibe o painel principal com as opções para o usuário
        while True:
            print('=' * self.__tamanho_painel())
            print(f'{"Cadastro de Cliente":^{self.__tamanho_painel()}}')
            print('=' * self.__tamanho_painel())
            print('1 - Cadastrar Cliente')
            print('2 - Ver clientes cadastrados')
            print('3 - Excluir Cliente')
            print('4 - Sair')
            esc = self.__validar_entrada('Sua opção: ')
            self.__escolhas_painel(self.__validar_opcoes(esc))

    def __escolhas_painel(self, escolha: int):
        # Direciona o fluxo do programa com base na escolha do usuário
        if escolha == 1:
            self.__cadastrar()
        elif escolha == 2:
            print('=' * self.__tamanho_painel())
            self.__select_cliente()
            print('=' * self.__tamanho_painel())
        elif escolha == 3:
            self.__delete_cliente()
        elif escolha == 4:
            print('Finalizando...')
            self.con.close()
            exit()

    def __create_table(self):
        # Cria a tabela 'clientes' no banco de dados, se não existir
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            nascimento TEXT,
            cpf VARCHAR(12) unique
        )
        ''')
        self.con.commit()

    def __cadastrar(self):
        # Cadastra um novo cliente no banco de dados
        cadastro = Cliente()
        nome = str(input('Nome: ')).capitalize()
        nascimento = str(input('Data de nascimento (AAAA-MM-DD): '))
        cpf = str(input('CPF: ')).replace('.', '').replace('-', '')
        # Valida o tamanho do cpf
        validar_cpf = self.__validar_tamanho_cpf(cpf)
        # Valida se existe um cpf igual o digitado já cadastrado
        validar_cpf_duplicata_list = list()
        validar_duplicata_cpf = cadastro.get_cpf(validar_cpf)
        tupla_cpfs = self.cursor.execute('SELECT cpf FROM clientes').fetchall()
        for cpf in tupla_cpfs:
            validar_cpf_duplicata_list.append(cpf[0])

        if validar_duplicata_cpf in validar_cpf_duplicata_list:
            print('Este cpf já está cadastrado.')
            return
        else:
            cadastro.nome = nome
            cadastro.nascimento = cadastro.get_nascimento(nascimento)
            cadastro.cpf = validar_cpf
            self.__create_table()
            self.cursor.execute(f'INSERT INTO clientes (nome, nascimento, cpf) VALUES ("{cadastro.nome}", '
                                f'"{cadastro.get_nascimento(nascimento)}", "{cadastro.get_cpf(cadastro.cpf)}")')
            self.con.commit()

            print('Cadastro realizado com sucesso!')

    def __select_cliente(self) -> list:
        # Seleciona e exibe todos os clientes cadastrados no banco de dados
        res = self.cursor.execute('SELECT * FROM clientes')
        for table in res.fetchall():
            self.dados.append(table)

        print(f"{'ID':<3} | {'Nome':<35} | {'Nascimento':<12} | {'CPF':<14}")
        for dado in self.dados:
            print(f'{dado[0]:<3} | {dado[1]:<35} | {dado[2]:<12} | {dado[3]:>14}')
        self.dados.clear()

    def __delete_cliente(self):
        # Exclui um cliente do banco de dados
        print('=' * self.__tamanho_painel())
        print(f"{'Excluir Cliente':^{self.__tamanho_painel()}}")
        print('=' * self.__tamanho_painel())

        id_cliente = self.__validar_entrada('Digite o ID do cliente que deseja excluir: ')
        if self.__validar_id_in_dados(id_cliente):
            self.__confirmar_delete()
            if self.acesso:
                self.cursor.execute(f'delete from clientes where ID = {id_cliente}')
                print('Cliente excluído com sucesso!')
                self.con.commit()
            else:
                return
        else:
            print('ID inválido.')


class Cliente:
    def __init__(self) -> None:
        self.nome = str()  # Nome do cliente
        self.__nascimento = str()  # Data de nascimento do cliente
        self.__cpf = str()  # CPF do cliente
        self.__idade = int()  # Idade do cliente
        self.__ano_nasc = int()  # Ano de nascimento do cliente

    def __format_cpf(self, valor) -> str:
        # Formata o CPF no padrão XXX.XXX.XXX-XX
        self.valor = valor
        self.valor = f'{self.__cpf[:3]}.{self.__cpf[3:6]}.{self.__cpf[6:9]}-{self.__cpf[9:]}'
        return self.valor

    def get_cpf(self, valor) -> str:
        # Retorna o CPF formatado
        self.__cpf = valor.replace('.', '').replace('-', '')
        return self.__format_cpf(self.__cpf)

    def get_idade(self) -> int:
        # Retorna a idade do cliente
        self.__idade = datetime.today().year - self.get_ano_nasc()
        return self.__idade

    def get_ano_nasc(self) -> int:
        # Retorna o ano de nascimento do cliente
        self.__ano_nasc = datetime.strptime(self.__nascimento, "%Y-%m-%d").year
        return self.__ano_nasc

    def get_nascimento(self, nasc) -> str:
        # Retorna a data de nascimento do cliente
        self.__nascimento = nasc
        return self.__nascimento


user = str(input('Usuário: '))
password = str(input('Senha: '))
execute_painel = Painel(password, user)
execute_painel.exibir_painel()

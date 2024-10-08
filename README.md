# Painel de Cadastro de Clientes

Este é um projeto simples em Python para um painel de cadastro de clientes utilizando SQLite3 como banco de dados. O sistema permite cadastrar, visualizar e excluir clientes, além de validar entradas e garantir a unicidade dos CPFs cadastrados.

## Funcionalidades

1. **Login de Usuário**: Validação de credenciais antes do acesso ao painel.
2. **Cadastrar Cliente**: Adicionar novos clientes ao banco de dados.
3. **Ver Clientes Cadastrados**: Exibir a lista de clientes cadastrados.
4. **Excluir Cliente**: Remover clientes do banco de dados após confirmação.

## Estrutura do Código

### Classe `Painel`

Responsável pela interface e funcionalidades principais do sistema. 

- **Métodos Principais**:
  - `__init__(self, password: str, user: str)`: Inicializa a conexão com o banco de dados e realiza o login.
  - `__logar_painel(self)`: Valida as credenciais do usuário.
  - `exibir_painel(self)`: Exibe o menu principal com as opções disponíveis.
  - `__create_table(self)`: Cria a tabela `clientes` no banco de dados, se ainda não existir.
  - `__cadastrar(self)`: Cadastra um novo cliente.
  - `__select_cliente(self)`: Exibe todos os clientes cadastrados.
  - `__delete_cliente(self)`: Exclui um cliente especificado pelo ID.

- **Métodos Auxiliares**:
  - `__tamanho_painel() -> int`: Retorna o tamanho do painel para formatação.
  - `__validar_entrada(entrada: str)`: Valida se a entrada é um número inteiro.
  - `__validar_opcoes(self, valor)`: Valida a opção escolhida pelo usuário no painel.
  - `__validar_tamanho_cpf(cpf: str)`: Verifica se o CPF tem 11 dígitos.
  - `__validar_id_in_dados(self, valor) -> bool`: Verifica se o ID existe na lista de dados.
  - `__confirmar_delete(self, acesso: bool = False)`: Confirma a exclusão após validação de senha.

### Classe `Cliente`

Contém os atributos e métodos relevantes para um cliente.

- **Atributos**:
  - `self.nome`: Nome do cliente.
  - `self.__nascimento`: Data de nascimento do cliente.
  - `self.__cpf`: CPF do cliente.
  - `self.__idade`: Idade do cliente.
  - `self.__ano_nasc`: Ano de nascimento do cliente.

- **Métodos**:
  - `__format_cpf(self, valor) -> str`: Formata o CPF no padrão `XXX.XXX.XXX-XX`.
  - `get_cpf(self, valor) -> str`: Retorna o CPF formatado.
  - `get_idade(self) -> int`: Retorna a idade do cliente.
  - `get_ano_nasc(self) -> int`: Retorna o ano de nascimento do cliente.
  - `get_nascimento(self) -> str`: Retorna a data de nascimento do cliente.

## Como Usar

1. Clone o repositório: `git clone https://github.com/SEU_USERNAME/painel-clientes.git`
2. Navegue até o diretório do projeto: `cd painel-clientes`
3. Execute o script: `python painel_clientes.py`

## Exemplo de Uso

```python
Usuário: root
Senha: 123456
Logado com sucesso!
========================================
        Cadastro de Cliente             
========================================
1 - Cadastrar Cliente
2 - Ver clientes cadastrados
3 - Excluir Cliente
4 - Sair
Sua opção: 1
```

## Requisitos

- Python 3.x
- SQLite3

## Estrutura do Banco de Dados

A tabela `clientes` é criada no banco de dados `Cadastro.db` e possui a seguinte estrutura:

```sql
CREATE TABLE IF NOT EXISTS clientes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    nascimento TEXT,
    cpf VARCHAR(12) UNIQUE
);
```

## Contato

Para dúvidas ou sugestões, entre em contato pelo email [lucasgpm00@gmail.com](lucasgpm00@gmail.com).

---

**Nota**: Certifique-se de ter o SQLite3 instalado e configurado em seu ambiente.

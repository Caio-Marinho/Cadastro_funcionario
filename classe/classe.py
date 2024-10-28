from configuration.mysql_connected import Connection


class Funcionario:
    """
    Representa um funcionário no sistema, com informações como nome e salário.
    Permite criar uma tabela de funcionários e iterar sobre os funcionários cadastrados.
    """

    def __init__(self, nome: str = None, salario: float = None):
        if nome and salario:  # Se os parâmetros nome e salário forem fornecidos, cria um novo funcionário
            self.nome = nome
            self.salario = salario
            self.criar()  # Cria a tabela de funcionários ao instanciar um funcionário
            self.adicionar_banco()  # Adiciona o funcionário ao banco de dados
        else:  # Caso contrário, apenas inicializa as variáveis
            self.nome = None
            self.salario = None

    @staticmethod
    def criar():
        """Cria a base de dados e a tabela de funcionários se não existirem."""
        with Connection() as conn:
            if conn.cursor:
                cursor = conn.cursor
                cursor.execute("CREATE DATABASE IF NOT EXISTS Funcionario;")
                cursor.execute("USE Funcionario;")
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Funcionario (
                       ID INT PRIMARY KEY AUTO_INCREMENT,
                       nome VARCHAR(255) NOT NULL,
                       salario DECIMAL(10, 2) NOT NULL
                    );"""
                )

    def adicionar_banco(self):
        """Adiciona o funcionário ao banco de dados."""
        with Connection() as conn:
            if conn.cursor:
                cursor = conn.cursor
                cursor.execute("USE Funcionario;")
                sql = "INSERT INTO Funcionario (nome, salario) VALUES (%s, %s);"
                values = (self.nome, self.salario)
                cursor.execute(sql, values)
                conn.commit()  # Confirma a transação

    @staticmethod
    def listar_funcionarios():
        """Retorna uma lista de todos os funcionários cadastrados no banco de dados."""
        with Connection() as conn:
            if conn.cursor:
                cursor = conn.cursor
                cursor.execute("USE Funcionario;")
                cursor.execute("SELECT * FROM Funcionario;")
                return cursor.fetchall()  # Retorna todos os funcionários

    def __iter__(self):
        """Inicializa a iteração sobre os funcionários cadastrados."""
        self.funcionarios = Funcionario.listar_funcionarios()  # Pega a lista de funcionários do banco
        self.index = 0  # Inicializa o índice para iteração
        return self

    def __next__(self):
        """Retorna o próximo funcionário da lista."""
        if self.index < len(self.funcionarios):
            funcionario = self.funcionarios[self.index]
            self.index += 5  # Incrementa o índice
            return funcionario
        else:
            raise StopIteration  # Se não houver mais funcionários, lança StopIteration


# Simulação de Cadastro e Consulta de Funcionários
if __name__ == "__main__":
    # Cadastro de funcionários
    funcionario1 = Funcionario("Alice", 3000.00)
    funcionario2 = Funcionario("Bob", 2500.00)
    funcionario3 = Funcionario("Carlos", 4000.00)

    # Criação de uma instância para iteração
    funcionario_iterador = Funcionario()  # Cria uma instância de Funcionario para iterar
    funcionario_iterador.__iter__()  # Inicializa a iteração

    # Usando next() para iterar sobre os funcionários
    print("Lista de Funcionários:")
    try:
        while True:
            funcionario = next(funcionario_iterador)  # Chama next() na instância
            print(f"Nome: {funcionario[1]}, Salário: {funcionario[2]:.2f}")  # Funcionario[1] é o nome, [2] é o salário
    except StopIteration:
        pass  # A exceção StopIteration indica que não há mais funcionários

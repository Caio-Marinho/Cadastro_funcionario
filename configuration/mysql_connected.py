import mysql.connector
from configuration.config import Configuration


class Connection(Configuration):
    def __init__(self):
        Configuration.__init__(self)
        try:
            self.conn = mysql.connector.connect(**self.config['MySQL'])
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao MySQL: {err}")  # Captura e imprime qualquer erro na conexão
        except Exception as erro:
            print(f"Falha de conexão: {erro}")
            exit(1)

    def connection(self):
        """
        Retorna a conexão ativa com o banco de dados.
        """
        return self.conn

    def cursor(self):
        """
        Retorna o cursor para executar consultas no banco de dados.
        """
        return self.cursor

    def commit(self):
        """
        Realiza o commit das transações no banco de dados.
        """
        return self.conn.commit()

    def fetchone(self):
        """
        Retorna a próxima linha do resultado da consulta.
        """
        return self.cursor.fetchone()

    def fetchall(self):
        """
        Retorna todas as linhas do resultado da consulta.
        """
        return self.cursor.fetchall()

    def execute(self):
        """
        Executa uma consulta SQL no banco de dados.
        """
        return self.cursor.execute()

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

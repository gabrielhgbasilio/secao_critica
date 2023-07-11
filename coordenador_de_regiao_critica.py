import socket
import threading
import sys

class Coordenador:
    def __init__(self, ip, porta, max_conexoes):
        self.ip = ip
        self.porta = porta
        self.max_conexoes = max_conexoes
        self.fila = []  # Fila de processos
        self.processos = {}  # Processos conectados
        self.lock = threading.Lock()  # Lock para sincronização

    def iniciar(self):
        # Iniciar a thread para receber conexoes de processos
        thread_conexao = threading.Thread(target=self.aceitar_conexoes)
        thread_conexao.start()

        # Iniciar a thread para executar o algoritmo de exclusão mutua distribuida
        thread_algoritmo = threading.Thread(target=self.executar_algoritmo)
        thread_algoritmo.start()

        # Executar a thread de interface no loop principal
        self.interface()

    def aceitar_conexoes(self):
        # Configurar o socket servidor para aceitar conexoes de processos
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.bind((self.ip, self.porta))
        socket_servidor.listen(self.max_conexoes)

        print("Aguardando conexões...")

        while True:
            # Aceitar conexoes e lidar com processos
            socket_cliente, endereco = socket_servidor.accept()
            thread_processo = threading.Thread(target=self.lidar_processo, args=(socket_cliente,))
            thread_processo.start()

    def lidar_processo(self, socket_cliente):
        # Lidar com um processo conectado
        id_processo = socket_cliente.recv(1024).decode()
        self.processos[id_processo] = socket_cliente  # Adicionar o processo ao dicionario de processos
        self.adicionar_a_fila(id_processo)  # Adicionar o processo na fila de pedidos
        print("Processo", id_processo, "conectado.")

    def adicionar_a_fila(self, id_processo):
        # Adicionar um processo na fila de pedidos
        self.lock.acquire()
        self.fila.append(id_processo)
        self.lock.release()

    def executar_algoritmo(self):
        # Executar o algoritmo de exclusao mutua distribuida
        while True:
            if self.fila:
                id_processo = self.fila[0]
                self.enviar_mensagem(id_processo, "GRANT")
                print("Acesso à região crítica concedido para o processo", id_processo)
                self.fila.pop(0)

    def enviar_mensagem(self, id_processo, mensagem):
        # Enviar uma mensagem para um processo especifico
        if id_processo in self.processos:
            socket_cliente = self.processos[id_processo]
            socket_cliente.send(mensagem.encode())

    def imprimir_fila(self):
        # Imprimir a fila de pedidos
        self.lock.acquire()
        print("\n== Fila de Pedidos ==")
        if self.fila:
            for id_processo in self.fila:
                print("Processo", id_processo)
        else:
            print("A fila de pedidos está vazia")
        print("=====================")
        self.lock.release()

    def imprimir_processos(self):
        # Imprimir os processos atendidos
        self.lock.acquire()
        print("\n== Processos Atendidos ==")
        if self.processos:
            for id_processo, socket_cliente in self.processos.items():
                print(f"Processo {id_processo} - Atendido", socket_cliente)
        else:
            print("Nenhum processo atendido ainda")
        print("========================")
        self.lock.release()

    def interface(self):
        # Interface do coordenador para interacao com o usuario
        while True:
            comando = input("\nComandos: 1) Imprimir fila de pedidos | 2) Imprimir processos atendidos | 3) Encerrar\n")
            if comando == "1":
                self.imprimir_fila()  # Chamar a funcao para imprimir a fila de pedidos
            elif comando == "2":
                self.imprimir_processos()  # Chamar a funcao para imprimir os processos atendidos
            elif comando == "3":
                self.encerrar_programa()  # Chamar a funcao para encerrar o programa

    def encerrar_programa(self):
        # Encerrar o programa
        print("Encerrando o programa...")
        sys.exit(0)

if __name__ == "__main__":
    coordenador = Coordenador("192.168.96.5", 5000, 10)
    coordenador.iniciar()

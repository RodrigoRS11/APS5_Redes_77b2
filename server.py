import threading
import socket
import mysql.connector
import time

host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
logins = []
senhas = []

jogo = 0

branco = " "
token = ["X", "O"]

jogador = 0 # jogador 1
board = [
        [branco, branco, branco],
        [branco, branco, branco],
        [branco, branco, branco],
        ]
ganhador = False

con = mysql.connector.connect(host='localhost',database='bancoteste',user='root',password='RS02112021')
if con.is_connected():
    db_info=con.get_server_info()
    print("Connectado ao servido mysql versao ",db_info)

def printBoard(board):
    for i in range(3):
        print("|".join(board[i]))
        message = ("|".join(board[i]).encode('utf-8'))
        broadcast(message)

        message = ('\n'.encode('utf-8'))
        broadcast(message)
        if(i < 2):
            print("------")
            message = ('------\n'.encode('utf-8'))
            broadcast(message)

def verificaMovimento(board, i , j):
    if(board[i][j] == branco):
        return True
    else:
        return False


def fazMovimento(board, i, j, jogador):
    board[i][j] = token[jogador]


def verificaGanhador(board):
    # linhas 
    for i in range(3):
        if(board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != branco):
            return board[i][0]
    
    # coluna
    for i in range(3):
        if(board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != branco):
            return board[0][i]

    # diagonal principal
    if(board[0][0] != branco and board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        return board[0][0]

    # diagonal secundaria
    if(board[0][2] != branco and board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        return board[0][2]

    for i in range(3):
        for j in range(3):
            if(board[i][j] == branco):
                return False

    return "EMPATE"

def game():
    print("Começando jogo")
    message = ('\nComeçando jogo\n'.encode('utf-8'))
    broadcast(message)
    
    ganhador = False
    jogador = 0
    while(not ganhador):
        if(jogador == 0):
            printBoard(board)
            print("Jogador X")
            message = ('Jogador X\n'.encode('utf-8'))
            broadcast(message)
        
            clients[0].send('linha?'.encode('utf-8'))
            linha = clients[0].recv(1024)
            print(linha)
            i = int(linha)

            clients[0].send('coluna?'.encode('utf-8'))
            coluna = clients[0].recv(1024).decode('utf-8')
            j = int(coluna)

        else:
            printBoard(board)
            print("Jogador O")
            message = ('Jogador O\n'.encode('utf-8'))
            broadcast(message)
        
            clients[1].send('linha?'.encode('utf-8'))
            linha = clients[1].recv(1024)
            print(linha)
            i = int(linha)

            clients[1].send('coluna?'.encode('utf-8'))
            coluna = clients[1].recv(1024).decode('utf-8')
            j = int(coluna)

        print("\n===================")
        message = ('\n===================\n'.encode('utf-8'))
        broadcast(message)

        print("\n===================")
        message = ('\n===================\n'.encode('utf-8'))
        broadcast(message)
        
        if(verificaMovimento(board, i, j)):
            fazMovimento(board, i, j, jogador)
            jogador = (jogador + 1)%2
        else:
            print("A posicao informado ja esta ocupada")
            message = ('A posicao informado ja esta ocupada\n'.encode('utf-8'))
            broadcast(message)
    
        ganhador = verificaGanhador(board)

    print("===================")
    message = ('===================\n'.encode('utf-8'))
    broadcast(message)
    
    printBoard(board)
    
    print("Ganhador = ", ganhador)
    message = (f'Ganhador = {ganhador}\n'.encode('utf-8'))
    broadcast(message)
    
    print("===================")
    message = ('===================\n'.encode('utf-8'))
    broadcast(message)
    

def autenticaLogin(l, s):
    try:
        login = l
        senha = s
        comando = f'SELECT * FROM usuario WHERE nome_usuario = "{login}" AND senha_usuario = "{senha}"'
        cursor = con.cursor()
        cursor.execute(comando)
        result = cursor.fetchall()
        cursor.close()

        if result == []:
            print("Nenhum resultado encontrado na autenticação, fazendo novo cadastro...")
            cadastraLogin(login, senha)
            return False 
        else:
            return True            
    except:
        print('ERRO na autenticacao!')

def cadastraLogin(l, s):
    try:
        login = l
        senha = s
        cursor = con.cursor()
        comando = f'INSERT INTO usuario (nome_usuario, senha_usuario) VALUES ("{login}", "{senha}")'
        cursor.execute(comando)
        con.commit()
        cursor.close()
    except:
        print("ERRO no cadastro")  
    
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients'connections
def handle_client(client):
    global jogo
    threadHand = 0
    while threadHand == 0:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == '!jogo':
                broadcast(message)
                threadHand = 1
                jogo = jogo + 1
            if message.decode('utf-8') == 'login?':
                print("Ja logado")
            if message.decode('utf-8') == 'senha?':
                print("Ja logado")
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            login = logins[index]
            broadcast(f'{login} Saiu do chat da sala!'.encode('utf-8'))
            print(f'{login} Saiu do chat da sala!')
            logins.remove(login)
            break
        
# Main function to receive the clients connection
def receive():
    nClientes = 0
    while nClientes < 2:
        print('Servidor esta rodando  e ouvindo ...')
        client, address = server.accept()
        print(f'conexao feita  com {str(address)}')
        
        client.send('login?'.encode('utf-8'))
        login = client.recv(1024).decode('utf-8')
        
        logins.append(login)
        clients.append(client)

        client.send('senha?'.encode('utf-8'))
        senha = client.recv(1024).decode('utf-8')

        time.sleep(1)
        
        senhas.append(senha)

        result = autenticaLogin(login, senha)

        if result == True:
            msg = (f'Cliente {login} Logado com sucesso!!!\n'.encode('utf-8'))
            broadcast(msg)
        else:
            msg = (f'Cliente {login} Cadastrado e Logado com sucesso!!!\n'.encode('utf-8'))
            broadcast(msg)

        client.send('Agora você esta conectado!\n'.encode('utf-8'))
        
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

        nClientes = nClientes + 1


if __name__ == "__main__":
    receive()
    count = 0
    while count == 0:
        if jogo == 2:
            game()
            count = 1

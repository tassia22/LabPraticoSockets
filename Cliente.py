import socket

import socket

def conectar_ao_servidor(ip, porta):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, porta))
        print("Conexão com o servidor estabelecida")
        return client_socket
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def cadastrar_conta(client_socket):
    username = input("Digite um username: ")
    senha = input("Digite uma senha: ")
    nome = input("Digite seu nome completo: ")

    requisicao = f"CADASTRAR|{username}|{senha}|{nome}"
    client_socket.send(requisicao.encode('utf-8'))
    resposta = client_socket.recv(1024).decode('utf-8')
    print(resposta)

def fazer_login(client_socket):
    username = input("Digite seu username: ")
    senha = input("Digite sua senha: ")

    requisicao = f"LOGIN|{username}|{senha}"
    client_socket.send(requisicao.encode('utf-8'))
    resposta = client_socket.recv(1024).decode('utf-8')
    print(resposta)

def enviar_email(client_socket):
    de = input("De: ")
    para = input("Para: ")
    assunto = input("Assunto: ")
    corpo = input("Corpo do e-mail: ")

    requisicao = f"ENVIAR_EMAIL|{de}|{para}|{assunto}|{corpo}"
    client_socket.send(requisicao.encode('utf-8'))
    resposta = client_socket.recv(1024).decode('utf-8')
    print(resposta)

def receber_emails(client_socket):
    username = input("Digite seu username: ")
    requisicao = f"RECEBER_EMAILS|{username}"
    client_socket.send(requisicao.encode('utf-8'))
    resposta = client_socket.recv(1024).decode('utf-8')
    print("Seus e-mails:")
    print(resposta)

def main():
    client_socket = None
    ip_servidor = "tassiasd.ddns.net"
    porta_servidor = 12345

    while True:
        print("\n-- Menu --")
        print("1. Conectar ao servidor")
        print("2. Cadastrar conta")
        print("3. Fazer login")
        print("4. Enviar e-mail")
        print("5. Receber e-mails")
        print("6. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            client_socket = conectar_ao_servidor(ip_servidor, porta_servidor)

        elif escolha == "2":
            if client_socket:
                cadastrar_conta(client_socket)
            else:
                print("Conecte-se ao servidor primeiro.")

        elif escolha == "3":
            if client_socket:
                fazer_login(client_socket)
            else:
                print("Conecte-se ao servidor primeiro.")

        elif escolha == "4":
            if client_socket:
                enviar_email(client_socket)
            else:
                print("Conecte-se ao servidor primeiro.")

        elif escolha == "5":
            if client_socket:
                receber_emails(client_socket)
            else:
                print("Conecte-se ao servidor primeiro.")

        elif escolha == "6":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    if client_socket:
        client_socket.close()

if __name__ == "__main__":
    main()
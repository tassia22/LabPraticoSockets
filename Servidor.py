import socket
import threading
from datetime import datetime

contas = {}  
emails = [] 

def lidar_com_cliente(client_socket):
   
    while True:
        try:
            
            requisicao = client_socket.recv(1024).decode('utf-8')
            if not requisicao:
                break

            partes = requisicao.split('|')
            comando = partes[0]  

            if comando == "CADASTRAR":
                username = partes[1]
                senha = partes[2]  
                nome = partes[3]

                if username in contas:
                    client_socket.send("Erro: Username já existe.".encode('utf-8'))
                else:
                    contas[username] = {'nome': nome, 'senha': senha}
                    client_socket.send("Conta criada com sucesso!".encode('utf-8'))

            elif comando == "LOGIN":
                username = partes[1]
                senha = partes[2]

                if username in contas and contas[username]['senha'] == senha:
                    client_socket.send(f"Bem-vindo, {contas[username]['nome']}!".encode('utf-8'))
                else:
                    client_socket.send("Erro: Usuário ou senha inválidos.".encode('utf-8'))

            elif comando == "ENVIAR_EMAIL":
                de = partes[1]
                para = partes[2]
                assunto = partes[3]
                corpo = partes[4]

                if para in contas:
                    email = {
                        'de': de,
                        'para': para,
                        'assunto': assunto,
                        'corpo': corpo,
                        'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    emails.append(email)
                    client_socket.send("E-mail enviado com sucesso".encode('utf-8'))
                else:
                    client_socket.send("Erro: Destinatário não existe.".encode('utf-8'))

            elif comando == "RECEBER_EMAILS":
                username = partes[1]
                emails_usuario = [email for email in emails if email['para'] == username]
                client_socket.send(str(emails_usuario).encode('utf-8'))

        except Exception as e:
            print(f"Erro: {e}")
            break

    client_socket.close()

def iniciar_servidor():
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 12345)) 
    servidor.listen(5)
    print("Servidor escutando na porta 12345...")

    while True:
        client_socket, addr = servidor.accept()
        print(f"Conexão aceita de {addr}")
        cliente_handler = threading.Thread(target=lidar_com_cliente, args=(client_socket,))
        cliente_handler.start()

if __name__ == "__main__":
    iniciar_servidor()
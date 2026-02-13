from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
# This is the "Welcoming door"
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    #This is the dedicated socket
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
from socket import *

# taking port number input
serverPort = int(input("Input port number: "))
serverSocket = socket(AF_INET, SOCK_STREAM)
# This is the "Welcoming door"
# "" means listening on all available network interface
try:
    serverSocket.bind(("", serverPort))
except OSError as e:
    print("Error: ", e)

serverSocket.listen(1)
print("The server is ready to receive on port", serverPort)

try:
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Created a connection...")
        # This is the dedicated socket
        sentence = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence.encode())
        connectionSocket.close()
        print("Closed a connection")
except KeyboardInterrupt:
    print("Closing server...")

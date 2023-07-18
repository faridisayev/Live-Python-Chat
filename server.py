import socket, threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((socket.gethostname(), 9999))

server_socket.listen()

# Create real time storage for clients and aliases

clients = []
aliases = []

# Broadcast message

def broadcast(message):
    for client in clients:
        client.send(f'\n{message}'.encode('ascii'))

# Handle client message

def handle_client(client):

    while True:

        try:

            message = client.recv(1024).decode('ascii')
            broadcast(message)

        except:

            # Get client index 
            
            client_index = clients.index(client)

            # Close connection and remove from clients

            client.close()
            clients.remove(client)

            # Remove aliase 

            aliase = aliases[client_index]
            aliases.remove(aliase)

            # Broadcast 

            broadcast(f'{aliase} has left the chat')

            # Break from loop

            break

# Receive incoming connection requests

def receive():

    while True:

        print('\nListening for incoming requests ...')

        # Accept the request

        client, address = server_socket.accept()

        print(f'\n{address[0]} connected to server on port {address[1]} ...')

        # Request aliase 

        client.send('ALIASE'.encode('ascii'))

        aliase = client.recv(1024).decode('ascii')

        # Store client and their aliase 

        clients.append(client)

        aliases.append(aliase)

        # Inform clients

        print(f'\n{address[0]} joined as {aliase} ...')

        broadcast(f'\n{aliase} joined the chat ...')

        client.send(f'\nYou have joined the chat as {aliase} ...'.encode('ascii'))

        # Create a separate thread for the client

        thread = threading.Thread(target = handle_client, args = (client,))

        thread.start()

# Run receive function 

if __name__ == '__main__':
    receive()

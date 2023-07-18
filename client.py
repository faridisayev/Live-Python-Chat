import socket, threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server

client_socket.connect((socket.gethostname(), 9999))

# Store user aliase to use later

aliase = input('\nChoose your alise: ')

# Define a receive function 

def receive():

    while True:

        try:

            message = client_socket.recv(1024).decode('ascii')

            if message == 'ALIASE':

                # Send the aliase on demand 

                client_socket.send(aliase.encode('ascii'))

            if len(message) > 0:

                print(message)

        except:

            print('\nWhile receiving a message, an error occured ...')

            client_socket.close()

            break

# Define a send function 

def send():

    while True:

        message = input('')

        client_socket.send(f'\n{aliase}: {message}'.encode('ascii'))

# Create two threads, one for receiving messages and one for sending messages

receive_thread = threading.Thread(target = receive)
send_thread = threading.Thread(target = send)

receive_thread.start()
send_thread.start()

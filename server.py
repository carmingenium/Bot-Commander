# SERVER CODE
# server.py

import socket
import threading

# Server needs to be accessible from anywhere, so we use '0.0.0.0' as the host to bind to all available interfaces.
def start_server():
  HOST = '0.0.0.0'  # Bind to all interfaces
  PORT = 12332  # Choose a port that is not commonly used

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((HOST, PORT))
  server_socket.listen(5)  # Allow up to 5 connections

  print(f"Server started on port {PORT}. Waiting for connections...")

  # Function to handle client connections
  def handle_client(client_socket, address):
    print(f"Connection established with {address}")
    try:
      while True:
        # Receive message from client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
          break
        print(f"Received from {address}: {data}")

        # Echo the message back
        response = f"Echo: {data}"
        client_socket.send(response.encode('utf-8'))
    except Exception as e:
      print(f"Error with client {address}: {e}")
    finally:
      print(f"Connection with {address} closed.")
      client_socket.close()

  while True:
    client_socket, address = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
    client_handler.start()



# functions planned to be implemented

# constant active function: show_status() # displays current status of all bots


# add(botname, location) # adds a new bot to the server
  # check if bot already exists


# start(botname) # starts given bot


# stop(botname) # stops given bot


# update(botname) # pulls latest changes from git
  # checks if bot is online first, if so, stop(botname)
  
# checkdata(botname) # displays current data for all servers.
  # display all servers
  # give option to display data of a specific server

# end of planned functions

if __name__ == "__main__":
  start_server()
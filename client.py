import socket
import threading

# UI PART #
# When no other function is active, only result of this function should be shown on the screen (just status for every bot)
# when any other function is active, program should be a black screen with only results from active function and input of the client.
# this UI should be on the client.

def start_client(server_ip):
  PORT = 12332

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    client_socket.connect((server_ip, PORT))
    print(f"Connected to server at {server_ip}:{PORT}")

    while True:
      message = input("Enter message to send (type 'exit' to quit): ")
      if message.lower() == 'exit':
        break

      client_socket.send(message.encode('utf-8'))
      response = client_socket.recv(1024).decode('utf-8')
      print(f"Server responded: {response}")
  except Exception as e:
    print(f"Error connecting to server: {e}")
  finally:
    print("Closing connection.")
    client_socket.close()

if __name__ == "__main__":
  server_ip = input("Enter server IP address: ").strip()
  start_client(server_ip)
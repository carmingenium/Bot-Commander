import socket
import threading
import time
# UI #
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize Colorama to fix Windows CMD issues


# UI PART #
# When no other function is active, only result of this function should be shown on the screen (just status for every bot)
# when any other function is active, program should be a black screen with only results from active function and input of the client.
# this UI should be on the client.
# UI Function #
def highlight_last_part(text, color):
  if ':' not in text:
    return text  # If no ":", return original
  before, _, last_part = text.rpartition(':')  # Split at the last ":"  
  colored_last_part = color + last_part.strip() + Style.RESET_ALL  # Apply color
  return f"{before}: {colored_last_part}"  # Reconstruct the full string


# there could be a list of keywords defined to understand which type of message is being sent from the server 
# (echo, error, status, response, etc.)
testlist = ["echo", "erro", "stat", "resp"] # keeping them 4 letters for ease of use





def handle_recv(client_socket, msg): 
  msgtype = msg[:4]
  if msgtype in testlist:
    print(f"{msgtype}  ", end="")
    if msgtype == "echo":
      msg = msg[6:-1]
      echo = Fore.CYAN + msg + Fore.RESET
      print(f"{echo}")

    elif msgtype == "erro":
      error = Fore.RED + "Error message from server: " + Fore.RESET
      print(f"{error}{msg[4:]}")

    elif msgtype == "stat":
      message = msg[msg.rfind(":")+2]
      if (message == "ONLINE"):
        message = highlight_last_part(msg, Fore.GREEN)
      else:
        message = highlight_last_part(msg, Fore.GREEN)
      print(f"Status update: {message[6:-1]}")
      
    elif msgtype == "resp":
      msg = msg[4:]
      msg = Fore.YELLOW + msg + Fore.RESET 
      print(f"Response message: {msg}")


  else:
    print(f"Message type error")
    return


def listener(client_socket):
  print(f"Starting listener.")
  try:
    while True:
      response = client_socket.recv(1024).decode('utf-8')
      print()
      handle_recv(client_socket, response)
  except Exception as e:
    print(f"Error with receiving a message: {e}")
  finally:
    print(f"Client socket closed.")
    client_socket.close()

def send_message(client_socket):
  time.sleep(0.1)
  print(f"Starting message sending thread.")
  try:
    while True:
      message = input("\nEnter message to send (type 'exit' to quit): ")
      if message.lower() == 'exit':
        client_socket.close()
      client_socket.send(message.encode('utf-8'))
      print(f"Message sent: {message}")
      time.sleep(1.5)
  except Exception as e:
    print(f"Error with sending a message: {e}")
  finally:
    print(f"Message sending thread closed.")

def start_client(server_ip):
  PORT = 12332
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    client_socket.connect((server_ip, PORT))
    print(f"Connected to server at {server_ip}:{PORT}")
    # start message sending thread:
    #   to separate the listening and sending systems.
    #   because client can only receive after client sends a message if they are combined.
    #   thats would be a problem because server will keep sending updates on bot updates etc.
    response_handler = threading.Thread(target=send_message, args=(client_socket,))
    response_handler.start()
    listener(client_socket)

    

  except Exception as e:
    print(f"Error connecting to server: {e}")
  finally:
    print("Closing connection.")
    client_socket.close()

if __name__ == "__main__":
  server_ip = input("Enter server IP address: ").strip()
  start_client(server_ip)
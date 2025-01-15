import socket
import threading
# DATABASE START # PLANNING TO SETUP DATABASE PART IN ANOTHER SCRIPT TO MODULARIZE TWO PARTS OF THE CODE, PLUS HOPING TO HAVE EASIER TIME TESTING
import sqlite3
from sqlite3 import Error
# DATABASE END

# Variables
HOST = '0.0.0.0'  # Bind to all interfaces
PORT = 12332
global server_socket
global botlist
global dbconnection
global clientlist
# Variables end

# Bot class for testing
class Bot:
  name = ""
  status = ""
  def __init__(self, name, status):
    self.name = name
    self.status = status



# Server needs to be accessible from anywhere, so we use '0.0.0.0' as the host to bind to all available interfaces.
def start_server():
  # creating listener socket.
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((HOST, PORT))
  server_socket.listen(5)  # Allow up to 5 connections

  print(f"Server started on port {PORT}. Waiting for connections...")
  # listener done.
  
  # connecting to database
  # load botlist -string list- from database.
  
  # for now, botlist is going to be manually set, because database implementation moved to last step.
  botlist = ["AM"]
  
  return server_socket, botlist

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


def add(botname, client): # adds a new bot to the botlist and therefore botcommander.
  print(f"Adding bot {botname}")
  # send this print to client also
  
  # check if bot already exists
  #   if exists, return error
  #   else, add to  database and refresh database variable
  
def remove(botname, client):
  print(f"Removing bot {botname}")
  # send this print to client also
  
  # check if bot exists
  #   if not, return error
  # check if bot is online
  #   if online, return error
  # remove bot from database and refresh database variable
  
def start(botname, client):
  print(f"Starting bot {botname}")
  # send this print to client also
  
  # check if bot exists
  #   if not, return error
  # check if bot is online
  #   if online, return error
  # start bot

def stop(botname, client):
  print(f"Stopping bot {botname}")
  # send this print to client also
  
  # check if bot exists
  #   if not, return error
  # check if bot is offline
  #   if offline, return error
  # stop bot

def update(botname, client):
  print(f"Updating bot {botname}")
  # send this print to client also
  
  # check if bot exists
  #   if not, return error
  # check if bot is online
  #   if online, stop bot
  # update bot from github
  
def checkdata(botname, client):
  print(f"Checking data for bot {botname}")
  # send this print to client also
  
  # check if bot exists
  #   if not, return error
  # check if bot is online
  #   if offline, return error
  # get data of bot from database
  # send client all the server names of the server data
  # give option to display data of a specific server
  # COULD LATER ADD CODE THAT SPESIFIES WHICH SERVERS DATA CAN BE REQUESTED FROM SPESIFIC CLIENTS FOR SECURITY.

def show_status(clientlist):
  # show online / offline status 
  # status will be changed on database by the bots, on status change this function needs to rerun to update the status.

  return
  
def main():
  if __name__ == "__main__":
    server_socket, botlist = start_server()
  else:
    print("Server failed to start, used by another module. Exiting...")
    return
  
  while True: # Keep the server running, listening for clients
    # create a new thread for automatic status update.
    # start show_status() and create the list of activebotlist -string list-.
    client_socket, address = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, address)) # new thread for every client
    client_handler.start()
    

main()

# TBD:
#      1-) Adding, starting, stopping bots
#      2-) Status update function
#      3-) Update bots
#      Database moved to last, because development is moving on a test machine and database implementation will slow down the process for now.
#      4-) Database setup, connection (SQLite)
#      5-) Data check function
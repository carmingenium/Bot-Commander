# Main #
import time
import socket
import threading
import subprocess
# DATABASE START # PLANNING TO SETUP DATABASE PART IN ANOTHER SCRIPT TO MODULARIZE TWO PARTS OF THE CODE, PLUS HOPING TO HAVE EASIER TIME TESTING
import sqlite3
from sqlite3 import Error
# DATABASE END
# UI #
from colorama import Fore


# Variables
HOST = '0.0.0.0'  # Bind to all interfaces
PORT = 12332
global server_socket
global botlist
global dbconnection
global clientlist
# Variables end



# function to run bots.
def run_script_external(script_path):
  """Executes a Python script as a separate process."""
  try:
    subprocess.run(["python", script_path], check=True)
    return "Script executed successfully."
  except subprocess.CalledProcessError as e:
    return f"Error executing script: {e.stderr}"


# Bot class for testing
class Bot:
  name = ""
  status = ""
  location = ""
  def __init__(self, name, status, location):
    self.name = name
    self.status = status
    self.location = location
  def get_name(self):
    return self.name
  def get_status(self):
    return self.status
  def get_location(self):
    return self.location
  def update_bot(self, name, location):
    self.name = name
    self.status = "offline"
    self.location = location
  def update_status(self, status):
    self.status = status
# Server needs to be accessible from anywhere, so we use '0.0.0.0' as the host to bind to all available interfaces.
def start_server():
  # creating listener socket.
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((HOST, PORT))
  server_socket.listen(2)  # Allow up to 2 connections

  print(f"Server started on port {PORT}. Waiting for connections...")
  # listener done.
  
  # connecting to database
  # load botlist -string list- from database.
  
  # for now, botlist is going to be manually set, because database implementation moved to last step.
  botlist = ["AM.py"] # for tests, this place can be set empty or not.
  
  return server_socket, botlist
# Function to accept clients - listener
def accept_clients(server_socket):
  while True: # Keep the server running, listening for clients
    # create a new thread for every client, for automatic status update.
    # start show_status() and create the list of activebotlist -string list-.
    client_socket, address = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, address)) # new thread for every client
    client_handler.start()
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
      echo_message(client_socket, response.encode('utf-8'))
  except Exception as e:
    print(f"Error with client {address}: {e}")
  finally:
    print(f"Connection with {address} closed.")
    client_socket.close()

# Basic Bot Actions
def add(botname, client, botlist): # adds a new bot to the botlist and therefore botcommander.
  print(f"Adding bot {botname}")
  response_message(client, (f"Adding bot {botname}".encode('utf-8')))

  # check if bot already exists
  if(botname in botlist):   #   if exists, return error
    print("Bot already exists.")
    response_message(client,"Bot already exists.".encode('utf-8'))
    return
  
  # around here need to add a system that checks for the github page or the file to find the actual bot.
  # and manage to run it without errors.

  # else, add to database and refresh database variable
  if (botname[-3:] != ".py"): # check if .py is in the name.
    botname = botname + ".py"
  botlist.append(botname)
  # add to database 
  # refresh database variable (sync with database)


  print(f"Added bot {botname}")
  response_message(client ,f"Added bot {botname}".encode('utf-8'))
  return
def change(botname, newbotname, client):
  print(f"Changing bot {botname} to {newbotname}")
  response_message(client, f"Changing bot {botname} to {newbotname}".encode('utf-8'))

  # check if bot exists
  if(botname not in botlist):
    # if not, return error   
    print("Bot does not exist.")
    # send this print to client also
    response_message(client,"Bot does not exist.".encode('utf-8'))
    return
  # check if bot is online
  #   if online, return error

  # change bot name in database and refresh database variable
  # maybe new functions for database interactions?

  print(f"Changed bot {botname} to {newbotname}")
  # send this print to client also
  response_message(client,f"Changed bot {botname} to {newbotname}".encode('utf-8'))
  return
def remove(botname, client):
  print(f"Removing bot {botname}")
  response_message(client, f"Removing bot {botname}".encode('utf-8'))
  
  # check if bot exists
  #   if not, return error
  # check if bot is online
  #   if online, return error
  # remove bot from database and refresh database variable
def start(botname, client, botlist):
  print(f"Starting bot {botname}")
  echo_message(client, f"Starting bot {botname}")
  
  try:
    # check if bot exists
    if (botname not in botlist):
      #   if not, return error
      print("Bot does not exist.")
      response_message(client, "Bot does not exist.".encode('utf-8'))
      return
    startingbot = botlist[botlist.index(botname)]
    # check if bot is online
    if (startingbot.get_status() == "online"):
      #   if online, return error
      print("Bot is already online.")
      response_message(client, "Bot is already online.".encode('utf-8'))
      return
    # start bot
    err = run_script_external(startingbot.get_location())
    if (err != "Script executed successfully."):
      raise Exception(err)    
  except Exception as e:
    print(f"Error starting bot {botname}: {e}")
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
def schedule_maintenance(botname, client):
  # used to set dates for maintenance
  # stops all bot activity, saves all data
  # could have/become its own discord bot to log everything on a discord server.
  return
# Data functions
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
def show_status(clientlist, botlist):
  # show online / offline status 

  # status will be changed on database by the bots,
  # on status change this function needs to rerun to update the status.
  status = ""
  for bot in botlist:
    status += f"{bot.name}: {bot.status}\n" # need to colorize and make pretty later on
  for client in clientlist:
    status_message(client, status) 
  return 
  
# Message type definition
def echo_message(client, message):
  client.send(f"echo{message}".encode('utf-8'))
  return
def error_message(client, message):
  client.send(f"erro{message}".encode('utf-8'))
  return
def status_message(client, message):
  client.send(f"stat{message}".encode('utf-8'))
  return
def response_message(client, message):
  client.send(f"resp{message}".encode('utf-8'))
  return





def main():
  if __name__ == "__main__":
    server_socket, botlist = start_server()
  else:
    print("Server failed to start, used by another module. Exiting...")
    return
  
  # setting up listener thread separately from main thread.
  client_accepter = threading.Thread(target=accept_clients, args=(server_socket,))
  client_accepter.start()

  # setup a current state for bots
  statelist = []
  for bot in botlist:
    statelist.append(Bot(bot, bot.status))

  # bot status checking and updating loop
  while True:
    # separated listeners from main thread to check bot changes every x seconds.
    # wait x seconds
    time.sleep(15)
    # bot checking functionality (not defined, not used anywhere else)
    check = False
    for bot in botlist:
      if bot.status != statelist[botlist.index(bot)].status: # might create error
        # update check
        check = True
        # update botlist
        statelist[botlist.index(bot)].status = bot.status
        # update bot status for every client.
        pass
    if (check):
      show_status(clientlist, botlist)
      check = False

main()
# TBD:
#      1-) Adding, starting, stopping bots    ADD half done, START DONE, STOP not done
#      2-) Status update function             DONE 
#      3-) Update bots
#      Database moved to last, because development is moving on a test machine and database implementation will slow down the process for now.
#      4-) Database setup, connection (SQLite (?))
#      5-) Data check function
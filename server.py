# Main #
import time
import socket
import threading
import subprocess
# Scheduling
from apscheduler.schedulers.background import BackgroundScheduler # pip install apscheduler
import datetime
# DATABASE START # PLANNING TO SETUP DATABASE PART IN ANOTHER SCRIPT TO MODULARIZE TWO PARTS OF THE CODE, PLUS HOPING TO HAVE EASIER TIME TESTING
import sqlite3
from sqlite3 import Error
# DATABASE END
# UI #
from colorama import Fore # pip install colorama


# Variables
HOST = '0.0.0.0'  # Bind to all interfaces
PORT = 12332
global server_socket
global online_botlist
global botlist
global dbconnection
global clientlist
global scheduler
# Variables end



# irrelevant functions
def run_script_external(bot, online_botlist):
  """Executes a Python script as a separate process."""
  try:
    online_botlist.append(subprocess.run(["python", bot.get_location], check=True))
    # if successful
    bot.update_status("online")
    return "Script executed successfully.", online_botlist
  except subprocess.CalledProcessError as e:
    return f"Error executing script: {e.stderr}", online_botlist
def convert_to_datetime(date_string):
  """
  Converts a string in the format '(YYYY, MM, DD, HH, MM)' to a datetime object.
  """
  try:
    # Remove parentheses and split the string by commas
    date_parts = date_string.strip("()").split(", ")
    
    # Convert each part to an integer
    year, month, day, hour, minute = map(int, date_parts)
    
    # Create and return a datetime object
    return datetime(year, month, day, hour, minute)
  
  except ValueError as e:
    print(f"Invalid format: {e}")
    return None

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

# UI
def menu():
  # main menu.
  # comes up on startup with status update?
  # need to find a place to put this
  # this is necessary to show the user what the inputs should be for every function and what the functions are.
  return
# Basic Bot Actions
def add(botname, client, botlist): # adds a new bot to the botlist and therefore botcommander.
  response_message(client, (f"Adding bot {botname}"))

  # check if bot already exists
  if(botname in botlist):   #   if exists, return error
    response_message(client,"Bot already exists.")
    return
  # around here need to add a system that checks for the github page or the file to find the actual bot.
  # and manage to run it without errors.

  # else, add to database and refresh database variable
  if (botname[-3:] != ".py"): # check if .py is in the name.
    botname = botname + ".py"
  botlist.append(botname)
  # add to database 
  # refresh database variable (sync with database)
  response_message(client ,f"Added bot {botname}")
  return
def change(botname, newbotname, client):
  response_message(client, f"Changing bot {botname} to {newbotname}")

  # check if bot exists
  if(botname not in botlist):
    # if not, return error   
    # send this print to client also
    response_message(client,"Bot does not exist.")
    return
  # check if bot is online
  #   if online, return error

  # change bot name in database and refresh database variable
  # maybe new functions for database interactions?

  # send this print to client also
  response_message(client,f"Changed bot {botname} to {newbotname}")
  return
def remove(botname, client):
  response_message(client, f"Removing bot {botname}")
  
  # check if bot exists
  #   if not, return error
  # check if bot is online
  #   if online, return error
  # remove bot from database and refresh database variable
def start(botname, client, botlist, online_botlist):
  echo_message(client, f"Starting bot {botname}")
  
  try:
    # check if bot exists
    if (botname not in botlist):
      #   if not, return error
      response_message(client, "Bot does not exist.")
      return
    startingbot = botlist[botlist.index(botname)]
    # check if bot is online
    if (startingbot.get_status() == "online"):
      #   if online, return error
      response_message(client, "Bot is already online.")
      return
    # start bot
    err, online_botlist = run_script_external(startingbot, online_botlist)
    if (err != "Script executed successfully."):
      raise Exception(err)    
  except Exception as e:
    response_message(client, f"Error starting bot {botname}: {e}")
  response_message(client, f"Started bot {botname}")
def stop(botname, client, botlist, online_botlist):
  response_message(client, f"Stopping bot {botname}")
  
  # check if bot exists
  if (botname not in botlist):
    #   if not, return error
    response_message(client, f"Bot '{botname}' does not exist.")
    return
  # check if bot is offline
  if(botname not in online_botlist):
    #   if offline, return error
    response_message(client, f"Bot '{botname}' is already offline.")
    return
  # before stopping, do any saving or take needed precautions.
  #empty
  # stop bot
  online_botlist[online_botlist.index(botname)].terminate()
  online_botlist[online_botlist.index(botname)].wait()
  online_botlist.remove(botname) # could create errors
  response_message(client, f"Stopped bot {botname}")
def update(botname, client, botlist, online_botlist):
  response_message(client, f"Updating bot {botname}")
  # check if bot exists
  if(botname not in botlist):
    #   if not, return error
    response_message(client, f"Bot '{botname}' does not exist.")
    return
  # check if bot is online
  if(botname in online_botlist):
    #   if online, stop bot
    stop(botname, client, botlist, online_botlist)
  # update bot from github
  # maybe add a variable to bot for this? idk
def schedule_maintenance(botname, client, time, botlist): # Set maintenance time (YYYY, MM, DD, HH, MM) #bot name is also used on a switch
  # used to set dates for maintainence
  maintenance_time = convert_to_datetime(time)
  if botname in botlist:
    # If botname is in botlist, it is a bot
    scheduler.add_job(bot_maintenance, 'date', run_date=maintenance_time, args=[client, [botname], online_botlist])
  elif botname == "bot":
    # Full bot maintenance
    for bot in botlist:
      scheduler.add_job(bot_maintenance, 'date', run_date=maintenance_time, args=[client, botlist, online_botlist])
  elif botname == "commander":
    # Self maintenance
    scheduler.add_job(self_maintenance, 'date', run_date=maintenance_time, args=[client, [], online_botlist])
  elif botname == "0":
    # Full maintenance (first bots, then commander)
    for bot in botlist:
      scheduler.add_job(bot_maintenance, 'date', run_date=maintenance_time, args=[client, botlist, online_botlist])
    scheduler.add_job(self_maintenance, 'date', run_date=maintenance_time + datetime.timedelta(minutes=1), args=[client, [], online_botlist])
  else:
    response_message(client, "Invalid botname for maintenance.")
    return
  print(f"Scheduling maintenance for bot {botname} at {time}")
  client.send(f"Scheduling maintenance for bot {botname} at {time}".encode('utf-8'))
  # could have/become its own discord bot to log everything on a discord server.
  return
def bot_maintenance(botname, client, botlist, online_botlist):
  # given bot activity
  # data save should be in stop function
  bot = botlist[botlist.index(botname)]
  stop(bot, client, botlist, online_botlist)
  return
def self_maintenance(client, botlist, online_botlist):
  # save all bot commander data
  # stop bot commander
  return
# Data functions
def checkdata(botname, client):
  response_message(client, f"Checking data of bot {botname}")
  
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
  print(f"Echoing message: {message}")
  client.send(f"echo{message}".encode('utf-8'))
  return
def error_message(client, message):
  print(f"Error: {message}")
  client.send(f"erro{message}".encode('utf-8'))
  return
def status_message(client, message):
  client.send(f"stat{message}".encode('utf-8'))
  return
def response_message(client, message):
  print(f"Response: {message}")
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

  # setting up maintenance thread
  scheduler = BackgroundScheduler()
  scheduler.start()
  # not fully decided on set interval maintenance, not sure if needed. skipping for now.

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
#      1-) Adding, starting, stopping bots    DONE FOR NOW | ADD half done (db, git)(finished later.), START DONE, STOP DONE
#      2-) Status update function             DONE 
#      3-) Update bots                        DONE FOR NOW | github issue
#      4-) Scheduling                         DONE
#      4.1 -) Refactoring
#      5-) Status formatting
#      6-) Making functions usable by the clients
#      7-) Testing
#      Database moved to last, because development is moving on a test machine and database implementation will slow down the process for now.
#      4-) Database setup, connection (SQLite (?))
#      5-) Data check function
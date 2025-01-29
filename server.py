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

# Security Notes #
#
# 1-) Exclusivity, Data Integrity
#   Multiple layers of connection, not every client should reach every data. And client should mostly be readonly (tbd)

# User System
# After version 1.0 has been finished, a new user system could be implemented.
# This system would need the global connection system to be done.
# Users of these bots could send applications for different levels of usership.
# Later on they can view or change data of the bots they have access to according to the usership.

# Variables
HOST = '0.0.0.0'  # Bind to all interfaces
PORT = 12332
server_socket = None
"""
Servers socket that clients connect to.
"""
botlist = None # holds Bot class objects.
"""
List of bots that the server manages.

Contains only 'Bot' class objects.
"""
online_botlist = None # may only be needed for terminating bots.
"""
List of bots that are currently online.

Contains subprocesses.
"""
clientlist = None
"""
List of clients that are currently connected to the server.

Contains sockets.
"""

scheduler = None # maintenance scheduler
"""
Scheduler for maintenance tasks.

Acts as a different thread (?)
"""
# Variables end



# irrelevant functions
def run_script_external(bot):
  """
  Executes a Python script as a separate process.

  Parameters
  ----------
  bot : Bot
    The bot to execute
  
  Returns
  -------
  str
    The output of the script execution (error or success message)
  """
  try:
    global online_botlist
    online_botlist.append(subprocess.run(["python", bot.get_location()], check=True))
    # if successful
    bot.update_status("online")
    return "Script executed successfully."
  except subprocess.CalledProcessError as e:
    return f"Error executing script: {e.stderr}"
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
def botfinder(botname):
  for bot in botlist:
    if bot.get_name() == botname:
      return bot
  return None
# Bot class
class Bot:
  """
  Class to represent discord bots.

  Variables:
  ----------
  name : str
    The name of the bot
  status : str
    The status of the bot (online or offline)
  location : str
    The location of the bot script
  
  Methods:
  --------
  get_name()
  get_status()
  get_location()

  update_bot(name, location)
  update_status(status)
  """
  name = ""
  status = ""
  location = ""
  # might add a github link var here.
  # with the github link var, location could be created by the commander for any added bot.
  def __init__(self, name, location = None, status = "offline"):
    """
    Constructor for the Bot class.
    """
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
    """
    Updates the bot's name and location.

    Sets the status offline automatically.

    This method needs to be used carefully, bot shouldn't be online while updating.
    """
    self.name = name
    self.status = "offline" #!
    self.location = location
  def update_status(self, status):
    self.status = status

# Connection functions
# Server needs to be accessible from anywhere, so we use '0.0.0.0' as the host to bind to all available interfaces.
def start_server():
  """
  Starts the server and returns the server socket and botlist.

  Updates botlist without the use of global
  """
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
  """
  Accepts clients and creates a new thread to handle each client.
  """
  global clientlist
  while True: # Keep the server running, listening for clients
    # create a new thread for every client, for automatic status update.
    # start show_status() and create the list of activebotlist -string list-.
    client_socket, address = server_socket.accept()

    client_handler = threading.Thread(target=handle_client, args=(client_socket, address)) # new thread for every client
    client_handler.start()
# Function to handle client connections
def handle_client(client_socket, address):
  """
  Listens the client constantly for input.

  Puts the client into clientlist to keep track of active clients.
  """
  global clientlist
  clientlist.append(client_socket)
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
    clientlist.remove(client_socket)
    client_socket.close()

# UI
def menu():
  # main menu.
  # comes up on startup with status update?
  # need to find a place to put this
  # this is necessary to show the user what the inputs should be for every function and what the functions are.
  return
# Basic Bot Actions
def add(botname, client, location = None): # adds a new bot to the botlist and therefore botcommander.
  """
  Adds a bot to the botlist.

  Github and database sync is not implemented yet.
  """
  global botlist
  response_message(client, (f"Adding bot {botname}"))

  # check if bot already exists
  bot = botfinder(botname)
  if(bot != None):
    response_message(client, f"Bot {botname} already exists.")
    return
  # around here need to add a system that checks for the github page or the file to find the actual bot.
  # and manage to run it without errors.

  # else, add to database and refresh database variable
  # this .py stuff is likely useless and irrelevant
  if (botname[-3:] != ".py"): # check if .py is in the name.
    botname = botname + ".py"
  botlist.append(Bot(botname, location))
  # add to database 
  # refresh database variable (sync with database)
  response_message(client ,f"Added bot {botname}")
  return
def remove(botname, client):
  """
  Removes a bot from the botlist.

  Database sync not implemented yet.
  """
  global botlist
  response_message(client, f"Removing bot {botname}")
  
  # check if bot exists
  bot = botfinder(botname)
  #   if not, return error
  if(bot == None):
    response_message(client, f"Bot {botname} does not exist.")
    return
  # check if bot is online
  if(bot.get_status() == "online"):
  #   if online, return error
    response_message(client, f"Bot {botname} is online. Stop the bot before removing.")
    return
  # remove bot from database and refresh database variable
def start(botname, client):
  """
  Starts a given bot.
  """
  global online_botlist
  echo_message(client, f"Starting bot {botname}")
  
  bot = botfinder(botname)
  try:
    # check if bot exists
    if (bot not in botlist):
      # if not, return error
      response_message(client, "Bot does not exist.")
      return
    # check if bot is online
    if (bot.get_status() == "online"):
      # if online, return error
      response_message(client, "Bot is already online.")
      return
    # start bot
    err = run_script_external(bot)
    if (err != "Script executed successfully."):
      raise Exception(err)    
  except Exception as e:
    response_message(client, f"Error starting bot {botname}: {e}")
  response_message(client, f"Started bot {botname}")
def stop(botname, client):
  """
  Stops a given bot.
  """
  global online_botlist
  response_message(client, f"Stopping bot {botname}")
  
  bot = botfinder(botname)
  # check if bot exists
  if (bot not in botlist):
    # if not, return error
    response_message(client, f"Bot '{botname}' does not exist.")
    return
  # check if bot is offline
  if(bot.get_status() == "offline"): # "bot not in online_botlist" removed due to error expectation 
    # if offline, return error
    response_message(client, f"Bot '{botname}' is already offline.")
    return
  # before stopping, do any saving or take needed precautions.
  #empty
  # stop bot
  # RESEARCH SUBPROCESSES, this should errors.
  online_botlist[online_botlist.index(botname)].terminate()
  online_botlist[online_botlist.index(botname)].wait()
  online_botlist.remove(botname)
  # NON-FUNCTIONAL CODE - FIX ASAP ^^^^

  response_message(client, f"Stopped bot {botname}")
def update(botname, client):
  """
  Updates a given bot from GitHub.
  """
  response_message(client, f"Updating bot {botname}")
  bot = botfinder(botname)
  # check if bot exists
  if(bot == None):
    # if not, return error
    response_message(client, f"Bot '{botname}' does not exist.")
    return
  # check if bot is online
  if(bot.get_status()== "online"):
    # if online, stop bot
    stop(botname, client)
  # update bot from github
def schedule_maintenance(botname, client, time): # Set maintenance time (YYYY, MM, DD, HH, MM) #bot name is also used on a switch
  """
  Used to set dates for maintainence

  botname: str
  ------------

  if is a name of a bot, that bot will be scheduled for maintenance.

  if "bot", all bots will be scheduled for maintenance.

  if "commander", the server will be scheduled for maintenance.

  if "0", all bots and the server will be scheduled for maintenance
  """
  maintenance_time = convert_to_datetime(time)
  bot = botfinder(botname)
  if bot in botlist:
    # If botname is in botlist, it is a bot
    # find bot
    scheduler.add_job(bot_maintenance, 'date', run_date=maintenance_time, args=[bot, client])
  elif botname == "bot":
    # Full bot maintenance
    for bot in botlist:
      scheduler.add_job(bot_maintenance, 'date', run_date=maintenance_time, args=[bot, client])
  elif botname == "commander":
    # Self maintenance
    scheduler.add_job(self_maintenance, 'date', run_date=maintenance_time, args=[client])
  elif botname == "0":
    # Full maintenance (first bots, then commander)
    for bot in botlist:
      scheduler.add_job(bot_maintenance, 'date', run_date=maintenance_time, args=[bot, client])
    scheduler.add_job(self_maintenance, 'date', run_date=maintenance_time + datetime.timedelta(minutes=1), args=[client])
  else:
    response_message(client, "Invalid botname for maintenance.")
    return
  print(f"Scheduling maintenance for bot {botname} at {time}")
  client.send(f"Scheduling maintenance for bot {botname} at {time}".encode('utf-8'))
  # could have/become its own discord bot to log everything on a discord server.
  return
def bot_maintenance(bot, client):
  # given bot activity
  # data save should be in stop function
  stop(bot.get_name(), client)
  return
def self_maintenance(client):
  # save all bot commander data
  # inform client
  client.send("Maintenance complete.".encode('utf-8'))
  # stop bot commander
  return
# Data functions
def checkdata(botname, client):
  """
  Display data of a selected bot.

  Later on needs to be improved with security levels and data of different servers. Not implemented yet.
  """
  response_message(client, f"Checking data of bot {botname}")
  # find bot
  bot = botfinder(botname)
  if(bot == None):
    print(f'Bot {botname} does not exist.')
    response_message(client, f"Bot '{botname}' does not exist.")
    return
  # check if bot exists
  #   if not, return error
  # check if bot is online
  #   if offline, return error
  # get data of bot from database
  # send client all the server names of the server data
  # give option to display data of a specific server
  # COULD LATER ADD CODE THAT SPESIFIES WHICH SERVERS DATA CAN BE REQUESTED FROM SPESIFIC CLIENTS FOR SECURITY.
def show_status():
  """
  Called on every bot status change.

  Creates a formatted message, which is sent to all clients.
  """
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
    statelist.append(bot)

  # bot status checking and updating loop
  while True:
    # separated listeners from main thread to check bot changes every x seconds.
    # wait x seconds
    time.sleep(15)
    # bot checking functionality (not defined, not used anywhere else)
    check = False
    for bot in botlist:
      if bot.get_status() != statelist[botlist.index(bot)].get_status():
        # update check
        check = True
        # update botlist
        statelist[botlist.index(bot)].update_status(bot.get_status())
        # update bot status for every client.
        print(f"Not implemented feature: Bot status changed to {bot.get_status()}")
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
#      4.1 -) Refactoring                     DONE
#      5-) Status formatting
#      6-) Making functions usable by the clients
#      7-) Testing
#      7.1-) Github Connection
#      7.2-) .env injection (token)
#      Database moved to last, because development is moving on a test machine and database implementation will slow down the process for now.
#      8-) Database setup, connection (SQLite (?)) (maybe pandas?)
#      9-) Data check function
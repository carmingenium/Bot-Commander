import sqlite3
import os

# Database file path
DB_PATH = os.path.join('data', 'bot_commander.db')
# Could set a login db also later on



def init_db():
  """Initialize the database and create tables if they don't exist."""
  os.makedirs('data', exist_ok=True)  # Ensure the 'data' folder exists
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS bots (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'offline',
      location TEXT NOT NULL,
      last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
  ''')
  conn.commit()
  conn.close()

def add_bot(name, status, location, token): # could move the default values to parameters on the function
  """Insert a new bot into the database.
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'offline',
      location TEXT NOT NULL,
      token TEXT NOT NULL,
      last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  """
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute('''
  INSERT INTO bots (name, status, location, token)
  VALUES (?, ?, ?, ?)
  ''', (name, status, location, token))
  conn.commit()
  conn.close()

def get_bots():
  """Retrieve all bot data from the database."""
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM bots')
  bots = cursor.fetchall() # fetchall returns an array of tuples, has all the data in tuple format
  conn.close()
  return bots

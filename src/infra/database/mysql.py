import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

class DataBase:
    
  def __init__(self,dictionary: bool = False ):
    try:
      self.ip = os.getenv("DATABASE_IP")
      self.port = os.getenv("DATABASE_PORT")
      self.database = os.getenv("DATABASE_DB")
      self.user = os.getenv("DATABASE_USER")
      self.password = os.getenv("DATABASE_PASSWORD")
      self.conn = mysql.connector.connect(
          host=self.ip,
          port=self.port,
          database=self.database,
          user=self.user,
          password=self.password
      )
      self.socket = self.conn.cursor(dictionary=dictionary)
      
    except mysql.connector.DatabaseError as err:
      print("DataBaseError: "+err)
    except mysql.connector.Error as err:
      print("Error: "+err)

  def close(self):
    self.socket.close()
    self.conn.close()
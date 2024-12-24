import mysql.connector


class DataBase :
    
  def __init__(self, ip, port, database, user, password):
    try:
      self.ip = ip
      self.port = port
      self.database = database
      self.user = user
      self.password = password
      self.conn = mysql.connector.connect(
          host=self.ip,
          port=self.port,
          database=self.database,
          user=self.user,
          password=self.password
      )
      self.socket = self.conn.cursor()
      
    except mysql.connector.DatabaseError as err:
      print("DataBaseError: "+err)
    except mysql.connector.Error as err:
      print("Error: "+err)


  


  def close(self):
    self.socket.close()
    self.conn.close()
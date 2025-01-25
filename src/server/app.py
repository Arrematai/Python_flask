from flask import Flask, json, request, jsonify
from flask_cors import CORS

## DATABASE
from src.infra.database.mysql import DataBase

## SERVER
from src.server.api import api_init
from src.server.middleware.limiter import init_limiter
from src.server.middleware.cors import init_cors


app = Flask(__name__)

def server_init():
  print("Inicio Aplicação")
  limiter = init_limiter(app)
  init_cors(app)
  database = DataBase(dictionary=True)  
  api_init(app=app,limiter=limiter,database=database)
  context = ('fullchain.pem', 'privkey.pem')#certificate and key files
  app.run(host='0.0.0.0', port=5001, ssl_context=context)
  
  if database.conn:
    database.conn.close()
  print("Aplicação Finalizada")
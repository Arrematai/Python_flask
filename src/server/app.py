from flask import Flask

## INFRA
from src.infra.service.Logging import Log

## DATABASE
from src.infra.database.mysql import DataBase

## SERVER
from src.server.routes import Routes
from src.server.middleware.limiter import init_limiter
from src.server.middleware.cors import init_cors

app = Flask(__name__)

def server_init():
  try:
    print("Inicio Aplicação")
    limiter = init_limiter(app)
    init_cors(app)
    log = Log("INIT")
    log.messageInfo("Inicio Aplicação")
    database = DataBase(dictionary=True)  
    Routes(app=app,limiter=limiter,database=database)
    context = ('fullchain.pem', 'privkey.pem')#certificate and key files
    app.run(host='0.0.0.0', port=5001, ssl_context=context)
    
    if database.conn:
      database.conn.close()

    log.messageInfo("Aplicação Finalizada")
    print("Aplicação Finalizada")
  except Exception as e:
    print(f"Erro detectado: {e}, reiniciando...")

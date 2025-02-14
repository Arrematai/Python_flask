from flask import Flask
import os
import signal
import subprocess

## INFRA
from src.infra.service.Logging import Log

## DATABASE
from src.infra.database.mysql import DataBase

## SERVER
from src.server.routes import Routes
from src.server.middleware.limiter import init_limiter
from src.server.middleware.cors import init_cors

app = Flask(__name__)

def graceful_shutdown(signum, frame):
    print("Recebido sinal de encerramento. Finalizando a aplicação...")
    os._exit(0)  # Finaliza o processo de forma controlada


def server_init():
  try:
    print("Inicio Aplicação")

    ## MIDDLES
    limiter = init_limiter(app)
    init_cors(app)

    ## LOGS
    log = Log("INIT")
    log.messageInfo("Inicio Aplicação")

    ## DATABASE
    database = DataBase(dictionary=True)  

    ## ROTAS  
    Routes(app=app,limiter=limiter,database=database)
    context = ('fullchain.pem', 'privkey.pem')#certificate and key files


    ## ONLINE
    try:
      subprocess.run(["poetry", "run" , "monitoramento", "init_app"], capture_output=True, text=True, check=True)
      log.messageInfo("Monitoramento Online executado")
    except subprocess.CalledProcessError as e:
      log.messageInfo("Monitoramento Online não foi executado")

    ## SERVER
    app.run(host='0.0.0.0', port=5001, ssl_context=context)


    if database.conn:
      database.conn.close()

    # Capturando o sinal SIGINT (Ctrl+C) para realizar o "graceful shutdown"
    signal.signal(signal.SIGINT, graceful_shutdown)

    log.messageInfo("Aplicação Finalizada")
    print("Aplicação Finalizada")
  except Exception as e:
    log.messageError("Aplicação ERRO GERAL")
    print(f"Erro detectado: {e}, reiniciando...")

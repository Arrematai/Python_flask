from flask import Flask
import os
import atexit
import signal

## INFRA
from src.infra.service.Logging import Log
from src.infra.service.SMTP import enviar_email

## DATABASE
from src.infra.database.mysql import DataBase

## SERVER
from src.server.routes import Routes
from src.server.middleware.limiter import init_limiter
from src.server.middleware.cors import init_cors

log = Log("")
app = Flask(__name__)

def graceful_shutdown(signum, frame):
    print("Recebido sinal de encerramento. Finalizando a aplicação aguarde...")
    log.messageInfo("Aplicação Finalizada")
    enviar_email("Aplicação Parada", f"Aplicação parada.", "Aplicação Parada", log)
    os._exit(0)  # Finaliza o processo de forma controlada

def server_init():
  try:
    print("Inicio Aplicação")

    ## MIDDLES SECURITY
    limiter = init_limiter(app)
    init_cors(app)

    ## DATABASE
    database = DataBase(dictionary=True)  

    ## ROTAS 
    print("________________ INIT ROUTES _______________________________")
    Routes(app=app,limiter=limiter,database=database)
    context = ('fullchain.pem', 'privkey.pem')#certificate and key files


    ## monitoramento
    log.messageInfo("Inicio Aplicação")
    log.monitoramento("Aplicação iniciada - Monitoramento Online executado")
    try:
      enviar_email("Aplicação Iniciada", f"Sucesso em iniciar a aplicação.", "Aplicação Iniciada", log)
    except subprocess.CalledProcessError as e:
      log.monitoramento("Monitoramento Online não foi executado")

    ## SERVER
    print("MODE",os.getenv("MODE"))
    print("DATABASE_DB",os.getenv("DATABASE_DB"))
    print("DATABASE_USER",os.getenv("DATABASE_USER"))
    print("DATABASE_PASSWORD",os.getenv("DATABASE_PASSWORD"))
    print("DATABASE_IP",os.getenv("DATABASE_IP"))
    print("DATABASE_PORT",os.getenv("DATABASE_PORT"))
    app.run(host='0.0.0.0', port=5001, ssl_context=context)


    if database.conn:
      database.conn.close()

    log.messageInfo("Aplicação Finalizada")
    print("Aplicação Finalizada")
  except Exception as e:
    log.messageError("Aplicação ERRO GERAL")
    print(f"Erro detectado: {e}, reiniciando...")


atexit.register(graceful_shutdown) # Captura saída normal
signal.signal(signal.SIGINT, graceful_shutdown) # Capturando o sinal SIGINT (Ctrl+C) para realizar o "graceful shutdown"
signal.signal(signal.SIGTERM, graceful_shutdown) # kill command
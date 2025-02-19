import psutil
import requests
import sys
import subprocess
import sys

## INFRA
from src.infra.service.Logging import Log
from src.infra.service.SMTP import enviar_email

log = Log("")


def supervisor_process( action = "restart", process_name = ""):
    try:
      if sys.platform.startswith("linux"):
        subprocess.run(
            ["supervisorctl", action, process_name], 
            capture_output=False, 
            text=False, 
            check=True
        )
        print(f"Processo {process_name} reiniciado com sucesso!")
      else:
        print(f"Supervisorctl só roda no linux.")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao reiniciar {process_name}:")
        print(e.stderr)

## COMPARA 2 LISTA E VERIFICA SE O RESULTADO DE UMA TEM NA OUTRA 
def contains_sublist(main_list, sublist):
    for i in range(len(main_list) - len(sublist) + 1):
        if main_list[i:i+len(sublist)] == sublist:
            return True
    return False

def monitorar_apiOnline(init_arrematai):
  try:
    response = requests.get("https://api.arremataisolucoes.com.br:5001/online", timeout=5)

    if response.status_code != 200:
      print(f"Erro ao acessar o site na página: {response.status_code}")
      enviar_email("Erro na aplicação", f"Erro em acesso a url: https://api.arremataisolucoes.com.br:5001/online, status: {response.status_code}", "Aplicação não está online",log)
      log.monitoramento("Aplicação não está funcionando")
      supervisor_process("restart", "arrematai_app")
      return False
    else:
      if init_arrematai:
        enviar_email("Aplicação funcionando", f"Sucesso em acessar a url: https://api.arremataisolucoes.com.br:5001/online, status: {response.status_code}", "Aplicação funcionando",log)
      
    log.monitoramento("Aplicação está funcionando")
              
  except Exception as e:
    print(f"Error: {e}")
    enviar_email("Erro na aplicação", f"Erro em acesso a url: https://api.arremataisolucoes.com.br:5001/online, status: {response.status_code}", "Aplicação não está online",log)
    log.monitoramento("Aplicação não está funcionando")
    supervisor_process("restart", "arrematai_app")
  
    

# Função para verificar processos
def monitorar_processos():
    # Defina os processos que deseja monitorar
    processos_criticados = ["run","arrematai"]  # Altere conforme necessário

    # Obter a lista de processos ativos
    for proc in psutil.process_iter(attrs=['pid', "name", "exe", "cmdline"]):
        try:
            # Se o processo estiver na lista dos monitorados
            if proc.info['cmdline'] and len(proc.info['cmdline']) > 0 and contains_sublist(proc.info['cmdline'], processos_criticados):
                # return proc.info['name']
                log.monitoramento("Processo encontrado.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

# Função principal para monitorar e disparar alerta
def verificar_erro():
  processo_encontrado = monitorar_processos()

  init_arrematai = sys.argv[1] if sys.argv and len(sys.argv) == 2 else None

  if processo_encontrado:

    if init_arrematai and init_arrematai == "init_app":
      enviar_email("Processo funcionando", f"Sucesso em encontrar processo no servidor.", "Processo funcionando", log)
      log.monitoramento("Processo funcionando")
    
    
    monitorar_apiOnline(init_arrematai)

  else:
    enviar_email("Processo não encontrado ou parado", f"Erro processo não está rodando no servidor.", "Processo não está em execução",log)
    log.monitoramento("Processo não encontrado ou parado")
    supervisor_process("start", "arrematai_app")

# Executar a verificação
def init():
  verificar_erro()

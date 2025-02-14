import psutil
import smtplib
import requests
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.infra.service.Logging import Log

log = Log("")

## COMPARA 2 LISTA E VERIFICA SE O RESULTADO DE UMA TEM NA OUTRA 
def contains_sublist(main_list, sublist):
    for i in range(len(main_list) - len(sublist) + 1):
        if main_list[i:i+len(sublist)] == sublist:
            return True
    return False


def monitorar_apiOnline(init_arrematai):
  response = requests.get("https://api.arremataisolucoes.com.br:5001/online")

  if response.status_code != 200:
    print(f"Erro ao acessar o site na página: {response.status_code}")
    enviar_email("Erro na aplicação", f"Erro em acesso a url: https://api.arremataisolucoes.com.br:5001/online, status: {response.status_code}", "Aplicação não está online")
    log.monitoramento("Aplicação não está funcionando")
    return False
  else:
    if init_arrematai:
      enviar_email("Aplicação funcionando", f"Sucesso em acessar a url: https://api.arremataisolucoes.com.br:5001/online, status: {response.status_code}", "Aplicação funcionando")
    
  log.monitoramento("Aplicação está funcionando")
    

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

# Função para enviar e-mail
def enviar_email(subject = "Monitoramento Arrematai", mensagem: str = "", tipo = ""):
    try:
      remetente = "monitoramento@arremataisolucoes.com.br"
      # destinatarios = ["Campos051192@hotmail.com", "rafaelnetto_@hotmail.com"]
      destinatarios = ["rafaelnetto_@hotmail.com"]
      senha = "monitoramento@P1s"
      
      # Configuração do servidor SMTP
      servidor = smtplib.SMTP_SSL('smtp.hostinger.com', 465)
      servidor.login(remetente, senha)
      
      # Criar mensagem
      msg = MIMEMultipart()
      msg['From'] = f"Monitoramento Arrematai <{remetente}>"
      msg['To'] = ", ".join(destinatarios)
      msg['Subject'] = subject
      msg.attach(MIMEText(mensagem, 'plain'))
      
      # Enviar e-mail
      servidor.sendmail(remetente, destinatarios, msg.as_string())
      message = f"Email de notificação disparo com sucesso. - Status: {tipo}"
      log.monitoramento(message)
      servidor.quit()
    except Exception as e:
      print(e)

# Função principal para monitorar e disparar alerta
def verificar_erro():
  processo_encontrado = monitorar_processos()

  init_arrematai = sys.argv[1] if sys.argv and len(sys.argv) == 2 else None

  if processo_encontrado:

    if init_arrematai and init_arrematai == "init_app":
      enviar_email("Processo funcionando", f"Sucesso em encontrar processo no servidor.", "Processo funcionando")
      log.monitoramento("Processo funcionando")
    
    
    monitorar_apiOnline(init_arrematai)

  else:
    enviar_email("Processo não encontrado ou parado", f"Erro processo não está rodando no servidor.", "Processo não está em execução")
    log.monitoramento("Processo não encontrado ou parado")

# Executar a verificação
def init():
  verificar_erro()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import os
load_dotenv()

from src.infra.service.Logging import Log

# Função para enviar e-mail
def enviar_email(subject: str, mensagem: str, tipo: str, log: Log):
    try:
      
      emails = [email.strip().strip('"') for email in os.getenv("SMTP_DESTINATARIOS").split(",")]

      print(emails)

      remetente = os.getenv("SMTP_REQUERENTE") or ""
      # destinatarios = ["Campos051192@hotmail.com", "rafaelnetto_@hotmail.com"]
      destinatarios = emails or []
      senha = os.getenv("SMTP_PASSWORD") or ""
      
      # Configuração do servidor SMTP
      servidor = smtplib.SMTP_SSL(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
      servidor.login(remetente, senha)
      
      # Criar mensagem
      msg = MIMEMultipart()
      msg['From'] = f"{os.getenv("MODE")} - Monitoramento Arrematai <{remetente}>"
      msg['To'] = ", ".join(destinatarios)
      msg['Subject'] = subject
      msg.attach(MIMEText(mensagem, 'plain'))
      
      # Enviar e-mail
      servidor.sendmail(remetente, destinatarios, msg.as_string())
      message = f"Email de notificação disparo com sucesso. - Status: {tipo}"
      log.monitoramento(message)
      servidor.quit()
    except Exception as e:
      print("Erro em enviar email", e)
      log.messageError("Erro em enviar email")


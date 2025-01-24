from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def init_limiter(app: Flask):
  print("_______________________ INIT LIMITER _______________________")
  # Lista de IPs/DNS a serem ignorados pelo limiter
  IGNORED_IPS = {"127.0.0.1", "localhost", "https://arremataisolucoes.com.br", "https://arrematai.com.br"}

  def custom_key_func():
      # Ignorar IPs específicos
      if get_remote_address() in IGNORED_IPS:
          return None
      # Para outros IPs, retornar o endereço IP
      return get_remote_address()

  limiter = Limiter(
      app=app,
      default_limits=["5000/hour", "500/minute"],
      storage_uri="memory://",
      key_func=custom_key_func
  )
  
  return limiter
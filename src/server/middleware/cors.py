from flask import Flask
from flask_cors import CORS


def init_cors(app:Flask):
  print("_______________________ INIT CORS _______________________")
  CORS(app, origins=["https://arremataisolucoes.com.br"],
supports_credentials=True, methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])
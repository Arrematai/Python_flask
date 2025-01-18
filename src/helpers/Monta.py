

def getMonta(monta: str):
     if 'pequena monta' in monta.lower():
          return 'Pequena Monta'
     if 'média monta' in monta.lower() or 'media monta' in monta.lower():
          return 'Média Monta'
     if 'grande monta' in monta.lower() or  'sucata' in monta.lower():
          return 'Grande Monta'
     if "no estado que se encontra" == monta.lower():
          return "No estado que se encontra"
     if "Não Informado":
          return "Não Informada"
     else:
          return "Não Informada"
     
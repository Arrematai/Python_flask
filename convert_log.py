import re
import pandas as pd
from datetime import datetime

# Lê o conteúdo do arquivo de log
with open("/mnt/data/log.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Expressão regular para extrair os dados
pattern = re.compile(
    r"\[(.*?)\] — EXECUTION — API: (.*?), Tempo de execução da: ([\d.]+) segundos, query: (.*)"
)

# Lista para armazenar os dados
data = []

# Processa cada linha do log
for line in lines:
    match = pattern.match(line)
    if match:
        horario_str, api, tempo, query = match.groups()
        # Converte o horário para um formato datetime
        horario = datetime.strptime(horario_str, "%d/%b/%y %H:%M:%S")
        data.append([horario, api, float(tempo), query])

# Cria um DataFrame com os dados
df = pd.DataFrame(data, columns=["horario", "API", "tempo_execucao", "query"])

# Salva em CSV
csv_path = "/mnt/data/log_convertido.csv"
df.to_csv(csv_path, index=False)

csv_path
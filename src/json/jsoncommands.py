import json
import os
pasta = "src/json"
file_name = "astryn.json"

def get_path(filename: str):
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, filename)

def save(dados: dict, filename: str = file_name):
    path = get_path(filename)
    os.makedirs("data", exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)
def load(filename: str) -> dict:
    path = get_path(filename)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

#Caso o arquivo não exista, criar uma base dele
try:
    data = load(file_name)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    data= {
   "server": {
    "status":{"nextjoin": 0 }
    },
    "user":{}
    }

    save(data, file_name)
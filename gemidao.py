import requests
import json
import fire
import re

TOTALVOICE = "https://api.totalvoice.com.br/composto"
GEMIDAO = 'https://github.com/haskellcamargo/gemidao-do-zap/raw/master/resources/gemidao.mp3'

def gemer(token: str, source: str, destination: str) -> None:
    if not re.match(r"^[a-f0-9]{32}$", token):
        raise ValueError("Invalid Token. Get one on https://totalvoice.com.br")
    if len(re.findall(r"[0-9]{10,11}", f"{source} {destination}")) < 2:
        raise ValueError('Um ou mais dos números de telefone é inválido')
        
    headers = {'Access-Token': token, 'Accept': 'application/json',
               'Content-Type': 'application/json'}
    payload = {"numero_destino": destination, "bina": source,
               "dados": [{"acao": 'audio', "acao_dados": {"url_audio": GEMIDAO}}]}
    
    resp = requests.post(TOTALVOICE, data=json.dumps(payload), headers=headers).json()
    if not resp["status"] == 200:
        raise RuntimeError(f"{resp['mensagem']}")
    print("Gemidão enviado com sucesso!")

if __name__ == "__main__":
    fire.Fire(lambda src, dst: gemer("1bfb98b07e60d3c89de7c1f835393ac7", src, dst))
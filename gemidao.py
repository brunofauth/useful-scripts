import requests
import json
import fire
import re


PHONE_PATTERN = re.compile(r"[0-9]{8,9}")
TOTALVOICE = "https://api.totalvoice.com.br/composto"
GEMIDAO = 'https://github.com/haskellcamargo/gemidao-do-zap/raw/master/resources/gemidao.mp3'


def gemer(token: str, src_phone: str, dst_phone: str) -> None:
    if not re.match(PHONE_PATTERN, src_phone):
        raise ValueError(f"Invalid 'src_phone' '{src_phone}'.")
    if not re.match(PHONE_PATTERN, dst_phone):
        raise ValueError(f"Invalid 'dst_phone' '{dst_phone}'.")
        
    headers = {'Access-Token': token, 'Accept': 'application/json',
               'Content-Type': 'application/json'}

    payload = {"numero_destino": dst_phone, "bina": src_phone,
               "dados": [{"acao": 'audio', "acao_dados": {"url_audio": GEMIDAO}}]}
    
    resp = requests.post(TOTALVOICE, data=json.dumps(payload), headers=headers).json()
    if not resp["status"] == 200:
        raise RuntimeError(f"{resp['mensagem']}")
    print("Gemidão enviado com sucesso!")


if __name__ == "__main__":
    fire.Fire(gemer)

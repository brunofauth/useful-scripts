import requests
import fire


TOTALVOICE = "https://api.totalvoice.com.br/composto"
GEMIDAO = 'https://github.com/haskellcamargo/gemidao-do-zap/raw/master/resources/gemidao.mp3'


def gemer(token: str, src_phone: str, dst_phone: str) -> None:
    headers = {'Access-Token': token, 'Accept': 'application/json',
               'Content-Type': 'application/json'}
    payload = {"numero_destino": dst_phone, "bina": src_phone,
               "dados": [{"acao": 'audio', "acao_dados": {"url_audio": GEMIDAO}}]}
    
    resp = requests.post(TOTALVOICE, data=payload, headers=headers)
    resp.raise_for_status()
    print("Gemidão enviado com sucesso!")


if __name__ == "__main__":
    fire.Fire(gemer)

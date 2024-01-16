import json
import os


def escrever_em_json(data, nome_arquivo=os.path.join(os.getcwd(), "arquivo_json_final.json"), modo="a"):
    with open(nome_arquivo, modo) as arquivo:
        json.dump(data, arquivo, indent=4,ensure_ascii=True)

def ler_de_json(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        data = json.load(arquivo)
    return data

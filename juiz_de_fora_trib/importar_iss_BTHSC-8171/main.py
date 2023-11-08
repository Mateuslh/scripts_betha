import json

from scripts_betha.tool_box.arquivos.arquivo import ler_arquivo, escrever_arquivo
from scripts_betha.tool_box.arquivos.txt import extrair_substrings, dividir_string

arquivo = ler_arquivo('arqiss_aut.txt', encoding=None)
list_json_Insercao = []

posicoes = {
    "inscricao_economico": (6, 14),
    "unica":(779, 791),
    "parcelas": (791, 946)
}

for linha in arquivo:
    dict_pos_arq = extrair_substrings(linha, posicoes)
    list_parcelas  = dividir_string(dict_pos_arq["parcelas"], 13)

    json_insercao = {
        "inscricao_economico":dict_pos_arq["inscricao_economico"],
        "unica":dict_pos_arq["unica"]
    }
    numero_parcela=0
    for parcela in list_parcelas:
        numero_parcela+=1
        if int(parcela)!=0:
            json_insercao[str(numero_parcela)] = parcela
    list_json_Insercao.append(json.dumps(json_insercao))

escrever_arquivo("resultado.json",list_json_Insercao)
import json
from json import loads
from tool_box.arquivos.arquivo import ler_arquivo
from tool_box.listas import flatten

alteracoes = []
imoveis = []

for linha in ler_arquivo("resultado.txt"):
    linha_dict = loads(linha)
    imoveis.append(linha_dict["imoveis"])

lista = flatten(imoveis)

from tool_box.arquivos.arquivo import escrever_arquivo

escrever_arquivo(nome_arquivo="resul.txt",linhas=json.dumps(lista))

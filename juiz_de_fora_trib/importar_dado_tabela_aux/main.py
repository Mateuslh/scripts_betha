import os
import requests
from scripts_betha.tool_box.arquivos.csv import ler_csv
from dotenv import load_dotenv

load_dotenv()

pastaArquivos = os.environ["pathPastaArquivos"]
urlTabelaAux = os.environ["urlServiceLayerTabelaAux"]
ListNomeArquivos = os.listdir(pastaArquivos)
arquivos = {}
listaLotes = []
headers = {
    "Authorization": os.environ["Authorization"]
}


def collate(lista, tamanho_sublista):
    sublistas = []
    for i in range(0, len(lista), tamanho_sublista):
        sublista = lista[i:i + tamanho_sublista]
        sublistas.append(sublista)
    return sublistas


for arquivo in ListNomeArquivos:
    pathAquivo = pastaArquivos + "/" + arquivo
    arquivos[arquivo] = ler_csv(pathAquivo, delimiter=";", ordem_cabecalhos=["idConcorrente", "baixa", "valor"])

for arquivo, itens in arquivos.items():
    contador = 0
    print(f'Montando lotes do arquivo arquivo {arquivo}...')
    jsonsPost = []
    for json in itens:
        contador += 1
        body = {
            "idIntegracao": contador.__str__(),
            "registrosTabaux": {
                "campo1": json["idConcorrente"],
                "campo2": json["baixa"],
                "campo3": json["valor"],
                "iTabelaAuxiliar": os.environ["numeroTabelaAux"],
                "idTabelaAuxiliar": os.environ["idTabelaAuxiliar"]
            }
        }
        jsonsPost.append(body)
    for lote in collate(jsonsPost, 50):
        listaLotes.append(lote)

if not os.path.exists("ultimate"):
    os.mkdir("ultimate")
erros = []
contador = 0
for lote in listaLotes:
    contador += 1
    print(contador)
    retorno = requests.post(url=urlTabelaAux, headers=headers, json=lote)
    if retorno.status_code != 200:
        retorno = requests.post(url=urlTabelaAux, headers=headers, json=lote)
        if retorno.status_code != 200:
            erros.append(
                {"codigo": retorno.status_code,
                 "contador":contador,
                 "erro":retorno.content})
            print(f'erro no arquivo {contador}')
            continue
    nomeArquivo = str(contador) +" -  "+retorno.json()["idLote"]
    with open(f'ultimate\\{nomeArquivo}.txt', 'w', encoding='utf-8') as arquivo:
        for item in lote:
            arquivo.write(str(item)+"\n")

with open('errros.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write(str(erros))
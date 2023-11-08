import json
import requests
import numpy as np

registros = []
headers = {
    "user-access": "y-OL_cLcuXhV8-5BYPY2Lg==",
    "Authorization": "Bearer 94074e4b-2423-4bfb-947a-7b5aa59ee2e5",
    "content-type": "application/json;charset=UTF-8"
}


def criaHeaders():
    global headers
    authorization = input("insira o Bearer, sem a palavra 'Bearer' no começo:")
    headers['Authorization'] = "Bearer "+authorization


def requisicaoTela(Method, Purl, Pdata=None, Pheaders=None, Pfiles=None, Pjson=None, Pparam=None):
    requisicao = requests.request(method=Method,
                                  url=Purl,
                                  headers=Pheaders,
                                  data=Pdata,
                                  files=Pfiles,
                                  json=Pjson,
                                  params=Pparam)
    if not verificaRetorno(requisicao):
        global headers
        requisicao = requisicaoTela(Method, Purl, Pheaders=Pheaders, Pdata=Pdata, Pfiles=Pfiles, Pjson=Pjson, Pparam=Pparam)
    return requisicao


def verificaRetorno(retorno):
    # verifica se a requisição foi bem sucedida
    if retorno.status_code != 200:
        print("A requisição foi mal sucedida, verificando motivo:")
        if retorno.status_code == 401:
            print("Possivel erro de autenticação\n ERRO:" + retorno.json()[
                "message"] + "\n\niniciando processo do novo token")
            criaHeaders()
            return False
        if retorno.status_code == 415:
            print("erro no corpo da requisição, verifica-la\n ERRO:" + retorno.json().__str__())
            exit()
        else:
            print(retorno.status_code)
            print(retorno.json())
            # continuar = input(
            #     "Não foi possivel indentificar o erro, Digite 's' caso queira continuar as demais requisições e 'n',"
            #     " caso não queira.")
            continuar = "s"
            if continuar == "n":
                exit()
            if continuar == "s":
                return True
    else:
        return retorno


def flatten(lst):
    aplanado = []
    for item in lst:
        if isinstance(item, list):
            aplanado.extend(flatten(item))
        else:
            aplanado.append(item)
    return aplanado


def collate(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]


offset = 0

while True:
    payloadParcelamentosParcela = {
        "offset": offset,
        "limit": 40,
        "tipoVisualizacao": None,
        "extraData": None,
        "filter": "situacao = 'ABERTO'",
        "sort": "nroParcelamento desc"
    }
    offset += 500
    url = "https://tributos.betha.cloud/tributos/v1/api/arrecadacao/parcelamentos/findBy"
    retornoJson = json.loads(requisicaoTela("post", Purl=url, Pheaders=headers, Pdata=json.dumps(payloadParcelamentosParcela)).text)
    registros += retornoJson["data"]
    print(retornoJson["hasNext"])
    print(np.size(registros))
    break

for registro in registros:
    print("Index: "+registros.index(registro).__str__())
    id = registro["id"].__str__()
    print(id)
    urlParcelamentos = "https://tributos.betha.cloud/tributos/v1/api/arrecadacao/parcelamentosParcelas/findBy"
    urlParcelamentosComposicoes = "https://tributos.betha.cloud/tributos/v1/api/arrecadacao/parcelamentosComposicoes/findBy"
    urlParcelamentosManutencao = "https://tributos.betha.cloud/tributos/v1/api/arrecadacao/parcelamentos/manutencao"

    payloadParcelamentosComposicoes = {
        "filter": "idParcelamento = "+id
    }
    payloadParcelamentosParcela = {
        "filter": "situacao not in('ELIMINADA') and idParcelamento = "+id,
        "sort": "nroParcela asc"
    }

    parcelamentosParcelasJson = json.loads(requisicaoTela("post", Purl=urlParcelamentos, Pheaders=headers, Pdata=json.dumps(payloadParcelamentosParcela)).text)
    ParcelamentosComposicoes = json.loads(requisicaoTela("post", Purl=urlParcelamentosComposicoes, Pheaders=headers, Pdata=json.dumps(payloadParcelamentosComposicoes)).text)
    pyloadManutencao = registro
    pyloadManutencao["parcelamentosComposicoes"] = ParcelamentosComposicoes["data"]
    pyloadManutencao["parcelamentosParcelas"] = parcelamentosParcelasJson["data"]
    print(pyloadManutencao)
    requisicaoTela("put", Purl=urlParcelamentosManutencao, Pheaders=headers,Pdata=json.dumps(pyloadManutencao))


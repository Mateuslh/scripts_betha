import requests
objetosTransferencia = {}
headers = {
    "user-access": "bhEXHhRrmulpElC9LB63iw==",
    "Authorization": "Bearer 23fa16e0-1561-49e8-9773-68eef189e3a5"
}


def criaHeaders():
    global headers
    user = input("insira o user access:")
    authorization = input("insira o Bearer, sem a palavra 'Bearer' no começo:")
    headers = {
        'user-access': user,
        'Authorization': 'Bearer ' + authorization
    }


def requisicaoTela(Method, Purl, Headers=dict(), Pdata=dict(), Pfiles=list(), Pjson=dict(), Pparam=dict()):
    requisicao = requests.request(Method,
                                  Purl,
                                  headers=Headers,
                                  data=Pdata,
                                  files=Pfiles,
                                  json=Pjson,
                                  params=Pparam
                                  )

    if not verificaRetorno(requisicao):
        global headers
        requisicaoTela(Method, Purl, Headers=headers, Pdata=Pdata, Pfiles=Pfiles, Pjson=Pjson)
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
            continuar = input(
                "Não foi possivel indentificar o erro, Digite 's' caso queira continuar as demais requisições e 'n',"
                " caso não queira.")
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
ids = []
urlTransferencias = "https://tributos.betha.cloud/tributos/v1/api/cadastros/referentes/transferencias-imoveis"
urlTransferencia = "https://tributos.betha.cloud/tributos/v1/api/core/transferenciaImoveis/"
hasNext = True

while hasNext:
    retorno = requisicaoTela("GET", Purl=urlTransferencias, Headers=headers, Pparam={
        "limit": 100,
        "offset": offset
    }).json()
    ids.append([item['id'] for item in retorno['content']])
    offset += 100
    hasNext = retorno["hasNext"]

for id in flatten(ids):
    retornoTransferencia = requisicaoTela("GET", Purl=urlTransferencia + id.__str__(), Headers=headers).json()
    retornoTransferenciaItens = requisicaoTela("GET", Purl=urlTransferencia + id.__str__() + "/transfImoveisItens",
                                               Headers=headers).json()
    objetosTransferencia[id.__str__()] = {}
    objetosTransferencia[id.__str__()]["TransferenciaItens"] = retornoTransferenciaItens
    objetosTransferencia[id.__str__()]["Transferencia"] = retornoTransferencia
lista = []
for chave, valor in objetosTransferencia:
    lista.append({
        "idIntegracao": chave,
        "transferenciaImoveis":{
            "codigo": valor["Transferencia"]["idTransfImoveis"],
            "idPagador":""
        }
    })
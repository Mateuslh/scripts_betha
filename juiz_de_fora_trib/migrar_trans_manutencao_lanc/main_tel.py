import json
import requests
from jsons import jsonFindCreditos

registros = []
headers = {
    "user-access": "y-OL_cLcuXhV8-5BYPY2Lg==",
    "Authorization": "Bearer e45d2225-08de-48ae-b351-14abd018fcfa",
    "accept":"application/json, text/plain, */*",
    "content-type": "application/json;charset=UTF-8"
}


def criaHeaders():
    global headers
    user = input("insira o user access:")
    authorization = input("insira o Bearer, sem a palavra 'Bearer' no começo:")
    headers['user-access'] = user
    headers['Authorization'] = authorization


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
        requisicaoTela(Method, Purl, Pheaders=Pheaders, Pdata=Pdata, Pfiles=Pfiles, Pjson=Pjson, Pparam=None)
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


def montarJsonPostUuid(jsonImovel, jsonRequerente, jsonFindCreditos):
    jsonImovelFormatado = {
        "id": jsonImovel["id"],
        "codigo": jsonImovel["codigo"],
        "inscricaoImobiliariaFormatada": jsonImovel["inscricaoImobiliariaFormatada"],
        "inscricaoIncra": jsonImovel["inscricaoIncra"],
        "inscricaoAnterior": jsonImovel["inscricaoAnterior"],
        "unidade": jsonImovel["unidade"],
        "nroImovel": jsonImovel["nroImovel"],
        "situacao": jsonImovel["situacao"],
        "tipoImovel": jsonImovel["tipoImovel"],
        "englobado": jsonImovel["englobado"],
        "denominacao": jsonImovel["denominacao"],
        "contribuinte": jsonImovel["contribuinte"],
        "condominio": jsonImovel["condominio"],
        "imoveisEnglobados": jsonImovel["imoveisEnglobados"],
        "enderecoDescritivo": jsonImovel["enderecoDescritivo"],
        "existeObra": jsonImovel["existeObra"],
        "templateId": jsonImovel["templateId"],
        "proprietarios": [
            {
                "id": jsonImovel["proprietarios"][0]["contribuinte"]["id"],
                "percentual": jsonImovel["proprietarios"][0]["percentual"].__int__(),
                "cpfCnpj": jsonImovel["proprietarios"][0]["contribuinte"]["cpfCnpj"],
                "nome": jsonImovel["proprietarios"][0]["contribuinte"]["nome"],
                "obito": jsonImovel["proprietarios"][0]["contribuinte"]["obito"]
            }
        ],
        "pessoa": jsonImovel["proprietarios"][0]["contribuinte"],
        "searchKeyword": jsonImovel["codigo"].__str__() + " - " + jsonImovel["contribuinte"]["nome"]
    }
    jsonFindCreditos["filtros"]["imovel"] = jsonImovelFormatado
    jsonFindCreditos["requerente"] = {
        "id": jsonRequerente["id"],
        "codigo": jsonRequerente["codigo"],
        "nome": jsonRequerente["nome"],
        "obito": jsonRequerente["obito"],
        "cpfCnpj": jsonRequerente["cpfCnpj"],
        "situacao": jsonRequerente["situacao"],
        "tipo": jsonRequerente["tipo"],
        "templateId": jsonRequerente["templateId"]
    }
    return jsonFindCreditos



with open("pessoas.txt", "r") as file:
    # Ler cada linha do arquivo
    for line in file:
        # Carregar a linha como um dicionário
        data = json.loads(line)
        # Adicionar o dicionário à lista
        registros.append(data)

for requisicao in registros:
    urlImovel = "https://tributos.betha.cloud/tributos/v1/api/cadastros/referentes/imoveis/" + requisicao["imovel"].__str__()
    urlRequerente = "https://tributos.betha.cloud/tributos/v1/api/cadastros/referentes/contribuintes/" + requisicao["responsavel"].__str__()
    urlFindCreditos = "https://tributos.betha.cloud/tributos/v1/api/core/manutencoesCalculos/findCreditos"

    jsonIntegralImovel = requisicaoTela("GET", urlImovel, Pheaders=headers).json()
    jsonIntegralContribuinte = requisicaoTela("GET", urlRequerente, Pheaders=headers).json()
    jsonUuid = montarJsonPostUuid(jsonIntegralImovel, jsonIntegralContribuinte, jsonFindCreditos)
    print(json.dumps(jsonIntegralContribuinte))
    print(json.dumps(jsonUuid))
    uuid = requisicaoTela("POST", urlFindCreditos, Pheaders=headers, Pdata=json.dumps(jsonUuid)).json()["uuid"]
    url = "https://tributos.betha.cloud/tributos/v1/api/core/manutencoesCalculos/findCreditos/" + uuid
    creditos = requisicaoTela(Method="GET",
                   Purl=url,
                   Pheaders=headers).text
    creditos = requisicaoTela(Method="GET",
                              Purl=url,
                              Pheaders=headers).text
    print("teste1"+creditos)

    exit()
    if not(creditos):
        continue

    print(requisicao)

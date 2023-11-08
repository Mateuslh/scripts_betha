import os
from  scripts_betha.domain.ClassRequisicaoTela import RequisicaoTela
from scripts_betha.domain.ClassHeaders import headers as headers_class
from dotenv import load_dotenv
load_dotenv()

def encontrarHistoricos(lista):
    for item in lista:
        if "historico" in item and item["historico"] is True:
            return item
    return None

headers = headers_class(autorization= os.environ["Authorization"],
                        otherfields=
                       {
                           "User-Access": os.environ["UserAccess"],
                           "Accept": os.environ["Accept"] # ,
                           # "content-type": os.environ["content-type"]
                       })
RequisicaoTela.header = headers

urlMatriculas = os.environ["urlMatriculas"]
urlRegistros = urlMatriculas+"/listagem-matricula?limit=3000&selecaoAvancada=id+in+("+os.environ["idSelecaoAvancada"]+")"
requestRegistros = RequisicaoTela(Method="GET", Purl=urlRegistros)
registros = requestRegistros.rodar().json()

requestPutMatricula = RequisicaoTela(Method="PUT", Purl=urlMatriculas + "/APOSENTADO")

for registro in registros["content"]:
    print(registro["id"])
    urlMatricula = urlMatriculas+"/"+registro["id"].__str__()
    requestMatricula = RequisicaoTela(Method="GET")
    jsonMatricula = requestMatricula.rodar(Purl=urlMatricula)

    urlHistorico = urlMatricula+"/historicos/diferencas?limit=50&offset=0"
    requestHistoricos = RequisicaoTela(Method="GET", Purl=urlHistorico)
    jsonHistoricos = encontrarHistoricos(requestHistoricos.rodar().json())

    for historico in jsonHistoricos["content"]:
        print(historico["id"])
        urlMatricula = urlMatriculas + "/" + historico["id"].__str__()
        jsonHistorico = requestMatricula.rodar(Purl=urlMatricula)
        requestPutMatricula.rodar(Pjson=jsonHistorico)

    requestPutMatricula.rodar(Pjson=jsonMatricula)

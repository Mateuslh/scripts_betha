from scripts_betha.domain.ClassRequisicaoTela import RequisicaoTela
from scripts_betha.domain.ClassHeaders import Headers as headersClass
from scripts_betha.tool_box.arquivos.csv import escrever_csv
from decouple import config


def format_body(dict):
    return {
        "nome": dict["titulo"],
        "id": dict["id"],
        "tipo": dict["tipo"],
        "cadastro": dict["cadastro"]
    }


headers = headersClass(autorization=config("autorization",cast=str),
                       otherfields=
                       {
                           "User-Access": config("User-Access",cast=str),
                           "Accept": config("Accept",default="application/json, text/plain, */*")  # ,
                           # "content-type": config("content-type",cast=str)
                       })
RequisicaoTela.header = headers


urlCamposAdicionais = config("urlCamposAdicionais",cast=str)

urlRegistros = urlCamposAdicionais+"?limit=1000"
requestRegistros = RequisicaoTela(Method="GET", Purl=urlCamposAdicionais)
registros = requestRegistros.rodar().json()


dicFinal = []
for registro in registros["content"]:
    urlRegistroDetalhado = urlCamposAdicionais+"/"+registro["id"].__str__()

    if registro["tipo"] == "LISTA_SELECAO":
        registroDetalhado = requestRegistros.rodar(Purl=urlRegistroDetalhado).json()
        dicFinal.append(format_body(registro))
        for opcao in registroDetalhado["opcoes"]:
            dicFinal.append(format_body(opcao))

    elif registro["tipo"] == "ITEM_SELECAO":
        pass
    else:
        dicFinal.append(format_body(registro))

escrever_csv(lista_de_dicts=dicFinal, nome_arquivo="campos_adicionais_jf.csv")

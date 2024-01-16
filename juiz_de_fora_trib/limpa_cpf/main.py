from json import loads

from tool_box.arquivos.arquivo import ler_arquivo
from domain.ClassRequisicaoSL import RequisicaoServiceLayer
alteracoes = []

for linha in ler_arquivo("resultado.txt"):
    dict_linha = loads(linha)
    json = {
        "idIntegracao": str(dict_linha["contribId"]),
        "pessoas": {
            "idGerado": {
                "id": dict_linha["contribId"]
            },
            "cpfCnpj": None
        }
    }
    alteracoes.append(json)


request = RequisicaoServiceLayer(Method="PATCH",
                                 Pheaders={"Authorization":"Bearer c99b5c6c-16be-4d0c-9fed-8af564b13805"},
                                 Purl="https://tributos.betha.cloud/service-layer-tributos/api/pessoas")

request.cria_lotes(tamanho_lote=50,list_registros=alteracoes)
request.envia_lotes()
request.cria_logs("C:\\Users\\mateus.hemkemeier\\Downloads\\scripts_betha\\juiz_de_fora_trib\\limpa_cpf")


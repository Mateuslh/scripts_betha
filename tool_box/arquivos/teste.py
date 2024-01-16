from aaa import resultado_final
from domain.ClassRequisicaoSL import RequisicaoServiceLayer
from os import path

request = RequisicaoServiceLayer(Method="PATCH",
                                 Purl="https://tributos.betha.cloud/service-layer-tributos/api/parcelamentosComposicoes",
                                 Pheaders={"Authorization": "Bearer c99b5c6c-16be-4d0c-9fed-8af564b13805"})

request.cria_lotes(list_registros=resultado_final,tamanho_lote=200)
request.envia_lotes()
request.cria_logs(path.realpath(__file__))

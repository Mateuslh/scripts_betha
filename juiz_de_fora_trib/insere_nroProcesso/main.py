import os

from dotenv import load_dotenv

from scripts_betha.domain.ClassRequisicaoSL import RequisicaoServiceLayer
from scripts_betha.tool_box.arquivos.csv import ler_csv

load_dotenv()

parcelamentos = ler_csv(nome_arquivo="simulacoes.csv",
                        ordem_cabecalhos=["id_parcelamento", "numero_parcelamento"],
                        delimiter=";",
                        remover_cabecalho=True)

jsons_alteracoes = []
for parcelamento in parcelamentos:
    comentario = str(parcelamento["numero_parcelamento"]) + "-PARC.SIMULADO"
    jsonAlteracao = \
        {
            "idIntegracao": "numero_parcelamento " + str(parcelamento["numero_parcelamento"]),
            "parcelamentos": {
                "idGerado": {
                    "id": parcelamento["id_parcelamento"]
                },
                "nroProcesso": comentario
            }
        }
    jsons_alteracoes.append(jsonAlteracao)

requisicaoDividasMovtos = RequisicaoServiceLayer(Method="PATCH",
                                                 Pheaders={
                                                     "Authorization": os.environ["token_migracao"]
                                                 },
                                                 Purl=os.environ["url_serviceLayer_parcelamentos"])
requisicaoDividasMovtos.cria_lotes(tamanho_lote=50, list_registros=jsons_alteracoes)
requisicaoDividasMovtos.envia_lotes()
requisicaoDividasMovtos.cria_logs(os.path.dirname(os.path.realpath(__file__)))

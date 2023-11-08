import os

from dotenv import load_dotenv

from scripts_betha.domain.ClassRequisicaoSL import RequisicaoServiceLayer
from scripts_betha.tool_box.arquivos.csv import ler_csv

load_dotenv()

manutencao_dividas_csv = ler_csv(nome_arquivo="divida_parcelamento.csv",
                                 ordem_cabecalhos=["parcelamento_codigo", "divida_id"],
                                 delimiter=";",
                                 remover_cabecalho=True)

jsons_alteracoes = []
data_altaracoes = os.environ["dh_alteracoes"]
for manutencao in manutencao_dividas_csv:
    comentario = "PARCELAMENTO "+str(manutencao["parcelamento_codigo"])
    jsonAlteracao = {
        "idIntegracao": "id divida " + str(manutencao["divida_id"]),
        "dividasMovtos":
            {
                "comentario": comentario,
                "dhManutencao": data_altaracoes,
                "dhMovimentacao": data_altaracoes,
                "idDividas": manutencao["divida_id"],
                "tiposMovimentacoesDivida": "COMENTARIO",
                "obsHomologManutencao": comentario}
    }
    jsons_alteracoes.append(jsonAlteracao)

requisicaoDividasMovtos = RequisicaoServiceLayer(Method="POST",
                                                 Pheaders={
                                                     "Authorization": os.environ["token_migracao"]
                                                 },
                                                 Purl=os.environ["url_serviceLayer_dividasMovtos"])
requisicaoDividasMovtos.cria_lotes(tamanho_lote=50, list_registros=jsons_alteracoes)
requisicaoDividasMovtos.envia_lotes()
requisicaoDividasMovtos.cria_logs(os.path.dirname(os.path.realpath(__file__)))

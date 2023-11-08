from scripts_betha.domain.ClassRequisicaoSL import RequisicaoServiceLayer
from scripts_betha.domain.ClassHeaders import Headers
from scripts_betha.tool_box.arquivos.arquivo_json import ler_de_json
from os import environ as env,path
from dotenv import load_dotenv

load_dotenv()
arquivo = ler_de_json(nome_arquivo=env["nomeArquivo"])
alteracoes = []

for debito in arquivo:
    id_integracao = ("debito: " + str(debito["debito"]) + " vlLancado: " + str(debito["vlLancado"]) + " referente|identificador: " +
                         str(debito["referente"]["tipo"]["valor"]) + "|" +str(debito["referente"]["identificador"]))

    alteracao = {
        "idIntegracao": id_integracao,
        "guias": {
            "idGerado": {
                "id": debito["debito"]
            },
            "situacao": "CANCELADA"
        }
    }
    alteracoes.append(alteracao)

requesicao = RequisicaoServiceLayer(Method="PATCH",
                                    Pheaders={"Authorization":env["tokenMigracao"]},
                                    Purl=env["urlDebito"])
requesicao.cria_lotes(list_registros=alteracoes,tamanho_lote=200)
requesicao.envia_lotes()
requesicao.cria_logs(path.dirname(path.realpath(__file__)))
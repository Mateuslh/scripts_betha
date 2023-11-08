import os
from datetime import datetime

from dotenv import load_dotenv

from scripts_betha.domain.ClassHeaders import Headers
from scripts_betha.domain.ClassRequisicaoSL import RequisicaoServiceLayer
from scripts_betha.domain.ClassRequisicaoTela import RequisicaoTela
from scripts_betha.tool_box.arquivos.arquivo import ler_arquivo, escrever_arquivo

load_dotenv()

diretorio_atual = os.path.dirname(os.path.realpath(__file__))

nome_arquivo_controle = diretorio_atual + "/arquivoControle.txt"
arquivo_controle_exite = os.path.exists(nome_arquivo_controle)
if arquivo_controle_exite:
    ids_inseridos = ler_arquivo(nome_arquivo_controle)[0].split(",")
else:
    ids_inseridos = []
print(ids_inseridos)
headers = Headers(autorization=os.environ["tokenTela"],
                  otherfields={
                      "User-Access": os.environ["UserAccess"],
                      "Accept": os.environ["Accept"]
                  })

url_manutencao_dividas = os.environ["url_manutencao_dividas"]
filtro_manutencao_dividas = os.environ["filtro_manutencao_dividas"]
url_manutencao_dividas_construida = url_manutencao_dividas + filtro_manutencao_dividas

requisicao_manutencao_dividas = RequisicaoTela(Method="GET",
                                               Pheaders=headers,
                                               Purl=url_manutencao_dividas_construida)
retorno_manutencao_dividas = requisicao_manutencao_dividas.rodarRegistrosMultiplos(retornarJson=True)

requisicao_manutencao_dividas_detalhado = RequisicaoTela(Method="GET",
                                                         Pheaders=headers,
                                                         Purl=url_manutencao_dividas,
                                                         Pparam={"calcularAcrescimos": False,
                                                                 "dataBase": datetime.today().strftime('%Y-%m-%d')})
manutencao_dividas = []
for manutencao_divida in retorno_manutencao_dividas:
    idManutencao = manutencao_divida["id"]
    if manutencao_divida["observacoes"] is None or idManutencao in ids_inseridos:
        continue
    ids_inseridos.append(idManutencao)
    url_manutencao_dividas_detalhado = requisicao_manutencao_dividas_detalhado.url + "/" + idManutencao + "/" + "dividas"
    retorno_manutencao_dividas_detalhado = requisicao_manutencao_dividas_detalhado.rodarRegistrosMultiplos(
        retornarJson=True, Purl=url_manutencao_dividas_detalhado)
    objFinalManutencaoDivida = {"manutencaoDivida": manutencao_divida,
                                "dividas": retorno_manutencao_dividas_detalhado}
    manutencao_dividas.append(objFinalManutencaoDivida)

jsonsAlteracoes = []
for manutencao in manutencao_dividas:
    manutencaoDivida = manutencao["manutencaoDivida"]
    for divida in manutencao["dividas"]:
        jsonAlteracao = \
            {
                "idIntegracao": "id divida " + str(divida["id"]),
                "dividasMovtos":
                    {
                        "comentario": manutencaoDivida["observacoes"],
                        "dhManutencao": manutencaoDivida["dhManutencao"],
                        "dhMovimentacao": manutencaoDivida["dhManutencao"],
                        "idDividas": divida["id"],
                        "nroProcesso": manutencaoDivida["nroProcesso"],
                        "tiposMovimentacoesDivida": "COMENTARIO",
                        "obsHomologManutencao": manutencaoDivida["observacoes"]}
            }
        jsonsAlteracoes.append(jsonAlteracao)

requisicaoDividasMovtos = RequisicaoServiceLayer(Method="POST",
                                                 Pheaders={
                                                     "Authorization": os.environ["tokenMigracao"]
                                                 },
                                                 Purl=os.environ["url_serviceLayer_dividasMovtos"])
requisicaoDividasMovtos.cria_lotes(tamanho_lote=50, list_registros=jsonsAlteracoes)
requisicaoDividasMovtos.envia_lotes()
requisicaoDividasMovtos.cria_logs(os.path.dirname(os.path.realpath(__file__)))
if arquivo_controle_exite:
    os.remove(nome_arquivo_controle)
escrever_arquivo(nome_arquivo=nome_arquivo_controle, linhas=[",".join(ids_inseridos)], pular_linhas=False)

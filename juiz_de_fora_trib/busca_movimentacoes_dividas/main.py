import os
from dotenv import load_dotenv
from scripts_betha.domain.ClassHeaders import Headers
from scripts_betha.domain.ClassRequisicaoTela import RequisicaoTela
from scripts_betha.tool_box.arquivos.arquivo_json import escrever_em_json
load_dotenv()

headers = Headers(autorization=os.environ["tokenTela"],
                  otherfields={
                      "User-Access": os.environ["UserAccess"],
                      "Accept": os.environ["Accept"]
                  })

url_dividasMovtos = os.environ["url_dividasMovtos"]
filtro_dividasMovtos = os.environ["filtro_dividasMovtos"]
url_dividasMovtos_construida = url_dividasMovtos + filtro_dividasMovtos

requisicao_manutencao_dividas = RequisicaoTela(Method="GET",
                                               Pheaders=headers,
                                               Purl=url_dividasMovtos_construida)
retorno_manutencao_dividas = requisicao_manutencao_dividas.rodarRegistrosMultiplos(retornarJson=True, Plimit=200)
escrever_em_json(data=retorno_manutencao_dividas)
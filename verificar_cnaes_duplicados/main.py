from scripts_betha.tool_box.arquivos.csv import ler_csv
from scripts_betha.tool_box.listas import groupBy
from numpy import size


arquivo = ler_csv(nome_arquivo="teste.csv",
        delimiter=";",
        ordem_cabecalhos=[
            "insc",
            "codEconomico",
            "dataInicioAtividade",
            "dataFimAtividade",
            "codSitucao",
            "descricaoSitAtividade",
            "atividadePrincipal"
        ])


lista = groupBy(arquivo,"insc","codEconomico")
for i in lista:
    if size(i) != 1:
        print(i)
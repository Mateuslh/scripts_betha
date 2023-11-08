import json
from datetime import datetime
# pré requisitos

# tabela com o id do imovel e do responsavel de cada inscrição imob
credito = {
    "descricao": "IMPOSTO PREDIAL E TERRITORIAL URBANO",
    "id": 132997,
    "abreviatura": "IPTU",
    "emUso": None,
    "desativado": "NAO",
    "flyProtocolo": "NAO",
    "indexadores": {
        "id": 40978,
        "nome": "REAIS",
        "sigla": "R$",
        "tipo": "MOEDA_DO_PAIS",
        "version": 2
    },
    "qtdadeReceitas": 12,
    "tipoCadastro": "IMOVEIS",
    "notificacaoIss": None,
    "version": 0
}

# ----------------------------------------------------#
# obter json do requerente e do imovel
jsonImovel = {}

# obter o uuid na api (https://tributos.betha.cloud/tributos/v1/api/core/manutencoesCalculos/findCreditos)
# baseados no dados chumbados e do json do imovel e requerente obtido
jsonFindCreditos = {"tipoRequerimento":"EXTERNO",
   "dtRequerimento":"2023-08-31",
   "filtros":{
      "imovel": None
   },
   "tipoSolicitacao":"REVISAO_CALCULO",
   "beneficioFiscal":None,
   "tipoSelecaoCreditos":"INDIVIDUAL",
   "tipoVigencia":"ANO",
   "abrangencia":"INDIVIDUAL",
   "percLancadoReq":None,
   "percJurosReq":None,
   "percMultaReq":None,
   "percCorrecaoReq":None,
   "requerente":'',
   "dtIniVigencia":None,
   "dtFimVigencia":None,
   "anoVigencia":2023,
   "observacao":"teste",
   "creditosTributarios":{
      "descricao":"IMPOSTO PREDIAL E TERRITORIAL URBANO",
      "id":132997,
      "abreviatura":"IPTU",
      "emUso":None,
      "desativado":"NAO",
      "flyProtocolo":"NAO",
      "indexadores":{
         "id":40978,
         "nome":"REAIS",
         "sigla":"R$",
         "tipo":"MOEDA_DO_PAIS",
         "version":2
      },
      "qtdadeReceitas":12,
      "tipoCadastro":"IMOVEIS",
      "notificacaoIss":None,
      "version":6038
   }
}
# obter os creditos na api (https://tributos.betha.cloud/tributos/v1/api/core/manutencoesCalculos/findCreditos/)
jsonFindCreditosUuid = {
    "idCredito": 132997,
    "abreviatura": "IPTU",
    "ano": 2023,
    "receitas": [
        {
            "creditoTributarioRec": {
                "ativa": "SIM",
                "creditosTributarios": {
                    "id": 132997
                },
                "id": 353980,
                "receitas": {
                    "abreviatura": "9487",
                    "classificacao": "TAXA",
                    "descricao": "TX COLETA RESIDUOS SOLIDOS",
                    "id": 478747,
                    "inscDividaAtiva": "SIM",
                    "version": "82690b7cc6441fc14eaabf1648bf31ac",
                    "possuiLancamento": False,
                    "atoNaoInscrito": None,
                    "atoInscrito": None,
                    "atoExecucaoFiscal": None,
                    "tipoVinculoAtoNaoInscrito": None,
                    "tipoVinculoAtoInscrito": None,
                    "codigoTCE": None,
                    "gerenciandoAtos": None,
                    "cobrancaCompartilhada": False,
                    "naoContabilizavel": None
                },
                "situacao": "ATIVA",
                "iReceitas": None,
                "version": "52355e30d7199b237345cc010e582b89"
            },
            "referente": {
                "id": None,
                "descricao": "Imóvel 52826007",
                "tipoCadastro": "IMOVEIS",
                "manutencaoCalculo": None,
                "lancamento": {
                    "id": 696825549
                },
                "contribuicaoMelhoria": None,
                "economico": None,
                "imovel": {
                    "id": 22182433
                },
                "notaAvulsa": None,
                "receitaDiversa": None,
                "receitaDiversaLancto": None,
                "transferenciaImovel": None,
                "pessoa": None,
                "obra": None,
                "referentesCnaes": None,
                "referentesListaServicos": None,
                "version": None
            },
            "valorLancado": 889.83,
            "valorCorrecao": 0.0000,
            "valorJuros": 0.0000,
            "valorMulta": 95.2000,
            "valorBeneficioLancadoReq": 0.00,
            "percLancado": 0,
            "percCorrecao": 0,
            "percJuros": 0,
            "percMulta": 0,
            "percLancadoReq": 0,
            "percCorrecaoReq": 0,
            "percJurosReq": 0,
            "percMultaReq": 0,
            "anosVigencia": "2023"
        },
        {
            "creditoTributarioRec": {
                "ativa": "SIM",
                "creditosTributarios": {
                    "id": 132997
                },
                "id": 353975,
                "receitas": {
                    "abreviatura": "6000",
                    "classificacao": "IMPOSTO",
                    "descricao": "IMP S/PROPR PRED E TER URBA",
                    "id": 478615,
                    "inscDividaAtiva": "SIM",
                    "version": "6fe83c6524d75a6b2454265b2d25bede",
                    "possuiLancamento": False,
                    "atoNaoInscrito": None,
                    "atoInscrito": None,
                    "atoExecucaoFiscal": None,
                    "tipoVinculoAtoNaoInscrito": None,
                    "tipoVinculoAtoInscrito": None,
                    "codigoTCE": None,
                    "gerenciandoAtos": None,
                    "cobrancaCompartilhada": False,
                    "naoContabilizavel": None
                },
                "situacao": "ATIVA",
                "iReceitas": None,
                "version": "1e3e49ceb9b56f7cc9fa7a26b00c466e"
            },
            "referente": {
                "id": None,
                "descricao": "Imóvel 52826007",
                "tipoCadastro": "IMOVEIS",
                "manutencaoCalculo": None,
                "lancamento": {
                    "id": 696825549
                },
                "contribuicaoMelhoria": None,
                "economico": None,
                "imovel": {
                    "id": 22182433
                },
                "notaAvulsa": None,
                "receitaDiversa": None,
                "receitaDiversaLancto": None,
                "transferenciaImovel": None,
                "pessoa": None,
                "obra": None,
                "referentesCnaes": None,
                "referentesListaServicos": None,
                "version": None
            },
            "valorLancado": 4526.80,
            "valorCorrecao": 0.0000,
            "valorJuros": 0.0000,
            "valorMulta": 484.3600,
            "valorBeneficioLancadoReq": 0.00,
            "percLancado": 0,
            "percCorrecao": 0,
            "percJuros": 0,
            "percMulta": 0,
            "percLancadoReq": 0,
            "percCorrecaoReq": 0,
            "percJurosReq": 0,
            "percMultaReq": 0,
            "anosVigencia": "2023"
        }
    ],
    "referente": {
        "id": None,
        "descricao": "Imóvel 52826007",
        "tipoCadastro": "IMOVEIS",
        "manutencaoCalculo": None,
        "lancamento": {
            "id": 696825549
        },
        "contribuicaoMelhoria": None,
        "economico": None,
        "imovel": {
            "id": 22182433
        },
        "notaAvulsa": None,
        "receitaDiversa": None,
        "receitaDiversaLancto": None,
        "transferenciaImovel": None,
        "pessoa": None,
        "obra": None,
        "referentesCnaes": None,
        "referentesListaServicos": None,
        "version": None
    },
    "lancamento": 696825549,
    "complementar": "NAO",
    "beneficioAplicado": False
}
# dar o post com o dados obtidos , exemplo de JSON:
jsonManutencoesCalculos = {
    "tipoRequerimento": "EXTERNO",
    "dtRequerimento": datetime.today().strftime('%Y-%m-%d'),
    "filtros": {},
    "tipoSolicitacao": "REVISAO_CALCULO",
    "beneficioFiscal": None,
    "tipoSelecaoCreditos": "INDIVIDUAL",
    "tipoVigencia": "ANO",
    "abrangencia": "INDIVIDUAL",
    "percLancadoReq": None,
    "percJurosReq": None,
    "percMultaReq": None,
    "percCorrecaoReq": None,
    "requerente": {
        "id": 62668469,
        "codigo": 9000063545,
        "nome": "JOSE CORREA OLIVEIRA SOBRINHO",
        "obito": "NAO",
        "cpfCnpj": "00000000000000",
        "situacao": "ATIVO",
        "tipo": "FISICA",
        "endereco": "R. JOAO MARIANO DE ALMEIDA, 00065, OSWALDO CRUZ-SANTA CRUZ, Juiz de Fora (MG)",
        "templateId": None
    },
    "observacao": "30070382023",
    "dtIniVigencia": None,
    "dtFimVigencia": None,
    "anoVigencia": 2023,
    "creditosTributarios": {
        "descricao": "IMPOSTO PREDIAL E TERRITORIAL URBANO",
        "id": 132997,
        "abreviatura": "IPTU",
        "emUso": None,
        "desativado": "NAO",
        "flyProtocolo": "NAO",
        "indexadores": {
            "id": 40978,
            "nome": "REAIS",
            "sigla": "R$",
            "tipo": "MOEDA_DO_PAIS",
            "version": 2
        },
        "qtdadeReceitas": 12,
        "tipoCadastro": "IMOVEIS",
        "notificacaoIss": None,
        "version": 6038
    },
    "classificacaoRevisaoCalculo": "IMPUGNACAO",
    "manutCalcCreditosRec": []
}
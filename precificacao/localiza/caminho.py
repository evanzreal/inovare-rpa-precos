"""
Localiza · precificacao.  [⏳ TODO — a mais usada/importante]

Da reuniao original: existe um Excel completo pra baixar (todas as combinacoes:
km, prazo, preco), mas pede 2FA a cada 15 dias e SO O SOCIO tem o autenticador
-> precisa coordenar login nesses momentos. NAO EXPLORAMOS essa rota ainda.

Rota que testamos e confirmamos manualmente (2026-09-13), e que vamos automatizar
primeiro por nao depender do 2FA do Excel:

    MENU > Oportunidade > (visao "Oportunidades abertas" -- a visao "Todas"
    trava carregando pra sempre, ver nota abaixo) > abrir uma oportunidade
    qualquer > botao "Nova Proposta" (canto superior direito).

Formulario "Proposta Meoo" (Salesforce LWC). Campos fixos pra TODA consulta:
    - Tipo da proposta: "Normal"
    - Categoria: "Todas" (nao filtrar por categoria)
    - Desconto (%): sempre "13" (o campo converte pra "13,00")

Pintura depende do que o modelo escolhido tem disponivel -- ordem de prioridade:
    1. "Solida"
    2. se nao tiver Solida, "Metalica"
    3. se nao tiver Metalica, "Perolizada"
(se so sobrar uma opcao de pintura na lista e ela nao for testada, pode dar erro
ao Calcular -- sempre conferir o que a lista de Pintura oferece pra cada modelo)

Variaveis que a gente varre DENTRO de cada modelo: Prazo e Franquia.

Ordem de varredura (loop aninhado):
    para cada Modelo (um datalist por Categoria; Categoria fica fixa em "Todas"):
        escolhe a Pintura (fallback Solida > Metalica > Perolizada)
        seta Desconto = 13
        para cada Prazo (12, 18, 24, 36, 48 meses):
            para cada Franquia (500, 750, 1000, 1250, 1500, 2000, 2500, 3000,
                                 3500, 4000, 4500 km):
                clica "Calcular" (o preco NAO recalcula sozinho ao trocar
                    prazo/franquia -- sem clicar em Calcular o valor fica
                    zerado/desatualizado)
                rola pra baixo e le:
                    - "Valor PMT Final"   -> LinhaPreco.preco
                    - "Km Excedente"      -> guardar em LinhaPreco.bruto
        troca de Modelo e repete

Cada combinacao (modelo, prazo, franquia) tem que ficar registrada com o Valor
PMT Final e o Km Excedente dessa combinacao especifica -- sao os dois dados que
alimentam a base final.

Login feito pelo Guilherme em 2026-06-26.
Portal (Salesforce Experience Cloud): https://localiza.my.site.com/meoorevendas/s/

PENDENTE: escrever o Playwright que segue exatamente esse roteiro (o form usa
componentes LWC -- provavel que precise do mesmo padrao "click -> fill('') ->
press_sequentially -> dispatch change/blur" ja usado no fluxo de credito, ver
rpa/fluxos/analise_credito/localiza/caminho.py no inovare-rpa).
"""

from modelos import LinhaPreco

PORTAL = "https://localiza.my.site.com/meoorevendas/s/"


class Localiza:
    nome = "localiza"
    metodo = "raspagem"  # simulacao via "Nova Proposta"; Excel com 2FA fica de reserva

    def coletar(self, context) -> list[LinhaPreco]:
        raise NotImplementedError(
            "Localiza precificacao ainda nao implementada "
            "(roteiro mapeado no docstring deste arquivo)."
        )

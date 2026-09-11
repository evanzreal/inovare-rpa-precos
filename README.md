# Inovare RPA · Precificação

Robô que entra nos portais das locadoras e coleta preços (mês × km × modelo)
para alimentar o **[Price Intelligence](https://github.com/evanzreal/price-intelligence-inovare)**
(Farol de Preço). Roda 1x/semana via cron/LaunchAgent — sem servidor, sem API.

## Por que é um repositório separado do `inovare-rpa`

O `inovare-rpa` (análise de crédito) roda 24/7 num servidor (`server.py`) que
mantém uma sessão de navegador logada; reiniciá-lo pede login de novo. Como a
precificação roda 1x/semana e não precisa de API, ela vive num processo (e
repositório) totalmente separado — assim mexer/quebrar/testar aqui nunca
derruba o servidor de crédito.

## Estrutura

```
navegador.py          navegador com perfil logado persistente (.perfil_chrome/)
modelos.py             LinhaPreco
precificacao/
├── base.py            contrato CaminhoPreco (coletar)
├── normalizacao.py     de-para nomes/meses/km → base única
├── pipeline.py         roda todos os caminhos, normaliza, concatena
├── unidas/    ⏳ baixar tabela de preço (SEM 2FA — começar aqui)
├── fluor/     ⏳ raspar tela (fácil)
├── sinedrive/ ⏳ filtrar PF/PJ + raspar (sessão cai)
├── localiza/  ⏳ baixar Excel (2FA a cada 15d, só o sócio tem)
├── lm/        ⏳ tempo real, ordem dinâmica (mais difícil)
├── movida/    ⏳ já tem Excel interno (por último)
├── livre/     ⏳ tabela de preços logada
├── nexia/     ⏳ confirmar fluxo (Stellantis)
└── byetech/   ⏳ agregador — pode trazer várias locadoras de uma vez
executar.py            entrypoint (roda o pipeline)
```

Migrado do `inovare-rpa` (`rpa/fluxos/precificacao/`), onde já existia como
esqueleto — só os contratos (`base.py`) e `pipeline.py` estavam prontos; nenhum
caminho de locadora tinha sido implementado ainda.

## Rodar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# logar nas locadoras uma vez (perfil fica salvo em .perfil_chrome/)
python3 executar.py
```

## Destino dos dados — TODO (etapa 2)

O pipeline hoje só coleta e imprime. Falta:
1. Implementar cada `caminho.py` (começar por Unidas — download direto, sem 2FA).
2. Gerar o Excel no formato que `Price Intelligence/etl/extract.py` espera
   (`Simulador*.xlsx` + `*Livre*.xlsx`) e salvar em
   `Price Intelligence/bases_base/<próximo número>/`.
3. Rodar `etl/extract.py && etl/seed_supabase.py` lá para publicar no Farol.

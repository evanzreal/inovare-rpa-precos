"""
Entrypoint standalone da precificacao.

Roda uma vez (chamado por cron/LaunchAgent semanal), sem servidor/API — de
propósito independente do inovare-rpa (credito), que roda 24/7 mantendo sessao
logada. Assim, mexer/testar aqui nunca derruba o servidor de credito nem exige
logar de novo nele.

[⏳ TODO — etapa 2] gerar o(s) Excel/planilha no formato que o ETL do
Price Intelligence espera e salvar em
../Price\ Intelligence/bases_base/<proximo numero>/, depois disparar
`etl/extract.py` + `etl/seed_supabase.py` la.
"""

from navegador import abrir_navegador
from precificacao.pipeline import rodar

if __name__ == "__main__":
    with abrir_navegador(headless=False) as context:
        linhas = rodar(context)
        print(f"\n{len(linhas)} linhas coletadas no total.")

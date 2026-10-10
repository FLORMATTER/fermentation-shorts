# -*- coding: utf-8 -*-
"""
Resolve o item aberto do guia do dinheiro: "confirme se o Brasil esta na lista" do
TikTok Creator Rewards. Checado em 26/09/2026 em duas fontes independentes.

Achados que mudam o guia:
  1. Brasil ESTA na lista (8 paises).
  2. O pagamento depende do pais do ESPECTADOR: view so paga se vier de um dos 8.
  3. O portao real e maior que "video de 60 s": 10.000 seguidores + 100.000 views/30 d,
     conta pessoal, 18+, e video ACIMA de 1 minuto.
  4. Nao ha RPM fixo publicado (~US$ 0,40-1,00 por 1.000 views qualificadas).

4 ancoras com contagem: qualquer uma fora do esperado -> ABORTA SEM GRAVAR.
"""
import io, os, shutil, sys

G = 'C:/Users/Saxa/Desktop/youtube-work/guias/como-ganhar-dinheiro.md'
d = io.open(G, encoding='utf-8').read()
ANTES = len(d)

# ---------------------------------------------------------------- 1. a linha da tabela
A1 = '| **TikTok Creator Rewards** | **US$ 500 \u2013 1.500** | v\u00eddeo 60 s+, pa\u00eds eleg\u00edvel |\n'
N1 = ('| **TikTok Creator Rewards** | **US$ 400 \u2013 1.000** | 10.000 seguidores **+ '
      '100.000 views / 30 d** + v\u00eddeo **> 1 min** + pa\u00eds eleg\u00edvel |\n')

# ------------------------------------------------- 2. o paragrafo "confirme se o Brasil"
A2 = ('**TikTok Creator Rewards exige pa\u00eds eleg\u00edvel.** **Confirme se o Brasil est\u00e1 na lista**\n'
      'antes de contar com essa linha \u2014 e note que seus v\u00eddeos t\u00eam 30\u201345 s, ent\u00e3o precisariam de\n'
      'uma vers\u00e3o de 60 s+.\n')
N2 = (
    '\u2705 **O Brasil EST\u00c1 na lista** \u2014 checado em 26/09/2026. O Creator Rewards roda em\n'
    '**8 pa\u00edses**: Estados Unidos, Reino Unido, Alemanha, Fran\u00e7a, Jap\u00e3o, Coreia do Sul,\n'
    '**Brasil** e M\u00e9xico (este entrou em 01/10/2025).\n'
    '\n'
    '\u26a0\ufe0f **Mas o dinheiro depende de onde est\u00e1 o ESPECTADOR, n\u00e3o de onde voc\u00ea est\u00e1.** Uma view\n'
    's\u00f3 conta como *qualified view* se **todas** valerem: v\u00eddeo **acima de 1 minuto**,\n'
    'assistido **5 s ou mais**, entregue na **For You**, e vista **de um dos 8 pa\u00edses**.\n'
    'View de audi\u00eancia brasileira em canal brasileiro paga **US$ 0**.\n'
    '\n'
    '> \U0001f511 **Isso n\u00e3o \u00e9 um problema \u2014 \u00e9 um argumento a favor do canal em ingl\u00eas.** Este guia j\u00e1\n'
    '> manda n\u00e3o traduzir (o RPM cai 3 a 5\u00d7). A mesma decis\u00e3o \u00e9 o que faz a view valer no\n'
    '> TikTok: canal EN mirando EUA/Reino Unido acerta o p\u00fablico que paga nas duas plataformas.\n'
    '\n'
    '\u26a0\ufe0f **O port\u00e3o do TikTok \u00e9 maior do que "v\u00eddeo de 60 s".** Al\u00e9m de v\u00eddeo > 1 min, exige\n'
    '**10.000 seguidores** e **100.000 views nos \u00faltimos 30 dias**, conta **pessoal** (n\u00e3o\n'
    'Business) e 18+. \u00c9 o segundo port\u00e3o mais duro da tabela \u2014 atr\u00e1s s\u00f3 do Facebook.\n'
    '\n'
    '\u26a0\ufe0f **N\u00e3o existe RPM fixo publicado.** A pr\u00f3pria TikTok diz que a f\u00f3rmula pesa\n'
    'originalidade, tempo assistido, valor de busca e engajamento. Estimativas de terceiros\n'
    'ficam em **US$ 0,40\u20131,00 por 1.000 views qualificadas** (\u2248 US$ 400\u20131.000 por milh\u00e3o) \u2014\n'
    'sempre por view **qualificada**, nunca por view total. Planeje pelo painel do TikTok Studio.\n'
)

# ------------------------------------- 3. a nota do corte de 60 s: a margem de 1 minuto
A3 = '`_criar-beet-garlic-60s.py`, que parte do arquivo validado.\n'
N3 = ('`_criar-beet-garlic-60s.py`, que parte do arquivo validado. Os **67,5 s** importam: o\n'
      'TikTok exige v\u00eddeo **acima de** 1 minuto, ent\u00e3o **n\u00e3o corte em 60,0 s cravados** \u2014\n'
      'deixe margem (65\u201370 s), sen\u00e3o o v\u00eddeo pode n\u00e3o contar como qualificado.\n')

# ---------------------------------------------------------------- 4. as fontes novas
A4 = '- FluxNote (26/06/2026) \u2014 RPM e elegibilidade do Facebook Content Monetization\n'
N4 = (A4 +
      '- TikTok Newsroom \u2014 an\u00fancio do Creator Rewards e requisitos oficiais (10.000\n'
      '  seguidores, 100.000 views/30 d, v\u00eddeo acima de 1 minuto)\n'
      '- quasa.io (26/07/2026) e monetizednow (18/09/2026) \u2014 lista dos 8 pa\u00edses e a regra de\n'
      '  que a view s\u00f3 paga se vier de um pa\u00eds eleg\u00edvel\n')

edicoes = [(A1, N1), (A2, N2), (A3, N3), (A4, N4)]
for i, (velho, novo) in enumerate(edicoes, 1):
    n = d.count(velho)
    if n != 1:
        print('ERRO: ancora %d casou %d vez(es), esperado 1. Nada gravado.' % (i, n))
        sys.exit(1)
    d = d.replace(velho, novo)

for t in ['**O Brasil EST\u00c1 na lista**', 'qualified view', 'n\u00e3o corte em 60,0 s cravados',
          'quasa.io (26/07/2026)', '10.000 seguidores **+ ']:
    if t not in d:
        print('ERRO: trecho novo ausente: %r. Nada gravado.' % t)
        sys.exit(1)

if 'Confirme se o Brasil' in d:
    print('ERRO: o pedido de confirmacao continua no arquivo. Nada gravado.')
    sys.exit(1)

if len(d) <= ANTES:
    print('ERRO: nao cresceu. Nada gravado.')
    sys.exit(1)

shutil.copy2(G, G + '.antes-do-tiktok')
with io.open(G, 'w', encoding='utf-8', newline='') as f:
    f.write(d)
print('OK: %d -> %d chars (+%d), %d ancoras' % (ANTES, len(d), len(d) - ANTES, len(edicoes)))

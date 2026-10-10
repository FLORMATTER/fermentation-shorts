# -*- coding: utf-8 -*-
"""_consertar-pt.py — conserta nos ARQUIVOS PORTUGUESES os 2 defeitos que ja
tinham sido corrigidos so no ingles.

Defeito 1 — `beterraba/shorts-beterraba-couve.html`, cena 1:
    o selo `TOTAL: 500 g` e `<rect x="34" y="556" width="337" height="76">`, ou seja
    cobre y 556..632. Os rotulos do grupo da beterraba estavam em y ABSOLUTO 566
    (BETERRABA) e 586 (300 g) — DENTRO do selo, e ainda por cima o grupo tem
    `floatUpDown` (sobe ate 7 px). Os rotulos da couve estao em 500/520, bem acima:
    era so a beterraba que estava baixa, porque o desenho tem raiz comprida.
    Conserto: encurtar a raiz (terminava em 148 relativo) e subir os dois rotulos
    para 150/170 relativo = 528/548 absoluto, com folga de 8 px do selo mesmo
    quando o grupo flutua para cima.

Defeito 2 — `pepino/shorts-pepino-speed.html`, cena 4:
    selo `<rect x="-132" width="264">` e texto `SEM TANINO = PEPINO MOLE` (24 car,
    19 px) precisa de ~294 px -> vaza nos dois lados. O selo ja e o MAIS LARGO do
    arquivo (os outros sao 60, 68, 76, 100, 208, 232), entao alargar para ~320
    ficaria fora de escala. Conserto: encurtar o texto para `SEM TANINO = MOLE`
    (17 car ~ 200 px), que e o espelho exato do ingles `NO TANNIN = MUSHY`.

Todas as ancoras sao conferidas ANTES de gravar; se qualquer uma nao casar
exatamente 1 vez, o script aborta sem escrever nada.
"""
import io
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
APLICAR = '--apply' in sys.argv

BET = 'beterraba/shorts-beterraba-couve.html'
PEP = 'pepino/shorts-pepino-speed.html'
DIC = '_dicionario-pt-en.py'

# (arquivo, rotulo, velho, novo)
TROCAS = [
    (BET, 'raiz da beterraba 148->130',
     '<path d="M-3,88 Q2,124 0,148" stroke="#5c0a34" stroke-width="8" fill="none" stroke-linecap="round"/>',
     '<path d="M-3,88 Q2,110 0,130" stroke="#5c0a34" stroke-width="8" fill="none" stroke-linecap="round"/>'),

    (BET, 'rotulo BETERRABA 188->150',
     '<text x="0" y="188" text-anchor="middle" font-size="16" font-weight="900" fill="#8e1a51" font-family="system-ui">BETERRABA</text>',
     '<text x="0" y="150" text-anchor="middle" font-size="16" font-weight="900" fill="#8e1a51" font-family="system-ui">BETERRABA</text>'),

    (BET, 'rotulo 300 g 208->170',
     '<text x="0" y="208" text-anchor="middle" font-size="12" font-weight="700" fill="#b09aa4" font-family="system-ui">300 g</text>',
     '<text x="0" y="170" text-anchor="middle" font-size="12" font-weight="700" fill="#b09aa4" font-family="system-ui">300 g</text>'),

    (PEP, 'selo SEM TANINO encurtado',
     '<text x="0" y="8" text-anchor="middle" font-size="19" font-weight="800" fill="#27500a" font-family="system-ui">SEM TANINO = PEPINO MOLE</text>',
     '<text x="0" y="8" text-anchor="middle" font-size="19" font-weight="800" fill="#27500a" font-family="system-ui">SEM TANINO = MOLE</text>'),

    (DIC, 'dicionario acompanha o texto novo',
     "    ('SEM TANINO = PEPINO MOLE', 'NO TANNIN = MUSHY'),",
     "    ('SEM TANINO = MOLE', 'NO TANNIN = MUSHY'),"),
]

# ── fase 1: so conferir ────────────────────────────────────────────────
conteudo = {}
for arq, rot, velho, novo in TROCAS:
    if arq not in conteudo:
        conteudo[arq] = io.open(os.path.join(RAIZ, arq), encoding='utf-8').read()
    c = conteudo[arq].count(velho)
    if c != 1:
        print('ABORTADO: [%s] casou %d vez(es), esperado 1.' % (rot, c))
        sys.exit(1)
    print('ok  %-34s %s' % (rot, arq))

# ── fase 2: aplicar em memoria ─────────────────────────────────────────
novo_conteudo = dict(conteudo)
for arq, rot, velho, novo in TROCAS:
    novo_conteudo[arq] = novo_conteudo[arq].replace(velho, novo, 1)

# ── fase 3: validar o resultado ────────────────────────────────────────
try:
    ns = {'__name__': 'dic'}
    exec(compile(novo_conteudo[DIC], DIC, 'exec'), ns)
    print('\ndicionario continua valido: %d entradas' % len(ns['DIC']))
except SyntaxError as e:
    print('ABORTADO: dicionario nao compila: %s' % e)
    sys.exit(1)

if not APLICAR:
    print('\n(dry-run — nada foi gravado. Use --apply para gravar.)')
    sys.exit(0)

# ── fase 4: backup + gravar ────────────────────────────────────────────
for arq in (BET, PEP, DIC):
    p = os.path.join(RAIZ, arq)
    bkp = p + '.antes-do-conserto'
    if not os.path.exists(bkp):
        shutil.copy2(p, bkp)
        print('backup: %s' % os.path.relpath(bkp, RAIZ).replace('\\', '/'))
    io.open(p, 'w', encoding='utf-8', newline='').write(novo_conteudo[arq])
    print('gravado: %s' % arq)

print('\npronto. Agora rodar: python _traduzir-serie.py --apply')

# -*- coding: utf-8 -*-
"""
_consertar-rodape.py — tira o conteudo de tras da barra de legenda.

A barra `.ncap` do player-video-longo-7-legumes.html cobre y = 647 ate 720.
5 cenas (37 a 41) tinham 8 elementos desenhados nessa faixa.

Sobe cada bloco afetado, mantendo o espacamento interno. Nao mexe em mais nada.
Cada troca e verificada: se a ancora nao casar EXATAMENTE 1 vez, aborta sem gravar.

Uso:
    python _consertar-rodape.py            # dry-run
    python _consertar-rodape.py --apply    # grava
"""
import io
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(RAIZ, 'video-longo', 'player-video-longo-7-legumes.html')
BACKUP = ARQ + '.antes-do-rodape'

# (rotulo, antigo, novo)  — cada 'antigo' tem de aparecer 1 vez so
TROCAS = [
    # cena 37 — alho no mel. titulo 626->604, sublegenda 656->632
    ('cena 37 (mel)',
     '<text x="202" y="626" text-anchor="middle" font-size="21" font-weight="900" fill="#3d3222" font-family="system-ui">MEL ATÉ O TOPO</text><text x="202" y="656" text-anchor="middle" font-size="12" font-weight="600" fill="#b8862b" font-family="system-ui">Cubra cada dente com 2 cm de mel</text>',
     '<text x="202" y="604" text-anchor="middle" font-size="21" font-weight="900" fill="#3d3222" font-family="system-ui">MEL ATÉ O TOPO</text><text x="202" y="632" text-anchor="middle" font-size="12" font-weight="600" fill="#b8862b" font-family="system-ui">Cubra cada dente com 2 cm de mel</text>'),

    # cena 38 — virar o pote. card 576+80 -> 568+64; textos 604/628/646 -> 590/608/624
    ('cena 38 (virar)',
     '<rect x="40" y="576" width="325" height="80" rx="14" fill="#fdf6e4" stroke="#e8d29a" stroke-width="2"/><text x="202" y="604" text-anchor="middle" font-size="13" font-weight="900" fill="#9a6a12" font-family="system-ui" letter-spacing="1.2">POR QUE VIRAR?</text><text x="202" y="628" text-anchor="middle" font-size="11.5" font-weight="600" fill="#6d5416" font-family="system-ui">O mel é pesado e desce. Virando,</text><text x="202" y="646" text-anchor="middle" font-size="11.5" font-weight="600" fill="#6d5416" font-family="system-ui">todo dente fica coberto.</text>',
     '<rect x="40" y="568" width="325" height="64" rx="14" fill="#fdf6e4" stroke="#e8d29a" stroke-width="2"/><text x="202" y="590" text-anchor="middle" font-size="13" font-weight="900" fill="#9a6a12" font-family="system-ui" letter-spacing="1.2">POR QUE VIRAR?</text><text x="202" y="608" text-anchor="middle" font-size="11.5" font-weight="600" fill="#6d5416" font-family="system-ui">O mel é pesado e desce. Virando,</text><text x="202" y="624" text-anchor="middle" font-size="11.5" font-weight="600" fill="#6d5416" font-family="system-ui">todo dente fica coberto.</text>'),

    # cena 39 — por dentro. titulo 578->548; card 648+52 -> 560+66; textos 668/688 -> 588/608
    # atencao: o 2o texto usa font-size="11" (nao 11.5)
    ('cena 39 (por dentro)',
     '<text x="202" y="578" text-anchor="middle" font-size="17" font-weight="900" fill="#3d3222" font-family="system-ui">O ALHO FICA ÂMBAR E MACIO</text><rect x="40" y="648" width="325" height="52" rx="12" fill="#fdf0e2" stroke="#f0c9a0" stroke-width="2"/><text x="202" y="668" text-anchor="middle" font-size="12" font-weight="900" fill="#c2551f" font-family="system-ui">Se ficar AZUL ou VERDE: ainda é seguro.</text><text x="202" y="688" text-anchor="middle" font-size="11" font-weight="600" fill="#7a4a26" font-family="system-ui">É reação natural, não é mofo.</text>',
     '<text x="202" y="548" text-anchor="middle" font-size="17" font-weight="900" fill="#3d3222" font-family="system-ui">O ALHO FICA ÂMBAR E MACIO</text><rect x="40" y="560" width="325" height="66" rx="12" fill="#fdf0e2" stroke="#f0c9a0" stroke-width="2"/><text x="202" y="588" text-anchor="middle" font-size="12" font-weight="900" fill="#c2551f" font-family="system-ui">Se ficar AZUL ou VERDE: ainda é seguro.</text><text x="202" y="608" text-anchor="middle" font-size="11" font-weight="600" fill="#7a4a26" font-family="system-ui">É reação natural, não é mofo.</text>'),

    # cena 40 — tempo. so o texto solto do fim: 692 -> 628
    ('cena 40 (tempo)',
     '<text x="202" y="692" text-anchor="middle" font-size="12.5" font-weight="800" fill="#b8862b" font-family="system-ui">Abra o pote todo dia pra soltar o gás</text>',
     '<text x="202" y="628" text-anchor="middle" font-size="12.5" font-weight="800" fill="#b8862b" font-family="system-ui">Abra o pote todo dia pra soltar o gás</text>'),

    # cena 41 — usar. titulo 576->540; card 622+56 -> 556+56; textos 646/666 -> 578/598
    # atencao: o 2o texto usa font-size="11" (nao 11.5)
    ('cena 41 (usar)',
     '<text x="202" y="576" text-anchor="middle" font-size="16" font-weight="900" fill="#3d3222" font-family="system-ui">E VOCÊ AINDA GANHA MEL DE ALHO</text><rect x="40" y="622" width="325" height="56" rx="13" fill="#f3ece0" stroke="#ddd0b8" stroke-width="2"/><text x="202" y="646" text-anchor="middle" font-size="12.5" font-weight="900" fill="#3d3222" font-family="system-ui">Qual eu fermento depois desse?</text><text x="202" y="666" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">Escreve nos comentários</text>',
     '<text x="202" y="540" text-anchor="middle" font-size="16" font-weight="900" fill="#3d3222" font-family="system-ui">E VOCÊ AINDA GANHA MEL DE ALHO</text><rect x="40" y="556" width="325" height="56" rx="13" fill="#f3ece0" stroke="#ddd0b8" stroke-width="2"/><text x="202" y="578" text-anchor="middle" font-size="12.5" font-weight="900" fill="#3d3222" font-family="system-ui">Qual eu fermento depois desse?</text><text x="202" y="598" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">Escreve nos comentários</text>'),
]

aplicar = '--apply' in sys.argv

txt = io.open(ARQ, encoding='utf-8').read()
antes = txt

falhas = []
for rotulo, velho, novo in TROCAS:
    n = txt.count(velho)
    if n != 1:
        falhas.append('%s: ancora casou %d vez(es), esperado 1' % (rotulo, n))
    else:
        txt = txt.replace(velho, novo)
        print('  ok  %s' % rotulo)

if falhas:
    print()
    for f in falhas:
        print('  ERRO  %s' % f)
    print()
    print('ABORTADO — nada foi gravado.')
    sys.exit(1)

# sanidade: nao pode ter sobrado <text> com y >= 640
sobra = [m.group(0) for m in re.finditer(r'<text[^>]*\by="(6[4-9]\d|7\d\d)"', txt)]
print()
if sobra:
    print('AVISO — ainda ha %d <text> com y>=640:' % len(sobra))
    for s in sobra[:10]:
        print('   %s' % s[:90])
else:
    print('nenhum <text> com y>=640 restante.')

print()
print('linhas: %d -> %d' % (antes.count('\n'), txt.count('\n')))

if aplicar:
    shutil.copyfile(ARQ, BACKUP)
    io.open(ARQ, 'w', encoding='utf-8', newline='').write(txt)
    print('GRAVADO. backup: %s' % os.path.basename(BACKUP))
else:
    print('DRY-RUN — nada gravado. Rode com --apply para gravar.')

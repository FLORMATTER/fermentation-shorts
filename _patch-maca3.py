# -*- coding: utf-8 -*-
"""
_patch-maca3.py — os defeitos que o RENDER mostrou no #27.

O que o `--final` e o `--no-anim` provaram (comparando os dois):
  ARtefato do --final (NAO e' defeito): as bolhas da cena 6 e os pontinhos verdes
  da cena 4 somem no `--final` porque `riseFast 1.4s` congela em 71,4%. No
  `--no-anim` os dois aparecem. Nao mexer.

  Defeito de verdade:
  1. CENA 1 — a faca cai EM CIMA da maca e cobre cabinho e folha; a lamina cinza
     lia como um TUBO. Vai para a direita, apontando para a maca.
  2. CENA 5 — os graos de sal sao brancos sobre a caixa verde-clara: INVISIVEIS.
     Escurecer (mesma licao do copo de acucar do #26).
  3. CENA 4 — vazia entre o circulo "2 DAYS" e a caixa de baixo. Entra uma BARRA
     DE TEMPO (0-2 silencio / 2-6 efervescendo), que informa e preenche.
  4. CENA 0 — a cenoura estava pequena demais ao lado da maca e do alho.
  5. CENA 3 — o jarro lia como um copo de liquido. Entram pedacos dentro.

Ancora com contagem esperada: ABORTA SEM GRAVAR se alguma nao casar.
"""
import io
import os
import sys

ALVO = '_criar-maca-alho-cenoura.py'

# ---- 1. a faca sai de cima da maca -----------------------------------------
FACA_ANTES = r'    <g transform="translate(322,334)">@FACA@</g>'
FACA_DEPOIS = r'    <g transform="translate(342,382) rotate(-12) scale(0.7)">@FACA@</g>'

# ---- 2. o sal escurece -----------------------------------------------------
# NAO usar r-string aqui: dentro de r-string o `\"` vira barra + aspas literal e
# a ancora nunca casa (o mesmo erro que ja' custou 2 rodadas neste arquivo).
SAL_ANTES = "' stroke=\"#c9bfa4\" stroke-width=\"1.2\"/>'"
SAL_DEPOIS = "' stroke=\"#8a7a5c\" stroke-width=\"1.6\"/>'"

# ---- 3. a barra de tempo da cena 5 ----------------------------------------
TEMPO_ANTES = '''    <g transform="translate(202,368)">
      <g style="animation:pulseBadge 2.2s ease-in-out infinite">
        <circle r="62" fill="#fff" stroke="@COR_CENOURA@" stroke-width="4"/>
        <text x="0" y="-4" text-anchor="middle" font-size="40" font-weight="800" fill="@COR_CENOURA_ESC@" font-family="system-ui">2</text>
        <text x="0" y="26" text-anchor="middle" font-size="14" font-weight="700" fill="#b98a5a" font-family="system-ui">DAYS</text>
      </g>
    </g>
    <g transform="translate(202,466)">
      <g style="animation:riseFast 1.4s ease-out infinite">
        <circle cx="-12" cy="0" r="5" fill="@COR_VERDE@" opacity=".8"/>
        <circle cx="14" cy="6" r="4" fill="@COR_VERDE@" opacity=".7"/>
      </g>
    </g>'''

TEMPO_DEPOIS = '''    <g transform="translate(202,330)">
      <g style="animation:pulseBadge 2.2s ease-in-out infinite">
        <circle r="58" fill="#fff" stroke="@COR_CENOURA@" stroke-width="4"/>
        <text x="0" y="-2" text-anchor="middle" font-size="38" font-weight="800" fill="@COR_CENOURA_ESC@" font-family="system-ui">2</text>
        <text x="0" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#b98a5a" font-family="system-ui">DAYS</text>
      </g>
    </g>
    <g transform="translate(202,444)">
      <rect x="-152" y="-20" width="304" height="40" rx="20" fill="#f2ecdd" stroke="#c9bfa4" stroke-width="2"/>
      <rect x="-150" y="-18" width="100" height="36" rx="18" fill="#e3d7bd"/>
      <rect x="-50" y="-18" width="200" height="36" rx="18" fill="#cfe6b8"/>
      <line x1="-50" y1="-27" x2="-50" y2="27" stroke="#8a7a5c" stroke-width="3"/>
      <text x="-100" y="6" text-anchor="middle" font-size="12" font-weight="800" fill="#8a7a5c" font-family="system-ui">SILENT</text>
      <text x="50" y="6" text-anchor="middle" font-size="12" font-weight="800" fill="#4e7a26" font-family="system-ui">FIZZING</text>
    </g>
    <g transform="translate(202,492)">
      <g style="animation:riseFast 1.4s ease-out infinite">
        <circle cx="-18" cy="0" r="5" fill="@COR_VERDE@" opacity=".85"/>
        <circle cx="8" cy="6" r="4" fill="@COR_VERDE@" opacity=".7"/>
        <circle cx="30" cy="-2" r="3.4" fill="@COR_VERDE@" opacity=".6"/>
      </g>
    </g>'''

# ---- 4. a cenoura cresce ---------------------------------------------------
CENOURA_ANTES = r"     .replace('@CENOURA@', cenoura(0, 0, 0.72))"
CENOURA_DEPOIS = r"     .replace('@CENOURA@', cenoura(0, 0, 0.95))"

# ---- 5. pedacos dentro do jarro da cena 4 ---------------------------------
JARRO_ANTES = '''    <g transform="translate(140,412)">
      <g style="animation:wobble 2.8s ease-in-out infinite">@JARRA@</g>
    </g>'''
JARRO_DEPOIS = '''    <g transform="translate(140,412)">
      <g style="animation:wobble 2.8s ease-in-out infinite">@JARRA@</g>
      <g transform="scale(0.72)">
        <rect x="-34" y="-44" width="28" height="19" rx="6" fill="@COR_MACA@" opacity=".9" transform="rotate(-16 -20 -34)"/>
        <rect x="8" y="-14" width="24" height="17" rx="6" fill="@COR_CENOURA@" opacity=".92" transform="rotate(13 20 -5)"/>
        <ellipse cx="-10" cy="34" rx="14" ry="11" fill="#fbf6ec" opacity=".95"/>
      </g>
    </g>'''

EDICOES = [
    (FACA_ANTES, FACA_DEPOIS, 1),
    (SAL_ANTES, SAL_DEPOIS, 3),
    (TEMPO_ANTES, TEMPO_DEPOIS, 1),
    (CENOURA_ANTES, CENOURA_DEPOIS, 1),
    (JARRO_ANTES, JARRO_DEPOIS, 1),
]


def main():
    if not os.path.exists(ALVO):
        print('ABORTA: nao achei %s' % ALVO)
        return 1
    with io.open(ALVO, encoding='utf-8', newline='') as f:
        d = f.read()
    antes = len(d.encode('utf-8'))

    for old, new, esperado in EDICOES:
        n = d.count(old)
        if n != esperado:
            print('ABORTA: ancora casou %d vez(es), esperava %d:' % (n, esperado))
            print('   %r' % old[:120])
            return 1
        d = d.replace(old, new, esperado)
        print('  ok  %d vez(es)  %s' % (n, old.split('\n')[0][:66]))

    # o token do sal continua sendo substituido?
    if '@SAL@' in d and ".replace('@SAL@'" not in d:
        print('ABORTA: @SAL@ sem replace')
        return 1

    compile(d, ALVO, 'exec')
    tmp = ALVO + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(d)
    os.replace(tmp, ALVO)
    print()
    print('gravado: %s  %d -> %d bytes' % (ALVO, antes, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

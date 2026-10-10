# -*- coding: utf-8 -*-
"""_criar-kombucha-beterraba-melancia.py — short KOMBUCHA DE BETERRABA + MELANCIA (EN).

    python _criar-kombucha-beterraba-melancia.py

🔴 TERCEIRO kombucha da serie (#23 = melancia + maca, #24 = maca + melao). A regra
e' "o formato pode repetir, a SUBSTANCIA nao". Entao NAO vale repetir:
  - #23: a garrafa pode estourar (pressao);
  - #24: o melao e' a unica fruta que nao e' acida (a linha 4,6).
E a beterraba ja' apareceu em #3/#4/#8/#14/#19/#25 — o assunto tem de ser novo.

O assunto AQUI: **a cor da beterraba tem uma JANELA de pH (3 a 6) — e a kombucha
termina exatamente dentro dela.**

Substancia (pesquisada, com fonte):
  - **betalaina (betanina) e' mais estavel entre pH 3 e 6** — "at low pH ranging
    from 3 to 6 was able to preserve the color" (Extraction, characterization and
    biochemical analysis of betacyanins from beetroot, 2021); fora dessa faixa
    (acima de 6 e abaixo de 3) o pigmento degrada — e' sensivel a **pH,
    temperatura, luz, oxigenio e agua** (review Springer, Betalain Recovery and
    Stability Assessment);
  - kombucha pronta (1a fermentacao): **pH 2,5 a 3,5** -> cai dentro da janela;
  - acucar (USDA): **beterraba 6,76 g / 100 g**, **melancia 6,2 g**, **melao
    cantalupo 7,86 g** — a beterraba ganha da MELANCIA mas PERDE do melao do
    #24. Comparar com o melao seria falso; o cartao diz "more than the watermelon";
  - **melancia: pH ~5,2 e ~92% agua** — dilui, nao acidifica;
  - **betalaina NAO e' indicador de pH como a antocianina** (a do repolho roxo):
    dentro de 3-6 a cor fica estavel, ela nao "vira azul". O que ela faz e'
    DESBOTAR (marrom/tijolo) quando passa da janela. E' por isso que o video diz
    "cor viva = dentro; tijolo = passou" — e nao "muda de cor com o pH";
  - a 2a fermentacao tambem gera **um pouco de alcool** (a mesma ressalva do #4).

Paleta: magenta da beterraba + rosa/verde da melancia sobre creme rosado —
diferente do laranja/verde do #24 e do vermelho/rosa do #23.

O QUE O RENDER ENSINOU (e ja' esta' aqui):
  - a JANELA pintada na barra e' um `<rect>` de cantos RETOS: so' serve porque a
    faixa 3-6 nao encosta nas pontas arredondadas da barra. Se encostasse, teria
    de ser PATH;
  - folha de beterraba com limbo LARGO e nervura (limbo fino le' como broto);
  - faca deitada/girada e com lamina larga (lamina estreita le' como termometro);
  - a barra de legenda do mp4 NAO pode repetir o titulo da cena (erro (k)) — o
    proprio gerador confere isso antes de gravar (`acha_repeticoes`).
"""
import io
import math
import os
import re
import sys

TEMPLATE = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'kombucha/shorts-beet-watermelon-en.html'

TAG = 'KOMBUCHA'

# ------------------------------------------------------------------- paleta
MAGENTA = '#b32d63'
MAGENTA_ESC = '#7b1440'
MAGENTA_CLARO = '#e58aae'
MELANCIA = '#e8556d'
MELANCIA_ESC = '#b83148'
VERDE = '#7fb542'
VERDE_ESC = '#4e7a26'
CREME = '#fdf1f4'
AMBAR = '#d9a441'
TEAL = '#1d9e75'
FUNDO = '#fdf6f8'


# ------------------------------------------------------------- beterraba
def beterraba(x, y, s=1.0):
    """Beterraba inteira: bulbo roxo, RAIZ comprida embaixo, folhas em cima.

    A raiz (cauda) e' o que faz ler "beterraba" em vez de "bolota roxa", e as
    folhas dizem que e' raiz, nao fruta. O LIMBO tem de ser LARGO e com nervura:
    limbo fino le' como broto (1o render, no #25).
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M-6,-40 C-18,-62 -32,-74 -42,-82" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M0,-42 C1,-68 4,-82 6,-94" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M7,-40 C19,-60 32,-70 42,-76" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M-42,-82 C-68,-98 -94,-90 -90,-72'
            ' C-82,-54 -54,-60 -42,-82 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M-42,-82 C-62,-86 -78,-82 -86,-76" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            f'<path d="M6,-94 C16,-122 42,-124 46,-105'
            ' C40,-86 20,-80 6,-94 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M6,-94 C20,-107 34,-114 44,-108" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            f'<path d="M42,-76 C66,-86 88,-76 82,-60'
            ' C70,-46 50,-54 42,-76 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M42,-76 C60,-78 74,-72 80,-64" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            f'<path d="M0,-44 C32,-44 52,-20 51,8 C50,34 30,56 0,56'
            f' C-30,56 -50,34 -51,8 C-52,-20 -32,-44 0,-44 Z"'
            f' fill="{MAGENTA}" stroke="{MAGENTA_ESC}" stroke-width="3.5"/>'
            f'<path d="M0,54 C-1,72 -4,88 -10,102" stroke="{MAGENTA_ESC}"'
            ' stroke-width="4.5" fill="none" stroke-linecap="round"/>'
            f'<ellipse cy="-16" rx="36" ry="7" fill="none" stroke="{MAGENTA_CLARO}"'
            ' stroke-width="2.4" opacity=".75"/>'
            f'<ellipse cy="8" rx="30" ry="6" fill="none" stroke="{MAGENTA_CLARO}"'
            ' stroke-width="2.4" opacity=".65"/>'
            f'<ellipse cy="30" rx="18" ry="4.5" fill="none" stroke="{MAGENTA_CLARO}"'
            ' stroke-width="2.4" opacity=".55"/>'
            '<ellipse cx="-20" cy="-16" rx="10" ry="18" fill="#fff" opacity=".2"/>'
            '</g>')


def beterraba_fatia(x, y, s=1.0, cor=None):
    """Fatia de frente: casca escura + aneis concentricos.

    `cor` da' a versao DESBOTADA (tijolo) — e' o contraste da cena 4.
    """
    c = cor or MAGENTA
    cl = MAGENTA_CLARO if cor is None else '#e0d0c8'
    ce = MAGENTA_ESC if cor is None else '#a89488'
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<circle r="40" fill="{c}" stroke="{ce}" stroke-width="3"/>'
            f'<circle r="32" fill="none" stroke="{cl}" stroke-width="2.4" opacity=".8"/>'
            f'<circle r="23" fill="none" stroke="{cl}" stroke-width="2.4" opacity=".65"/>'
            f'<circle r="13" fill="none" stroke="{cl}" stroke-width="2.2" opacity=".5"/>'
            '<ellipse cx="-13" cy="-13" rx="8" ry="12" fill="#fff" opacity=".16"/>'
            '</g>')


def melancia(x, y, s=1.0):
    """Fatia semicircular: casca verde, faixa branca, polpa rosa, sementes."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M-86,0 A86,86 0 0 1 86,0 Z" fill="{VERDE}" stroke="{VERDE_ESC}"'
            ' stroke-width="3"/>'
            '<path d="M-76,0 A76,76 0 0 1 76,0 Z" fill="#f4f7e8"/>'
            f'<path d="M-68,0 A68,68 0 0 1 68,0 Z" fill="{MELANCIA}"/>'
            '<ellipse cx="-30" cy="-30" rx="4" ry="6" fill="#3a2b2b"/>'
            '<ellipse cx="6" cy="-40" rx="4" ry="6" fill="#3a2b2b"/>'
            '<ellipse cx="38" cy="-20" rx="4" ry="6" fill="#3a2b2b"/>'
            '<ellipse cx="-10" cy="-16" rx="4" ry="6" fill="#3a2b2b"/>'
            '</g>')


# ------------------------------------------------------------------ vasilhame
def jarra(liquido, s=1.0):
    """Jarro alto com liquido — mais alto que largo (a licao da silhueta)."""
    return (f'<g transform="scale({s:g})">'
            '<path d="M-62,-104 L-62,84 Q-62,104 -42,104 L42,104 Q62,104 62,84'
            ' L62,-104 Z" fill="#fdf6ea" stroke="#8a6a2f" stroke-width="4"/>'
            f'<path d="M-54,-72 L-54,80 Q-54,96 -38,96 L38,96 Q54,96 54,80 L54,-72 Z"'
            f' fill="{liquido}"/>'
            '<ellipse cx="-38" cy="-10" rx="7" ry="46" fill="#fff" opacity=".28"/>'
            '</g>')


def garrafa(liquido, s=1.0, tampa=True):
    """Garrafa de boca larga — mais ALTA que larga."""
    t = ''
    if tampa:
        t = ('<rect x="-19" y="-140" width="38" height="16" rx="5"'
             ' fill="#cfd8c4" stroke="#8a6a2f" stroke-width="3"/>'
             '<line x1="0" y1="-140" x2="0" y2="-124" stroke="#8a6a2f"'
             ' stroke-width="2"/>')
    return (f'<g transform="scale({s:g})">'
            '<path d="M-40,-56 L-40,70 Q-40,88 -22,88 L22,88 Q40,88 40,70 L40,-56'
            ' Q40,-70 26,-80 L14,-92 L14,-124 L-14,-124 L-14,-92 L-26,-80'
            ' Q-40,-70 -40,-56 Z" fill="#fdf6ea" stroke="#8a6a2f"'
            ' stroke-width="4"/>'
            f'<path d="M-34,-28 L-34,66 Q-34,82 -20,82 L20,82 Q34,82 34,66 L34,-28'
            f' Q34,-42 22,-52 L12,-62 L12,-118 L-12,-118 L-12,-62 L-22,-52'
            f' Q-34,-42 -34,-28 Z" fill="{liquido}"/>'
            '<ellipse cx="-19" cy="18" rx="7" ry="42" fill="#fff" opacity=".22"/>'
            + t + '</g>')


def bolhas():
    """Dois grupos de borbulha subindo (o `riseFast` da serie)."""
    return ('<g style="animation:riseFast 1.4s ease-out infinite">'
            '<circle cx="-10" cy="52" r="4" fill="#fff" opacity=".8"/>'
            '<circle cx="14" cy="62" r="3.2" fill="#fff" opacity=".75"/>'
            '</g>'
            '<g style="animation:riseFast 1.4s ease-out .5s infinite">'
            '<circle cx="2" cy="44" r="3.6" fill="#fff" opacity=".7"/>'
            '<circle cx="-24" cy="58" r="3" fill="#fff" opacity=".65"/>'
            '</g>')


def faca(x, y, rot=0):
    """Faca de cozinha: lamina LARGA, com bolster e cabo de rebites.

    Lamina estreita le' como TERMOMETRO (o que o render do #25 mostrou).
    """
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g})">'
            '<g style="animation:chop2x 1.7s ease-in-out infinite">'
            '<path d="M-92,-13 L22,-13 L22,13 L-62,13 Q-92,13 -92,-1 Z"'
            ' fill="#cdd6dc" stroke="#7a8a92" stroke-width="2.5"'
            ' stroke-linejoin="round"/>'
            '<path d="M-88,-9 L20,-9 L20,-2 L-88,-2 Z" fill="#eef3f6"/>'
            '<rect x="22" y="-15" width="9" height="30" rx="3" fill="#9aa8b0"'
            ' stroke="#6f7d85" stroke-width="2"/>'
            '<rect x="31" y="-12" width="46" height="24" rx="8" fill="#8a5a34"'
            ' stroke="#5e3a1f" stroke-width="2.5"/>'
            '<circle cx="44" cy="0" r="2.6" fill="#5e3a1f"/>'
            '<circle cx="62" cy="0" r="2.6" fill="#5e3a1f"/>'
            '</g></g>')


def gota(x, y, s=1.0, cor=MELANCIA):
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M0,-15 Q7,-5 7,2 Q7,9 0,9 Q-7,9 -7,2 Q-7,-5 0,-15 Z"'
            f' fill="{cor}" stroke="{MELANCIA_ESC}" stroke-width="2"/></g>')


def sol_riscado(x, y, s=1.0):
    """Sol com um X por cima — "nada de luz". Raios calculados em `math`."""
    p = []
    for k in range(8):
        a = math.radians(45 * k)
        p.append(f'<line x1="{math.cos(a) * 22:g}" y1="{math.sin(a) * 22:g}"'
                 f' x2="{math.cos(a) * 34:g}" y2="{math.sin(a) * 34:g}"'
                 ' stroke="#d9a441" stroke-width="4" stroke-linecap="round"/>')
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<circle r="16" fill="#f7d774" stroke="#d9a441" stroke-width="3"/>'
            + ''.join(p) +
            '<line x1="-30" y1="-30" x2="30" y2="30" stroke="#c0392b"'
            ' stroke-width="6" stroke-linecap="round"/>'
            '<line x1="30" y1="-30" x2="-30" y2="30" stroke="#c0392b"'
            ' stroke-width="6" stroke-linecap="round"/>'
            '</g>')


# --------------------------------------------------------------- escalas de pH
def _px(v, w):
    return -w / 2 + (v - 2) / 5.0 * w


def escala_ph_janela(x, y, w=312, h=34, de=3.0, ate=6.0, marcas=()):
    """Barra de pH de 2 a 7 com a JANELA [de, ate] sombreada.

    A faixa e' um `<rect>` de cantos RETOS: funciona porque 3 e 6 nao encostam
    nas pontas arredondadas da barra. Se encostassem, teria de ser PATH — dois
    `<rect rx>` lado a lado deixam uma emenda redonda no meio.
    """
    r = h / 2.0
    xa, xb = _px(de, w), _px(ate, w)
    p = [f'<rect x="{-w / 2:g}" y="{-r:g}" width="{w:g}" height="{h:g}" rx="{r:g}"'
         ' fill="#f7ecf1"/>',
         f'<rect x="{xa:g}" y="{-r:g}" width="{xb - xa:g}" height="{h:g}"'
         f' fill="{MAGENTA_CLARO}" opacity=".55"/>',
         f'<rect x="{-w / 2:g}" y="{-r:g}" width="{w:g}" height="{h:g}" rx="{r:g}"'
         ' fill="none" stroke="#c9bda8" stroke-width="2.5"/>']
    for v in (de, ate):
        p.append(f'<line x1="{_px(v, w):g}" y1="{-r - 8:g}" x2="{_px(v, w):g}"'
                 f' y2="{r + 8:g}" stroke="{MAGENTA_ESC}" stroke-width="2.5"/>')
        p.append(f'<text x="{_px(v, w):g}" y="{-r - 15:g}" text-anchor="middle"'
                 f' font-size="14" font-weight="800" fill="{MAGENTA_ESC}"'
                 f' font-family="system-ui">{v:g}</text>')
    for ph, cor, rotulo in marcas:
        p.append(f'<circle cx="{_px(ph, w):g}" cy="0" r="9" fill="{cor}"'
                 ' stroke="#fff" stroke-width="2.5"/>')
        p.append(f'<text x="{_px(ph, w):g}" y="{r + 25:g}" text-anchor="middle"'
                 f' font-size="13" font-weight="800" fill="{cor}"'
                 f' font-family="system-ui">{rotulo}</text>')
    return f'<g transform="translate({x:g},{y:g})">' + ''.join(p) + '</g>'


def escala_ph_vertical_janela(x, y, h=300, w=30, de=3.0, ate=6.0):
    """A mesma janela em pe' — e' o gancho: a kombucha cai DENTRO da faixa."""
    def py(v):
        return h / 2 - (v - 2) / 5.0 * h

    ya, yb = py(ate), py(de)
    return (f'<g transform="translate({x:g},{y:g})">'
            f'<rect x="{-w / 2:g}" y="{-h / 2:g}" width="{w:g}" height="{h:g}"'
            f' rx="{w / 2:g}" fill="#f7ecf1" stroke="#c9bda8" stroke-width="2.5"/>'
            f'<rect x="{-w / 2:g}" y="{ya:g}" width="{w:g}" height="{yb - ya:g}"'
            f' fill="{MAGENTA_CLARO}" opacity=".6"/>'
            f'<line x1="{-w / 2 - 18:g}" y1="{ya:g}" x2="{w / 2 + 18:g}" y2="{ya:g}"'
            f' stroke="{MAGENTA_ESC}" stroke-width="2.5"/>'
            f'<line x1="{-w / 2 - 18:g}" y1="{yb:g}" x2="{w / 2 + 18:g}" y2="{yb:g}"'
            f' stroke="{MAGENTA_ESC}" stroke-width="2.5"/>'
            f'<text x="{-w / 2 - 24:g}" y="{ya + 5:g}" text-anchor="end"'
            f' font-size="14" font-weight="800" fill="{MAGENTA_ESC}"'
            ' font-family="system-ui">6</text>'
            f'<text x="{-w / 2 - 24:g}" y="{yb + 5:g}" text-anchor="end"'
            f' font-size="14" font-weight="800" fill="{MAGENTA_ESC}"'
            ' font-family="system-ui">3</text>'
            f'<circle cx="0" cy="{py(3.0):g}" r="10" fill="{TEAL}" stroke="#fff"'
            ' stroke-width="2.5"/>'
            f'<text x="{w / 2 + 22:g}" y="{py(3.0) + 5:g}" font-size="13"'
            f' font-weight="800" fill="{TEAL}" font-family="system-ui">3.0</text>'
            f'<text x="0" y="{h / 2 + 24:g}" text-anchor="middle" font-size="13"'
            ' font-weight="800" fill="#a08a5c" font-family="system-ui">2</text>'
            f'<text x="0" y="{-h / 2 - 12:g}" text-anchor="middle" font-size="13"'
            ' font-weight="800" fill="#a08a5c" font-family="system-ui">7</text>'
            '</g>')


# --------------------------------------------------- cena 1: o gancho (a janela)
def s0(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <circle cx="256" cy="300" r="150" fill="@CREME@" opacity=".85"/>
    @ESCALA@
    <g transform="translate(252,404)">
      <g style="animation:wobble 2.8s ease-in-out infinite">
        @JARRA@
      </g>
    </g>
    <g transform="translate(252,404)">@BOLHAS@</g>
    <g transform="translate(214,168)">
      <g style="animation:pulseBadge 2.2s ease-in-out infinite">
        <rect x="-62" y="-19" width="124" height="38" rx="19" fill="@MAGENTA@" stroke="#fff" stroke-width="3"/>
        <text x="0" y="7" text-anchor="middle" font-size="17" font-weight="800" fill="#fff" font-family="system-ui">pH 3 - 6</text>
      </g>
    </g>
    <g transform="translate(202,568)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@MAGENTA@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">RED BETWEEN 3 AND 6</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">outside that window the pigment breaks down</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@CREME@', CREME) \
     .replace('@MAGENTA@', MAGENTA).replace('@MAGENTA_ESC@', MAGENTA_ESC) \
     .replace('@ESCALA@', escala_ph_vertical_janela(84, 300)) \
     .replace('@JARRA@', jarra(MAGENTA, 0.78)) \
     .replace('@BOLHAS@', bolhas())


# --------------------------------------------- cena 2: a kombucha cai na janela
def s1(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <g transform="translate(202,196)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@TEAL@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#0f6e56" font-family="system-ui">THE JAR MATCHES THE WINDOW</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#4a8a6e" font-family="system-ui">the first ferment ends inside the safe band</text>
    </g>
    @ESCALA@
    <g transform="translate(202,450)">
      <g style="animation:wobble 2.6s ease-in-out infinite">@GARRAFA@</g>
    </g>
    <g transform="translate(202,420)">@BOLHAS@</g>
    <g transform="translate(202,556)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#eaf7f1" stroke="@TEAL@" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="#0f6e56" font-family="system-ui">2.5 TO 3.5 IS WHERE IT STOPS</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#4a8a6e" font-family="system-ui">the pigment holds inside the band</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@TEAL@', TEAL) \
     .replace('@ESCALA@', escala_ph_janela(
         202, 300, 312, 34, 3.0, 6.0,
         [(3.0, TEAL, 'KOMBUCHA'), (5.2, MELANCIA_ESC, 'WATERMELON')])) \
     .replace('@GARRAFA@', garrafa(MAGENTA, 0.55)) \
     .replace('@BOLHAS@', bolhas())


# ------------------------------------------------ cena 3: a melancia e' agua
def s2(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <circle cx="188" cy="286" r="136" fill="@CREME@" opacity=".8"/>
    <g transform="translate(188,318)">
      <g style="animation:wobble 2.9s ease-in-out infinite">@MELANCIA@</g>
    </g>
    <g transform="translate(322,340)">@FACA@</g>
    @GOTAS@
    <g transform="translate(202,556)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@MELANCIA_ESC@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@MELANCIA_ESC@" font-family="system-ui">MOSTLY WATER</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#c07a8a" font-family="system-ui">pH 5.2 and 92% water - it dilutes, not acidifies</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@CREME@', CREME) \
     .replace('@MELANCIA_ESC@', MELANCIA_ESC).replace('@MELANCIA@', melancia(0, 0, 1.0)) \
     .replace('@FACA@', faca(0, 0, 35)) \
     .replace('@GOTAS@', '\n    '.join([
         gota(152, 348, 1.0), gota(192, 364, 1.25), gota(230, 346, 0.85)]))


# --------------------------------------------- cena 4: a beterraba e' o combustivel
def s3(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <circle cx="202" cy="292" r="140" fill="@CREME@" opacity=".8"/>
    <g transform="translate(202,292)">
      <g style="animation:wobble 3.0s ease-in-out infinite">@BETERRABA@</g>
    </g>
    <g transform="translate(202,130)">
      <g style="animation:pour2x 1.6s ease-out infinite">
        <g transform="rotate(28) scale(.88)">
          <path d="M-30,-32 L30,-32 L23,26 Q0,38 -23,26 Z" fill="#f2ead6" stroke="#a8935f" stroke-width="3.5"/>
          <text x="0" y="6" text-anchor="middle" font-size="15" font-weight="800" fill="#6b5a3a" font-family="system-ui">SUGAR</text>
        </g>
      </g>
    </g>
    @GRAOS@
    <g transform="translate(202,468)">
      <rect x="-160" y="-34" width="320" height="68" rx="12" fill="#fff" stroke="@MAGENTA@" stroke-width="3"/>
      <text x="0" y="-2" text-anchor="middle" font-size="17" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">FUEL AND COLOUR AT ONCE</text>
      <text x="0" y="22" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">7 g of sugar per 100 g - more than the watermelon</text>
    </g>
    <g transform="translate(202,588)">
      <rect x="-176" y="-38" width="352" height="76" rx="12" fill="#fdf0f5" stroke="@MAGENTA_CLARO@" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="15" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">SUGAR FEEDS THE SECOND FERMENT</text>
      <text x="0" y="19" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">and the pigment comes along for free</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@CREME@', CREME) \
     .replace('@MAGENTA@', MAGENTA).replace('@MAGENTA_ESC@', MAGENTA_ESC) \
     .replace('@MAGENTA_CLARO@', MAGENTA_CLARO).replace('@BETERRABA@', beterraba(0, 0, 1.0)) \
     .replace('@GRAOS@', '\n    '.join(
         '<circle cx="%d" cy="%d" r="%s" fill="#ffffff" stroke="#a8935f"'
         ' stroke-width="1.8"/>' % (x, y, r)
         for x, y, r in ((184, 196, 3.4), (204, 208, 2.8), (194, 224, 3.2),
                         (212, 190, 2.6), (178, 212, 2.4))))


# --------------------------------------------------- cena 5: leia o jarro
def s4(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <g transform="translate(202,116)">
      <text x="0" y="0" text-anchor="middle" font-size="17" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">SAME JUICE, TWO STATES</text>
    </g>
    <g transform="translate(118,268)">
      <g style="animation:wobble 2.8s ease-in-out infinite">@FATIA_BOA@</g>
    </g>
    <g transform="translate(290,268)">
      <g style="animation:wobble 3.1s ease-in-out infinite">@FATIA_RUIM@</g>
    </g>
    <g transform="translate(118,344)">
      <g style="animation:tick 2.2s ease-in-out infinite">
        <path d="M-14,-8 L-3,4 L15,-16" stroke="@VERDE_ESC@" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </g>
    <g transform="translate(290,344)">
      <path d="M-13,-13 L13,13 M13,-13 L-13,13" stroke="#c0392b" stroke-width="6" stroke-linecap="round"/>
    </g>
    <g transform="translate(118,424)">
      <rect x="-72" y="-26" width="144" height="52" rx="10" fill="#fdf0f5" stroke="@MAGENTA@" stroke-width="2.5"/>
      <text x="0" y="7" text-anchor="middle" font-size="19" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">MAGENTA</text>
    </g>
    <g transform="translate(290,424)">
      <rect x="-72" y="-26" width="144" height="52" rx="10" fill="#f2ece6" stroke="#a89488" stroke-width="2.5"/>
      <text x="0" y="7" text-anchor="middle" font-size="19" font-weight="800" fill="#7d6a5c" font-family="system-ui">BRICK</text>
    </g>
    <g transform="translate(202,548)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@MAGENTA@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">THE JAR IS THE STATUS LIGHT</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">vivid means in, brick means you went past</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@MAGENTA@', MAGENTA) \
     .replace('@MAGENTA_ESC@', MAGENTA_ESC).replace('@VERDE_ESC@', VERDE_ESC) \
     .replace('@FATIA_BOA@', beterraba_fatia(0, 0, 1.05)) \
     .replace('@FATIA_RUIM@', beterraba_fatia(0, 0, 1.05, cor='#b07a68'))


# ---------------------------------------------------- cena 6: longe da luz
def s5(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <rect x="66" y="118" width="272" height="292" rx="18" fill="#2b2233"/>
    <rect x="86" y="138" width="232" height="252" rx="12" fill="#3a2f45"/>
    <g transform="translate(202,290)">
      <g style="animation:wobble 3.2s ease-in-out infinite">@GARRAFA@</g>
    </g>
    <g transform="translate(202,290)">@BOLHAS@</g>
    <g transform="translate(322,164)">@SOL@</g>
    <g transform="translate(202,468)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@MAGENTA@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">NO SUN, NO HEAT</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">light and warmth break the pigment</text>
    </g>
    <g transform="translate(202,580)">
      <rect x="-172" y="-38" width="344" height="76" rx="12" fill="#fdf0f5" stroke="@MAGENTA_CLARO@" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="15" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">A CUPBOARD, NOT A WINDOWSILL</text>
      <text x="0" y="19" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">the colour fades in daylight</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@MAGENTA@', MAGENTA) \
     .replace('@MAGENTA_ESC@', MAGENTA_ESC).replace('@MAGENTA_CLARO@', MAGENTA_CLARO) \
     .replace('@GARRAFA@', garrafa(MAGENTA, 0.72)) \
     .replace('@BOLHAS@', bolhas()).replace('@SOL@', sol_riscado(0, 0, 1.15))


# ------------------------------------------------------- cena 7: o alcool
def s6(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <circle cx="202" cy="250" r="136" fill="@CREME@" opacity=".8"/>
    <g transform="translate(202,250)">
      <g style="animation:wobble 2.7s ease-in-out infinite">@GARRAFA@</g>
    </g>
    <g transform="translate(202,250)">@BOLHAS@</g>
    <g transform="translate(202,412)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@AMBAR@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#8a6a2f" font-family="system-ui">DRINK IT FRESH</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">the longer it sits, the more alcohol it makes</text>
    </g>
    <g transform="translate(202,508)">
      <rect x="-172" y="-40" width="344" height="80" rx="12" fill="#fff8e6" stroke="@AMBAR@" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="15" font-weight="800" fill="#8a6a2f" font-family="system-ui">THREE DAYS, THEN THE FRIDGE</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">cold slows it down and holds the colour</text>
    </g>
    <g transform="translate(202,604)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#0f6e56" font-family="system-ui">which one should I ferment next?</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@CREME@', CREME) \
     .replace('@AMBAR@', AMBAR).replace('@GARRAFA@', garrafa(MAGENTA, 0.78)) \
     .replace('@BOLHAS@', bolhas())


# ---------------------------------------------------------------- montagem
TEXTOS = {
    'titulo': 'Shorts animado — Beetroot and watermelon kombucha (2nd ferment)',
    'badge': '🟣 + 🍉',
    'capdiv': ('Beetroot and watermelon kombucha'
               '<small>the colour tells you where you are</small>'),
    'cenas': [
        ('s0', 6400, '%s 1 / 7' % TAG, 'The colour has a window',
         'beetroot only holds its red between pH 3 and 6', MAGENTA_ESC),
        ('s1', 6400, '%s 2 / 7' % TAG, 'And kombucha lands inside it',
         'the first ferment ends at pH 2.5 to 3.5', TEAL),
        ('s2', 6200, '%s 3 / 7' % TAG, 'Watermelon is water with sugar',
         'pH 5.2 and 92% water - it dilutes', MELANCIA_ESC),
        ('s3', 6400, '%s 4 / 7' % TAG, 'The beetroot is the fuel',
         '7 g of sugar per 100 g, and the pigment', MAGENTA),
        ('s4', 6400, '%s 5 / 7' % TAG, 'Read the jar, not the clock',
         'vivid magenta is in, dull brick is past', '#7d6a5c'),
        ('s5', 6200, '%s 6 / 7' % TAG, 'Keep it in the dark',
         'light and heat break the pigment', '#3a2f45'),
        ('s6', 6400, '%s 7 / 7' % TAG, 'It makes a little alcohol',
         'the longer it sits, the more it makes', '#8a6a2f'),
    ],
}


def cena(cid, corpo, primeira=False):
    cls = 'scene on' if primeira else 'scene'
    return ('  <svg class="%s" id="%s" viewBox="0 0 405 720" '
            'xmlns="http://www.w3.org/2000/svg">\n' % (cls, cid)) + corpo + '\n  </svg>'


def monta_cenas(t):
    return {cid: cena(cid, fn(t), primeira=(cid == 's0'))
            for cid, fn in (('s0', s0), ('s1', s1), ('s2', s2), ('s3', s3),
                            ('s4', s4), ('s5', s5), ('s6', s6))}


def monta_array(cenas):
    linhas = ['const scenes = [']
    for i, (cid, ms, tag, cap, sub, cor) in enumerate(cenas):
        fim = '' if i == len(cenas) - 1 else ','
        linhas.append("  { id:'%s', ms:%d, tag:'%s', cap:'%s', sub:'%s', color:'%s' }%s"
                      % (cid, ms, tag, cap, sub, cor, fim))
    linhas.append('];')
    return '\n'.join(linhas)


def acha_cena(d, cid):
    return re.search(r'(?ms)^([ \t]*)<svg class="scene[^"]*"[^>]*id="%s".*?</svg>' % cid, d)


def acha_repeticoes(d, cenas):
    """O erro (k): a barra de legenda do mp4 repetindo o que ja' esta' na cena.

    Varre TODOS os `<text>` de cada cena e compara com o `cap` e o `sub` daquela
    cena. Nao selecionar "o titulo" por `font-size`: as cenas titulam com 15, 16,
    17 e 18 px — foi assim que a 1a versao deste verificador errou a conta.
    """
    achados = []
    for cid, ms, tag, cap, sub, cor in cenas:
        m = acha_cena(d, cid)
        if not m:
            continue
        textos = [x.strip().lower()
                  for x in re.findall(r'<text[^>]*>([^<]*)</text>', m.group(0))]
        for campo, valor in (('cap', cap), ('sub', sub)):
            if valor.strip().lower() in textos:
                achados.append('%s %s="%s"' % (cid, campo, valor))
    return achados


def main():
    with io.open(TEMPLATE, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    print('template : %s (%d bytes, %s)' % (TEMPLATE, len(d),
                                            'CRLF' if eol == '\r\n' else 'LF'))
    t = TEXTOS

    novo = monta_cenas(t)
    for cid in ('s0', 's1', 's2', 's3', 's4', 's5', 's6'):
        m = acha_cena(d, cid)
        if not m:
            print('ERRO: nao achei a cena %s' % cid)
            return 1
        indent = m.group(1)
        linhas = novo[cid].replace('\n', eol).split(eol)
        linhas[0] = indent + linhas[0]
        d = d[:m.start()] + eol.join(linhas) + d[m.end():]

    trocas = [
        ('<title>Shorts animado — Carrot with apple (fermented)</title>',
         '<title>%s</title>' % t['titulo']),
        ('>🥕 + APPLE</div>', '>%s</div>' % t['badge']),
        ('>SCENE 1 / 7</div>', '>%s</div>' % t['cenas'][0][2]),
        ('<div class="cap" id="cap">Carrot with apple<small>the sweet one - and it fizzes</small></div>',
         '<div class="cap" id="cap">%s</div>' % t['capdiv']),
    ]
    for velho, novo_txt in trocas:
        if d.count(velho) != 1:
            print('ERRO: ancora casou %d vez(es): %s' % (d.count(velho), velho[:60]))
            return 1
        d = d.replace(velho, novo_txt)

    m = re.search(r'const scenes = \[.*?\n\];', d, re.S)
    if not m:
        print('ERRO: nao achei `const scenes`')
        return 1
    d = d.replace(m.group(0), monta_array(t['cenas']).replace('\n', eol), 1)

    defs = set(re.findall(r'@keyframes\s+(\w+)', d))
    usados = set(re.findall(r'animation:\s*([\w-]+)', d))
    orfaos = defs - usados
    if orfaos:
        print('ERRO: keyframe nunca usado: %s' % sorted(orfaos))
        return 1

    rep = acha_repeticoes(d, t['cenas'])
    if rep:
        print('ERRO: a legenda do mp4 repete o texto da cena: %s' % rep)
        return 1

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with io.open(DESTINO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('%-46s %d bytes | %d cenas | keyframes %d/%d'
          % (DESTINO, len(d.encode('utf-8')), len(t['cenas']),
             len(usados & defs), len(defs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

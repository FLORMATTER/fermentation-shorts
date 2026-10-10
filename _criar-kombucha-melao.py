# -*- coding: utf-8 -*-
"""_criar-kombucha-melao.py — cria o short KOMBUCHA DE MACA + MELAO (EN).

    python _criar-kombucha-melao.py

🔴 CUIDADO: este e' o SEGUNDO kombucha da serie (o #23 foi melancia + maca). A
regra da serie e' "o formato pode repetir, a SUBSTANCIA nao" — repetir o assunto
do #23 ("a garrafa pode estourar") seria conteudo duplicado com verniz novo.

O assunto AQUI e' outro: **o melao e' a unica fruta da serie que NAO e' acida.**

Substancia (pesquisada, com fonte):
  - melao (cantalupo): **pH 6,0 - 6,7** (Engineering ToolBox, tabela de pH de
    alimentos). Acima de 4,6 = alimento de BAIXA ACIDEZ, onde patogenos crescem;
  - maca: **pH 2,9 - 3,3**. Mesmo acucar, quase **1.800x** mais acido (pH e' escala
    log: 10^3,25 ~ 1.800);
  - kombucha pronta (1a fermentacao): **pH 2,5 - 3,5**. E' ela que puxa o melao
    para baixo da linha;
  - **4,6** e' a linha: abaixo dela, os patogenos nao crescem;
  - a **casca rendada** do melao e' fator de risco conhecido (Salmonella, Listeria
    se agarram na rede) — a faca arrasta isso para a polpa. Lavar antes de cortar;
  - melao e' ~90% agua E nao tem acido: dilui a acidez, nao so' o sabor -> menos
    fruta que no caso da melancia.

Paleta: laranja do melao + verde da maca sobre creme quente. **Diferente do #23**,
que era vermelho/rosa de melancia.

O QUE O RENDER ENSINOU (1a versao, consertado aqui):
  - a escala de pH horizontal precisa de cantos arredondados SO' nas pontas: dois
    `<rect rx>` lado a lado criam uma emenda redonda no meio. Usar PATH;
  - a rede do melao inteiro tem de ser desenhada com cordas calculadas
    (`sqrt(R^2 - c^2)`), senao as linhas retas saem do circulo — ou seria preciso
    um `<clipPath>` com id, que e' risco de id duplicado.
"""
import io
import math
import os
import re
import sys

TEMPLATE = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'kombucha/shorts-apple-melon-en.html'

TAG = 'KOMBUCHA'
LARANJA = '#e07b2e'
LARANJA_ESC = '#b45c17'
CREME = '#fdf1e2'
VERDE = '#8cc152'
VERDE_ESC = '#4e7a26'
AMBAR = '#d9a441'
TEAL = '#1d9e75'


# ------------------------------------------------------------------ desenhos
def melao_metade(x, y, s=1.0):
    """Meio melao visto do CORTE: casca, casca palida, faixa branca, polpa.

    A CASCA tem de ser GROSSA e escura: casca fina faz o desenho ler como
    LARANJA (1o render). Ordem importa — cada circulo por cima do anterior.
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<circle r="78" fill="#8f9c53" stroke="#6f7c3d" stroke-width="3"/>'
            '<circle r="69" fill="#c3cd93"/>'
            '<circle r="62" fill="#ece6cc"/>'
            '<circle r="53" fill="#f0a24a"/>'
            '<circle r="53" fill="#f7bb72" opacity=".28"/>'
            '<ellipse rx="18" ry="12" fill="#f7dcb0"/>'
            '<ellipse cx="-6" cy="-3" rx="3.2" ry="4.6" fill="#d99a4a"/>'
            '<ellipse cx="6" cy="4" rx="3.2" ry="4.6" fill="#d99a4a"/>'
            '<ellipse cx="1" cy="-6" rx="3.2" ry="4.6" fill="#d99a4a"/>'
            '<ellipse cx="-3" cy="6" rx="3.2" ry="4.6" fill="#d99a4a"/>'
            '</g>')


def melao_inteiro(x, y, s=1.0):
    """Melao inteiro: casca BEGE, com SUTURAS e uma rede esparsa por cima.

    Grade simetrica le' como WAFFLE (2o render); bola lisa le' como bola. O que
    faz ler "melao" sao as LOMBADAS de cima a baixo (as suturas). Com elas, a
    rede pode ser ondulada e irregular — que e' como o cantalupo parece.
    """
    R = 76
    p = []
    for c, bojo in ((-44, 12), (-16, 14), (16, 14), (44, 12)):
        p.append(f'<path d="M{c},-64 C{c + bojo},-24 {c + bojo},24 {c},64"'
                 ' fill="none" stroke="#c0ab7d" stroke-width="2.4" opacity=".75"/>')
    for c, bojo in ((-56, 5), (-30, 9), (-6, 6), (18, 10), (42, 7), (58, 4)):
        h = (R * R - c * c) ** 0.5 * 0.93
        p.append(f'<path d="M{c},{-h:.1f} C{c + bojo},{-h * 0.45:.1f}'
                 f' {c - bojo * 0.6:.1f},{h * 0.45:.1f} {c},{h:.1f}" fill="none"'
                 ' stroke="#f7f0dc" stroke-width="3.4" opacity=".92"'
                 ' stroke-linecap="round"/>')
    for c, bojo in ((-48, 6), (-22, 5), (2, 9), (26, 6), (48, 5)):
        h = (R * R - c * c) ** 0.5 * 0.93
        p.append(f'<path d="M{-h:.1f},{c} C{-h * 0.45:.1f},{c + bojo:.1f}'
                 f' {h * 0.45:.1f},{c - bojo * 0.6:.1f} {h:.1f},{c}" fill="none"'
                 ' stroke="#f7f0dc" stroke-width="3.4" opacity=".92"'
                 ' stroke-linecap="round"/>')
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<circle r="{R}" fill="#cbb98c" stroke="#a8935f" stroke-width="3.5"/>'
            f'<circle r="{R - 3}" fill="#e2d3ad"/>'
            + ''.join(p) +
            '<ellipse cy="-71" rx="8" ry="5.5" fill="#a8935f"/>'
            '</g>')


def maca(x, y, s=1.0):
    """Maca inteira, verde: corpo + cabinho + folha (igual a do #23)."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<line x1="0" y1="-44" x2="0" y2="-72" stroke="#7a5a2a"'
            ' stroke-width="5" stroke-linecap="round"/>'
            '<path d="M0,-64 C16,-82 34,-74 32,-60 C24,-50 8,-52 0,-64 Z"'
            ' fill="#4e7a26"/>'
            '<path d="M0,-44 C24,-66 60,-54 62,-14 C64,24 36,54 0,54'
            ' C-36,54 -64,24 -62,-14 C-60,-54 -24,-66 0,-44 Z" fill="#8cc152"'
            ' stroke="#4e7a26" stroke-width="3.5"/>'
            '<ellipse cx="-24" cy="-14" rx="9" ry="16" fill="#fff" opacity=".3"/>'
            '</g>')


def garrafa(liquido, s=1.0, tampa=True):
    """Garrafa de boca larga — mais ALTA que larga (a licao da silhueta)."""
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


def jarra(liquido, s=1.0):
    """Jarro alto com liquido — mais alto que largo."""
    return (f'<g transform="scale({s:g})">'
            '<path d="M-62,-104 L-62,84 Q-62,104 -42,104 L42,104 Q62,104 62,84'
            ' L62,-104 Z" fill="#fdf6ea" stroke="#8a6a2f" stroke-width="4"/>'
            f'<path d="M-54,-72 L-54,80 Q-54,96 -38,96 L38,96 Q54,96 54,80 L54,-72 Z"'
            f' fill="{liquido}"/>'
            '<ellipse cx="-38" cy="-10" rx="7" ry="46" fill="#fff" opacity=".28"/>'
            '</g>')


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


def medidor(x, y, s=1.0):
    """Jarra de medida que balanca (`chop2x`)."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<g style="animation:chop2x 1.6s ease-in-out infinite">'
            '<path d="M-22,-30 L-18,26 Q-17,32 -10,32 L10,32 Q17,32 18,26 L22,-30 Z"'
            ' fill="#fdf1e2" stroke="#c9803a" stroke-width="3"/>'
            '<path d="M-15,2 L-12,26 Q-11,30 -6,30 L6,30 Q11,30 12,26 L15,2 Z"'
            ' fill="#f0a24a"/>'
            '<line x1="-14" y1="-8" x2="14" y2="-8" stroke="#c9803a"'
            ' stroke-width="2" opacity=".7"/>'
            '<line x1="-15" y1="8" x2="15" y2="8" stroke="#c9803a"'
            ' stroke-width="2" opacity=".7"/>'
            '</g></g>')


def colher_prova(x, y, s=1.0):
    """Colher de prova com kombucha na cuia, mergulhando (`chop2x`)."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<g style="animation:chop2x 1.6s ease-in-out infinite">'
            '<path d="M2,-66 L11,-62 L4,2 L-5,0 Z" fill="#c9d8c0" stroke="#5c7a29"'
            ' stroke-width="2.5" stroke-linejoin="round"/>'
            '<ellipse cx="-6" cy="16" rx="27" ry="17" fill="#c9d8c0"'
            ' stroke="#5c7a29" stroke-width="3"/>'
            '<ellipse cx="-6" cy="16" rx="19" ry="11" fill="#d9a441"/>'
            '</g></g>')


def faca(x, y, rot=0):
    """Faca de cozinha: lamina LARGA, afiada de um lado, com cabo e rebites.

    Lamina estreita le' como TERMOMETRO — foi o que o 1o render mostrou.
    """
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g})">'
            '<g style="animation:chop2x 1.7s ease-in-out infinite">'
            '<path d="M-15,-68 L15,-64 L17,30 Q17,38 8,38 L-15,38 Z"'
            ' fill="#cdd6dc" stroke="#7a8a92" stroke-width="2.5"'
            ' stroke-linejoin="round"/>'
            '<path d="M-15,-68 L15,-64 L16,-24 L-15,-26 Z" fill="#eef3f6"/>'
            '<path d="M-15,30 L17,30" stroke="#9aa8b0" stroke-width="2"/>'
            '<rect x="-13" y="38" width="26" height="52" rx="9" fill="#8a5a34"'
            ' stroke="#5e3a1f" stroke-width="2.5"/>'
            '<circle cx="0" cy="53" r="2.6" fill="#5e3a1f"/>'
            '<circle cx="0" cy="69" r="2.6" fill="#5e3a1f"/>'
            '</g></g>')


def gota(x, y, s=1.0, cor='#7fc3dd'):
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M0,-15 Q7,-5 7,2 Q7,9 0,9 Q-7,9 -7,2 Q-7,-5 0,-15 Z"'
            f' fill="{cor}" stroke="#3a8fb0" stroke-width="2"/></g>')


def escala_ph(x, y, w=312, h=34, marcas=()):
    """Barra de pH de 2 a 7, dividida em 4,6. `marcas` = [(ph, cor, rotulo)].

    As duas metades sao PATH, nao `<rect rx>`: dois retangulos arredondados lado a
    lado deixariam uma emenda redonda no meio da barra. So' as pontas arredondam.
    """
    r = h / 2.0

    def px(v):
        return -w / 2 + (v - 2) / 5.0 * w

    x46 = px(4.6)
    seguro = (f'M{x46:g},{-r:g} H{-w / 2 + r:g}'
              f' A{r:g},{r:g} 0 0 0 {-w / 2 + r:g},{r:g} H{x46:g} Z')
    inseguro = (f'M{x46:g},{-r:g} H{w / 2 - r:g}'
                f' A{r:g},{r:g} 0 0 1 {w / 2 - r:g},{r:g} H{x46:g} Z')
    p = [f'<path d="{seguro}" fill="#d9efe3"/>',
         f'<path d="{inseguro}" fill="#fbe0cd"/>',
         f'<rect x="{-w / 2:g}" y="{-r:g}" width="{w:g}" height="{h:g}" rx="{r:g}"'
         ' fill="none" stroke="#c9bda8" stroke-width="2.5"/>',
         f'<line x1="{x46:g}" y1="{-r - 9:g}" x2="{x46:g}" y2="{r + 9:g}"'
         ' stroke="#8a6a2f" stroke-width="3"/>',
         f'<text x="{x46:g}" y="{-r - 17:g}" text-anchor="middle" font-size="15"'
         ' font-weight="800" fill="#8a6a2f" font-family="system-ui">4.6</text>']
    for ph, cor, rotulo in marcas:
        pxx = px(ph)
        p.append(f'<circle cx="{pxx:g}" cy="0" r="9" fill="{cor}" stroke="#fff"'
                 ' stroke-width="2.5"/>')
        p.append(f'<text x="{pxx:g}" y="{r + 25:g}" text-anchor="middle"'
                 f' font-size="13" font-weight="800" fill="{cor}"'
                 f' font-family="system-ui">{rotulo}</text>')
    return f'<g transform="translate({x:g},{y:g})">' + ''.join(p) + '</g>'


def escala_ph_vertical(x, y, h=300, w=26):
    """A MESMA escala, em pe' — e' o gancho: o melao fica ACIMA da linha."""
    def py(v):
        return h / 2 - (v - 2) / 5.0 * h

    y46 = py(4.6)
    return (f'<g transform="translate({x:g},{y:g})">'
            f'<rect x="{-w / 2:g}" y="{-h / 2:g}" width="{w:g}" height="{h:g}"'
            f' rx="{w / 2:g}" fill="#f3ece0" stroke="#c9bda8" stroke-width="2.5"/>'
            f'<line x1="{-w / 2 - 16:g}" y1="{y46:g}" x2="{w / 2 + 16:g}" y2="{y46:g}"'
            ' stroke="#8a6a2f" stroke-width="3" stroke-dasharray="7 5"/>'
            f'<text x="{w / 2 + 22:g}" y="{y46 + 6:g}" font-size="15"'
            ' font-weight="800" fill="#8a6a2f" font-family="system-ui">4.6</text>'
            f'<text x="0" y="{h / 2 + 24:g}" text-anchor="middle" font-size="13"'
            ' font-weight="800" fill="#a08a5c" font-family="system-ui">2</text>'
            f'<text x="0" y="{-h / 2 - 12:g}" text-anchor="middle" font-size="13"'
            ' font-weight="800" fill="#a08a5c" font-family="system-ui">7</text>'
            '</g>')


# ------------------------------------------------------- cena 1: o gancho
def s0(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="252" cy="300" r="152" fill="#fdf1e2" opacity=".8"/>
    @ESCALA@
    <g transform="translate(248,212)">
      <g style="animation:wobble 3.0s ease-in-out infinite">
        @MELAO@
      </g>
    </g>
    <g transform="translate(248,402)">
      <g style="animation:wobble 2.6s ease-in-out infinite">
        @GARRAFA@
      </g>
    </g>
    <g transform="translate(202,556)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#e07b2e" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#b45c17" font-family="system-ui">MELON SITS ABOVE THE LINE</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#c98a5c" font-family="system-ui">pH 6.0 - the only fruit here that is not acid</text>
    </g>'''.replace('@ESCALA@', escala_ph_vertical(86, 300)) \
     .replace('@MELAO@', melao_metade(0, 0, 0.85)) \
     .replace('@GARRAFA@', garrafa(AMBAR, 0.7))


# ------------------------------------------------------- cena 2: a linha 4,6
def s1(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    @ESCALA@
    <g transform="translate(202,470)">
      <rect x="-172" y="-46" width="344" height="92" rx="12" fill="#fff" stroke="#8a6a2f" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#8a6a2f" font-family="system-ui">ABOVE 4.6, BACTERIA GROW</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">below it, they do not - that is the whole trick</text>
    </g>
    <g transform="translate(202,580)">
      <text x="0" y="0" text-anchor="middle" font-size="14" font-weight="700" fill="#5c7a29" font-family="system-ui">THE KOMBUCHA DRAGS THE MELON UNDER IT</text>
    </g>'''.replace('@ESCALA@', escala_ph(
        202, 268, 312, 34,
        [(3.0, TEAL, 'KOMBUCHA'), (6.35, LARANJA, 'MELON')]))


# ------------------------------------------------------- cena 3: o cha e' o acido
def s2(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="202" cy="336" r="146" fill="#fdf1e2" opacity=".7"/>
    <g transform="translate(202,336)">
      <g style="animation:wobble 2.8s ease-in-out infinite">
        @JARRA@
        <path d="M-34,-40 L-8,-52 L4,-30 L-22,-16 Z" fill="#e07b2e" stroke="#b45c17" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M10,-18 L36,-28 L44,-6 L16,4 Z" fill="#e07b2e" stroke="#b45c17" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M-30,10 L-4,0 L6,22 L-20,32 Z" fill="#f0a24a" stroke="#b45c17" stroke-width="2.5" stroke-linejoin="round"/>
      </g>
    </g>
    <g transform="translate(202,340)">@BOLHAS@</g>
    <g transform="translate(202,206)">
      <g style="animation:pour2x 1.6s ease-out infinite">
        <path d="M-9,-46 L9,-46 L13,8 Q0,20 -13,8 Z" fill="#d9a441" opacity=".92"/>
      </g>
    </g>
    <g transform="translate(202,560)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#1d9e75" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#0f6e56" font-family="system-ui">THE KOMBUCHA IS THE ACID</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#4a8a6e" font-family="system-ui">pH 2.5 to 3.5 when the first ferment is done</text>
    </g>'''.replace('@JARRA@', jarra('#f8dfb8')) \
     .replace('@BOLHAS@', bolhas())


# ------------------------------------------------------- cena 4: a maca e' o seguro
def s3(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <g transform="translate(202,186)">
      <rect x="-176" y="-52" width="352" height="104" rx="14" fill="#fff" stroke="#e07b2e" stroke-width="3.5"/>
      <text x="0" y="-14" text-anchor="middle" font-size="18" font-weight="800" fill="#b45c17" font-family="system-ui">THE APPLE IS THE INSURANCE</text>
      <text x="0" y="16" text-anchor="middle" font-size="13" font-weight="600" fill="#c98a5c" font-family="system-ui">it pulls the jar back under the line</text>
    </g>
    <g transform="translate(104,306)">
      <g style="animation:wobble 2.9s ease-in-out infinite">@MACA@</g>
    </g>
    <g transform="translate(300,306)">
      <g style="animation:wobble 3.1s ease-in-out infinite">@MELAO@</g>
    </g>
    <g transform="translate(202,306)">
      <path d="M0,-24 L0,18 M-9,8 L0,22 L9,8" stroke="#8a6a2f" stroke-width="4" fill="none" stroke-linecap="round"/>
    </g>
    <g transform="translate(104,398)">
      <rect x="-60" y="-28" width="120" height="56" rx="10" fill="#eaf5dc" stroke="#7fb542" stroke-width="2.5"/>
      <text x="0" y="7" text-anchor="middle" font-size="26" font-weight="800" fill="#2f5c0d" font-family="system-ui">3.0</text>
    </g>
    <g transform="translate(300,398)">
      <rect x="-60" y="-28" width="120" height="56" rx="10" fill="#fdecdb" stroke="#e07b2e" stroke-width="2.5"/>
      <text x="0" y="7" text-anchor="middle" font-size="26" font-weight="800" fill="#b45c17" font-family="system-ui">6.4</text>
    </g>
    <g transform="translate(202,520)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#fff8e6" stroke="#d9a441" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="15" font-weight="800" fill="#8a6a2f" font-family="system-ui">ABOUT 2500 TIMES MORE ACID</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">each pH point is ten times more acid</text>
    </g>'''.replace('@MACA@', maca(0, 0, 0.72)) \
     .replace('@MELAO@', melao_metade(0, 0, 0.60))


# ------------------------------------------------------- cena 5: a prova
def s4(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="202" cy="256" r="130" fill="#fdf1e2" opacity=".75"/>
    <g transform="translate(202,232)">@COLHER@</g>
    <g transform="translate(112,352)">
      <g style="animation:tick 2.2s ease-in-out infinite">
        <path d="M0,20 L-10,2 L10,2 Z" fill="#7fb542"/>
      </g>
    </g>
    <g transform="translate(112,422)">
      <rect x="-70" y="-38" width="140" height="76" rx="12" fill="#eaf5dc" stroke="#7fb542" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="17" font-weight="800" fill="#2f5c0d" font-family="system-ui">TART</text>
      <text x="0" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="#6b8f3a" font-family="system-ui">ready</text>
    </g>
    <g transform="translate(292,422)">
      <rect x="-70" y="-38" width="140" height="76" rx="12" fill="#fdeef0" stroke="#e8556d" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="17" font-weight="800" fill="#c9334d" font-family="system-ui">SWEET</text>
      <text x="0" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="#d4757f" font-family="system-ui">not ready</text>
    </g>
    <g transform="translate(202,552)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#d9a441" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#8a6a2f" font-family="system-ui">TASTE IT BEFORE YOU ADD</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">sweet kombucha is not acid enough to carry fruit</text>
    </g>'''.replace('@COLHER@', colher_prova(0, 0, 1.35))


# ------------------------------------------------------- cena 6: a casca
def s5(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="176" cy="300" r="130" fill="#fdf1e2" opacity=".7"/>
    <g transform="translate(176,300)">
      <g style="animation:wobble 2.9s ease-in-out infinite">@MELAO@</g>
    </g>
    @GOTAS@
    <g transform="translate(322,238)">@FACA@</g>
    <g transform="translate(202,540)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#8a9a5b" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#5c6b2f" font-family="system-ui">WASH THE RIND FIRST</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#7d8a45" font-family="system-ui">the net is where the bacteria actually live</text>
    </g>'''.replace('@MELAO@', melao_inteiro(0, 0, 1.0)) \
     .replace('@FACA@', faca(0, 0, 18)) \
     .replace('@GOTAS@', '\n    '.join([
         gota(132, 176, 1.0), gota(176, 158, 1.25), gota(216, 184, 0.85)]))


# ------------------------------------------------------- cena 7: a proporcao
def s6(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="202" cy="182" r="106" fill="#fdf1e2" opacity=".8"/>
    <g transform="translate(202,182)">@MEDIDOR@</g>
    <g transform="translate(202,350)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#e07b2e" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#b45c17" font-family="system-ui">LESS FRUIT, NOT MORE</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#c98a5c" font-family="system-ui">1 part melon to 4 parts kombucha</text>
    </g>
    <g transform="translate(202,474)">
      <rect x="-176" y="-42" width="352" height="84" rx="12" fill="#fff8e6" stroke="#d9a441" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="#8a6a2f" font-family="system-ui">AND DRINK IT FAST</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">melon fades before the fizz does</text>
    </g>
    <g transform="translate(202,584)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">which one should I ferment next?</text>
    </g>'''.replace('@MEDIDOR@', medidor(0, 0, 1.5))


# ---------------------------------------------------------------- montagem
TEXTOS = {
    'titulo': 'Shorts animado — Apple and melon kombucha (2nd ferment)',
    'badge': '🍎 + 🍈',
    'capdiv': ('Apple and melon kombucha'
               '<small>the melon is the one that is not acid</small>'),
    'cenas': [
        ('s0', 6400, '%s 1 / 7' % TAG, 'The one fruit that is not acid',
         'its pH is 6.0 to 6.7', LARANJA_ESC),
        ('s1', 6400, '%s 2 / 7' % TAG, 'Why 4.6 is the line',
         'above it, bacteria can grow', '#8a6a2f'),
        ('s2', 6200, '%s 3 / 7' % TAG, 'The kombucha is the acid',
         'pH 2.5 to 3.5 when it is done', TEAL),
        ('s3', 6600, '%s 4 / 7' % TAG, 'And the apple is the insurance',
         'pH 3 against the melon 6', VERDE_ESC),
        ('s4', 6200, '%s 5 / 7' % TAG, 'Taste it before you add',
         'sweet means not acid enough', AMBAR),
        ('s5', 6400, '%s 6 / 7' % TAG, 'The rind is the problem',
         'wash it before the knife goes in', '#5c6b2f'),
        ('s6', 6400, '%s 7 / 7' % TAG, 'Less fruit, not more',
         'and drink it before the aroma goes', '#2f5c0d'),
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

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with io.open(DESTINO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('%-46s %d bytes | %d cenas | keyframes %d/%d'
          % (DESTINO, len(d.encode('utf-8')), len(t['cenas']),
             len(usados & defs), len(defs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

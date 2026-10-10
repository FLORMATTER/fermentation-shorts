# -*- coding: utf-8 -*-
"""
_criar-beterraba-kvass.py — Short #28: "Beet kvass with garlic".

O ASSUNTO (o que nenhum dos 27 ensina):
  A salmoura do kvass de beterraba e' a MAIS FRACA da serie: 1 colher de cha' por
  litro de agua = ~0,6% de sal — um TERCO do chucrute (2%) e um OITAVO de uma
  conserva (3,5-5%). E ela e' medida na AGUA, nao no peso do legume.
  Essa diferenca de BASE ("2% de que?") e' o video inteiro.

  E a salmoura fraca explica todo o resto, na propria fonte: "keeping oxygen out
  is important SINCE THE BRINE IS RELATIVELY LOW IN SALT".

  Fonte: American Homebrewers Association / Zymurgy (Amahl Turczyn), "How to Make
  Beet Kvass" — receita com ALHO e gengibre, 1 colher de cha' de sal por litro,
  4-7 dias a 18-21 C, provar do 3o dia, reabastecer o jarro para o 2o lote, jogar
  fora se ficar viscoso/limoso, e nao ralar ("releases too much sugar too quickly,
  and you'll end up with alcoholic beet beer").

  Por que NAO repete a serie:
    #19 (beterraba+alho) -> PICLES em cunhas, 2% do LEGUME, camadas, 2 semanas
    #1  (chucrute)        -> 2% do LEGUME, sem agua acrescentada
    #23-#26 (kombucha)    -> bebida, mas com cha' e SCOBY
  Aqui e' BEBIDA (agua acrescentada), 0,6% da AGUA, 4-7 dias, sem starter.

TOKENS: cor e desenho usam nomes DIFERENTES (@COR_BETERRABA@ vs @BETERRABA@) —
a licao do #27, onde o mesmo token para os dois fez o primeiro .replace()
consumir o token e o desenho nunca entrar.

Uso:  python _criar-beterraba-kvass.py
"""
import io
import os
import re
import sys

TEMPLATE = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'beterraba/shorts-beet-kvass-garlic-en.html'
TAG = 'KVASS'

# ------------------------------------------------------------------- paleta
BETERRABA = '#9c1b4f'
BETERRABA_ESC = '#6d0f36'
BETERRABA_CLARO = '#c9336b'
LIQUIDO = '#8e1240'
ALHO = '#f2e9d8'
ALHO_ESC = '#a89468'
ALHO_ESCURO = '#6b5a3a'
VERDE = '#7fb542'
VERDE_ESC = '#4e7a26'
CREME = '#fdf6ea'
FUNDO = '#fdf7f3'


# ------------------------------------------------------------------- desenhos
def beterraba(x, y, s=1.0):
    """Beterraba: bulbo largo + raiz afunilada embaixo + talos em cima.

    Os talos e a raiz existem para a SILHUETA ficar mais ALTA que larga. So' o
    bulbo le como caixa (a licao da silhueta).
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M-8,-46 C-20,-76 -34,-92 -46,-96 C-40,-78 -28,-62 -12,-50 Z"'
            f' fill="{VERDE_ESC}"/>'
            f'<path d="M6,-48 C10,-80 22,-98 34,-104 C32,-84 24,-64 12,-50 Z"'
            f' fill="{VERDE}"/>'
            f'<path d="M0,-44 C-44,-44 -60,-6 -60,18 C-60,46 -32,62 0,62'
            f' C32,62 60,46 60,18 C60,-6 44,-44 0,-44 Z" fill="{BETERRABA}"/>'
            f'<path d="M0,-44 C-18,-40 -26,-4 -26,20 C-26,48 -12,60 0,62'
            f' C12,60 26,48 26,20 C26,-4 18,-40 0,-44 Z" fill="{BETERRABA_CLARO}"'
            f' opacity=".45"/>'
            f'<path d="M-9,56 L9,56 L2,112 L-2,112 Z" fill="{BETERRABA_ESC}"/>'
            f'<path d="M-6,74 L6,74 L2,104 L-2,104 Z" fill="{BETERRABA}"/>'
            '</g>')


def alho(x, y, s=1.0):
    """Bulbo de alho: ponta em cima, gomos separados por linhas claras.

    Os gomos usam ALHO_ESC (#a89468) e nao um tom palido: com o tom palido o
    alho lia como CEBOLA no zoom 3x (a licao do #27).
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M0,-50 C-30,-50 -54,-16 -54,14 C-54,44 -28,58 0,58'
            f' C28,58 54,44 54,14 C54,-16 30,-50 0,-50 Z" fill="{ALHO}"/>'
            f'<path d="M0,-50 C-15,-42 -23,-14 -23,14 C-23,42 -12,55 0,58'
            f' C12,55 23,42 23,14 C23,-14 15,-42 0,-50 Z" fill="#fbf6ec"/>'
            f'<path d="M-54,14 C-54,44 -28,58 0,58" fill="none"'
            f' stroke="{ALHO_ESC}" stroke-width="3"/>'
            f'<path d="M54,14 C54,44 28,58 0,58" fill="none"'
            f' stroke="{ALHO_ESC}" stroke-width="3"/>'
            f'<path d="M-34,32 L-18,54" stroke="{ALHO_ESC}" stroke-width="2.6"'
            f' fill="none"/>'
            f'<path d="M34,32 L18,54" stroke="{ALHO_ESC}" stroke-width="2.6"'
            f' fill="none"/>'
            f'<path d="M-23,20 L-12,50" stroke="{ALHO_ESC}" stroke-width="2.2"'
            f' fill="none"/>'
            f'<path d="M23,20 L12,50" stroke="{ALHO_ESC}" stroke-width="2.2"'
            f' fill="none"/>'
            f'<path d="M0,-50 C-7,-62 -3,-70 5,-76 C3,-62 7,-56 12,-50 Z"'
            f' fill="{ALHO_ESC}"/>'
            '</g>')


def endro(x, y, s=1.0):
    """Raminho de endro — o par tradicional do kvass de beterraba."""
    galhos = []
    for y0, dx in ((26, -22), (12, 22), (-2, -24), (-16, 20), (-28, -18)):
        galhos.append(f'<path d="M0,{y0} L{dx},{y0 - 8}" stroke="{VERDE}"'
                      f' stroke-width="2.4" fill="none"/>')
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M0,40 L0,-36" stroke="{VERDE_ESC}" stroke-width="3"/>'
            + ''.join(galhos) + '</g>')


def jarra(liquido, s=1.0):
    """Jarro alto com liquido — mais alto que largo (a licao da silhueta)."""
    return (f'<g transform="scale({s:g})">'
            '<path d="M-62,-104 L-62,84 Q-62,104 -42,104 L42,104 Q62,104 62,84'
            ' L62,-104 Z" fill="#fdf6ea" stroke="#8a6a2f" stroke-width="4"/>'
            f'<path d="M-54,-72 L-54,80 Q-54,96 -38,96 L38,96 Q54,96 54,80 L54,-72 Z"'
            f' fill="{liquido}"/>'
            '<ellipse cx="-38" cy="-10" rx="7" ry="46" fill="#fff" opacity=".28"/>'
            '</g>')


def bolhas():
    """Borbulha subindo (o `riseFast` da serie)."""
    return ('<g style="animation:riseFast 1.4s ease-out infinite">'
            '<circle cx="-10" cy="52" r="4" fill="#fff" opacity=".8"/>'
            '<circle cx="14" cy="62" r="3.2" fill="#fff" opacity=".75"/>'
            '</g>'
            '<g style="animation:riseFast 1.4s ease-out .5s infinite">'
            '<circle cx="2" cy="44" r="3.6" fill="#fff" opacity=".7"/>'
            '<circle cx="-24" cy="58" r="3" fill="#fff" opacity=".65"/>'
            '</g>')


def colher(x, y, s=1.0):
    """Colher de cha' com o sal dentro — a MEDIDA do video."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<rect x="-8" y="-56" width="16" height="70" rx="8" fill="#dbe4e9"'
            ' stroke="#7a8a92" stroke-width="3"/>'
            '<ellipse cx="0" cy="26" rx="34" ry="24" fill="#e8eef2"'
            ' stroke="#7a8a92" stroke-width="3"/>'
            '<ellipse cx="0" cy="24" rx="26" ry="17" fill="#fdfaf0"/>'
            '<ellipse cx="0" cy="22" rx="18" ry="10" fill="#f3ece0"/>'
            '</g>')


def sal_graos(x, y, s=1.0):
    """Graos de sal caindo — o `pour2x` da serie.

    11 px com contorno escuro. Grao pequeno e claro sobre fundo claro fica
    INVISIVEL no render (aconteceu no #26 e de novo no #27).
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<g style="animation:pour2x 1.6s ease-out infinite">'
            '<rect x="-6" y="-9" width="11" height="11" rx="2.5" fill="#fdfaf0"'
            ' stroke="#8a7a5c" stroke-width="2"/>'
            '<rect x="10" y="1" width="10" height="10" rx="2.5" fill="#fdfaf0"'
            ' stroke="#8a7a5c" stroke-width="2"/>'
            '<rect x="-13" y="11" width="9" height="9" rx="2" fill="#fdfaf0"'
            ' stroke="#8a7a5c" stroke-width="2"/>'
            '</g></g>')


def faca(x, y, rot=0):
    """Faca de cozinha: lamina LARGA (estreita le' como termometro)."""
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


def ampulheta(x, y, s=1.0):
    """Ampulheta — os dias que o kvass leva."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<rect x="-40" y="-58" width="80" height="9" rx="4" fill="#8a6a2f"/>'
            '<rect x="-40" y="49" width="80" height="9" rx="4" fill="#8a6a2f"/>'
            '<path d="M-30,-49 L30,-49 L4,0 L30,49 L-30,49 L-4,0 Z"'
            ' fill="#fdf6ea" stroke="#8a6a2f" stroke-width="3"/>'
            f'<path d="M-22,-42 L22,-42 L3,-6 L-3,-6 Z" fill="{BETERRABA_CLARO}"/>'
            f'<path d="M-20,42 L20,42 L0,6 Z" fill="{BETERRABA_CLARO}"/>'
            '<rect x="-4" y="-6" width="8" height="12" fill="#8a6a2f"/>'
            '</g>')


def tampa(x, y, s=1.0):
    """Tampa com airlock — o que separa o kvass do ar."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<rect x="-9" y="-52" width="18" height="46" rx="6" fill="#e8f0f4"'
            ' stroke="#7a8a92" stroke-width="2.5"/>'
            '<rect x="-15" y="-70" width="30" height="20" rx="7" fill="#cfe6f2"'
            ' stroke="#7a8a92" stroke-width="2.5"/>'
            '<ellipse cx="0" cy="0" rx="48" ry="16" fill="#cdd6dc"'
            ' stroke="#7a8a92" stroke-width="3"/>'
            '<ellipse cx="0" cy="-6" rx="39" ry="12" fill="#eef3f6"/>'
            '<circle cx="0" cy="-40" r="3.4" fill="#7a8a92" opacity=".75"/>'
            '<circle cx="0" cy="-26" r="2.6" fill="#7a8a92" opacity=".6"/>'
            '</g>')


def leveduras(pontos, cor='#6b4a1f'):
    """Bacterias na CASCA: celula clara com anel, em cima do contorno.

    Ponto escuro DENTRO da silhueta le' como machucado (a licao do #27). Por
    isso o anel escuro com miolo claro, colocado no contorno.
    """
    saida = []
    for x, y, r in pontos:
        saida.append(
            f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="#f9edc9"'
            f' stroke="{cor}" stroke-width="2"/>'
            f'<circle cx="{x - r * 0.5:g}" cy="{y - r * 0.5:g}" r="{r * 0.42:g}"'
            f' fill="{cor}" opacity=".5"/>')
    return '\n    '.join(saida)


def ralado(x, y, s=1.0):
    """Beterraba RALADA: monte de fiapos — o jeito errado."""
    fiapos = []
    for x0, y0, dx, dy in ((-30, -4, 22, -14), (-14, 4, 26, -18),
                           (2, -2, 24, -16), (18, 6, 20, -12),
                           (-22, 12, 30, -10), (-4, 16, 18, -8)):
        fiapos.append(f'<path d="M{x0},{y0} l{dx},{dy}" stroke="{BETERRABA_CLARO}"'
                      f' stroke-width="2.6" fill="none"/>')
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<ellipse cx="0" cy="16" rx="42" ry="20" fill="{BETERRABA}"'
            f' opacity=".9"/>' + ''.join(fiapos) + '</g>')


def barras():
    """As tres salmouras lado a lado — a conta do video, em desenho.

    Largura proporcional ao sal: 0,6% / 2% / 3,5-5%. A barra do kvass fica
    MINUSCULA de proposito: e' o argumento inteiro.
    """
    dados = (('KVASS', '0.6%', 0.6, BETERRABA),
             ('KRAUT', '2%', 2.0, VERDE),
             ('PICKLE', '3.5-5%', 5.0, VERDE_ESC))
    escala = 42.0
    saida = []
    y = 296
    for nome, valor, pct, cor in dados:
        largura = max(12.0, pct * escala)
        saida.append(
            f'<g transform="translate(64,{y:g})">'
            f'<text x="-10" y="5" text-anchor="end" font-size="13" font-weight="800"'
            f' fill="#5c4a3c" font-family="system-ui">{nome}</text>'
            f'<rect x="0" y="-14" width="{largura:g}" height="28" rx="9" fill="{cor}"/>'
            f'<text x="{largura + 10:g}" y="5" font-size="13" font-weight="800"'
            f' fill="#5c4a3c" font-family="system-ui">{valor}</text>'
            f'</g>')
        y += 66
    return '\n    '.join(saida)


# --------------------------------------------------- cena 1: o gancho (a medida)
def s0(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <circle cx="202" cy="264" r="150" fill="@COR_CREME@" opacity=".9"/>
    <g transform="translate(132,272)">@BETERRABA@</g>
    <g transform="translate(276,262)">@ALHO@</g>
    <g transform="translate(202,432)">
      <g style="animation:pulseBadge 2.2s ease-in-out infinite">
        <rect x="-118" y="-21" width="236" height="42" rx="21" fill="@COR_BETERRABA@" stroke="#fff" stroke-width="3"/>
        <text x="0" y="7" text-anchor="middle" font-size="15" font-weight="800" fill="#fff" font-family="system-ui">ONE TEASPOON PER LITRE</text>
      </g>
    </g>
    <g transform="translate(202,566)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_BETERRABA@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_BETERRABA_ESC@" font-family="system-ui">THE WEAKEST BRINE HERE</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8727c" font-family="system-ui">no other jar in this series runs this low</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_CREME@', CREME) \
     .replace('@COR_BETERRABA@', BETERRABA).replace('@COR_BETERRABA_ESC@', BETERRABA_ESC) \
     .replace('@BETERRABA@', beterraba(0, 0, 0.72)).replace('@ALHO@', alho(0, 0, 0.72))


# ------------------------------------------------- cena 2: a beterraba (o combustivel)
def s1(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,190)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_BETERRABA@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_BETERRABA_ESC@" font-family="system-ui">DO NOT PEEL IT</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8727c" font-family="system-ui">the bacteria you need live on the skin</text>
    </g>
    <circle cx="202" cy="382" r="126" fill="#fbe8ef" opacity=".8"/>
    <g transform="translate(202,382)">@BETERRABA@</g>
    @PONTOS@
    <g transform="translate(202,558)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#fbe8ef" stroke="@COR_BETERRABA@" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="@COR_BETERRABA_ESC@" font-family="system-ui">7 g OF SUGAR IN 100 g</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#a8727c" font-family="system-ui">the sweetest root in this whole series</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_BETERRABA@', BETERRABA) \
     .replace('@COR_BETERRABA_ESC@', BETERRABA_ESC) \
     .replace('@BETERRABA@', beterraba(0, 0, 1.0)) \
     .replace('@PONTOS@', leveduras([(150, 348, 5.4), (254, 344, 5),
                                     (144, 392, 5.6), (260, 396, 5.2),
                                     (166, 434, 4.8), (238, 436, 5),
                                     (202, 340, 4.6)]))


# ------------------------------------------------- cena 3: a medida (0,6%)
def s2(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,188)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="#8a6a2f" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#5c4a3c" font-family="system-ui">MEASURED ON THE WATER</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#9a8a7a" font-family="system-ui">not on the weight of the beet</text>
    </g>
    <g transform="translate(136,376)">@COLHER@</g>
    <g transform="translate(212,344)">@SAL@</g>
    <g transform="translate(304,394)">@JARRA@</g>
    <g transform="translate(202,558)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#f5f0e8" stroke="#8a6a2f" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="17" font-weight="800" fill="#5c4a3c" font-family="system-ui">1 TEASPOON = 0.6%</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#9a8a7a" font-family="system-ui">about 6 g of salt in 1 litre of water</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO) \
     .replace('@COLHER@', colher(0, 0, 1.0)).replace('@SAL@', sal_graos(0, 0, 1.0)) \
     .replace('@JARRA@', jarra(LIQUIDO, 0.62))


# ------------------------------------------------- cena 4: a comparacao (as barras)
def s3(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,190)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_VERDE_ESC@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_VERDE_ESC@" font-family="system-ui">A THIRD OF KRAUT</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#6f8f4a" font-family="system-ui">and an eighth of a 5% pickle brine</text>
    </g>
    @BARRAS@
    <g transform="translate(202,558)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#eef7e6" stroke="@COR_VERDE_ESC@" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="@COR_VERDE_ESC@" font-family="system-ui">SAME WORD, DIFFERENT JAR</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#6f8f4a" font-family="system-ui">a percentage means nothing without its base</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO) \
     .replace('@COR_VERDE_ESC@', VERDE_ESC).replace('@BARRAS@', barras())


# ------------------------------------------------- cena 5: o ar (salmoura fraca)
def s4(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,188)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="#c0392b" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#a02a1e" font-family="system-ui">AIR IS THE ENEMY HERE</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b07a72" font-family="system-ui">a weak brine cannot defend the surface</text>
    </g>
    <g transform="translate(202,404)">
      <g style="animation:wobble 2.8s ease-in-out infinite">@JARRA@<g transform="translate(0,-75) scale(0.93)">@TAMPA@</g></g>
    </g>
    <g transform="translate(202,566)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fdf1ee" stroke="#c0392b" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="17" font-weight="800" fill="#a02a1e" font-family="system-ui">KEEP IT UNDER THE LIQUID</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b07a72" font-family="system-ui">and burp the jar once a day</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO) \
     .replace('@JARRA@', jarra(LIQUIDO, 0.72)).replace('@TAMPA@', tampa(0, 0, 0.9))


# ------------------------------------------------- cena 6: os dois jeitos de perder
def s5(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,188)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="#c0392b" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#a02a1e" font-family="system-ui">DICE IT, DO NOT SHRED IT</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b07a72" font-family="system-ui">shredded beet gives up its sugar too fast</text>
    </g>
    <g transform="translate(112,352)">
      <rect x="-64" y="-64" width="128" height="128" rx="14" fill="#f6f1e4" stroke="#c0392b" stroke-width="3"/>
      <g transform="translate(-14,16)">@RALADO@</g>
      <line x1="-52" y1="-52" x2="52" y2="52" stroke="#c0392b" stroke-width="6" stroke-linecap="round"/>
      <line x1="52" y1="-52" x2="-52" y2="52" stroke="#c0392b" stroke-width="6" stroke-linecap="round"/>
      <text x="0" y="86" text-anchor="middle" font-size="14" font-weight="800" fill="#a02a1e" font-family="system-ui">SHREDDED</text>
    </g>
    <g transform="translate(292,352)">
      <rect x="-64" y="-64" width="128" height="128" rx="14" fill="#f6f1e4" stroke="@COR_VERDE_ESC@" stroke-width="3"/>
      <g transform="translate(-2,-40) rotate(-8) scale(0.44)">@FACA@</g>
      <g transform="translate(0,20)">@CUBOS@</g>
      <text x="0" y="86" text-anchor="middle" font-size="14" font-weight="800" fill="@COR_VERDE_ESC@" font-family="system-ui">2 CM CUBES</text>
    </g>
    <g transform="translate(202,500)">
      <rect x="-178" y="-30" width="356" height="60" rx="12" fill="#fff" stroke="#c0392b" stroke-width="3"/>
      <text x="0" y="6" text-anchor="middle" font-size="15" font-weight="800" fill="#a02a1e" font-family="system-ui">SLIMY MEANS THROW IT AWAY</text>
    </g>
    <g transform="translate(202,588)">
      <text x="0" y="0" text-anchor="middle" font-size="13" font-weight="600" fill="#9a8a7a" font-family="system-ui">it stays under 1% alcohol, but it is not zero</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_VERDE_ESC@', VERDE_ESC) \
     .replace('@RALADO@', ralado(0, 0, 0.6)).replace('@CUBOS@', cubos()) \
     .replace('@FACA@', faca(0, 0, 0))


# ------------------------------------------------- cena 7: o fecho (dias)
def s6(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <circle cx="202" cy="316" r="142" fill="@COR_CREME@" opacity=".85"/>
    <g transform="translate(140,340)">
      <g style="animation:wobble 2.6s ease-in-out infinite">@JARRA@</g>
    </g>
    <g transform="translate(140,300)">@BOLHAS@</g>
    <g transform="translate(300,352)"><g style="animation:tick 2.2s ease-in-out infinite">@AMPULHETA@</g></g>
    <g transform="translate(202,196)">
      <g style="animation:pulseBadge 2.2s ease-in-out infinite">
        <rect x="-96" y="-20" width="192" height="40" rx="20" fill="@COR_VERDE_ESC@" stroke="#fff" stroke-width="3"/>
        <text x="0" y="6" text-anchor="middle" font-size="15" font-weight="800" fill="#fff" font-family="system-ui">TASTE IT ON DAY 3</text>
      </g>
    </g>
    <g transform="translate(202,556)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_BETERRABA_ESC@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_BETERRABA_ESC@" font-family="system-ui">FOUR TO SEVEN DAYS</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8727c" font-family="system-ui">then refill the jar for a lighter second batch</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_CREME@', CREME) \
     .replace('@COR_BETERRABA_ESC@', BETERRABA_ESC).replace('@COR_VERDE_ESC@', VERDE_ESC) \
     .replace('@JARRA@', jarra(LIQUIDO, 0.72)).replace('@BOLHAS@', bolhas()) \
     .replace('@AMPULHETA@', ampulheta(0, 0, 0.6))


def cubos():
    """Cubos de 2 cm — o jeito certo, dentro do painel verde."""
    return (f'<g>'
            f'<rect x="-36" y="-36" width="32" height="32" rx="7" fill="{BETERRABA}"/>'
            f'<rect x="4" y="-36" width="32" height="32" rx="7" fill="{BETERRABA_CLARO}"/>'
            f'<rect x="-36" y="4" width="32" height="32" rx="7" fill="{BETERRABA_CLARO}"/>'
            f'<rect x="4" y="4" width="32" height="32" rx="7" fill="{BETERRABA}"/>'
            '</g>')


# ---------------------------------------------------------------- montagem
TEXTOS = {
    'titulo': 'Shorts animado — Beet kvass with garlic (fermented)',
    'badge': 'BEET + GARLIC',
    'capdiv': ('Beet kvass with garlic'
               '<small>beet, water, salt, and one clove'),
    'cenas': [
        ('s0', 6600, '%s 1 / 7' % TAG, 'Beet kvass with garlic',
         'beet, water, salt, and one clove', BETERRABA_ESC),
        ('s1', 6400, '%s 2 / 7' % TAG, 'The beet brings the fuel',
         'about 7 g of sugar in every 100 g', BETERRABA),
        ('s2', 6200, '%s 3 / 7' % TAG, 'One teaspoon per litre',
         'that is about 0.6% salt, by water weight', '#5c4a3c'),
        ('s3', 6600, '%s 4 / 7' % TAG, 'How it compares to other jars',
         'kraut runs at 2%, pickle brine at 3.5 to 5', VERDE_ESC),
        ('s4', 6200, '%s 5 / 7' % TAG, 'So the lid matters more here',
         'keep it under the surface and burp it daily', '#a02a1e'),
        ('s5', 6800, '%s 6 / 7' % TAG, 'The two ways to lose the batch',
         'alcohol from shredding, slime from the wrong microbes', '#a02a1e'),
        ('s6', 6400, '%s 7 / 7' % TAG, 'Taste it from day three',
         'strain, chill, then refill the same jar', VERDE_ESC),
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
    """A barra de legenda do mp4 nao pode repetir o texto que ja' esta' na cena."""
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

    sobrou = sorted(set(re.findall(r'@[A-Z_]{3,}@', d)))
    if sobrou:
        print('ERRO: token nao substituido: %s' % sobrou)
        return 1

    rep = acha_repeticoes(d, t['cenas'])
    if rep:
        print('ERRO: a legenda do mp4 repete o texto da cena: %s' % rep)
        return 1

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with io.open(DESTINO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    total = sum(c[1] for c in t['cenas']) / 1000.0
    print('%-48s %d bytes | %d cenas | %.1f s | keyframes %d/%d'
          % (DESTINO, len(d.encode('utf-8')), len(t['cenas']), total,
             len(usados & defs), len(defs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

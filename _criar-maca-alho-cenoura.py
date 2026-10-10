# -*- coding: utf-8 -*-
"""
_criar-maca-alho-cenoura.py — Short #27: "Apple + garlic + carrot".

O ASSUNTO (o que nenhum dos 26 ensina):
  O alho nao e' so' antibacteriano — o allicin e' tambem ANTIFUNGICO. Ele ataca
  justamente a levedura selvagem que vem na casca da maca. Ou seja: num mesmo
  jarro, a maca traz o motor da efervescencia e o alho envenena esse motor.
  O resultado pratico: o jarro fica PARADO nos primeiros dias e depois engata.

  Fonte: "Allicin-induced global gene expression profile of Saccharomyces
  cerevisiae" (2010) — trata o allicin como fungicida natural contra a propria
  S. cerevisiae. E o #22 ja' estabeleceu que o allicin degrada em ~2 dias.

  Por que NAO repete a serie:
    #18 (cenoura+maca)  -> "a maca faz efervescer" (acucar + levedura) = o MOTOR
    #22 (pepino+alho)   -> allicin antimicrobiano e a degradacao em 2 dias
    #9/#19 (alho)       -> allicin arde e depois adoca; camadas
  Ninguem cruzou o motor (#18) com o freio (#22). Este video e' o cruzamento.

  E traz um ponto de SEGURANCA que a serie nao tinha: alho em OLEO e' risco de
  botulismo (anaerobio + baixa acidez). Na salmoura a acidez fecha essa janela.

TOKENS: cor e desenho usam nomes DIFERENTES (@COR_MACA@ vs @MACA@). A primeira
versao usou @MACA@ para os dois e o primeiro .replace() consumiu o token — o
desenho nunca entrava e o SVG saia com a string de cor no lugar da maca.

Uso:  python _criar-maca-alho-cenoura.py
"""
import io
import os
import re
import sys

TEMPLATE = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'cenoura/shorts-apple-garlic-carrot-en.html'
TAG = 'FERMENT'

# ------------------------------------------------------------------- paleta
MACA = '#c9334d'
MACA_ESC = '#8f1f33'
MACA_CLARO = '#d94a62'
VERDE = '#7fb542'
VERDE_ESC = '#4e7a26'
ALHO = '#f2e9d8'
ALHO_ESC = '#a89468'
ALHO_ESCURO = '#6b5a3a'
CENOURA = '#e07b1f'
CENOURA_ESC = '#a8541a'
CREME = '#fdf6ea'
FUNDO = '#fdf7f3'


# ------------------------------------------------------------------- desenhos
def maca(x, y, s=1.0):
    """Maca redonda com cabinho e folha."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<circle cx="-26" cy="10" r="41" fill="{MACA}"/>'
            f'<circle cx="26" cy="10" r="41" fill="{MACA}"/>'
            f'<rect x="-48" y="-8" width="96" height="56" rx="26" fill="{MACA}"/>'
            f'<circle cx="-30" cy="0" r="28" fill="{MACA_CLARO}" opacity=".5"/>'
            '<rect x="-5" y="-58" width="10" height="30" rx="5" fill="#7a4a2a"/>'
            f'<path d="M4,-52 C24,-68 48,-60 48,-46 C48,-32 24,-32 6,-44 Z"'
            f' fill="{VERDE}"/>'
            '</g>')


def alho(x, y, s=1.0):
    """Bulbo de alho: ponta em cima, gomos separados por linhas claras."""
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


def cenoura(x, y, s=1.0):
    """Cenoura afunilada com folhas. Mais ALTA que larga."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M-32,-32 L32,-32 L0,74 Z" fill="{CENOURA}"/>'
            f'<path d="M-32,-32 L0,-32 L0,74 Z" fill="#ef8f34"/>'
            f'<path d="M-8,-28 L-3,-6" stroke="{CENOURA_ESC}" stroke-width="2.6"/>'
            f'<path d="M10,-26 L3,-2" stroke="{CENOURA_ESC}" stroke-width="2.6"/>'
            f'<path d="M-17,-22 L-12,-4" stroke="{CENOURA_ESC}" stroke-width="2.6"/>'
            f'<path d="M-8,-32 C-26,-54 -40,-60 -46,-58 C-38,-46 -26,-38 -13,-34 Z"'
            f' fill="{VERDE_ESC}"/>'
            f'<path d="M4,-32 C16,-56 30,-64 38,-62 C30,-48 20,-38 8,-34 Z"'
            f' fill="{VERDE}"/>'
            '</g>')


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
    """Dois grupos de borbulha subindo (o `riseFast` da serie)."""
    return ('<g style="animation:riseFast 1.4s ease-out infinite">'
            '<circle cx="-10" cy="52" r="4" fill="#fff" opacity=".8"/>'
            '<circle cx="14" cy="62" r="3.2" fill="#fff" opacity=".75"/>'
            '</g>'
            '<g style="animation:riseFast 1.4s ease-out .5s infinite">'
            '<circle cx="2" cy="44" r="3.6" fill="#fff" opacity=".7"/>'
            '<circle cx="-24" cy="58" r="3" fill="#fff" opacity=".65"/>'
            '</g>')


def leveduras(pontos, cor='#a8842e'):
    """Levedura selvagem: celula com anel, no CONTORNO da maca.

    Ponto escuro EM CIMA da maca lia como MACHUCADO, nao como levedura (o
    zoom 3x mostrou). Agora fica fora da silhueta, com anel, e numa cor que
    nao e' a da fruta.
    """
    saida = []
    for x, y, r in pontos:
        saida.append(
            f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="#f9edc9"'
            f' stroke="{cor}" stroke-width="2"/>'
            f'<circle cx="{x - r * 0.5:g}" cy="{y - r * 0.5:g}" r="{r * 0.42:g}"'
            f' fill="{cor}" opacity=".5"/>')
    return '\n    '.join(saida)


def leveduras_riscadas(pontos):
    """A mesma levedura, riscada: o allicin chegou nela."""
    saida = []
    for x, y, r in pontos:
        saida.append(
            f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="none"'
            f' stroke="#b9a88c" stroke-width="2.4" stroke-dasharray="4 3"/>'
            f'<line x1="{x - r:g}" y1="{y - r:g}" x2="{x + r:g}" y2="{y + r:g}"'
            f' stroke="#c0392b" stroke-width="3" stroke-linecap="round"/>')
    return '\n    '.join(saida)


def ampulheta(x, y, s=1.0):
    """Ampulheta — o tempo que o allicin leva para sumir."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<rect x="-40" y="-58" width="80" height="9" rx="4" fill="#8a6a2f"/>'
            '<rect x="-40" y="49" width="80" height="9" rx="4" fill="#8a6a2f"/>'
            '<path d="M-30,-49 L30,-49 L4,0 L30,49 L-30,49 L-4,0 Z"'
            ' fill="#fdf6ea" stroke="#8a6a2f" stroke-width="3"/>'
            f'<path d="M-22,-42 L22,-42 L3,-6 L-3,-6 Z" fill="{MACA_CLARO}"/>'
            f'<path d="M-20,42 L20,42 L0,6 Z" fill="{MACA_CLARO}"/>'
            '<rect x="-4" y="-6" width="8" height="12" fill="#8a6a2f"/>'
            '</g>')


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


def sal_graos(x, y, s=1.0):
    """Graos de sal caindo — o `pour2x` da serie.

    Grao de 6 px, branco, sobre a caixa verde-clara ficava INVISIVEL no render
    (a mesma licao do copo de acucar do #26: contraste se julga no render, nao
    na coordenada). Agora 11 px e contorno escuro.
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


# --------------------------------------------------- cena 1: o gancho (o conflito)
def s0(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <circle cx="202" cy="266" r="152" fill="@COR_CREME@" opacity=".9"/>
    <g transform="translate(106,262)">@MACA@</g>
    <g transform="translate(202,286)">@ALHO@</g>
    <g transform="translate(300,270)">@CENOURA@</g>
    <g transform="translate(202,428)">
      <g style="animation:pulseBadge 2.2s ease-in-out infinite">
        <rect x="-98" y="-21" width="196" height="42" rx="21" fill="@COR_MACA@" stroke="#fff" stroke-width="3"/>
        <text x="0" y="7" text-anchor="middle" font-size="15" font-weight="800" fill="#fff" font-family="system-ui">ONE FIGHTS THE OTHERS</text>
      </g>
    </g>
    <g transform="translate(202,566)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_MACA@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_MACA_ESC@" font-family="system-ui">THE JAR ARGUES</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8727c" font-family="system-ui">one ingredient here slows the whole jar down</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_CREME@', CREME) \
     .replace('@COR_MACA@', MACA).replace('@COR_MACA_ESC@', MACA_ESC) \
     .replace('@MACA@', maca(0, 0, 0.8)).replace('@ALHO@', alho(0, 0, 0.8)) \
     .replace('@CENOURA@', cenoura(0, 0, 0.95))


# ------------------------------------------------- cena 2: o motor (a maca)
def s1(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,190)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_MACA@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_MACA_ESC@" font-family="system-ui">WHAT THE APPLE BRINGS</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8727c" font-family="system-ui">sugar in the flesh, yeast on the skin</text>
    </g>
    <circle cx="202" cy="374" r="128" fill="#fdeef1" opacity=".8"/>
    <g transform="translate(202,378)">@MACA@</g>
    <g transform="translate(330,382) rotate(-12) scale(0.7)">@FACA@</g>
    @PONTOS@
    <g transform="translate(202,558)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#fdeef1" stroke="@COR_MACA@" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="@COR_MACA_ESC@" font-family="system-ui">SUGAR + WILD YEAST</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#a8727c" font-family="system-ui">the yeast is what makes the bubbles</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_MACA@', MACA) \
     .replace('@COR_MACA_ESC@', MACA_ESC) \
     .replace('@MACA@', maca(0, 0, 1.05)) \
     .replace('@PONTOS@', leveduras([(118, 338, 5.4), (286, 348, 5),
                                     (126, 428, 4.6), (282, 424, 5.2),
                                     (168, 288, 4.4), (252, 294, 4.6),
                                     (196, 450, 4.6)])).replace('@FACA@', faca(0, 0, 30))


# ------------------------------------------------- cena 3: a virada (fungicida)
def s2(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,188)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_ALHO_ESC@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_ALHO_ESCURO@" font-family="system-ui">IT IS A FUNGICIDE TOO</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#9a8a6a" font-family="system-ui">allicin does not only kill bacteria</text>
    </g>
    <circle cx="202" cy="376" r="126" fill="#fdf6ea" opacity=".85"/>
    <g transform="translate(202,376)">@ALHO@</g>
    @MORTAS@
    <g transform="translate(202,558)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#fff" stroke="#c0392b" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="#a02a1e" font-family="system-ui">IT HITS THE YEAST TOO</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#b07a72" font-family="system-ui">the very thing that makes the bubbles</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_ALHO_ESC@', ALHO_ESC) \
     .replace('@COR_ALHO_ESCURO@', ALHO_ESCURO) \
     .replace('@ALHO@', alho(0, 0, 1.05)) \
     .replace('@MORTAS@', leveduras_riscadas([(150, 342, 6), (256, 354, 5.4),
                                              (166, 424, 5), (246, 418, 6),
                                              (204, 322, 5.2), (140, 390, 5.6),
                                              (268, 394, 5.2)]))


# ------------------------------------------------- cena 4: o jarro parado
def s3(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,188)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="#7d6a5c" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#5c4a3c" font-family="system-ui">SO THE FIZZ IS LATE</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#9a8a7a" font-family="system-ui">the allicin has to fade first</text>
    </g>
    <g transform="translate(140,412)">
      <g style="animation:wobble 2.8s ease-in-out infinite">@JARRA@</g>
      <g transform="scale(0.72)">
        <rect x="-34" y="-44" width="28" height="19" rx="6" fill="@COR_MACA@" opacity=".9" transform="rotate(-16 -20 -34)"/>
        <rect x="8" y="-14" width="24" height="17" rx="6" fill="@COR_CENOURA@" opacity=".92" transform="rotate(13 20 -5)"/>
        <ellipse cx="-10" cy="34" rx="14" ry="11" fill="#fbf6ec" opacity=".95"/>
      </g>
    </g>
    <g transform="translate(300,400)"><g style="animation:tick 2.2s ease-in-out infinite">@AMPULHETA@</g></g>
    <g transform="translate(202,558)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#f5f0e8" stroke="#7d6a5c" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="#5c4a3c" font-family="system-ui">NO BUBBLES ON DAY TWO</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#9a8a7a" font-family="system-ui">that is normal in this jar</text>
    </g>'''     .replace('@COR_FUNDO@', FUNDO) \
     .replace('@JARRA@', jarra('#e8c98a', 0.72)) \
     .replace('@AMPULHETA@', ampulheta(0, 0, 0.62)) \
     .replace('@COR_MACA@', MACA).replace('@COR_CENOURA@', CENOURA)


# ------------------------------------------------- cena 5: os dois dias
def s4(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,190)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_CENOURA_ESC@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_CENOURA_ESC@" font-family="system-ui">THE JAR GOES QUIET</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b98a5a" font-family="system-ui">allicin breaks down on its own</text>
    </g>
    <g transform="translate(202,330)">
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
    </g>
    <g transform="translate(202,558)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#eef7e6" stroke="@COR_VERDE_ESC@" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="@COR_VERDE_ESC@" font-family="system-ui">THEN IT TAKES OFF</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#6f8f4a" font-family="system-ui">the yeast comes back and the jar wakes up</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_CENOURA@', CENOURA) \
     .replace('@COR_CENOURA_ESC@', CENOURA_ESC).replace('@COR_VERDE@', VERDE) \
     .replace('@COR_VERDE_ESC@', VERDE_ESC)


# ------------------------------------------------- cena 6: a seguranca (oleo)
def s5(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <g transform="translate(202,188)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="#c0392b" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#a02a1e" font-family="system-ui">GARLIC NEEDS ACID</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b07a72" font-family="system-ui">in oil it is a botulism risk - brine fixes it</text>
    </g>
    <g transform="translate(112,352)">
      <rect x="-64" y="-64" width="128" height="128" rx="14" fill="#f6f1e4" stroke="#c0392b" stroke-width="3"/>
      <g transform="translate(0,4)">@ALHO_P@</g>
      <line x1="-52" y1="-52" x2="52" y2="52" stroke="#c0392b" stroke-width="6" stroke-linecap="round"/>
      <line x1="52" y1="-52" x2="-52" y2="52" stroke="#c0392b" stroke-width="6" stroke-linecap="round"/>
      <text x="0" y="86" text-anchor="middle" font-size="14" font-weight="800" fill="#a02a1e" font-family="system-ui">OIL</text>
    </g>
    <g transform="translate(292,296)">@SAL@</g>
    <g transform="translate(292,352)">
      <rect x="-64" y="-64" width="128" height="128" rx="14" fill="#eef7e6" stroke="@COR_VERDE_ESC@" stroke-width="3"/>
      <g transform="translate(0,4)">@ALHO_P@</g>
      <path d="M-34,34 L-24,46 L-6,20" fill="none" stroke="@COR_VERDE_ESC@" stroke-width="6" stroke-linecap="round"/>
      <text x="0" y="86" text-anchor="middle" font-size="14" font-weight="800" fill="@COR_VERDE_ESC@" font-family="system-ui">BRINE</text>
    </g>
    <g transform="translate(202,500)">
      <rect x="-178" y="-30" width="356" height="60" rx="12" fill="#fff" stroke="@COR_VERDE_ESC@" stroke-width="3"/>
      <text x="0" y="6" text-anchor="middle" font-size="15" font-weight="800" fill="@COR_VERDE_ESC@" font-family="system-ui">2% SALT, UNDER THE BRINE</text>
    </g>
    <g transform="translate(202,588)">
      <text x="0" y="0" text-anchor="middle" font-size="13" font-weight="600" fill="#9a8a7a" font-family="system-ui">no air plus acid is what makes it safe</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_VERDE_ESC@', VERDE_ESC) \
     .replace('@ALHO_P@', alho(0, 0, 0.5)).replace('@SAL@', sal_graos(0, 0, 1.0))


# ------------------------------------------------- cena 7: o fecho
def s6(t):
    return '''    <rect width="405" height="720" fill="@COR_FUNDO@"/>
    <circle cx="202" cy="316" r="142" fill="@COR_CREME@" opacity=".85"/>
    <g transform="translate(202,340)">
      <g style="animation:wobble 2.6s ease-in-out infinite">@JARRA@</g>
    </g>
    <g transform="translate(202,300)">@BOLHAS@</g>
    <g transform="translate(202,196)">
      <g style="animation:pulseBadge 2.2s ease-in-out infinite">
        <rect x="-92" y="-20" width="184" height="40" rx="20" fill="@COR_VERDE_ESC@" stroke="#fff" stroke-width="3"/>
        <text x="0" y="6" text-anchor="middle" font-size="15" font-weight="800" fill="#fff" font-family="system-ui">TWO MORE DAYS</text>
      </g>
    </g>
    <g transform="translate(202,556)">
      <rect x="-178" y="-46" width="356" height="92" rx="12" fill="#fff" stroke="@COR_MACA_ESC@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@COR_MACA_ESC@" font-family="system-ui">THE GARLIC COSTS 2 DAYS</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8727c" font-family="system-ui">want it fast? leave the garlic out</text>
    </g>'''.replace('@COR_FUNDO@', FUNDO).replace('@COR_CREME@', CREME) \
     .replace('@COR_MACA_ESC@', MACA_ESC).replace('@COR_VERDE_ESC@', VERDE_ESC) \
     .replace('@JARRA@', jarra('#d96a7e', 0.72)).replace('@BOLHAS@', bolhas())


# ---------------------------------------------------------------- montagem
TEXTOS = {
    'titulo': 'Shorts animado — Apple, garlic and carrot (fermented)',
    'badge': '🍎 + 🧄',
    'capdiv': ('Apple, garlic, carrot'
               '<small>one of them fights the other two</small>'),
    'cenas': [
        ('s0', 6400, '%s 1 / 7' % TAG, 'Apple, garlic, carrot',
         'one of them fights the other two', MACA_ESC),
        ('s1', 6400, '%s 2 / 7' % TAG, 'The apple is the engine',
         'sugar, plus the yeast on its skin', MACA),
        ('s2', 6200, '%s 3 / 7' % TAG, 'Allicin is a fungicide',
         'garlic does not only kill bacteria', ALHO_ESCURO),
        ('s3', 6400, '%s 4 / 7' % TAG, 'So the fizz arrives late',
         'your jar is not dead - it is waiting', '#7d6a5c'),
        ('s4', 6200, '%s 5 / 7' % TAG, 'Two days of silence',
         'allicin fades, then the yeast takes over', CENOURA_ESC),
        ('s5', 6600, '%s 6 / 7' % TAG, 'Garlic in oil is the risk',
         'no air, no acid - the brine adds the acid', '#a02a1e'),
        ('s6', 6400, '%s 7 / 7' % TAG, 'Six days, not four',
         'or leave the garlic out and it is fast again', VERDE_ESC),
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
    """A barra de legenda do mp4 nao pode repetir o texto que ja' esta' na cena.

    Varre TODOS os `<text>` da cena e compara com o `cap` e o `sub` daquela cena.
    Nao selecionar "o titulo" por `font-size`: as cenas titulam com 15, 16, 17 e
    18 px — foi assim que a 1a versao deste verificador errou a conta.
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

    # nenhum token sobrou sem substituir (o erro que a 1a versao cometeu)
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
    print('%-46s %d bytes | %d cenas | %.1f s | keyframes %d/%d'
          % (DESTINO, len(d.encode('utf-8')), len(t['cenas']), total,
             len(usados & defs), len(defs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

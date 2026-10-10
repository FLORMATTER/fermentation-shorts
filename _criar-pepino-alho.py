# -*- coding: utf-8 -*-
"""_criar-pepino-alho.py — cria o short PEPINO + ALHO (EN).

    python _criar-pepino-alho.py

Nao existia nada de pepino+alho na serie. O pepino ja' aparece em #6 (pepino-speed)
e #17 (pepino-apple) — entao este NAO pode repetir o truque da folha de louro (e' o
assunto do #6) nem o "acucar nao e' tanino" (e' o #17). O assunto AQUI e' o ALHO.

Substancia (pesquisada, nao inventada):
  - o alho NAO e' so' sabor: ele e' FONTE de bacterias lacticas. Leuconostoc sp. e
    Weissella sp. foram isoladas do alho e sao as que iniciam a fermentacao
    (Kim et al., Food Sci Biotechnol 2015, cabbage-kimchi sem cada ingrediente);
  - mas o alho cru tem ALICINA, que e' antimicrobiana — ela ataca tambem as LAB.
    O que salva a fermentacao e' que a alicina se DEGRADA em ~2 dias;
  - o dente de alho fica AZUL ou VERDE: o acido (latico) reage com os compostos de
    enxofre e forma POLIPIRROIS. Nao e' mofo, nao e' toxico, nao muda o sabor de
    verdade — e' PROVA de que o acido apareceu;
  - na China isso e' procurado: o "laba garlic" (labasuan) e' verde de proposito,
    comido no Ano Novo;
  - pepino flutua, alho afunda (mais denso que a salmoura) -> um jarro, duas direcoes;
  - o pepino precisa de MAIS sal que o repolho (3,5-5% contra 2%) porque e' ~96% agua
    e mole: sal fraco = pepino mole.

Paleta: verde do pepino (menta) + creme do alho. O AZUL do alho e' a cor do gancho.

O QUE O RENDER ENSINOU (1a versao, consertado aqui):
  - o dente de alho feito so' de oval bicudo lê como FOLHA/SEMENTE — pior ainda com
    duas curvas internas, que viram NERVURAS. O que faz ler "alho" e' a BASE CHATA
    (o corte) — por isso o helper `dente()` desenha a linha da base;
  - o bulbo tambem lê como folha se a silhueta for lisa: precisa dos GOMOS (lobulos);
  - o jarro da ultima cena ficou 104x114 — quase quadrado — e virou CAIXA. Jarro e'
    sempre mais alto que largo (a licao da silhueta);
  - a colher de sal (elipse + retangulo + trapezio) virou POTINHO com tampa. Uma
    colher precisa de CABO fino e comprido e da cuia com o monte de sal DENTRO.
"""
import io
import os
import re
import sys

TEMPLATE = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'pepino/shorts-cucumber-garlic-en.html'

TAG = 'CUCUMBER+GARLIC'


def cena(cid, corpo, primeira=False):
    cls = 'scene on' if primeira else 'scene'
    return ('  <svg class="%s" id="%s" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">\n'
            % (cls, cid)) + corpo + '\n  </svg>'


def fatia(cx, cy, rot, r, cor='#639922'):
    """Uma rodela de pepino: casca escura, miolo claro, sementes.

    Elipse lisa le' como azeitona — foi o defeito do 2o render. O que faz ler
    "pepino" e' o anel de casca + o miolo palido + as sementes.
    """
    return (f'<g transform="translate({cx:g},{cy:g}) rotate({rot:g})">'
            f'<ellipse rx="{r:g}" ry="{r*0.44:g}" fill="{cor}"'
            f' stroke="#2f5c0d" stroke-width="2.5"/>'
            f'<ellipse rx="{r*0.66:g}" ry="{r*0.29:g}" fill="#e2f0cc"/>'
            f'<ellipse cx="{-r*0.36:g}" rx="{r*0.09:g}" ry="{r*0.10:g}" fill="#a9c97e"/>'
            f'<ellipse cx="{r*0.36:g}" rx="{r*0.09:g}" ry="{r*0.10:g}" fill="#a9c97e"/>'
            f'<ellipse cy="{-r*0.17:g}" rx="{r*0.09:g}" ry="{r*0.10:g}" fill="#a9c97e"/>'
            f'<ellipse cy="{r*0.17:g}" rx="{r*0.09:g}" ry="{r*0.10:g}" fill="#a9c97e"/>'
            '</g>')


def dente(x, y, fill, stroke, s=1.0, w=2.5):
    """Dente de alho DESCASCADO — a casca (barriga) + a FACE DO CORTE.

    Gota simetrica le' como pingo d'agua (1o render); a linha da base nao bastou
    (2o); o lado reto sozinho ainda le' como baga (3o). O que faltava era a FAIXA
    CLARA do corte, do lado reto — e' ela que faz ler "dente cortado".
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<path d="M-5,-24 C7,-18 16,-7 16,5 C16,16 10,22 1,22'
            ' L-12,22 C-16,22 -17,17 -17,7 L-16,-9 C-15,-17 -11,-21 -5,-24 Z"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="{w/s:g}"'
            ' stroke-linejoin="round"/>'
            '<path d="M-5,-24 C-11,-21 -15,-17 -16,-9 L-17,7 C-17,16 -16,20 -12,22'
            ' L-5,22 C-2,8 -1,-8 -5,-24 Z" fill="#ffffff" opacity=".42"/>'
            '<path d="M-5,-24 C-1,-8 -2,8 -5,22" fill="none"'
            f' stroke="{stroke}" stroke-width="{w*0.7/s:g}" opacity=".3"/>'
            '</g>')


def colher_sal(x, y):
    """Colher de medida com sal, inclinada pela `chop2x`.

    Cabo FINO e comprido + cuia oval + monte DENTRO. A 1a versao (elipse grossa +
    retangulo + trapezio por cima) lê como potinho com tampa.
    """
    return ('<g transform="translate(%g,%g)">'
            '<g style="animation:chop2x 1.5s ease-in-out infinite">'
            '<path d="M3,-58 L12,-54 L5,0 L-3,-3 Z" fill="#c9d8c0" stroke="#5c7a29" stroke-width="2.5"/>'
            '<ellipse cx="-4" cy="10" rx="27" ry="16" fill="#c9d8c0" stroke="#5c7a29" stroke-width="3"/>'
            '<path d="M-24,8 Q-4,-14 16,8 Z" fill="#fffdf6" stroke="#aebba4" stroke-width="2"/>'
            '</g>'
            '</g>') % (x, y)


def cravo(cx, cy, rot, w, h, fill, stroke='#b08f4e', sw=3):
    """Um dente COM CASCA, visto de frente — a peca de construcao do bulbo."""
    return (f'<g transform="translate({cx:g},{cy:g}) rotate({rot:g})">'
            f'<path d="M0,{-h:g}'
            f' C{w*0.62:g},{-h*0.42:g} {w*0.52:g},{-h*0.10:g} {w*0.50:g},0'
            f' C{w*0.62:g},{h*0.50:g} {w*0.42:g},{h*0.86:g} {w*0.36:g},{h*0.86:g}'
            f' L{-w*0.36:g},{h*0.86:g}'
            f' C{-w*0.42:g},{h*0.86:g} {-w*0.62:g},{h*0.50:g} {-w*0.50:g},0'
            f' C{-w*0.52:g},{-h*0.10:g} {-w*0.62:g},{-h*0.42:g} 0,{-h:g} Z"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"'
            ' stroke-linejoin="round"/>'
            '</g>')


def bulbo_alho(x, y):
    """Bulbo = CASCA (silhueta palida pontilhada) + 5 DENTES + colo.

    Silhueta unica com lobulos le' como CONCHA (2o render). Dentes separados leem
    como FLOR de petalas abertas, com o colo flutuando (3o render). A CASCA
    resolve os dois. Mas o bulbo tem de ser ATARRAQUADO — mais LARGO que ALTO:
    alto e bicudo le' como BOTAO/cebola (4o render). Alho de verdade e' baixo, o
    terco de cima e' so' casca e os dentes aparecem embaixo.
    """
    casca = ('<path d="M0,-62 C-16,-50 -28,-36 -40,-18 C-56,-4 -64,10 -60,26'
             ' C-54,46 -30,60 0,60 C30,60 54,46 60,26 C64,10 56,-4 40,-18'
             ' C28,-36 16,-50 0,-62 Z" fill="#f9f2e0" stroke="#cbb98c"'
             ' stroke-width="2.5" stroke-dasharray="6 5"/>')
    colo = ('<path d="M-9,-60 L-6,-78 L6,-78 L9,-60 Z" fill="#e6d9b6"'
            ' stroke="#b08f4e" stroke-width="3" stroke-linejoin="round"/>'
            '<line x1="0" y1="-78" x2="0" y2="-92" stroke="#b08f4e"'
            ' stroke-width="3" stroke-linecap="round"/>')
    dentes = [(-46, 32, -16, 28, 28, '#e6d9b6'),
              (46, 32, 16, 28, 28, '#e6d9b6'),
              (-29, 24, -7, 34, 36, '#f2e6c9'),
              (29, 24, 7, 34, 36, '#f2e6c9'),
              (0, 20, 0, 40, 42, '#f7eed6')]
    corpo = ''.join(cravo(*d) for d in dentes)
    return (f'<g transform="translate({x:g},{y:g})">'
            '<g style="animation:wobble 2.7s ease-in-out infinite">'
            + casca + colo + corpo + '</g></g>')


def lab(x, y, rot, cor='#1d9e75', t=1.0):
    """Uma bacteria lactica: BASTONETE. Nao e' bolinha — circulos soltos liam
    como pontos aleatorios no render."""
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g})">'
            f'<rect x="{-9*t:g}" y="{-3.6*t:g}" width="{18*t:g}" height="{7.2*t:g}"'
            f' rx="{3.6*t:g}" fill="{cor}" opacity=".85"/>'
            '</g>')


def nuvem_lab():
    """Os bastonetes em volta do bulbo. Ficam ATRAS dele (o token vem antes)."""
    pos = [(112, 200, -18), (84, 268, 12), (114, 340, -8), (294, 196, 20),
           (322, 266, -14), (292, 342, 8), (196, 104, 4), (268, 118, -22)]
    return '\n    '.join(lab(*p) for p in pos)


# ---------------------------------------------------------------- cena 1: o gancho
def s0(t):
    return '''    <rect width="405" height="720" fill="#f6fbf3"/>
    <circle cx="202" cy="290" r="158" fill="#e1f5ee" opacity=".55"/>
    <g transform="translate(202,290)">
      <g style="animation:wobble 2.9s ease-in-out infinite">
        <path d="M-78,-96 L-78,88 Q-78,110 -56,110 L56,110 Q78,110 78,88 L78,-96 Z" fill="#eef8f0" stroke="#3b6d11" stroke-width="4"/>
        <rect x="-86" y="-114" width="172" height="22" rx="8" fill="#dcecd6" stroke="#3b6d11" stroke-width="4"/>
        <path d="M-72,-62 L-72,84 Q-72,104 -50,104 L50,104 Q72,104 72,84 L72,-62 Z" fill="#cde5bf"/>
        <ellipse cx="-52" cy="6" rx="9" ry="56" fill="#fff" opacity=".35"/>
        @F1@
        @F2@
        @F3@
        @D1@
        @D2@
        @D3@
        <g style="animation:riseFast 1.5s ease-out infinite">
          <circle cx="-44" cy="66" r="4" fill="#fff" opacity=".85"/>
          <circle cx="8" cy="78" r="3.4" fill="#fff" opacity=".8"/>
        </g>
        <g style="animation:riseFast 1.5s ease-out .5s infinite">
          <circle cx="-14" cy="84" r="3.8" fill="#fff" opacity=".65"/>
          <circle cx="38" cy="80" r="3.2" fill="#fff" opacity=".6"/>
        </g>
      </g>
    </g>
    <g transform="translate(202,516)">
      <rect x="-166" y="-44" width="332" height="88" rx="12" fill="#fff" stroke="#3b6d11" stroke-width="3"/>
      <text x="0" y="-8" text-anchor="middle" font-size="21" font-weight="800" fill="#2f5c0d" font-family="system-ui">THE GARLIC TURNS BLUE</text>
      <text x="0" y="22" text-anchor="middle" font-size="14" font-weight="600" fill="#6b8f3a" font-family="system-ui">that is the acid working</text>
    </g>'''.replace('@F1@', fatia(-26, -22, -12, 38)) \
     .replace('@F2@', fatia(28, -6, 10, 36)) \
     .replace('@F3@', fatia(-6, 16, -3, 36)) \
     .replace('@D1@', dente(-36, 72, '#3a8fb0', '#1f5f7d')) \
     .replace('@D2@', dente(4, 80, '#3a8fb0', '#1f5f7d')) \
     .replace('@D3@', dente(44, 62, '#f2e6c9', '#b08f4e'))


# ---------------------------------------------------------------- cena 2: duas direcoes
def s1(t):
    return '''    <rect width="405" height="720" fill="#f6fbf3"/>
    <g transform="translate(202,300)">
      <g style="animation:wobble 3.1s ease-in-out infinite">
        <path d="M-84,-118 L-84,96 Q-84,116 -64,116 L64,116 Q84,116 84,96 L84,-118 Z" fill="#eef8f0" stroke="#3b6d11" stroke-width="4"/>
        <rect x="-90" y="-134" width="180" height="20" rx="7" fill="#dcecd6" stroke="#3b6d11" stroke-width="4"/>
        <path d="M-80,-92 L-80,92 Q-80,112 -60,112 L60,112 Q80,112 80,92 L80,-92 Z" fill="#cde5bf"/>
        <ellipse cx="-14" cy="-64" rx="44" ry="17" fill="#639922" stroke="#2f5c0d" stroke-width="3"/>
        <ellipse cx="24" cy="-40" rx="38" ry="15" fill="#79a92f" stroke="#2f5c0d" stroke-width="3"/>
        @D1@
        @D2@
        @D3@
      </g>
    </g>
    <g transform="translate(96,220)">
      <path d="M0,26 L0,-18 M-9,-8 L0,-20 L9,-8" stroke="#2f5c0d" stroke-width="4" fill="none" stroke-linecap="round"/>
    </g>
    <text x="96" y="266" text-anchor="middle" font-size="14" font-weight="800" fill="#2f5c0d" font-family="system-ui">FLOATS</text>
    <g transform="translate(308,412)">
      <path d="M0,-26 L0,18 M-9,8 L0,20 L9,8" stroke="#8a6a2f" stroke-width="4" fill="none" stroke-linecap="round"/>
    </g>
    <text x="308" y="458" text-anchor="middle" font-size="14" font-weight="800" fill="#8a6a2f" font-family="system-ui">SINKS</text>'''.replace('@D1@', dente(-30, 74, '#f2e6c9', '#b08f4e')) \
     .replace('@D2@', dente(10, 80, '#f2e6c9', '#b08f4e')) \
     .replace('@D3@', dente(46, 70, '#f2e6c9', '#b08f4e'))


# ---------------------------------------------------------------- cena 3: o sal
def s2(t):
    return '''    <rect width="405" height="720" fill="#f6fbf3"/>
    <g transform="translate(202,238)">
      <rect x="-160" y="-72" width="320" height="144" rx="14" fill="#fff" stroke="#3b6d11" stroke-width="3.5"/>
      <text x="0" y="16" text-anchor="middle" font-size="52" font-weight="800" fill="#2f5c0d" font-family="system-ui">3.5 - 5%</text>
      <text x="0" y="48" text-anchor="middle" font-size="14" font-weight="700" fill="#6b8f3a" font-family="system-ui">salt by weight of water</text>
    </g>
    @COLHER@
    <g transform="translate(112,412)">
      <rect x="-66" y="-34" width="132" height="68" rx="10" fill="#eef8f0" stroke="#97c459" stroke-width="2.5"/>
      <text x="0" y="2" text-anchor="middle" font-size="24" font-weight="800" fill="#5c7a29" font-family="system-ui">2%</text>
      <text x="0" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#7d9459" font-family="system-ui">cabbage</text>
    </g>
    <g transform="translate(292,412)">
      <rect x="-66" y="-34" width="132" height="68" rx="10" fill="#fff8e6" stroke="#d9b872" stroke-width="2.5"/>
      <text x="0" y="2" text-anchor="middle" font-size="24" font-weight="800" fill="#8a6a2f" font-family="system-ui">3.5-5%</text>
      <text x="0" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#b08f4e" font-family="system-ui">cucumber</text>
    </g>
    <g transform="translate(202,524)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">A CUCUMBER IS 96% WATER</text>
      <text x="0" y="24" text-anchor="middle" font-size="13" font-weight="600" fill="#6b8f3a" font-family="system-ui">so the brine has to carry more salt</text>
    </g>'''.replace('@COLHER@', colher_sal(314, 140))


# ---------------------------------------------------------------- cena 4: o alho traz bacteria
def s3(t):
    return '''    <rect width="405" height="720" fill="#f6fbf3"/>
    @LABS@
    @BULBO@
    <g transform="translate(202,414)">
      <rect x="-168" y="-40" width="336" height="80" rx="12" fill="#fff" stroke="#1d9e75" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="17" font-weight="800" fill="#0f6e56" font-family="system-ui">LEUCONOSTOC + WEISSELLA</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#4a8a6e" font-family="system-ui">the bacteria that start the ferment</text>
    </g>
    <g transform="translate(202,520)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">THEY RIDE IN ON THE GARLIC</text>
    </g>'''.replace('@LABS@', nuvem_lab()) \
     .replace('@BULBO@', bulbo_alho(202, 244))


# ---------------------------------------------------------------- cena 5: a alicina passa
def s4(t):
    return '''    <rect width="405" height="720" fill="#f6fbf3"/>
    <g transform="translate(202,222)">
      <rect x="-170" y="-56" width="340" height="112" rx="14" fill="#fff8e6" stroke="#d9b872" stroke-width="3.5"/>
      <text x="0" y="-12" text-anchor="middle" font-size="17" font-weight="800" fill="#8a6a2f" font-family="system-ui">CRUSHED GARLIC IS A DEFENCE</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">allicin kills bacteria, the good ones too</text>
    </g>
    <g transform="translate(202,372)">
      <g style="animation:tick 2.6s ease-in-out infinite">
        <path d="M0,-14 L8,-30 L-8,-30 Z" fill="#8a6a2f"/>
      </g>
      <line x1="-150" y1="0" x2="150" y2="0" stroke="#c9d8c0" stroke-width="3"/>
      <circle cx="-150" cy="0" r="11" fill="#d9b872"/>
      <circle cx="0" cy="0" r="11" fill="#97c459"/>
      <circle cx="150" cy="0" r="11" fill="#1d9e75"/>
      <text x="-150" y="36" text-anchor="middle" font-size="11" font-weight="800" fill="#8a6a2f" font-family="system-ui">DAY 0</text>
      <text x="0" y="36" text-anchor="middle" font-size="11" font-weight="800" fill="#5c7a29" font-family="system-ui">DAY 2</text>
      <text x="150" y="36" text-anchor="middle" font-size="11" font-weight="800" fill="#0f6e56" font-family="system-ui">DAY 3</text>
      <text x="-150" y="60" text-anchor="middle" font-size="12" font-weight="600" fill="#a08a5c" font-family="system-ui">allicin</text>
      <text x="0" y="60" text-anchor="middle" font-size="12" font-weight="600" fill="#7d9459" font-family="system-ui">fading</text>
      <text x="150" y="60" text-anchor="middle" font-size="12" font-weight="600" fill="#4a8a6e" font-family="system-ui">acid</text>
    </g>
    <g transform="translate(202,516)">
      <rect x="-158" y="-40" width="316" height="80" rx="12" fill="#fff" stroke="#3b6d11" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="#2f5c0d" font-family="system-ui">ALLICIN DOES NOT LAST</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#6b8f3a" font-family="system-ui">so it cannot stop the ferment</text>
    </g>'''


# ---------------------------------------------------------------- cena 6: o azul
def s5(t):
    return '''    <rect width="405" height="720" fill="#f6fbf3"/>
    <circle cx="202" cy="246" r="132" fill="#e1f5ee" opacity=".5"/>
    <g transform="translate(202,250)">
      <g style="animation:wobble 2.8s ease-in-out infinite">
        <path d="M0,-82 Q42,-44 46,12 Q44,58 26,72 L-26,72 Q-44,58 -46,12 Q-42,-44 0,-82 Z" fill="#3a8fb0" stroke="#1f5f7d" stroke-width="4"/>
        <line x1="-26" y1="72" x2="26" y2="72" stroke="#1f5f7d" stroke-width="5" stroke-linecap="round"/>
        <ellipse cx="-15" cy="4" rx="8" ry="32" fill="#7fc3dd" opacity=".5"/>
      </g>
    </g>
    <g transform="translate(202,132)">
      <g style="animation:pour2x 1.6s ease-out infinite">
        <path d="M-11,-20 Q0,-34 11,-20 Q11,-4 0,12 Q-11,-4 -11,-20Z" fill="#9fd8ea" stroke="#1f5f7d" stroke-width="2.5"/>
      </g>
    </g>
    <g transform="translate(202,428)">
      <rect x="-172" y="-46" width="344" height="92" rx="12" fill="#fff" stroke="#1f5f7d" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#1f5f7d" font-family="system-ui">POLYPYRROLES</text>
      <text x="0" y="14" text-anchor="middle" font-size="13" font-weight="600" fill="#4a7f96" font-family="system-ui">sulfur plus acid, and the clove changes colour</text>
    </g>
    <g transform="translate(202,536)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">NO ACID, NO COLOUR</text>
    </g>'''


# ---------------------------------------------------------------- cena 7: o erro
def s6(t):
    return '''    <rect width="405" height="720" fill="#f6fbf3"/>
    <circle cx="202" cy="236" r="118" fill="#e1f5ee" opacity=".6"/>
    <g transform="translate(202,236)">
      <g style="animation:wobble 2.6s ease-in-out infinite">
        <path d="M-44,76 L-44,-42 Q-44,-56 -30,-56 L30,-56 Q44,-56 44,-42 L44,76 Z" fill="#eef8f0" stroke="#3b6d11" stroke-width="4"/>
        <rect x="-50" y="-72" width="100" height="18" rx="6" fill="#dcecd6" stroke="#3b6d11" stroke-width="4"/>
        <path d="M-40,44 L-40,-34 Q-40,-48 -26,-48 L26,-48 Q40,-48 40,-34 L40,44 Z" fill="#cde5bf"/>
        @D1@
        @D2@
      </g>
    </g>
    <g transform="translate(202,392)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#3b6d11" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#2f5c0d" font-family="system-ui">TRIM THE BLOSSOM END</text>
      <text x="0" y="14" text-anchor="middle" font-size="13" font-weight="600" fill="#6b8f3a" font-family="system-ui">that end holds the softening enzyme</text>
    </g>
    <g transform="translate(202,516)">
      <rect x="-176" y="-42" width="352" height="84" rx="12" fill="#eef8f0" stroke="#97c459" stroke-width="3"/>
      <text x="0" y="-8" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">IN CHINA THE GREEN IS THE POINT</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#5c7a29" font-family="system-ui">which one should I ferment next?</text>
    </g>'''.replace('@D1@', dente(-16, 10, '#3a8fb0', '#1f5f7d')) \
     .replace('@D2@', dente(16, 24, '#3a8fb0', '#1f5f7d'))


TEXTOS = {
    'titulo': 'Shorts animado — Cucumber with garlic (fermented)',
    'badge': '🥒 + GARLIC',
    'capdiv': 'Cucumber with garlic<small>the garlic turns blue, and that is fine</small>',
    'cenas': [
        ('s0', 5800, '%s 1 / 7' % TAG, 'It is not spoiled',
         'blue garlic is a reaction, not mould', '#3a8fb0'),
        ('s1', 6200, '%s 2 / 7' % TAG, 'One jar, two directions',
         'the cucumber floats, the garlic sinks', '#639922'),
        ('s2', 6600, '%s 3 / 7' % TAG, 'Stronger than cabbage',
         'and the reason is all that water', '#8a6a2f'),
        ('s3', 6600, '%s 4 / 7' % TAG, 'The garlic is not just flavour',
         'it carries the culture in with it', '#1d9e75'),
        ('s4', 6800, '%s 5 / 7' % TAG, 'Why the garlic does not stop it',
         'the defence is only temporary', '#d9b872'),
        ('s5', 6600, '%s 6 / 7' % TAG, 'This is the good sign',
         'the colour arrives with the acid', '#1f5f7d'),
        ('s6', 6400, '%s 7 / 7' % TAG, 'One last thing',
         'trim the blossom end before you start', '#2f5c0d'),
    ],
}


def monta_cenas(t):
    """Devolve o bloco INTEIRO de cada cena, ja' com a tag <svg> em volta.

    A tag tem de vir junto: o regex de troca casa `<svg ...>...</svg>` inteiro,
    entao substituir so' pelo miolo APAGA o <svg>.
    """
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
    print('template : %s (%d bytes, %s)' % (TEMPLATE, len(d), 'CRLF' if eol == '\r\n' else 'LF'))
    t = TEXTOS

    # ---- 1. as 7 cenas (regex; so' a 1a linha leva o recuo)
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

    # ---- 2. cabecalho
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

    # ---- 3. barra de legenda
    m = re.search(r'const scenes = \[.*?\n\];', d, re.S)
    if not m:
        print('ERRO: nao achei `const scenes`')
        return 1
    d = d.replace(m.group(0), monta_array(t['cenas']).replace('\n', eol), 1)

    # ---- 4. prova de que os keyframes continuam todos usados
    defs = set(re.findall(r'@keyframes\s+(\w+)', d))
    usados = set(re.findall(r'animation:\s*([\w-]+)', d))
    orfaos = defs - usados
    if orfaos:
        print('ERRO: keyframe nunca usado: %s' % sorted(orfaos))
        return 1

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with io.open(DESTINO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('%-42s %d bytes | %d cenas | keyframes %d/%d'
          % (DESTINO, len(d.encode('utf-8')), len(t['cenas']),
             len(usados & defs), len(defs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

# -*- coding: utf-8 -*-
"""_criar-pao.py — cria o short NOVO de FERMENTACAO DE PAO (levain), EN e PT.

    python _criar-pao.py

Por que: nao existia nada de pao na serie (nenhum arquivo com 'pao'/'bread'/
'sourdough'/'fermento'). Este e' o primeiro video realmente novo desde o #20.

Como: o motor, o CSS, o modo ?rec e a estrutura de 7 cenas vem do template do
#18 (`cenoura/shorts-carrot-apple-en.html`) — que e' o template mais novo e
validado da serie. O que se troca e' **o desenho das 7 cenas** e o texto.

As 7 cenas saem por REGEX (`<svg class="scene" ... id="sN">...</svg>`), nao por
ancora literal: sao ~40 linhas de SVG cada, e copiar isso a mao e' a maneira mais
facil de errar recuo. So' a PRIMEIRA linha do bloco leva o recuo da cena.

Os 6 keyframes do template tem de continuar TODOS usados, senao o
`_validar-short.py` reprova com "@keyframes nunca usado". Mapa:
  chop2x   -> a colher mexendo no pote (cena 3)
  pour2x   -> a agua caindo (cena 1)
  riseFast -> as bolhas subindo (cena 1)
  wobble   -> o pote e a massa (cenas 1, 5, 6)
  tick     -> os dois termometros (cena 4)
  pulseBadge -> o selo (vem do CSS, nao da cena)

Substancia (pesquisada, nao inventada):
  - o levain e' uma simbiose de levedura selvagem + bacterias lacticas (LAB);
    as bacterias superam a levedura em ~100:1;
  - a levedura faz CO2 e etanol (e' ela que levanta); as LAB fazem acido lactico
    (suave, lacteo) e acetico (agudo, de vinagre) — a proporcao e' o sabor;
  - LAB gostam de 30-35 °C, a levedura de ~25 °C. Quente = mais lactico = mais
    suave; frio (20-24 °C) = mais acetico = mais acido;
  - a alimentacao 1:1:1 (mesmo PESO) e' o que mantem a cultura estavel;
  - o pao cresce porque o CO2 fica preso na rede de gluten;
  - o "teste da colher": uma colher de levain maduro boia;
  - rosa ou laranja = mofo, joga fora. Liquido escuro em cima = alcool, mistura.
"""
import io
import os
import re
import sys

TEMPLATE = 'cenoura/shorts-carrot-apple-en.html'
DEST_EN = 'pao/shorts-sourdough-en.html'
DEST_PT = 'pao/shorts-sourdough.html'

# --------------------------------------------------------------- contraste
# As 12 trocas abaixo sairam do `_consertar-pao-contraste.py`, que foi rodado
# ANTES de existir este gerador. Ficam AQUI, e nao num script a parte, porque o
# gerador e' a fonte da verdade: sem isto, regerar o short desfazia o conserto
# e o pote voltava a ler como bloco vazio.
#
# Medido com `_medir-contraste-pao.py` (limite ~130 = "da' pra ver"):
#
#   cena 0  pote de vidro sobre o halo .........  52  FRACO
#   cena 0  levain dentro do pote ..............  66  FRACO  -> pote = BLOCO VAZIO
#   cena 2  circulo levain x circulo farinha ...  14  INVISIVEL -> eram o MESMO
#   cena 4  massa sobre o halo .................   2  INVISIVEL -> a massa ERA o halo
#
# DEPOIS: 154 (levain no pote) / 141 (levain x farinha) / 131 (massa x halo).
#
# O `velho` e' o desenho que as funcoes s0()/s2()/s4() deste arquivo emitem
# (o mesmo markup do template), entao a lista casa no arquivo recem-gerado.
# As entradas com quebra de linha usam '\n'; o laco 3c converte para o `eol`
# do arquivo antes de contar.
CONTRASTE = [
    # ------------------------------------------------------- cena 0: o pote
    ('<path d="M-44,66 L-44,-6 Q-44,-22 -28,-22 L28,-22 Q44,-22 44,-6 L44,66 Z" fill="#efe0bd"/>',
     '<path d="M-44,74 L-44,-6 Q-44,-22 -28,-22 L28,-22 Q44,-22 44,-6 L44,74 Z" fill="#d9b872"/>', 1),
    ('<path d="M-46,54 Q-42,2 -15,-8 Q10,-18 27,1 Q44,19 42,54 Z" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="3"/>',
     '<path d="M-46,54 Q-42,2 -15,-8 Q10,-18 27,1 Q44,19 42,54 Z" fill="#f2e6c9" stroke="#b08f4e" stroke-width="3.5"/>', 1),
    ('<path d="M-10,-18 Q0,-30 10,-18 Q10,-4 0,12 Q-10,-4 -10,-18Z" fill="#7fb2e0" stroke="#3d7ab5" stroke-width="2.5"/>',
     '<path d="M-14,-24 Q0,-40 14,-24 Q14,-4 0,16 Q-14,-4 -14,-24Z" fill="#7fb2e0" stroke="#3d7ab5" stroke-width="2.5"/>', 1),

    # --------------------------------------------------- cena 2: os 3 circulos
    ('<circle cx="0" cy="0" r="40" fill="#efe0bd" stroke="#8a6a3b" stroke-width="3"/>',
     '<circle cx="0" cy="0" r="40" fill="#d9b872" stroke="#8a6a3b" stroke-width="3"/>', 1),
    ('<circle cx="0" cy="0" r="40" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="3"/>',
     '<circle cx="0" cy="0" r="40" fill="#fbf7ec" stroke="#c9ab6d" stroke-width="3"/>', 1),
    ('<circle cx="0" cy="0" r="40" fill="#e6f1fb" stroke="#3d7ab5" stroke-width="3"/>',
     '<circle cx="0" cy="0" r="40" fill="#6fb0dd" stroke="#1f5c8a" stroke-width="3"/>', 1),
    # o "1 : 1 : 1" ja' diz que e' 1 de cada: os tres rotulos eram ruido.
    ('      <text x="0" y="64" text-anchor="middle" font-size="13" font-weight="700" fill="#8a6a3b" font-family="system-ui">1</text>\n',
     '', 2),
    ('      <text x="0" y="64" text-anchor="middle" font-size="13" font-weight="700" fill="#3d7ab5" font-family="system-ui">1</text>\n',
     '', 1),
    # a "colher" era um pirulito (cabo fino + bolinha) — agora tem cabo e cuia.
    ('    <g transform="translate(202,556)">\n'
     '      <g style="animation:chop2x .7s ease-in-out infinite">\n'
     '        <rect x="-4" y="-52" width="8" height="46" rx="3" fill="#8a6a3b"/>\n'
     '        <ellipse cx="0" cy="6" rx="16" ry="11" fill="#d9c9a3" stroke="#8a6a3b" stroke-width="2.5"/>\n'
     '      </g>\n'
     '    </g>',
     '    <g transform="translate(202,552)">\n'
     '      <g style="animation:chop2x .7s ease-in-out infinite">\n'
     '        <g transform="rotate(-22)">\n'
     '          <path d="M-3.5,-66 L3.5,-66 L5,-10 L-5,-10 Z" fill="#c0ab7d" stroke="#8a6a3b" stroke-width="2"/>\n'
     '          <ellipse cx="0" cy="10" rx="20" ry="15" fill="#efe0bd" stroke="#8a6a3b" stroke-width="2.5"/>\n'
     '          <ellipse cx="0" cy="10" rx="11" ry="7" fill="#d9c9a3"/>\n'
     '        </g>\n'
     '      </g>\n'
     '    </g>', 1),

    # ----------------------------------------------------- cena 4: a massa
    ('<circle cx="202" cy="282" r="140" fill="#e8d9b5" opacity=".5"/>',
     '<circle cx="202" cy="282" r="140" fill="#e8d9b5" opacity=".35"/>', 1),
    ('<circle cx="0" cy="0" r="104" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="4"/>',
     '<circle cx="0" cy="0" r="104" fill="#d4ad64" stroke="#a9713a" stroke-width="4"/>', 1),
    ('<g stroke="#c9ab6d" stroke-width="2.5" fill="none" opacity=".85">',
     '<g stroke="#7a4d1c" stroke-width="2.5" fill="none" opacity=".85">', 1),
]


def cena(cid, corpo, primeira=False):
    cls = 'scene on' if primeira else 'scene'
    return ('  <svg class="%s" id="%s" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">\n'
            % (cls, cid)) + corpo + '\n  </svg>'


# ---------------------------------------------------------------- cena 1: gancho
def s0(t):
    return '''    <rect width="405" height="720" fill="#faf3e3"/>
    <circle cx="202" cy="296" r="142" fill="#e8d9b5" opacity=".55"/>
    <g transform="translate(148,296)">
      <path d="M-44,108 L-44,-56 Q-44,-72 -28,-72 L28,-72 Q44,-72 44,-56 L44,108 Z" fill="#fffdf6" stroke="#8a6a3b" stroke-width="4"/>
      <path d="M-44,66 L-44,-6 Q-44,-22 -28,-22 L28,-22 Q44,-22 44,-6 L44,66 Z" fill="#efe0bd"/>
      <rect x="-44" y="-72" width="88" height="20" rx="6" fill="#e8d9b5" stroke="#8a6a3b" stroke-width="4"/>
      <g style="animation:riseFast 1.3s ease-out infinite">
        <circle cx="-20" cy="34" r="5.2" fill="#fff" opacity=".9"/>
        <circle cx="6" cy="42" r="4.2" fill="#fff" opacity=".85"/>
        <circle cx="26" cy="32" r="4.8" fill="#fff" opacity=".9"/>
      </g>
      <g style="animation:riseFast 1.3s ease-out .45s infinite">
        <circle cx="-8" cy="48" r="4.4" fill="#fff" opacity=".7"/>
        <circle cx="20" cy="52" r="5" fill="#fff" opacity=".7"/>
      </g>
      <g style="animation:riseFast 1.3s ease-out .9s infinite">
        <circle cx="-26" cy="54" r="4" fill="#fff" opacity=".55"/>
        <circle cx="12" cy="60" r="4.4" fill="#fff" opacity=".55"/>
      </g>
      <ellipse cx="-26" cy="-30" rx="7" ry="30" fill="#fff" opacity=".35"/>
    </g>
    <g transform="translate(300,332)">
      <path d="M-46,54 Q-42,2 -15,-8 Q10,-18 27,1 Q44,19 42,54 Z" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="3"/>
      <text x="0" y="92" text-anchor="middle" font-size="15" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
    </g>
    <g transform="translate(300,196)">
      <g style="animation:pour2x 1.4s ease-out infinite">
        <path d="M-10,-18 Q0,-30 10,-18 Q10,-4 0,12 Q-10,-4 -10,-18Z" fill="#7fb2e0" stroke="#3d7ab5" stroke-width="2.5"/>
      </g>
      <text x="0" y="50" text-anchor="middle" font-size="15" font-weight="800" fill="#1f4e79" font-family="system-ui">%s</text>
    </g>''' % (t['farinha'], t['agua'])


# ---------------------------------------------------------------- cena 2: as duas vidas
def s1(t):
    return '''    <rect width="405" height="720" fill="#faf3e3"/>
    <ellipse cx="202" cy="546" rx="168" ry="36" fill="#e8d9b5" opacity=".4"/>
    <g transform="translate(106,282)">
      <g style="animation:wobble 2.6s ease-in-out infinite">
        <circle cx="0" cy="0" r="54" fill="#f2e6c9" stroke="#8a6a3b" stroke-width="3.5"/>
        <circle cx="-16" cy="-8" r="12" fill="#fffdf6" stroke="#8a6a3b" stroke-width="2.5"/>
        <circle cx="14" cy="10" r="9" fill="#fffdf6" stroke="#8a6a3b" stroke-width="2.5"/>
        <circle cx="6" cy="-22" r="7" fill="#fffdf6" stroke="#8a6a3b" stroke-width="2.5"/>
      </g>
      <text x="0" y="86" text-anchor="middle" font-size="16" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
      <text x="0" y="106" text-anchor="middle" font-size="12" font-weight="600" fill="#a9713a" font-family="system-ui">%s</text>
    </g>
    <g transform="translate(298,282)">
      <g style="animation:tick 2.2s ease-in-out infinite">
        <rect x="-42" y="-20" width="84" height="40" rx="20" fill="#e6f1fb" stroke="#3d7ab5" stroke-width="3.5"/>
        <circle cx="-16" cy="0" r="6" fill="#9fc7e8"/>
        <circle cx="10" cy="0" r="6" fill="#9fc7e8"/>
        <circle cx="34" cy="0" r="6" fill="#9fc7e8"/>
      </g>
      <text x="0" y="86" text-anchor="middle" font-size="16" font-weight="800" fill="#1f4e79" font-family="system-ui">%s</text>
      <text x="0" y="106" text-anchor="middle" font-size="12" font-weight="600" fill="#3d7ab5" font-family="system-ui">%s</text>
    </g>
    <g transform="translate(202,470)">
      <rect x="-152" y="-38" width="304" height="76" rx="12" fill="#fff" stroke="#8a6a3b" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="19" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
      <text x="0" y="24" text-anchor="middle" font-size="14" font-weight="600" fill="#a9713a" font-family="system-ui">%s</text>
    </g>''' % (t['levedura'], t['levedura_sub'], t['bacteria'], t['bacteria_sub'],
                t['s1_cx'], t['s1_cx_sub'])


# ---------------------------------------------------------------- cena 3: 1:1:1
def s2(t):
    return '''    <rect width="405" height="720" fill="#faf3e3"/>
    <g transform="translate(202,268)">
      <rect x="-152" y="-54" width="304" height="108" rx="14" fill="#fffdf6" stroke="#8a6a3b" stroke-width="3.5"/>
      <text x="0" y="10" text-anchor="middle" font-size="44" font-weight="800" fill="#6b4f22" font-family="system-ui">1 : 1 : 1</text>
      <text x="0" y="38" text-anchor="middle" font-size="13" font-weight="600" fill="#a9713a" font-family="system-ui">%s</text>
    </g>
    <g transform="translate(78,428)">
      <circle cx="0" cy="0" r="40" fill="#efe0bd" stroke="#8a6a3b" stroke-width="3"/>
      <text x="0" y="6" text-anchor="middle" font-size="14" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
      <text x="0" y="64" text-anchor="middle" font-size="13" font-weight="700" fill="#8a6a3b" font-family="system-ui">1</text>
    </g>
    <g transform="translate(202,428)">
      <circle cx="0" cy="0" r="40" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="3"/>
      <text x="0" y="6" text-anchor="middle" font-size="14" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
      <text x="0" y="64" text-anchor="middle" font-size="13" font-weight="700" fill="#8a6a3b" font-family="system-ui">1</text>
    </g>
    <g transform="translate(326,428)">
      <circle cx="0" cy="0" r="40" fill="#e6f1fb" stroke="#3d7ab5" stroke-width="3"/>
      <text x="0" y="6" text-anchor="middle" font-size="14" font-weight="800" fill="#1f4e79" font-family="system-ui">%s</text>
      <text x="0" y="64" text-anchor="middle" font-size="13" font-weight="700" fill="#3d7ab5" font-family="system-ui">1</text>
    </g>
    <g transform="translate(202,556)">
      <g style="animation:chop2x .7s ease-in-out infinite">
        <rect x="-4" y="-52" width="8" height="46" rx="3" fill="#8a6a3b"/>
        <ellipse cx="0" cy="6" rx="16" ry="11" fill="#d9c9a3" stroke="#8a6a3b" stroke-width="2.5"/>
      </g>
    </g>''' % (t['s2_cx_sub'], t['levain'], t['farinha'], t['agua'])


# ---------------------------------------------------------------- cena 4: temperatura
def s3(t):
    return '''    <rect width="405" height="720" fill="#faf3e3"/>
    <g transform="translate(98,272)">
      <g style="animation:tick 2.4s ease-in-out infinite">
        <rect x="-16" y="-96" width="32" height="150" rx="16" fill="#fffdf6" stroke="#8a6a3b" stroke-width="3.5"/>
        <rect x="-9" y="-40" width="18" height="88" rx="9" fill="#e08a3c"/>
        <circle cx="0" cy="62" r="26" fill="#e08a3c" stroke="#8a6a3b" stroke-width="3.5"/>
      </g>
      <text x="0" y="132" text-anchor="middle" font-size="17" font-weight="800" fill="#8a4b12" font-family="system-ui">%s</text>
      <text x="0" y="154" text-anchor="middle" font-size="12" font-weight="600" fill="#a9713a" font-family="system-ui">%s</text>
    </g>
    <g transform="translate(304,272)">
      <g style="animation:tick 2.4s ease-in-out infinite">
        <rect x="-16" y="-96" width="32" height="150" rx="16" fill="#fffdf6" stroke="#8a6a3b" stroke-width="3.5"/>
        <rect x="-9" y="-10" width="18" height="58" rx="9" fill="#3d7ab5"/>
        <circle cx="0" cy="62" r="26" fill="#3d7ab5" stroke="#8a6a3b" stroke-width="3.5"/>
      </g>
      <text x="0" y="132" text-anchor="middle" font-size="17" font-weight="800" fill="#1f4e79" font-family="system-ui">%s</text>
      <text x="0" y="154" text-anchor="middle" font-size="12" font-weight="600" fill="#3d7ab5" font-family="system-ui">%s</text>
    </g>
    <g transform="translate(202,470)">
      <rect x="-152" y="-38" width="304" height="76" rx="12" fill="#fff" stroke="#8a6a3b" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="18" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
      <text x="0" y="24" text-anchor="middle" font-size="14" font-weight="600" fill="#a9713a" font-family="system-ui">%s</text>
    </g>''' % (t['quente'], t['quente_sub'], t['frio'], t['frio_sub'], t['s3_cx'], t['s3_cx_sub'])


# ---------------------------------------------------------------- cena 5: o gluten
def s4(t):
    return '''    <rect width="405" height="720" fill="#faf3e3"/>
    <circle cx="202" cy="282" r="140" fill="#e8d9b5" opacity=".5"/>
    <g transform="translate(202,282)">
      <g style="animation:wobble 2.8s ease-in-out infinite">
        <circle cx="0" cy="0" r="104" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="4"/>
        <g stroke="#c9ab6d" stroke-width="2.5" fill="none" opacity=".85">
          <path d="M-96,-20 Q-40,-60 0,-30 Q44,-4 92,-34"/>
          <path d="M-88,26 Q-30,-8 12,26 Q56,58 94,22"/>
          <path d="M-50,-92 Q-20,-40 8,-86"/>
          <path d="M-30,92 Q4,44 40,88"/>
        </g>
        <circle cx="-34" cy="-10" r="13" fill="#fff" opacity=".95"/>
        <circle cx="26" cy="-46" r="9" fill="#fff" opacity=".95"/>
        <circle cx="46" cy="14" r="15" fill="#fff" opacity=".95"/>
        <circle cx="-16" cy="44" r="11" fill="#fff" opacity=".95"/>
        <circle cx="8" cy="-6" r="7" fill="#fff" opacity=".9"/>
      </g>
    </g>
    <g transform="translate(202,462)">
      <text x="0" y="0" text-anchor="middle" font-size="21" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
      <text x="0" y="30" text-anchor="middle" font-size="14" font-weight="600" fill="#a9713a" font-family="system-ui">%s</text>
    </g>''' % (t['s4_t'], t['s4_t_sub'])


# ---------------------------------------------------------------- cena 6: o teste
def s5(t):
    return '''    <rect width="405" height="720" fill="#f1efe8"/>
    <circle cx="202" cy="282" r="130" fill="#d3d1c7" opacity=".4"/>
    <g transform="translate(202,278)">
      <path d="M-70,-40 L70,-40 L60,104 Q0,122 -60,104 Z" fill="#e6f1fb" stroke="#3d7ab5" stroke-width="3.5"/>
      <rect x="-64" y="-30" width="128" height="14" rx="4" fill="#b5d4f4"/>
      <g style="animation:wobble 2.6s ease-in-out infinite">
        <ellipse cx="0" cy="4" rx="42" ry="22" fill="#efe0bd" stroke="#8a6a3b" stroke-width="3"/>
        <circle cx="-14" cy="2" r="5" fill="#fff" opacity=".9"/>
        <circle cx="12" cy="8" r="4" fill="#fff" opacity=".9"/>
      </g>
    </g>
    <g transform="translate(202,462)">
      <rect x="-126" y="-32" width="252" height="64" rx="12" fill="#faf3e3" stroke="#8a6a3b" stroke-width="3"/>
      <text x="0" y="9" text-anchor="middle" font-size="21" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
    </g>
    <g transform="translate(202,544)">
      <text x="0" y="0" text-anchor="middle" font-size="14" font-weight="600" fill="#8a6a3b" font-family="system-ui">%s</text>
    </g>''' % (t['s5_pill'], t['s5_t'])


# ---------------------------------------------------------------- cena 7: o erro sem volta
def s6(t):
    return '''    <rect width="405" height="720" fill="#faf3e3"/>
    <circle cx="202" cy="248" r="126" fill="#e8d9b5" opacity=".55"/>
    <g transform="translate(202,248)">
      <circle cx="0" cy="0" r="80" fill="#fffdf6" stroke="#8a6a3b" stroke-width="4"/>
      <circle cx="-26" cy="-22" r="17" fill="#e8a3b8"/>
      <circle cx="20" cy="-30" r="12" fill="#e8a3b8"/>
      <circle cx="34" cy="20" r="15" fill="#e8a3b8"/>
      <circle cx="-18" cy="34" r="11" fill="#e8a3b8"/>
      <circle cx="-2" cy="2" r="9" fill="#e8a3b8"/>
    </g>
    <g transform="translate(202,398)">
      <text x="0" y="0" text-anchor="middle" font-size="21" font-weight="800" fill="#8a3b52" font-family="system-ui">%s</text>
      <text x="0" y="28" text-anchor="middle" font-size="14" font-weight="600" fill="#a9713a" font-family="system-ui">%s</text>
    </g>
    <g transform="translate(202,500)">
      <rect x="-154" y="-40" width="308" height="80" rx="12" fill="#fff" stroke="#8a6a3b" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="15" font-weight="800" fill="#6b4f22" font-family="system-ui">%s</text>
      <text x="0" y="22" text-anchor="middle" font-size="13" font-weight="600" fill="#a9713a" font-family="system-ui">%s</text>
    </g>''' % (t['s6_t'], t['s6_t_sub'], t['s6_cx'], t['s6_cx_sub'])


# ================================================================ textos
TEXTOS = {
    'en': {
        'titulo': 'Shorts animado — Sourdough starter (fermented)',
        'badge': '🍞 + LEVAIN',
        'capdiv': 'Sourdough starter<small>flour and water, and time</small>',
        'farinha': 'flour', 'agua': 'water', 'levain': 'starter',
        'levedura': 'yeast', 'levedura_sub': 'lifts the dough',
        'bacteria': 'bacteria', 'bacteria_sub': 'makes it sour',
        's1_cx': 'YEAST + BACTERIA', 's1_cx_sub': '100 bacteria for every yeast',
        's2_cx_sub': 'weight, not volume',
        'quente': '30-35 °C', 'quente_sub': 'milder',
        'frio': '20-24 °C', 'frio_sub': 'sharper',
        's3_cx': 'TEMPERATURE DECIDES', 's3_cx_sub': 'between 20 and 35 °C',
        's4_t': 'THE GLUTEN HOLDS THE GAS',
        's4_t_sub': 'that is what makes the bread rise',
        's5_pill': '5 TO 10 DAYS', 's5_t': 'the spoon floats when it is ready',
        's6_t': 'PINK OR ORANGE = OUT', 's6_t_sub': 'do not try to save it',
        's6_cx': 'DARK LIQUID ON TOP?',
        's6_cx_sub': 'that is alcohol - stir it back in',
        'cenas': [
            ('s0', 5600, 'SOURDOUGH 1 / 7', 'Flour and water, nothing else',
             'a starter is a culture, not a recipe', '#a9713a'),
            ('s1', 6600, 'SOURDOUGH 2 / 7', 'Two lives in one jar',
             'they keep each other alive', '#3d7ab5'),
            ('s2', 6200, 'SOURDOUGH 3 / 7', 'Feed it every day',
             'equal parts of starter, flour and water', '#8a6a3b'),
            ('s3', 6800, 'SOURDOUGH 4 / 7', 'Warm is mild, cool is sharp',
             'you choose with the thermometer', '#e08a3c'),
            ('s4', 6200, 'SOURDOUGH 5 / 7', 'The bubbles stay trapped',
             'the gluten net holds them in', '#c9ab6d'),
            ('s5', 6000, 'SOURDOUGH 6 / 7', 'Ready in 5 to 10 days',
             'then keep it in the fridge', '#5f5e5a'),
            ('s6', 7000, 'SOURDOUGH 7 / 7', 'The one mistake with no way back',
             'mould goes right through the whole jar', '#8a3b52'),
        ],
    },
    'pt': {
        'titulo': 'Shorts animado — Levain (fermentação de pão)',
        'badge': '🍞 + LEVAIN',
        'capdiv': 'Levain<small>farinha e água, e tempo</small>',
        'farinha': 'farinha', 'agua': 'água', 'levain': 'levain',
        'levedura': 'levedura', 'levedura_sub': 'levanta a massa',
        'bacteria': 'bactéria', 'bacteria_sub': 'deixa azedinho',
        's1_cx': 'LEVEDURA + BACTÉRIA', 's1_cx_sub': '100 bactérias para cada levedura',
        's2_cx_sub': 'peso, não volume',
        'quente': '30-35 °C', 'quente_sub': 'mais suave',
        'frio': '20-24 °C', 'frio_sub': 'mais ácido',
        's3_cx': 'A TEMPERATURA MANDA', 's3_cx_sub': 'entre 20 e 35 °C',
        's4_t': 'O GLÚTEN SEGURA O GÁS',
        's4_t_sub': 'é isso que faz o pão crescer',
        's5_pill': '5 A 10 DIAS', 's5_t': 'a colher boia quando está pronta',
        's6_t': 'ROSA OU LARANJA = FORA', 's6_t_sub': 'não tente salvar',
        's6_cx': 'LÍQUIDO ESCURO EM CIMA?',
        's6_cx_sub': 'é álcool - misture de volta',
        'cenas': [
            ('s0', 5600, 'LEVAIN 1 / 7', 'Farinha e água, só isso',
             'levain é cultura, não receita', '#a9713a'),
            ('s1', 6600, 'LEVAIN 2 / 7', 'Duas vidas no mesmo jarro',
             'uma não vive sem a outra', '#3d7ab5'),
            ('s2', 6200, 'LEVAIN 3 / 7', 'Alimente todo dia',
             'partes iguais de levain, farinha e água', '#8a6a3b'),
            ('s3', 6800, 'LEVAIN 4 / 7', 'Quente é suave, frio é ácido',
             'você escolhe no termômetro', '#e08a3c'),
            ('s4', 6200, 'LEVAIN 5 / 7', 'As bolhas ficam presas',
             'a rede de glúten segura elas', '#c9ab6d'),
            ('s5', 6000, 'LEVAIN 6 / 7', 'Pronto em 5 a 10 dias',
             'depois guarde na geladeira', '#5f5e5a'),
            ('s6', 7000, 'LEVAIN 7 / 7', 'O único erro sem volta',
             'o mofo atravessa o pote inteiro', '#8a3b52'),
        ],
    },
}


def monta_cenas(t):
    """Devolve o bloco INTEIRO de cada cena, ja' com a tag <svg> em volta.

    A tag tem de vir junto: o regex de troca casa `<svg ...>...</svg>` inteiro,
    entao substituir so' pelo miolo APAGA o <svg> (foi o que aconteceu na 1a
    versao — o arquivo saiu com 0 tags <svg> e o validador acusou
    `svg ids != js ids -> []`).
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
        base = fh.read()
    eol = '\r\n' if base.count('\r\n') else '\n'
    print('template   : %s (%d bytes, %s)'
          % (TEMPLATE, len(base), 'CRLF' if eol == '\r\n' else 'LF'))

    for lingua, destino in (('en', DEST_EN), ('pt', DEST_PT)):
        t = TEXTOS[lingua]
        d = base
        novo = monta_cenas(t)

        # ---- 1. troca as 7 cenas (regex; so' a 1a linha leva o recuo)
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
            ('<html lang="en">', '<html lang="%s">' % ('en' if lingua == 'en' else 'pt-BR')),
            ('<title>Shorts animado — Carrot with apple (fermented)</title>',
             '<title>%s</title>' % t['titulo']),
            ('>🥕 + APPLE</div>', '>%s</div>' % t['badge']),
            ('>SCENE 1 / 7</div>', '>%s</div>' % t['cenas'][0][2]),
            ('<div class="cap" id="cap">Carrot with apple<small>the sweet one - and it fizzes</small></div>',
             '<div class="cap" id="cap">%s</div>' % t['capdiv']),
        ]
        for velho, novo_txt in trocas:
            if d.count(velho) != 1:
                print('ERRO (%s): ancora casou %d vez(es): %s'
                      % (lingua, d.count(velho), velho[:60]))
                return 1
            d = d.replace(velho, novo_txt)

        # ---- 3. barra de legenda
        m = re.search(r'const scenes = \[.*?\n\];', d, re.S)
        if not m:
            print('ERRO (%s): nao achei `const scenes`' % lingua)
            return 1
        d = d.replace(m.group(0), monta_array(t['cenas']).replace('\n', eol), 1)

        # ---- 3b. botoes: so' o PT precisa (o EN ja' nasce com 'Pause'/'Watch').
        #      O `_sobras-vs-original.py` pegou isto: a barra de legenda estava
        #      traduzida e o botao nao, porque o botao nao esta' em `cap:`/`sub:`
        #      nem e' no de texto do corpo — o extrator nao o ve'.
        if lingua == 'pt':
            for vb, nb, esp in (('⏸ Pause', '⏸ Pausar', 2),
                                ("'▶ Watch'", "'▶ Assistir'", 1)):
                c = d.count(vb)
                if c != esp:
                    print('ERRO (pt): botao %r casou %d (esperado %d)'
                          % (vb, c, esp))
                    return 1
                d = d.replace(vb, nb)

        # ---- 3c. contraste. Medido com `_medir-contraste-pao.py`; os numeros
        #      antes/depois estao no docstring do `_consertar-pao-contraste.py`.
        #      Fica AQUI, e nao num script separado, para o gerador continuar
        #      sendo a fonte da verdade: sem isto, regerar o short desfazia o
        #      conserto e o pote voltava a ler como bloco vazio.
        for vc, nc, esp in CONTRASTE:
            vc = vc.replace('\n', eol)
            nc = nc.replace('\n', eol)
            c = d.count(vc)
            if c != esp:
                print('ERRO (%s): contraste %r casou %d (esperado %d)'
                      % (lingua, vc[:44], c, esp))
                return 1
            d = d.replace(vc, nc)

        # ---- 4. prova de que os 6 keyframes continuam usados
        defs = set(re.findall(r'@keyframes\s+(\w+)', d))
        usados = set()
        for a in re.findall(r'animation:\s*([\w-]+)', d):
            usados.add(a)
        orfaos = defs - usados
        if orfaos:
            print('ERRO (%s): keyframe nunca usado: %s' % (lingua, sorted(orfaos)))
            return 1
        print('%-10s -> %s (%d bytes) | %d cenas | keyframes %d/%d'
              % (lingua, destino, len(d), len(t['cenas']), len(usados & defs), len(defs)))

        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with io.open(destino, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d)
    return 0


if __name__ == '__main__':
    sys.exit(main())

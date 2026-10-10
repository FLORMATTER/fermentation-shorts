# -*- coding: utf-8 -*-
"""_criar-kombucha.py — cria o short KOMBUCHA DE MELANCIA + MACA (EN).

    python _criar-kombucha.py

A serie ja' tem melancia em #4 (beterraba + melancia) e maca em #18/#20. O que
NAO existia era KOMBUCHA — e o assunto aqui nao e' o legume, e' a SEGUNDA
FERMENTACAO na garrafa.

Substancia (pesquisada, nao inventada):
  - a 2a fermentacao (2F) e' kombucha + fruta, engarrafada e FECHADA. A garrafa
    vira um vaso de pressao: a levedura continua comendo o acucar da fruta e
    soltando CO2, que nao tem para onde ir;
  - melancia e' ~92% agua. Ela traz AGUA e pouco acucar -> se entrar em volume
    igual, ela dilui o cha e a bebida sai aguada. Por isso 1 parte de suco para
    3 de kombucha (ou menos);
  - maca traz FRUTOSE, o acucar que a levedura fermenta mais facil. E' ela que
    garante a carbonatacao rapida — 1 a 3 dias em temperatura ambiente;
  - o espaco vazio no gargalo ("headspace") e' ~2,5 cm (1 polegada). Muito ar =
    fica choca; pouco ar = o gas nao tem onde se formar;
  - abrir a garrafa uma vez por dia (sobre a pia) libera a pressao. Garrafa
    fechada com levedura viva estoura de verdade;
  - a geladeira DESACELERA a levedura, nao a mata: por isso a garrafa vai para a
    geladeira quando esta' firme, e nao quando esta' "pronta".

Paleta: vermelho da melancia + verde da maca + ambar do cha.

O QUE O RENDER ENSINOU:
  - garrafa mais LARGA que ALTA le' como lata/vaso (a licao da silhueta) — a
    garrafa aqui e' 80x224;
  - o `%` em string de SVG quebra formatacao `%` do Python: aqui as cenas usam
    TOKENS (`@GARRAFA@`) e `.replace()`, e os helpers usam f-string.
"""
import io
import math
import os
import re
import sys

TEMPLATE = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'kombucha/shorts-watermelon-apple-en.html'

TAG = 'KOMBUCHA'
VERMELHO = '#e8556d'
VERM_ESC = '#c9334d'
VERDE = '#8cc152'
VERDE_ESC = '#4e7a26'
AMBAR = '#d9a441'


# ------------------------------------------------------------------ desenhos
def garrafa(liquido, tampa=True, s=1.0):
    """Garrafa de boca larga — 80 de largura por 224 de altura.

    Mais larga que alta leria como LATA; a silhueta vem antes da cor.
    """
    t = ''
    if tampa:
        t = ('<rect x="-19" y="-140" width="38" height="16" rx="5"'
             ' fill="#cfd8c4" stroke="#8a6a2f" stroke-width="3"/>'
             '<line x1="0" y1="-140" x2="0" y2="-124" stroke="#8a6a2f"'
             ' stroke-width="2"/>')
    return (f'<g transform="scale({s:g})">'
            '<path d="M-40,-56 L-40,70 Q-40,88 -22,88 L22,88 Q40,88 40,70 L40,-56'
            ' Q40,-70 26,-80 L14,-92 L14,-124 L-14,-124 L-14,-92 L-26,-80'
            ' Q-40,-70 -40,-56 Z" fill="#fdeef0" stroke="#c9334d"'
            ' stroke-width="4"/>'
            f'<path d="M-34,-28 L-34,66 Q-34,82 -20,82 L20,82 Q34,82 34,66 L34,-28'
            f' Q34,-42 22,-52 L12,-62 L12,-118 L-12,-118 L-12,-62 L-22,-52'
            f' Q-34,-42 -34,-28 Z" fill="{liquido}"/>'
            '<ellipse cx="-19" cy="18" rx="7" ry="42" fill="#fff" opacity=".22"/>'
            + t + '</g>')


def bolhas(cor='#fff', op='.8'):
    """Dois grupos de borbulha subindo (o `riseFast` da serie)."""
    return ('<g style="animation:riseFast 1.4s ease-out infinite">'
            f'<circle cx="-10" cy="52" r="4" fill="{cor}" opacity="{op}"/>'
            f'<circle cx="14" cy="62" r="3.2" fill="{cor}" opacity="{op}"/>'
            '</g>'
            '<g style="animation:riseFast 1.4s ease-out .5s infinite">'
            f'<circle cx="2" cy="44" r="3.6" fill="{cor}" opacity="{op}"/>'
            f'<circle cx="-24" cy="58" r="3" fill="{cor}" opacity="{op}"/>'
            '</g>')


def melancia(x, y, s=1.0):
    """Fatia semicircular: casca verde, faixa branca, polpa rosa, sementes."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<path d="M-86,0 A86,86 0 0 1 86,0 Z" fill="#7fb542" stroke="#4e7a26"'
            ' stroke-width="3"/>'
            '<path d="M-76,0 A76,76 0 0 1 76,0 Z" fill="#f4f7e8"/>'
            '<path d="M-68,0 A68,68 0 0 1 68,0 Z" fill="#e8556d"/>'
            '<ellipse cx="-30" cy="-30" rx="4" ry="6" fill="#3a2b2b"/>'
            '<ellipse cx="6" cy="-40" rx="4" ry="6" fill="#3a2b2b"/>'
            '<ellipse cx="38" cy="-20" rx="4" ry="6" fill="#3a2b2b"/>'
            '<ellipse cx="-10" cy="-16" rx="4" ry="6" fill="#3a2b2b"/>'
            '</g>')


def maca(x, y, s=1.0):
    """Maca inteira, verde: corpo + cabinho + folha."""
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


def floco(x, y, r=26, cor='#3a8fb0', w=3.5):
    """Floco de neve: 3 eixos + 6 pares de raminhos."""
    p = []
    for k in range(3):
        a = math.radians(60 * k)
        dx, dy = math.cos(a) * r, math.sin(a) * r
        p.append(f'<line x1="{-dx:g}" y1="{-dy:g}" x2="{dx:g}" y2="{dy:g}"'
                 f' stroke="{cor}" stroke-width="{w:g}" stroke-linecap="round"/>')
    for k in range(6):
        a = math.radians(60 * k)
        for t in (0.55, 1.0):
            bx, by = math.cos(a) * r * t, math.sin(a) * r * t
            for lado in (-1, 1):
                a2 = a + lado * math.radians(38)
                ex = bx + math.cos(a2) * r * 0.3
                ey = by + math.sin(a2) * r * 0.3
                p.append(f'<line x1="{bx:g}" y1="{by:g}" x2="{ex:g}" y2="{ey:g}"'
                         f' stroke="{cor}" stroke-width="{w * 0.7:g}"'
                         ' stroke-linecap="round"/>')
    return f'<g transform="translate({x:g},{y:g})">' + ''.join(p) + '</g>'


def medidor(x, y):
    """Jarra de medida que balanca (`chop2x`) — o medidor do 1:3."""
    return (f'<g transform="translate({x:g},{y:g})">'
            '<g style="animation:chop2x 1.6s ease-in-out infinite">'
            '<path d="M-22,-30 L-18,26 Q-17,32 -10,32 L10,32 Q17,32 18,26 L22,-30 Z"'
            ' fill="#fdeef0" stroke="#c9334d" stroke-width="3"/>'
            '<path d="M-15,2 L-12,26 Q-11,30 -6,30 L6,30 Q11,30 12,26 L15,2 Z"'
            ' fill="#e8556d"/>'
            '<line x1="-14" y1="-8" x2="14" y2="-8" stroke="#c9334d"'
            ' stroke-width="2" opacity=".7"/>'
            '<line x1="-15" y1="8" x2="15" y2="8" stroke="#c9334d"'
            ' stroke-width="2" opacity=".7"/>'
            '</g></g>')


# ---------------------------------------------------------------- cena 1: o gancho
def s0(t):
    return '''    <rect width="405" height="720" fill="#fff6f2"/>
    <circle cx="202" cy="296" r="152" fill="#fde3e6" opacity=".7"/>
    <g transform="translate(202,296)">
      <g style="animation:wobble 2.6s ease-in-out infinite">
        @GARRAFA@
        @BOLHAS@
      </g>
    </g>
    <g transform="translate(300,196)">
      <g style="animation:tick 1.6s ease-in-out infinite">
        <path d="M0,-28 L6,-9 L28,-7 L11,6 L17,28 L0,15 L-17,28 L-11,6 L-28,-7 L-6,-9 Z" fill="#f2c14e" stroke="#c98a1f" stroke-width="2.5" stroke-linejoin="round"/>
      </g>
    </g>
    <g transform="translate(202,506)">
      <rect x="-172" y="-46" width="344" height="92" rx="12" fill="#fff" stroke="#c9334d" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="20" font-weight="800" fill="#c9334d" font-family="system-ui">SEAL IT AND IT CAN BLOW</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#d4757f" font-family="system-ui">the sugar is still alive in there</text>
    </g>'''.replace('@GARRAFA@', garrafa(VERMELHO)) \
     .replace('@BOLHAS@', bolhas())


# ---------------------------------------------------------------- cena 2: duas frutas
def s1(t):
    return '''    <rect width="405" height="720" fill="#fff6f2"/>
    <circle cx="118" cy="286" r="104" fill="#fde3e6" opacity=".75"/>
    <circle cx="292" cy="286" r="98" fill="#eaf5dc" opacity=".85"/>
    <g transform="translate(118,320)">
      <g style="animation:wobble 3.0s ease-in-out infinite">
        @MELANCIA@
      </g>
    </g>
    <g transform="translate(292,296)">
      <g style="animation:wobble 2.7s ease-in-out infinite">
        @MACA@
      </g>
    </g>
    <text x="118" y="424" text-anchor="middle" font-size="14" font-weight="800" fill="#c9334d" font-family="system-ui">WATER</text>
    <text x="292" y="424" text-anchor="middle" font-size="14" font-weight="800" fill="#4e7a26" font-family="system-ui">SUGAR</text>
    <g transform="translate(202,516)">
      <rect x="-172" y="-46" width="344" height="92" rx="12" fill="#fff" stroke="#7fb542" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="19" font-weight="800" fill="#2f5c0d" font-family="system-ui">ONE THINS, ONE FEEDS</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#6b8f3a" font-family="system-ui">and the apple is the one that fizzes</text>
    </g>'''.replace('@MELANCIA@', melancia(0, 0)) \
     .replace('@MACA@', maca(0, 0, 0.85))


# ---------------------------------------------------------------- cena 3: a proporcao
def s2(t):
    return '''    <rect width="405" height="720" fill="#fff6f2"/>
    <g transform="translate(202,222)">
      <rect x="-172" y="-76" width="344" height="152" rx="14" fill="#fff" stroke="#c9334d" stroke-width="3.5"/>
      <text x="0" y="18" text-anchor="middle" font-size="56" font-weight="800" fill="#c9334d" font-family="system-ui">1 : 3</text>
      <text x="0" y="54" text-anchor="middle" font-size="14" font-weight="700" fill="#d4757f" font-family="system-ui">juice to kombucha</text>
    </g>
    @MEDIDOR@
    <g transform="translate(112,412)">
      <rect x="-66" y="-34" width="132" height="68" rx="10" fill="#fdeef0" stroke="#e8556d" stroke-width="2.5"/>
      <text x="0" y="2" text-anchor="middle" font-size="24" font-weight="800" fill="#c9334d" font-family="system-ui">1</text>
      <text x="0" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#d4757f" font-family="system-ui">watermelon</text>
    </g>
    <g transform="translate(292,412)">
      <rect x="-66" y="-34" width="132" height="68" rx="10" fill="#fff8e6" stroke="#d9a441" stroke-width="2.5"/>
      <text x="0" y="2" text-anchor="middle" font-size="24" font-weight="800" fill="#8a6a2f" font-family="system-ui">3</text>
      <text x="0" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#b08f4e" font-family="system-ui">kombucha</text>
    </g>
    <g transform="translate(202,528)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">WATERMELON IS 92% WATER</text>
      <text x="0" y="24" text-anchor="middle" font-size="13" font-weight="600" fill="#6b8f3a" font-family="system-ui">equal parts and you drink pink water</text>
    </g>'''.replace('@MEDIDOR@', medidor(316, 138))


# ---------------------------------------------------------------- cena 4: o espaco vazio
def s3(t):
    return '''    <rect width="405" height="720" fill="#fff6f2"/>
    <circle cx="202" cy="300" r="150" fill="#fde3e6" opacity=".6"/>
    <g transform="translate(202,300)">
      <g style="animation:wobble 2.9s ease-in-out infinite">
        @GARRAFA@
      </g>
    </g>
    <g transform="translate(202,258)">
      <line x1="-96" y1="0" x2="96" y2="0" stroke="#c98a1f" stroke-width="3" stroke-dasharray="7 5"/>
      <path d="M96,-8 L112,0 L96,8 Z" fill="#c98a1f"/>
      <path d="M-96,-8 L-112,0 L-96,8 Z" fill="#c98a1f"/>
    </g>
    <g transform="translate(202,196)">
      <rect x="-96" y="-24" width="192" height="40" rx="9" fill="#fff8e6" stroke="#d9a441" stroke-width="2.5"/>
      <text x="0" y="5" text-anchor="middle" font-size="16" font-weight="800" fill="#8a6a2f" font-family="system-ui">ONE INCH OF AIR</text>
    </g>
    <g transform="translate(202,512)">
      <rect x="-172" y="-46" width="344" height="92" rx="12" fill="#fff" stroke="#d9a441" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="19" font-weight="800" fill="#8a6a2f" font-family="system-ui">FILL IT TO THE MARK</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">too much air and it just stays flat</text>
    </g>'''.replace('@GARRAFA@', garrafa(VERMELHO))


# ---------------------------------------------------------------- cena 5: por que a maca
def s4(t):
    return '''    <rect width="405" height="720" fill="#fff6f2"/>
    <g transform="translate(202,214)">
      <rect x="-170" y="-56" width="340" height="112" rx="14" fill="#fff8e6" stroke="#d9a441" stroke-width="3.5"/>
      <text x="0" y="-12" text-anchor="middle" font-size="17" font-weight="800" fill="#8a6a2f" font-family="system-ui">THE APPLE, NOT THE MELON</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">fructose is the sugar yeast eats first</text>
    </g>
    <g transform="translate(202,372)">
      <g style="animation:tick 2.4s ease-in-out infinite">
        <path d="M0,-14 L8,-30 L-8,-30 Z" fill="#8a6a2f"/>
      </g>
      <line x1="-150" y1="0" x2="150" y2="0" stroke="#e6d9b6" stroke-width="3"/>
      <circle cx="-150" cy="0" r="11" fill="#d9a441"/>
      <circle cx="0" cy="0" r="11" fill="#8cc152"/>
      <circle cx="150" cy="0" r="11" fill="#4e7a26"/>
      <text x="-150" y="36" text-anchor="middle" font-size="11" font-weight="800" fill="#8a6a2f" font-family="system-ui">DAY 1</text>
      <text x="0" y="36" text-anchor="middle" font-size="11" font-weight="800" fill="#4e7a26" font-family="system-ui">DAY 2</text>
      <text x="150" y="36" text-anchor="middle" font-size="11" font-weight="800" fill="#2f5c0d" font-family="system-ui">DAY 3</text>
      <text x="-150" y="60" text-anchor="middle" font-size="12" font-weight="600" fill="#b08f4e" font-family="system-ui">still</text>
      <text x="0" y="60" text-anchor="middle" font-size="12" font-weight="600" fill="#6b8f3a" font-family="system-ui">fizzing</text>
      <text x="150" y="60" text-anchor="middle" font-size="12" font-weight="600" fill="#4e7a26" font-family="system-ui">firm</text>
    </g>
    <g transform="translate(202,516)">
      <rect x="-166" y="-40" width="332" height="80" rx="12" fill="#fff" stroke="#7fb542" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="#2f5c0d" font-family="system-ui">TWO DAYS IS USUALLY ENOUGH</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#6b8f3a" font-family="system-ui">room temperature, out of the sun</text>
    </g>'''


# ---------------------------------------------------------------- cena 6: abrir todo dia
def s5(t):
    return '''    <rect width="405" height="720" fill="#fff6f2"/>
    <circle cx="202" cy="308" r="146" fill="#fde3e6" opacity=".6"/>
    <g transform="translate(202,308)">
      <g style="animation:wobble 2.5s ease-in-out infinite">
        @GARRAFA@
      </g>
    </g>
    <g transform="translate(202,152)">
      <g style="animation:pour2x 1.6s ease-out infinite">
        <rect x="-19" y="-8" width="38" height="16" rx="5" fill="#cfd8c4" stroke="#8a6a2f" stroke-width="3"/>
      </g>
    </g>
    <g transform="translate(202,104)" stroke="#c98a1f" stroke-width="3.5" fill="none" stroke-linecap="round">
      <path d="M-40,10 C-30,-6 -18,-10 -8,-8"/>
      <path d="M0,2 L0,-16"/>
      <path d="M40,10 C30,-6 18,-10 8,-8"/>
    </g>
    <g transform="translate(202,502)">
      <rect x="-172" y="-46" width="344" height="92" rx="12" fill="#fff" stroke="#c98a1f" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="19" font-weight="800" fill="#8a6a2f" font-family="system-ui">OPEN IT EVERY DAY</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">over the sink, then close it again</text>
    </g>'''.replace('@GARRAFA@', garrafa(VERMELHO, tampa=False))


# ---------------------------------------------------------------- cena 7: firme = pronta
def s6(t):
    return '''    <rect width="405" height="720" fill="#fff6f2"/>
    <circle cx="168" cy="286" r="128" fill="#fde3e6" opacity=".65"/>
    <g transform="translate(168,286)">
      <g style="animation:wobble 2.8s ease-in-out infinite">
        @GARRAFA@
      </g>
    </g>
    <g transform="translate(322,196)">
      <g style="animation:tick 3.0s ease-in-out infinite">
        @FLOCO@
      </g>
    </g>
    <g transform="translate(322,316)">
      <rect x="-62" y="-30" width="124" height="60" rx="10" fill="#eef6fb" stroke="#3a8fb0" stroke-width="2.5"/>
      <text x="0" y="-2" text-anchor="middle" font-size="15" font-weight="800" fill="#1f5f7d" font-family="system-ui">FRIDGE</text>
      <text x="0" y="18" text-anchor="middle" font-size="11" font-weight="700" fill="#4a7f96" font-family="system-ui">slows, never stops</text>
    </g>
    <g transform="translate(202,428)">
      <rect x="-176" y="-44" width="352" height="88" rx="12" fill="#fff" stroke="#c9334d" stroke-width="3"/>
      <text x="0" y="-10" text-anchor="middle" font-size="18" font-weight="800" fill="#c9334d" font-family="system-ui">FIRM MEANS READY</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#d4757f" font-family="system-ui">cold slows the yeast, it does not kill it</text>
    </g>
    <g transform="translate(202,530)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">AND THEN YOU CHILL IT</text>
      <text x="0" y="24" text-anchor="middle" font-size="13" font-weight="600" fill="#6b8f3a" font-family="system-ui">which one should I ferment next?</text>
    </g>'''.replace('@GARRAFA@', garrafa(VERMELHO)) \
     .replace('@FLOCO@', floco(0, 0, 30))


# ---------------------------------------------------------------- montagem
TEXTOS = {
    'titulo': 'Shorts animado — Watermelon and apple kombucha (2nd ferment)',
    'badge': '🍉 + 🍎',
    'capdiv': 'Watermelon and apple kombucha<small>the bottle that fights back</small>',
    'cenas': [
        ('s0', 6400, '%s 1 / 7' % TAG, 'It can blow',
         'the sugar is still alive in there', VERM_ESC),
        ('s1', 6200, '%s 2 / 7' % TAG, 'Two fruits, two jobs',
         'one brings water, the other brings sugar', VERDE),
        ('s2', 6600, '%s 3 / 7' % TAG, 'One to three',
         'juice to kombucha, and no more', VERMELHO),
        ('s3', 6400, '%s 4 / 7' % TAG, 'Leave an inch',
         'too much air and it stays flat', AMBAR),
        ('s4', 6800, '%s 5 / 7' % TAG, 'The apple does the work',
         'fructose is the sugar yeast eats first', VERDE_ESC),
        ('s5', 6400, '%s 6 / 7' % TAG, 'Open it every day',
         'over the sink, then close it again', '#8a6a2f'),
        ('s6', 6600, '%s 7 / 7' % TAG, 'Firm means ready',
         'the fridge slows it, it never stops it', '#2f5c0d'),
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
    print('%-44s %d bytes | %d cenas | keyframes %d/%d'
          % (DESTINO, len(d.encode('utf-8')), len(t['cenas']),
             len(usados & defs), len(defs)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

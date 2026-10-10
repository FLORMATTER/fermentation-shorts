# -*- coding: utf-8 -*-
"""_criar-beterraba-cenoura.py — cria o short BETERRABA + CENOURA (EN).

    python _criar-beterraba-cenoura.py

🔴 Este e' o #25 da serie. Beterraba ja' apareceu em #3, #4, #8, #14 e #19;
cenoura em #12 e #18. A regra da serie e' "o formato pode repetir, a SUBSTANCIA
nao" — entao o video NAO pode ser "corte os dois e ponha sal".

O assunto AQUI e' outro, e e' o unico da serie: **a cenoura protege o vermelho
da beterraba.**

Substancia (pesquisada, com fonte):

  - **MDPI Applied Sciences 2023, 13, 6113** — fermentacao lactica de suco de
    beterraba, de cenoura e da MISTURA 1:1 (2% de NaCl, 28 C, 7 dias,
    *Lactiplantibacillus plantarum* / *Levilactobacillus brevis*):
      * todas as amostras chegaram a **pH abaixo de 4,5**; o menor pH foi **3,3**
        (beterraba + L. plantarum, 7 dias);
      * o suco de **cenoura** foi o de **maior pH** dos tres, e o de beterraba o
        de maior "extract" (solidos soluveis = acucar);
      * **a degradacao das betalainas foi SIGNIFICATIVAMENTE MENOR na mistura** —
        os autores atribuem isso a **protecao antioxidante dos carotenoides**;
      * apareceu **neobetanina** depois da fermentacao (pigmento que nao existe
        no suco fresco) e a betanina caiu um pouco;
      * beterraba e' o mais ESCURO (L* 2,5-7,5) e a cenoura o mais CLARO (L* 31-37);
      * recomendaram **4 a 5 dias**.
  - **pH (tabela FDA / webpal "Approximate pH of Foods")**: beterraba
    **5,30-6,60**, cenoura **5,88-6,40** — as duas **ACIMA de 4,6**. Para
    comparar: repolho cru 5,50-6,75 e chucrute 3,30-3,60 — e' a fermentacao que
    derruba. **4,6** e' a linha.
  - **Acucar**: beterraba ~**7 g/100 g**, cenoura ~**4,7 g/100 g** -> a beterraba
    carrega ~**50% mais acucar**. E' ela que alimenta a bacteria e produz o acido.

Paleta: roxo/magenta da beterraba + laranja da cenoura sobre creme.
"""

PALETA_NOTA = 'roxo da beterraba + laranja da cenoura (nunca usada junto na serie)'

import io
import math
import os
import re
import sys

TEMPLATE = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'beterraba/shorts-beet-carrot-en.html'

TAG = 'BEET+CARROT'
ROXO = '#8e3a68'
ROXO_ESC = '#5e2344'
ROXO_CLARO = '#b4648e'
LARANJA = '#e0801f'
LARANJA_ESC = '#a8541a'
VERDE = '#3f6b1e'
CREME = '#fffaf0'
PALIDO = '#e8b8cc'


# ------------------------------------------------------------------ desenhos
def beterraba(x, y, s=1.0):
    """Beterraba inteira: bulbo roxo, RAIZ comprida embaixo, folhas em cima.

    A raiz (cauda) e' o que faz ler "beterraba" em vez de "bolota roxa" — e as
    folhas dizem que e' raiz, nao fruta. O LIMBO tem de ser LARGO e com nervura:
    limbo fino le' como broto (1o render).
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            # hastes
            f'<path d="M-6,-40 C-18,-62 -32,-74 -42,-82" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M0,-42 C1,-68 4,-82 6,-94" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M7,-40 C19,-60 32,-70 42,-76" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            # folha esquerda
            f'<path d="M-42,-82 C-68,-98 -94,-90 -90,-72'
            ' C-82,-54 -54,-60 -42,-82 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M-42,-82 C-62,-86 -78,-82 -86,-76" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            # folha do meio
            f'<path d="M6,-94 C16,-122 42,-124 46,-105'
            ' C40,-86 20,-80 6,-94 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M6,-94 C20,-107 34,-114 44,-108" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            # folha direita
            f'<path d="M42,-76 C66,-86 88,-76 82,-60'
            ' C70,-46 50,-54 42,-76 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M42,-76 C60,-78 74,-72 80,-64" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            # bulbo
            f'<path d="M0,-44 C32,-44 52,-20 51,8 C50,34 30,56 0,56'
            f' C-30,56 -50,34 -51,8 C-52,-20 -32,-44 0,-44 Z"'
            f' fill="{ROXO}" stroke="{ROXO_ESC}" stroke-width="3.5"/>'
            # raiz comprida
            f'<path d="M0,54 C-1,72 -4,88 -10,102" stroke="{ROXO_ESC}"'
            ' stroke-width="4.5" fill="none" stroke-linecap="round"/>'
            # aneis de zoneamento
            f'<ellipse cy="-16" rx="36" ry="7" fill="none" stroke="{ROXO_CLARO}"'
            ' stroke-width="2.4" opacity=".75"/>'
            f'<ellipse cy="8" rx="30" ry="6" fill="none" stroke="{ROXO_CLARO}"'
            ' stroke-width="2.4" opacity=".65"/>'
            f'<ellipse cy="30" rx="18" ry="4.5" fill="none" stroke="{ROXO_CLARO}"'
            ' stroke-width="2.4" opacity=".55"/>'
            '<ellipse cx="-20" cy="-16" rx="10" ry="18" fill="#fff" opacity=".2"/>'
            '</g>')


def beterraba_fatia(x, y, s=1.0, cor=None):
    """Fatia de beterraba vista de frente: casca escura + aneis concentricos.

    `cor` permite a versao DESBOTADA (a que perdeu o vermelho) — e' o contraste
    da cena 2.
    """
    c = cor or ROXO
    cl = ROXO_CLARO if cor is None else '#d8c2cc'
    ce = ROXO_ESC if cor is None else '#a8909c'
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<circle r="40" fill="{c}" stroke="{ce}" stroke-width="3"/>'
            f'<circle r="32" fill="none" stroke="{cl}" stroke-width="2.4" opacity=".8"/>'
            f'<circle r="23" fill="none" stroke="{cl}" stroke-width="2.4" opacity=".65"/>'
            f'<circle r="13" fill="none" stroke="{cl}" stroke-width="2.2" opacity=".5"/>'
            '<ellipse cx="-13" cy="-13" rx="8" ry="12" fill="#fff" opacity=".16"/>'
            '</g>')


def cenoura(x, y, s=1.0):
    """Cenoura inteira: cone laranja AFINANDO para baixo + folhas + aneis.

    O cone tem de afinar de verdade — corpo de largura constante le' como
    "bastao laranja". E o limbo da folha tem de ser largo, senao le' como broto.
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<path d="M-7,-44 C-20,-64 -34,-74 -44,-80" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M0,-46 C2,-72 5,-86 7,-96" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M8,-44 C20,-62 33,-70 43,-74" stroke="{VERDE}"'
            ' stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M-44,-80 C-68,-94 -92,-86 -88,-68'
            ' C-80,-52 -54,-58 -44,-80 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M-44,-80 C-62,-84 -78,-80 -86,-74" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            f'<path d="M7,-96 C17,-122 43,-124 47,-106'
            ' C41,-88 21,-82 7,-96 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M7,-96 C21,-108 35,-115 45,-109" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            f'<path d="M43,-74 C67,-84 89,-74 83,-58'
            ' C71,-44 51,-52 43,-74 Z"'
            ' fill="#5c8f2a" stroke="#3f6b1e" stroke-width="2"/>'
            f'<path d="M43,-74 C61,-76 75,-70 81,-62" stroke="#3f6b1e"'
            ' stroke-width="1.8" fill="none" opacity=".55"/>'
            f'<path d="M-25,-44 L25,-44 L7,84 Q0,96 -7,84 Z"'
            f' fill="{LARANJA}" stroke="{LARANJA_ESC}" stroke-width="3.5"'
            ' stroke-linejoin="round"/>'
            f'<path d="M-21,-24 L21,-24" stroke="{LARANJA_ESC}" stroke-width="2"'
            ' opacity=".55"/>'
            f'<path d="M-18,-4 L18,-4" stroke="{LARANJA_ESC}" stroke-width="2"'
            ' opacity=".5"/>'
            f'<path d="M-14,18 L14,18" stroke="{LARANJA_ESC}" stroke-width="2"'
            ' opacity=".45"/>'
            f'<path d="M-9,42 L9,42" stroke="{LARANJA_ESC}" stroke-width="2"'
            ' opacity=".4"/>'
            '<path d="M-16,-34 L-6,44" stroke="#fff" stroke-width="6" opacity=".22"'
            ' stroke-linecap="round"/>'
            '</g>')


def cenoura_palito(x, y, s=1.0, rot=0):
    """Palito de cenoura: barra laranja arredondada e GROSSA (o "grosso")."""
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g}) scale({s:g})">'
            f'<rect x="-30" y="-13" width="60" height="26" rx="11"'
            f' fill="{LARANJA}" stroke="{LARANJA_ESC}" stroke-width="2.8"/>'
            f'<line x1="-18" y1="-7" x2="-18" y2="7" stroke="{LARANJA_ESC}"'
            ' stroke-width="2" opacity=".45"/>'
            f'<line x1="2" y1="-7" x2="2" y2="7" stroke="{LARANJA_ESC}"'
            ' stroke-width="2" opacity=".45"/>'
            '<rect x="-24" y="-8" width="16" height="5" rx="2.5" fill="#fff"'
            ' opacity=".28"/>'
            '</g>')


def escudo(x, y, s=1.0):
    """Escudo — o simbolo de "protege" na cena do truque (`pulseBadge`)."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<g style="animation:pulseBadge 1.8s ease-in-out infinite">'
            f'<path d="M0,-40 L34,-26 L34,6 C34,28 18,42 0,50'
            ' C-18,42 -34,28 -34,6 L-34,-26 Z"'
            f' fill="#fdf0e0" stroke="{LARANJA_ESC}" stroke-width="3.5"'
            ' stroke-linejoin="round"/>'
            f'<path d="M0,-24 L20,-16 L20,4 C20,18 10,27 0,32'
            ' C-10,27 -20,18 -20,4 L-20,-16 Z"'
            f' fill="{LARANJA}" opacity=".35"/>'
            f'<path d="M-12,0 L-3,10 L14,-10" stroke="{ROXO_ESC}"'
            ' stroke-width="5" fill="none" stroke-linecap="round"'
            ' stroke-linejoin="round"/>'
            '</g></g>')


def jarra_dois(liquido, s=1.0):
    """Jarro alto (mais ALTO que largo — a licao da silhueta)."""
    return (f'<g transform="scale({s:g})">'
            f'<path d="M-46,-96 L-46,74 Q-46,92 -28,92 L28,92 Q46,92 46,74 L46,-96 Z"'
            ' fill="#fdf6ea" stroke="#8a6a2f" stroke-width="4"/>'
            f'<path d="M-39,-64 L-39,70 Q-39,84 -25,84 L25,84 Q39,84 39,70 L39,-64 Z"'
            f' fill="{liquido}"/>'
            '<ellipse cx="-27" cy="-6" rx="6" ry="40" fill="#fff" opacity=".26"/>'
            '</g>')


def bolhas():
    """Borbulhas subindo (`riseFast`)."""
    return ('<g style="animation:riseFast 1.4s ease-out infinite">'
            '<circle cx="-8" cy="46" r="4" fill="#fff" opacity=".8"/>'
            '<circle cx="12" cy="56" r="3.2" fill="#fff" opacity=".75"/>'
            '</g>'
            '<g style="animation:riseFast 1.4s ease-out .5s infinite">'
            '<circle cx="2" cy="40" r="3.6" fill="#fff" opacity=".7"/>'
            '<circle cx="-20" cy="52" r="3" fill="#fff" opacity=".65"/>'
            '</g>')


def colher_sal(x, y, s=1.0):
    """Colher com sal, balancando — e os graos caindo (`pour2x`).

    O QUE FAZ LER "colher" e' a dupla **CUIA + CABO**. A 1a versao desenhava so' a
    cuia de perfil (um quadrilatero chato) e o render mostrou uma **folha de papel
    flutuando**. A cuia tem de ser uma elipse FUNDA com aro, e o cabo tem de
    aparecer preso nela.
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<g style="animation:wobble 3.2s ease-in-out infinite">'
            '<g transform="rotate(-24)">'
            # cabo (com ponta arredondada)
            '<path d="M24,-12 L84,-36 Q92,-39 94,-31 Q96,-23 88,-21 L28,2 Z"'
            ' fill="#e6e2d6" stroke="#9a927c" stroke-width="2.5"'
            ' stroke-linejoin="round"/>'
            '<ellipse cx="86" cy="-28" rx="9" ry="7" fill="#e6e2d6"'
            ' stroke="#9a927c" stroke-width="2"/>'
            # cuia: elipse funda + aro interno
            '<ellipse rx="40" ry="27" fill="#fbf8ee" stroke="#9a927c"'
            ' stroke-width="2.5"/>'
            '<ellipse rx="31" ry="19" fill="#efe9da"/>'
            # monte de sal
            '<path d="M-23,-6 C-13,-21 13,-21 23,-6 Z" fill="#fff"'
            ' stroke="#cfc7b2" stroke-width="1.6"/>'
            '</g></g>'
            # graos caindo
            '<g style="animation:pour2x 1.7s ease-out infinite">'
            '<circle cx="-16" cy="40" r="3" fill="#fff" stroke="#cfc7b2"'
            ' stroke-width="1.3"/>'
            '<circle cx="-4" cy="56" r="2.6" fill="#fff" stroke="#cfc7b2"'
            ' stroke-width="1.3"/>'
            '<circle cx="-15" cy="72" r="2.4" fill="#fff" stroke="#cfc7b2"'
            ' stroke-width="1.3"/>'
            '<circle cx="-3" cy="86" r="2.2" fill="#fff" stroke="#cfc7b2"'
            ' stroke-width="1.3"/>'
            '</g></g>')


def faca(x, y, rot=0, s=1.0):
    """Faca de chef vista de LADO: lamina longa + cabo curto. Depois girada.

    Em pe' (lamina para cima, cabo para baixo) a lamina estreita e vertical le'
    como **tubo de ensaio** — foi o que o render mostrou. Deitada, com lamina
    longa e cabo curto, e' inconfundivel.
    """
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g}) scale({s:g})">'
            '<g style="animation:chop2x 1.7s ease-in-out infinite">'
            # lamina
            '<path d="M-92,-13 L22,-13 L22,13 L-62,13 Q-92,13 -92,-1 Z"'
            ' fill="#cdd6dc" stroke="#7a8a92" stroke-width="2.5"'
            ' stroke-linejoin="round"/>'
            # fio (borda de corte), mais claro
            '<path d="M-92,2 L22,2 L22,13 L-62,13 Q-92,13 -92,2 Z"'
            ' fill="#eef3f6"/>'
            # bolster
            '<rect x="22" y="-16" width="12" height="32" rx="3" fill="#9aa8b0"'
            ' stroke="#6d7c85" stroke-width="2"/>'
            # cabo
            '<rect x="34" y="-14" width="62" height="28" rx="11" fill="#5e3a1f"'
            ' stroke="#40260f" stroke-width="2.5"/>'
            '<circle cx="52" cy="0" r="3.4" fill="#cdd6dc"/>'
            '<circle cx="72" cy="0" r="3.4" fill="#cdd6dc"/>'
            '</g></g>')


def relogio(x, y, s=1.0):
    """Relogio com ponteiro batendo (`tick`).

    Com 4 marcas so' ele le' como **bussola** (1o render). Sao **12** marcas, com
    as das horas mais compridas, e o pino central pequeno.
    """
    marcas = []
    for k in range(12):
        a = math.radians(k * 30)
        r1 = 29 if k % 3 == 0 else 34
        marcas.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8a6a2f"'
            ' stroke-width="%.1f" stroke-linecap="round"/>'
            % (r1 * math.sin(a), -r1 * math.cos(a),
               45 * math.sin(a), -45 * math.cos(a),
               4 if k % 3 == 0 else 2.6))
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<circle r="62" fill="#fdf6ea" stroke="#8a6a2f" stroke-width="5"/>'
            '<circle r="54" fill="none" stroke="#e2d7c0" stroke-width="2"/>'
            + ''.join(marcas) +
            '<g style="animation:tick 2s steps(12) infinite">'
            '<line x1="0" y1="8" x2="0" y2="-40" stroke="#5e2344" stroke-width="5"'
            ' stroke-linecap="round"/>'
            '</g>'
            '<circle r="4" fill="#5e2344"/></g>')


def escala_ph(x, y, w=312, h=34, marcas=()):
    """Barra de pH de 2 a 7, dividida em 4,6. `marcas` = [(ph, cor, rotulo[, dy])].

    As duas metades sao PATH, nao `<rect rx>`: dois retangulos arredondados lado
    a lado deixam uma emenda redonda no meio da barra. So' as pontas arredondam.

    `dy` desloca o ROTULO so' na vertical. Sem ele, dois marcadores proximos
    colam os rotulos: "BEET" (5,3) e "CARROT" (5,9) estao a 0,6 de pH = **37 px**,
    e "CARROT" a 13 px tem ~47 px -> saiu "BEETCARROT" no render.
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
    for marca in marcas:
        ph, cor, rotulo = marca[0], marca[1], marca[2]
        dy = marca[3] if len(marca) > 3 else 0
        pxx = px(ph)
        p.append(f'<circle cx="{pxx:g}" cy="0" r="9" fill="{cor}" stroke="#fff"'
                 ' stroke-width="2.5"/>')
        p.append(f'<text x="{pxx:g}" y="{r + 25 + dy:g}" text-anchor="middle"'
                 f' font-size="13" font-weight="800" fill="{cor}"'
                 f' font-family="system-ui">{rotulo}</text>')
    return f'<g transform="translate({x:g},{y:g})">' + ''.join(p) + '</g>' 


# ------------------------------------------------- cena 1: o gancho
def s0(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="202" cy="292" r="150" fill="#fdf1e2" opacity=".8"/>
    <g transform="translate(126,286)">
      <g style="animation:wobble 2.9s ease-in-out infinite">@BETERRABA@</g>
    </g>
    <g transform="translate(288,290)">
      <g style="animation:wobble 3.2s ease-in-out infinite">@CENOURA@</g>
    </g>
    <g transform="translate(202,548)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#8e3a68" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#5e2344" font-family="system-ui">TWO ROOTS, TWO JOBS</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#9a6a86" font-family="system-ui">one makes the acid, one keeps the colour</text>
    </g>'''.replace('@BETERRABA@', beterraba(0, 0, 0.92)) \
     .replace('@CENOURA@', cenoura(0, 0, 0.92))


# ------------------------------------------------- cena 2: o vermelho se perde
def s1(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="202" cy="300" r="132" fill="#fdf1e2" opacity=".65"/>
    <g transform="translate(112,262)">@FRESCA@</g>
    <g transform="translate(292,262)">@FADADA@</g>
    <g transform="translate(202,262)">
      <g style="animation:tick 2s ease-in-out infinite">
        <path d="M-30,0 L30,0 M20,-11 L34,0 L20,11" stroke="#8a6a2f" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </g>
    <g transform="translate(112,352)">
      <text x="0" y="0" text-anchor="middle" font-size="12" font-weight="800" fill="#5e2344" font-family="system-ui">DAY 1</text>
    </g>
    <g transform="translate(292,352)">
      <text x="0" y="0" text-anchor="middle" font-size="12" font-weight="800" fill="#a8909c" font-family="system-ui">DAY 5</text>
    </g>
    <g transform="translate(202,556)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#8e3a68" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#5e2344" font-family="system-ui">BEETROOT LOSES ITS RED</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#9a6a86" font-family="system-ui">light, heat and oxygen break the pigment down</text>
    </g>'''.replace('@FRESCA@', beterraba_fatia(0, 0, 1.35)) \
     .replace('@FADADA@', beterraba_fatia(0, 0, 1.35, cor=PALIDO))


# ------------------------------------------------- cena 3: o sal
def s2(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="202" cy="250" r="128" fill="#fdf1e2" opacity=".7"/>
    <g transform="translate(202,214)">@COLHER@</g>
    <g transform="translate(202,376)">
      <rect x="-118" y="-62" width="236" height="124" rx="16" fill="#fff" stroke="#8a6a2f" stroke-width="3.5"/>
      <text x="0" y="-8" text-anchor="middle" font-size="46" font-weight="800" fill="#5e2344" font-family="system-ui">2%</text>
      <text x="0" y="34" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6a2f" font-family="system-ui">SALT, WEIGHED</text>
    </g>
    <g transform="translate(202,548)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#8a6a2f" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#8a6a2f" font-family="system-ui">20 G OF SALT PER KILO</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">that is 2% of the vegetable weight</text>
    </g>'''.replace('@COLHER@', colher_sal(0, 0, 1.25))


# ------------------------------------------------- cena 4: o corte
def s3(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <g transform="translate(310,168)">@FACA@</g>
    <g transform="translate(108,270)">
      <g style="animation:wobble 3.0s ease-in-out infinite">@FATIA@</g>
    </g>
    <g transform="translate(108,372)">
      <rect x="-62" y="-24" width="124" height="48" rx="10" fill="#fbeaf2" stroke="#8e3a68" stroke-width="2.5"/>
      <text x="0" y="7" text-anchor="middle" font-size="15" font-weight="800" fill="#5e2344" font-family="system-ui">BEET THIN</text>
    </g>
    <g transform="translate(292,268)">
      <g style="animation:wobble 3.4s ease-in-out infinite">@PALITO@</g>
    </g>
    <g transform="translate(292,372)">
      <rect x="-62" y="-24" width="124" height="48" rx="10" fill="#fdecdb" stroke="#e0801f" stroke-width="2.5"/>
      <text x="0" y="7" text-anchor="middle" font-size="15" font-weight="800" fill="#a8541a" font-family="system-ui">CARROT THICK</text>
    </g>
    <g transform="translate(202,540)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#a8541a" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#a8541a" font-family="system-ui">THE CUT IS NOT THE SAME</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#c98a5c" font-family="system-ui">one releases sugar, one keeps the crunch</text>
    </g>'''.replace('@FACA@', faca(0, 0, -34, 0.68)) \
     .replace('@FATIA@', beterraba_fatia(0, 0, 1.0)) \
     .replace('@PALITO@', cenoura_palito(0, 0, 1.15, 8))


# ------------------------------------------------- cena 5: O TRUQUE
def s4(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="202" cy="272" r="140" fill="#fdf1e2" opacity=".6"/>
    <g transform="translate(116,290)">
      <g style="animation:wobble 3.0s ease-in-out infinite">@JARRA_FRACA@</g>
    </g>
    <g transform="translate(292,290)">
      <g style="animation:wobble 2.7s ease-in-out infinite">@JARRA_FORTE@</g>
    </g>
    <g transform="translate(116,300)">@BOLHAS@</g>
    <g transform="translate(202,148)">@ESCUDO@</g>
    <g transform="translate(116,428)">
      <text x="0" y="0" text-anchor="middle" font-size="12" font-weight="800" fill="#a8909c" font-family="system-ui">BEET ALONE</text>
    </g>
    <g transform="translate(292,428)">
      <text x="0" y="0" text-anchor="middle" font-size="12" font-weight="800" fill="#5e2344" font-family="system-ui">BEET + CARROT</text>
    </g>
    <g transform="translate(202,556)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#e0801f" stroke-width="3.5"/>
      <text x="0" y="-12" text-anchor="middle" font-size="17" font-weight="800" fill="#a8541a" font-family="system-ui">THE CARROT PROTECTS THE RED</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#c98a5c" font-family="system-ui">carotenoids block the oxidation</text>
    </g>'''.replace('@JARRA_FRACA@', jarra_dois(PALIDO, 0.92)) \
     .replace('@JARRA_FORTE@', jarra_dois('#8e1f4e', 0.92)) \
     .replace('@ESCUDO@', escudo(0, 0, 0.9)) \
     .replace('@BOLHAS@', bolhas())


# ------------------------------------------------- cena 6: por dentro (pH)
def s5(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    @ESCALA@
    <g transform="translate(202,468)">
      <rect x="-172" y="-46" width="344" height="92" rx="12" fill="#fff" stroke="#8a6a2f" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#8a6a2f" font-family="system-ui">BOTH START ABOVE 4.6</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">the sugar takes them under in about 5 days</text>
    </g>
    <g transform="translate(202,584)">
      <text x="0" y="0" text-anchor="middle" font-size="14" font-weight="700" fill="#2f5c0d" font-family="system-ui">RAW BEET 5.3 - RAW CARROT 5.9</text>
    </g>'''.replace('@ESCALA@', escala_ph(
        202, 268, 312, 34,
        [(3.6, '#2f5c0d', 'AFTER'), (5.3, ROXO, 'BEET'), (5.9, LARANJA, 'CARROT', 22)]))


# ------------------------------------------------- cena 7: tempo + CTA
def s6(t):
    return '''    <rect width="405" height="720" fill="#fffaf0"/>
    <circle cx="202" cy="182" r="104" fill="#fdf1e2" opacity=".8"/>
    <g transform="translate(202,182)">@RELOGIO@</g>
    <g transform="translate(202,352)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="#5e2344" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#5e2344" font-family="system-ui">5 DAYS, THEN THE FRIDGE</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#9a6a86" font-family="system-ui">cold slows the bacteria down - it does not stop it</text>
    </g>
    <g transform="translate(202,476)">
      <rect x="-176" y="-42" width="352" height="84" rx="12" fill="#fbeaf2" stroke="#8e3a68" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="#5e2344" font-family="system-ui">THE BEET IS THE FUEL</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#9a6a86" font-family="system-ui">about 50% more sugar than the carrot</text>
    </g>
    <g transform="translate(202,584)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">which one should I ferment next?</text>
    </g>'''.replace('@RELOGIO@', relogio(0, 0, 1.5))


# ---------------------------------------------------------------- montagem
TEXTOS = {
    'titulo': 'Shorts animado — Beetroot and carrot (fermented)',
    'badge': '🟣 + 🥕',
    'capdiv': ('Beetroot and carrot'
               '<small>one makes the acid, one saves the colour</small>'),
    # Cada cena tem 4 campos de texto e eles NAO podem repetir a mesma frase:
    # titulo do cartao (SVG) / sublinha do cartao (SVG) / cap (barra) / sub (barra)
    'cenas': [
        ('s0', 6400, '%s 1 / 7' % TAG, 'Beetroot and carrot',
         'one bleeds red, one stays orange', ROXO_ESC),
        ('s1', 6400, '%s 2 / 7' % TAG, 'Why it fades',
         'betanin is the pigment - and it is fragile', '#a8909c'),
        ('s2', 6200, '%s 3 / 7' % TAG, 'Use salt without iodine',
         'iodine stalls the bacteria you want', '#8a6a2f'),
        ('s3', 6400, '%s 4 / 7' % TAG, 'Beet thin, carrot thick',
         'surface area decides how fast the sugar comes out', LARANJA_ESC),
        ('s4', 7000, '%s 5 / 7' % TAG, 'Two jars, same beet',
         'only the one with carrot keeps its colour', LARANJA_ESC),
        ('s5', 6400, '%s 6 / 7' % TAG, 'Nothing here is acid',
         'the acid has to be made - that is what the sugar is for', '#8a6a2f'),
        ('s6', 6400, '%s 7 / 7' % TAG, 'Five days is a guide',
         'taste it - sour means ready, sweet means wait', '#2f5c0d'),
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
        ('<div class="speed-badge">🥕 + APPLE</div>',
         '<div class="speed-badge">%s</div>' % t['badge']),
        ('<div class="tag" id="tag">SCENE 1 / 7</div>',
         '<div class="tag" id="tag">%s</div>' % t['cenas'][0][2]),
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
    faltando = usados - defs
    if faltando:
        print('ERRO: animation sem keyframe: %s' % sorted(faltando))
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

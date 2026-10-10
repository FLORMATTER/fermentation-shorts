# -*- coding: utf-8 -*-
"""_melhorar-beterraba-cenoura.py — 4 consertos de FORMA no gerador #25.

Todos vieram do RENDER (o grep e o validador nao veem forma):

  cena 2  a colher leu como **folha de papel flutuando** — eu desenhei so' a cuia
          de perfil, um quadrilatero chato. O que faz ler "colher" e' a dupla
          **CUIA + CABO**.
  cena 5  os rotulos "BEET" e "CARROT" sairam colados ("BEETCARROT"): os dois
          marcadores estao a 0,6 de pH = **37 px**, e o rotulo "CARROT" a 13 px
          tem ~47 px. -> escalonar em altura (`dy`).
  cena 6  o relogio com 4 marcas leu como **bussola** -> 12 marcas, horas mais
          compridas, pino central menor.
  cena 0  o limbo das folhas era fino demais e leu como **broto** -> limbo largo
          com nervura.

O conserto vai no GERADOR (fonte da verdade), com contagem conferida: se qualquer
ancora nao casar exatamente 1 vez, aborta SEM GRAVAR.

    python _melhorar-beterraba-cenoura.py
"""
import io
import re
import sys

ALVO = '_criar-beterraba-cenoura.py'

# --------------------------------------------------------------- beterraba
BETERRABA = '''def beterraba(x, y, s=1.0):
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
            '</g>')'''

# ---------------------------------------------------------------- cenoura
CENOURA = '''def cenoura(x, y, s=1.0):
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
            '</g>')'''

# ------------------------------------------------------------- colher_sal
COLHER = '''def colher_sal(x, y, s=1.0):
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
            '</g></g>')'''

# --------------------------------------------------------------- relogio
RELOGIO = '''def relogio(x, y, s=1.0):
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
            '<circle r="4" fill="#5e2344"/></g>')'''

# -------------------------------------------------------------- escala_ph
ESCALA = '''def escala_ph(x, y, w=312, h=34, marcas=()):
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
    return f'<g transform="translate({x:g},{y:g})">' + ''.join(p) + '</g>' '''

# (nome, texto novo, fim do bloco — ATENCAO: o `.*?\n` ja' consome um \n, entao
#  no lookahead sobram DOIS \n, nao tres)
BLOCOS = (
    ('beterraba', BETERRABA, r'\n\ndef beterraba_fatia\('),
    ('cenoura', CENOURA, r'\n\ndef cenoura_palito\('),
    ('colher_sal', COLHER, r'\n\ndef faca\('),
    ('relogio', RELOGIO, r'\n\ndef escala_ph\('),
    ('escala_ph', ESCALA, r'\n\n#'),
)

# trocas literais (ancora, substituto, quantas vezes)
TROCAS = (
    ('import io\nimport os\nimport re\nimport sys',
     'import io\nimport math\nimport os\nimport re\nimport sys', 1),
    ("[(3.6, '#2f5c0d', 'AFTER'), (5.3, ROXO, 'BEET'), (5.9, LARANJA, 'CARROT')]))",
     "[(3.6, '#2f5c0d', 'AFTER'), (5.3, ROXO, 'BEET'), (5.9, LARANJA, 'CARROT', 22)]))",
     1),
)


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'

    # --- 1) confere TODAS as ancoras antes de escrever
    for nome, novo, fim in BLOCOS:
        pat = re.compile(r'def %s\(.*?\n(?=%s)' % (nome, fim), re.S)
        n = len(pat.findall(d))
        if n != 1:
            print('ERRO: bloco %s casou %d vez(es)' % (nome, n))
            return 1
    for velho, _, n in TROCAS:
        achou = d.count(velho)
        if achou != n:
            print('ERRO: ancora casou %d vez(es), esperava %d: %s'
                  % (achou, n, velho[:60]))
            return 1

    # --- 2) aplica os blocos
    for nome, novo, fim in BLOCOS:
        pat = re.compile(r'def %s\(.*?\n(?=%s)' % (nome, fim), re.S)
        d = pat.sub(lambda m: novo.replace('\n', eol) + eol, d, count=1)
        print('  bloco trocado: %s' % nome)

    # --- 3) aplica as trocas literais
    for velho, novo, n in TROCAS:
        d = d.replace(velho, novo.replace('\n', eol), n)
        print('  troca literal: %s' % velho.split('\n')[0][:46])

    # --- 4) sanidade: cada funcao existe UMA vez, e o arquivo compila
    for nome in ('beterraba', 'beterraba_fatia', 'cenoura', 'cenoura_palito',
                 'escudo', 'jarra_dois', 'bolhas', 'colher_sal', 'faca',
                 'relogio', 'escala_ph'):
        if len(re.findall(r'^def %s\(' % nome, d, re.M)) != 1:
            print('ERRO: `def %s` sumiu ou duplicou' % nome)
            return 1
    if 'import math' not in d:
        print('ERRO: import math nao entrou')
        return 1
    if 'CARROT\', 22)' not in d:
        print('ERRO: o dy do CARROT nao entrou')
        return 1
    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: 5 blocos + 2 trocas | %d bytes' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())

# -*- coding: utf-8 -*-
"""_atualizar-applier2.py — dois ajustes finos no _traduzir-serie.py.

D) troca_nos_html: a classe de espaco era [ \\t] e nao pegava no de texto
   quebrado em varias linhas, como
       <p style="...">\\n    Grave a tela no OBS...\\n  </p>
   Vira \\s (nao atravessa '<', entao continua seguro).

E) NEUTRO_EXATO: strings que ja sao iguais nos dois idiomas de proposito.
   Nao sao sobra de traducao -- sao iguais porque nao tem idioma.
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(RAIZ, '_traduzir-serie.py')
d = io.open(ALVO, encoding='utf-8').read()
orig = d

D_velho = """    padrao = re.compile(r'(?<=>)([ \\t]*)' + re.escape(pt) + r'([ \\t]*)(?=<)')"""
D_novo = """    padrao = re.compile(r'(?<=>)(\\s*)' + re.escape(pt) + r'(\\s*)(?=<)')"""

E_velho = """NEUTRO_IGUAL = re.compile(
    r'^(pH|kg|g|ml|L|Pizza|Tacos|Sushi|OBS|Canva|CapCut|YouTube|'
    r'\\d+\\s*(MIN|SEG|G|KG|ML|L|MM|CM)|'
    r'\\$\\{[^}]*\\}|[^A-Za-zÀ-ÿ]*)$')"""

E_novo = """NEUTRO_IGUAL = re.compile(
    r'^(pH|kg|g|ml|L|Pizza|Tacos|Sushi|OBS|Canva|CapCut|YouTube|'
    r'\\d+\\s*(MIN|SEG|G|KG|ML|L|MM|CM)|'
    r'\\$\\{[^}]*\\}|[^A-Za-zÀ-ÿ]*)$')

# iguais nos dois idiomas porque NAO TEM IDIOMA (numero, unidade, emoji)
NEUTRO_EXATO = {
    'TOTAL: 500 g', '⚡ SPEED', 'pH', 'kg', '10 MIN',
    'Pizza', 'Tacos', 'OBS', 'Canva', 'CapCut',
}"""

for rot, velho, novo in (('D espaco multilinha', D_velho, D_novo),
                         ('E neutros exatos', E_velho, E_novo)):
    c = d.count(velho)
    if c != 1:
        print('ABORTADO: ancora %s casou %d vez(es), esperado 1.' % (rot, c))
        sys.exit(1)
    d = d.replace(velho, novo, 1)
    print('ok ancora %s' % rot)

# a guarda passa a consultar tambem o conjunto exato
G_velho = """                       if tem_letras(s) and not NEUTRO_IGUAL.match(s))"""
G_novo = """                       if tem_letras(s)
                       and not NEUTRO_IGUAL.match(s)
                       and s not in NEUTRO_EXATO)"""
c = d.count(G_velho)
if c != 1:
    print('ABORTADO: ancora G casou %d vez(es), esperado 1.' % c)
    sys.exit(1)
d = d.replace(G_velho, G_novo, 1)
print('ok ancora G guarda usa NEUTRO_EXATO')

try:
    compile(d, ALVO, 'exec')
except SyntaxError as e:
    print('ABORTADO: nao compila: %s' % e)
    sys.exit(1)

io.open(ALVO, 'w', encoding='utf-8', newline='').write(d)
print('\ngravado: %d -> %d bytes' % (len(orig.encode('utf-8')),
                                     len(d.encode('utf-8'))))

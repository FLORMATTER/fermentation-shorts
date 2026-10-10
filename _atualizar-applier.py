# -*- coding: utf-8 -*-
"""_atualizar-applier.py — melhora o _traduzir-serie.py em 3 pontos.

Por que um script e nao 3 edicoes soltas: edicoes paralelas no MESMO arquivo
sao aplicadas sobre o mesmo snapshot e a ultima apaga as outras. Aqui cada
ancora e conferida e, se qualquer uma nao casar, o script ABORTA sem gravar.

A) aplica()  -> 4a e 5a formas de ancora + troca de no de texto do HTML.
                As 3 formas antigas (literal JS, >X</text>, >X<) nao pegavam
                '>CHUCRUTE<br>' nem '>EM <span>' -- era por isso que essas
                frases nunca eram traduzidas.
B) guarda   -> troca o filtro por lista de palavras pela COMPARACAO com o
                original em portugues. O filtro antigo tinha ponto cego
                (\bfermenta\b nao casa 'FERMENTACAO') e dava 'tudo ok' falso.
C) helpers  -> NEUTRO_IGUAL e tem_letras usados pela guarda nova.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(RAIZ, '_traduzir-serie.py')

d = io.open(ALVO, encoding='utf-8').read()
orig = d

# ───────────────────────── ancora A: aplica() ─────────────────────────
A_velho = '''def aplica(d, dic):
    """Aplica o dicionario. Da frase mais longa para a mais curta."""
    n = 0
    for pt, en in sorted(dic, key=lambda x: -len(x[0])):
        for velho, novo in (("'%s'" % pt, "'%s'" % en),
                            ('>%s</text>' % pt, '>%s</text>' % en),
                            ('>%s<' % pt, '>%s<' % en)):
            c = d.count(velho)
            if c:
                d = d.replace(velho, novo)
                n += c
    return d, n
'''

A_novo = '''def troca_nos_html(d, pt, en):
    """Troca a frase quando ela e um NO DE TEXTO do HTML (entre duas tags).

    Necessario porque as formas literais nao pegam '>EM <span>' nem
    '>CHUCRUTE<br>' -- foi assim que 'CHUCRUTE / EM / 7 DIAS' ficou em
    portugues no cartao do chucrute.

    A troca e limitada ao corpo do HTML (de </style> ate <script>). Isso e
    proposital: dentro do <script>, '>' e '<' sao operadores de comparacao e
    uma troca solta ali quebraria o JavaScript.
    """
    ini = d.find('</style>')
    if ini < 0:
        return d, 0
    fim = d.find('<script>')
    if fim < 0:
        fim = len(d)
    corpo = d[ini:fim]
    padrao = re.compile(r'(?<=>)([ \\t]*)' + re.escape(pt) + r'([ \\t]*)(?=<)')
    novo, k = padrao.subn(lambda m: m.group(1) + en + m.group(2), corpo)
    if k:
        d = d[:ini] + novo + d[fim:]
    return d, k


def aplica(d, dic):
    """Aplica o dicionario. Da frase mais longa para a mais curta.

    Cinco formas ancoradas por frase. As ancoras sao o que impede
    'Couve' de casar dentro de 'Couve-flor'.
    """
    n = 0
    for pt, en in sorted(dic, key=lambda x: -len(x[0])):
        for velho, novo in (("'%s'" % pt, "'%s'" % en),
                            ('>%s</text>' % pt, '>%s</text>' % en),
                            ('>%s<' % pt, '>%s<' % en),
                            ('>%s<br>' % pt, '>%s<br>' % en),
                            ('>%s <' % pt, '>%s <' % en)):
            c = d.count(velho)
            if c:
                d = d.replace(velho, novo)
                n += c
        d, k = troca_nos_html(d, pt, en)
        n += k
    return d, n
'''

# ───────────────────────── ancora B: guarda ─────────────────────────
B_velho = '''        # o que sobrou de portugues nas strings visiveis
        sobra = sorted({s for s in visiveis(novo) if PT.search(s)})
        # decimais com virgula que escaparam (mostrar a FRASE, nao so o digito)
        virg = sorted({s for s in visiveis(novo) if re.search(r'\\d,\\d', s)})
'''

B_novo = '''        # SOBRA = string visivel que ficou IDENTICA ao original em portugues.
        # Nao adivinha idioma: compara os dois arquivos. O filtro antigo por
        # lista de palavras tinha ponto cego (\\bfermenta\\b nao casa
        # 'FERMENTACAO') e por isso aprovava arquivo meio traduzido.
        sobra = sorted(s for s in (visiveis(novo) & visiveis(d))
                       if tem_letras(s) and not NEUTRO_IGUAL.match(s))
        # decimais com virgula que escaparam (mostrar a FRASE, nao so o digito)
        virg = sorted({s for s in visiveis(novo) if re.search(r'\\d,\\d', s)})
'''

# ───────────────────────── ancora C: helpers ─────────────────────────
C_velho = """                r'tinge|salmoura|iodo|sem|só|nao|faca|água)\\b', re.I)
"""

C_novo = """                r'tinge|salmoura|iodo|sem|só|nao|faca|água)\\b', re.I)

# strings que sao iguais nos dois idiomas de proposito: nao sao sobra
NEUTRO_IGUAL = re.compile(
    r'^(pH|kg|g|ml|L|Pizza|Tacos|Sushi|OBS|Canva|CapCut|YouTube|'
    r'\\d+\\s*(MIN|SEG|G|KG|ML|L|MM|CM)|'
    r'\\$\\{[^}]*\\}|[^A-Za-zÀ-ÿ]*)$')


def tem_letras(s):
    \"\"\"Pelo menos 2 letras seguidas -> vale a pena conferir.\"\"\"
    return re.search(r'[A-Za-zÀ-ÿ]{2}', s) is not None
"""

for rot, velho, novo in (('A aplica()', A_velho, A_novo),
                         ('B guarda', B_velho, B_novo),
                         ('C helpers', C_velho, C_novo)):
    c = d.count(velho)
    if c != 1:
        print('ABORTADO: ancora %s casou %d vez(es), esperado 1.' % (rot, c))
        sys.exit(1)
    d = d.replace(velho, novo, 1)
    print('ok ancora %s' % rot)

if d == orig:
    print('ABORTADO: nada mudou.')
    sys.exit(1)

# conferencia: o arquivo novo precisa continuar compilando
try:
    compile(d, ALVO, 'exec')
except SyntaxError as e:
    print('ABORTADO: o resultado nao compila: %s' % e)
    sys.exit(1)

io.open(ALVO, 'w', encoding='utf-8', newline='').write(d)
print('\ngravado: %s (%d -> %d bytes)' % (os.path.basename(ALVO),
                                          len(orig.encode('utf-8')),
                                          len(d.encode('utf-8'))))

# -*- coding: utf-8 -*-
"""_encurtar-selos.py — corrige o erro (h): selo com texto mais largo que a caixa.

Em SVG o texto NAO quebra linha nem encolhe. Quando o ingles fica maior que o
portugues, o selo vaza para os dois lados. Achar isso exige OLHAR o render --
o _validar-short.py mede coordenada, nao largura, e o _largura-texto.py e so
estimativa (ele deu falso positivo em 5 casos e falso negativo em outros).

Os 9 casos abaixo foram CONFIRMADOS no render (PNG em _revisao/).

A correcao e encurtar o INGLES ate a densidade do portugues, e nao alargar a
caixa: a caixa ja ocupa 83% do cartao e alargar ate 98% ficaria colado na borda.
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(RAIZ, '_dicionario-pt-en.py')
d = io.open(ALVO, encoding='utf-8').read()
orig = d

# (rotulo, entrada antiga, entrada nova)  — casamento exato, 1 vez cada
TROCAS = [
    ('couve-flor s5',
     "    ('O SAL VIRA CONSERVA', 'THE SALT TURNS IT INTO A PRESERVE'),",
     "    ('O SAL VIRA CONSERVA', 'THE SALT PRESERVES IT'),"),

    ('beterraba-svg-puro s5',
     "    ('É ISSO QUE CONSERVA O LEGUME', 'THIS IS WHAT PRESERVES THE VEGETABLE'),",
     "    ('É ISSO QUE CONSERVA O LEGUME', 'THIS IS WHAT PRESERVES IT'),"),

    ('repolho-maos-canva s2',
     "    ('A MÃO CORTA BEM FINO', 'THE HAND CUTS IT NICE AND THIN'),",
     "    ('A MÃO CORTA BEM FINO', 'THE HAND CUTS IT THIN'),"),

    ('chucrute-30s s3',
     "    ('PRENSA ATÉ COBRIR DE LÍQUIDO', 'PRESS UNTIL THE LIQUID COVERS IT'),",
     "    ('PRENSA ATÉ COBRIR DE LÍQUIDO', 'PRESS IT UNDER THE LIQUID'),"),

    ('chucrute-30s s2',
     "    ('A ÁGUA SAI DELA MESMA', 'THE WATER COMES OUT ON ITS OWN'),",
     "    ('A ÁGUA SAI DELA MESMA', 'WATER COMES OUT ON ITS OWN'),"),

    ('beterraba-couve s6',
     "    ('A COUVE ABSORVE A COR DA BETERRABA', 'THE CABBAGE ABSORBS THE COLOUR OF THE BEET'),",
     "    ('A COUVE ABSORVE A COR DA BETERRABA', 'THE CABBAGE SOAKS UP THE COLOUR'),"),

    ('pepino s3',
     "    ('SEM TANINO = PEPINO MOLE', 'NO TANNIN = SOFT CUCUMBER'),",
     "    ('SEM TANINO = PEPINO MOLE', 'NO TANNIN = MUSHY'),"),

    ('beterraba-couve s1',
     "    ('LAVE E TIRE OS TALOS DUROS', 'WASH AND REMOVE THE TOUGH STEMS'),",
     "    ('LAVE E TIRE OS TALOS DUROS', 'WASH AND REMOVE THE STEMS'),"),

    ('repolho-maos-canva s3',
     "    ('SEM ÁGUA. ELA SAI DO REPOLHO.', 'NO WATER. IT COMES OUT OF THE CABBAGE.'),",
     "    ('SEM ÁGUA. ELA SAI DO REPOLHO.', 'NO WATER. THE CABBAGE DOES IT.'),"),
]

for rot, velho, novo in TROCAS:
    c = d.count(velho)
    if c != 1:
        print('ABORTADO: %s casou %d vez(es), esperado 1.' % (rot, c))
        sys.exit(1)
    d = d.replace(velho, novo, 1)
    print('ok %-22s %s' % (rot, novo.split(", '")[1].rstrip("'),")))

# o arquivo tem que continuar sendo Python valido e com o mesmo numero de entradas
antes = orig.count("    ('")
try:
    ns = {'__name__': 'dic'}
    exec(compile(d, ALVO, 'exec'), ns)
except SyntaxError as e:
    print('ABORTADO: nao compila: %s' % e)
    sys.exit(1)
print('\nentradas no dicionario: %d' % len(ns['DIC']))

io.open(ALVO, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %d -> %d bytes' % (len(orig.encode('utf-8')), len(d.encode('utf-8'))))

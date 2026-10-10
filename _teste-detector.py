# -*- coding: utf-8 -*-
"""Por que a frase VELOCIDADE DA FERMENTACAO escapou do detector?

O regex PT do _traduzir-serie.py termina as alternativas com \b. Em Python 3,
'\b' e o limite entre \w e nao-\w, e 'C-cedilha' CONTA como \w (letra Unicode).
Logo \bfermenta\b NAO casa dentro de 'FERMENTACAO' -- depois do 'a' vem 'C',
que tambem e palavra. A frase nunca era reportada como faltando.

Este script prova o diagnostico em vez de supor.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

# o regex atual, copiado do _traduzir-serie.py
PT_ATUAL = re.compile(r'\b(que|para|com|nao|não|você|voce|água|agua|sal|dias|semanas|'
                      r'pote|dentes?|mão|mao|fermenta|prensa|massageia|repolho|cenoura|'
                      r'rabanete|beterraba|couve|alho|cebola|pepino|pronta|pronto|'
                      r'crocante|bancada|esperar|volta|cor|sua|seu|isso|mais|legume|'
                      r'tinge|salmoura|iodo|sem|só|nao|faca|água)\b', re.I)

CASOS = [
    'VELOCIDADE DA FERMENTAÇÃO',
    'RABANETE FERMENTADO',
    'FERMENTAÇÃO RÁPIDA',
    'CROCANTES',
    'LEGUMES',
    'POTES',
    'PRONTAS',
    'SUAS MÃOS',
    'TINGIU A ÁGUA',
    'FERMENTAR',
    'VOLTAR',
]

print('=' * 70)
print('1) REGEX ATUAL: por que nao ve')
print('=' * 70)
for c in CASOS:
    m = PT_ATUAL.search(c)
    print('  %-26s -> %s' % (c, ('VE: ' + m.group(0)) if m else 'NAO VE  <-- ponto cego'))

print()
print('=' * 70)
print('2) DIACRITICOS: o marcador que nao depende de lista de palavras')
print('=' * 70)
PT_DIAC = re.compile(r'[ãõçáéíóúâêôàÃÕÇÁÉÍÓÚÂÊÔÀ]')
for c in CASOS:
    print('  %-26s -> %s' % (c, 'DIACRITICO PT' if PT_DIAC.search(c) else '-'))

print()
print('=' * 70)
print('3) COMO O _traduzir-serie.py ENXERGA a linha 512 do arquivo -en')
print('=' * 70)
p = os.path.join(RAIZ, 'rabanete', 'shorts-rabanete-animado-en.html')
d = io.open(p, encoding='utf-8', errors='replace').read()
alvo = 'VELOCIDADE DA FERMENTAÇÃO'

# a mesma extracao do visiveis()
out = []
for chave in ('cap', 'sub', 'hint', 'nome', 'nivel', 'sal', 'tempo'):
    out += re.findall(r"\b%s\s*:\s*'((?:[^'\\]|\\.)*)'" % chave, d)
out += [t.strip() for t in re.findall(r'<text\b[^>]*>(.*?)</text>', d, re.S)]
corpo = d.split('</style>', 1)[-1].split('<script>', 1)[0]
out += [' '.join(n.split()) for n in re.findall(r'>([^<>{}]+)<', corpo)]
out = [s for s in out if s.strip()]

print('  a frase esta na lista de visiveis?  %s' % (alvo in out))
print('  o regex PT atual casa?              %s' % bool(PT_ATUAL.search(alvo)))
print('  => a frase passou nos DOIS filtros, por isso nao foi reportada.')

print()
print('  mas o HTML realmente contem a frase? %s' % (alvo in d))

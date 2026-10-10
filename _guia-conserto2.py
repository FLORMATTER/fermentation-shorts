# -*- coding: utf-8 -*-
"""Reescreve o blockquote do corte de 60 s com a quebra de linha certa (sem "> " no meio)."""
import io, shutil, sys

G = 'C:/Users/Saxa/Desktop/youtube-work/guias/como-ganhar-dinheiro.md'
d = io.open(G, encoding='utf-8').read()
ANTES = len(d)

A = ('> para o TikTok. Feito por > `_criar-beet-garlic-60s.py`, que parte do arquivo validado. '
     'Os **67,5 s** importam: o\n'
     '> TikTok exige v\u00eddeo **acima de** 1 minuto, ent\u00e3o **n\u00e3o corte em 60,0 s cravados** \u2014\n'
     '> deixe margem (65\u201370 s), sen\u00e3o o v\u00eddeo pode n\u00e3o contar como qualificado.\n')

N = ('> para o TikTok. Feito por `_criar-beet-garlic-60s.py`, que parte do arquivo validado.\n'
     '> Os **67,5 s** importam: o TikTok exige v\u00eddeo **acima de** 1 minuto, ent\u00e3o **n\u00e3o corte\n'
     '> em 60,0 s cravados** \u2014 deixe margem (65\u201370 s), sen\u00e3o o v\u00eddeo pode n\u00e3o contar como\n'
     '> qualificado.\n')

n = d.count(A)
if n != 1:
    print('ERRO: ancora casou %d vez(es), esperado 1. Nada gravado.' % n)
    sys.exit(1)
d = d.replace(A, N)

if 'Feito por >' in d or 'por > `' in d:
    print('ERRO: ainda ha "> " no meio de frase. Nada gravado.')
    sys.exit(1)

# so' as MINHAS linhas novas precisam caber; o guia ja' tem linhas longas de tabela
longas = [l for l in N.split('\n') if len(l) > 100]
if longas:
    print('ERRO: linha nova acima de 100 chars: %r. Nada gravado.' % longas[0][:90])
    sys.exit(1)

if len(d) <= ANTES - 200:
    print('ERRO: encolheu demais. Nada gravado.')
    sys.exit(1)

shutil.copy2(G, G + '.antes-do-blockquote')
with io.open(G, 'w', encoding='utf-8', newline='') as f:
    f.write(d)
print('OK: %d -> %d chars' % (ANTES, len(d)))

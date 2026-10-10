# -*- coding: utf-8 -*-
"""Conserta 2 falhas de formatacao do patch anterior no guia do dinheiro."""
import io, shutil, sys

G = 'C:/Users/Saxa/Desktop/youtube-work/guias/como-ganhar-dinheiro.md'
d = io.open(G, encoding='utf-8').read()
ANTES = len(d)

# 1. sobrau o emoji de aviso antes do check: "⚠️ ✅ O Brasil ESTA na lista"
A1 = '\u26a0\ufe0f \u2705 **O Brasil EST\u00c1 na lista**'
N1 = '\u2705 **O Brasil EST\u00c1 na lista**'

# 2. a frase nova saiu de dentro do blockquote (perdeu o "> ") e ficou mal quebrada
A2 = ('`_criar-beet-garlic-60s.py`, que parte do arquivo validado. Os **67,5 s** importam: o\n'
      'TikTok exige v\u00eddeo **acima de** 1 minuto, ent\u00e3o **n\u00e3o corte em 60,0 s cravados** \u2014\n'
      'deixe margem (65\u201370 s), sen\u00e3o o v\u00eddeo pode n\u00e3o contar como qualificado.\n')
N2 = ('> `_criar-beet-garlic-60s.py`, que parte do arquivo validado. Os **67,5 s** importam: o\n'
      '> TikTok exige v\u00eddeo **acima de** 1 minuto, ent\u00e3o **n\u00e3o corte em 60,0 s cravados** \u2014\n'
      '> deixe margem (65\u201370 s), sen\u00e3o o v\u00eddeo pode n\u00e3o contar como qualificado.\n')

for i, (velho, novo) in enumerate([(A1, N1), (A2, N2)], 1):
    n = d.count(velho)
    if n != 1:
        print('ERRO: ancora %d casou %d vez(es), esperado 1. Nada gravado.' % (i, n))
        sys.exit(1)
    d = d.replace(velho, novo)

if '\u26a0\ufe0f \u2705' in d:
    print('ERRO: o emoji duplo continua. Nada gravado.')
    sys.exit(1)

# a frase tem de estar DENTRO do blockquote agora
if '> deixe margem (65\u201370 s)' not in d:
    print('ERRO: a frase nao entrou no blockquote. Nada gravado.')
    sys.exit(1)

shutil.copy2(G, G + '.antes-do-conserto-emoji')
with io.open(G, 'w', encoding='utf-8', newline='') as f:
    f.write(d)
print('OK: %d -> %d chars' % (ANTES, len(d)))

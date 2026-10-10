# -*- coding: utf-8 -*-
"""
A galeria (galeria-shorts.html) varre uma lista fixa de pastas. Nem `cores/`
nem `brocolis/` estavam nela, entao os dois ultimos videos ficavam fora do
indice visual. Acrescenta as duas pastas.
"""
import io, os, shutil, sys

ARQ = '_gerar-galeria.py'

TROCAS = [
    ("    'video-longo': 'Video longo (16:9)',",
     "    'video-longo': 'Video longo (16:9)',\n"
     "    'cores': 'Cores (alho + cebola + beterraba)',\n"
     "    'brocolis': 'Brocolis + laranja',", 1),

    ("ORDEM = ['guia-geral', 'repolho', 'beterraba', 'cebola', 'alho', 'cenoura',\n"
     "         'couve-flor', 'pepino', 'rabanete', 'video-longo', '_arquivo']",
     "ORDEM = ['guia-geral', 'repolho', 'beterraba', 'cebola', 'alho', 'cenoura',\n"
     "         'couve-flor', 'pepino', 'rabanete', 'cores', 'brocolis',\n"
     "         'video-longo', '_arquivo']", 1),
]

with io.open(ARQ, 'r', encoding='utf-8') as f:
    d = f.read()

antes = len(d)
for ancora, novo, n in TROCAS:
    c = d.count(ancora)
    if c != n:
        print('ABORTADO — a ancora casou %d vez(es), esperava %d:' % (c, n))
        print('   ' + repr(ancora[:80]))
        sys.exit(1)

for ancora, novo, n in TROCAS:
    d = d.replace(ancora, novo, n)

bk = ARQ + '.antes-do-video15'
if not os.path.exists(bk):
    shutil.copy2(ARQ, bk)
    print('backup  ->', bk)

with io.open(ARQ, 'w', encoding='utf-8', newline='') as f:
    f.write(d)

print('OK — %d trocas aplicadas (%d -> %d bytes)' % (len(TROCAS), antes, len(d)))

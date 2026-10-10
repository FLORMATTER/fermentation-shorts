# -*- coding: utf-8 -*-
"""
Remove as duas @keyframes mortas do short de brocolis+laranja.
Padrao do projeto: cada troca precisa casar N vezes ou o script ABORTA sem gravar.
"""
import io, os, shutil, sys

ARQ = 'brocolis/shorts-broccoli-orange-en.html'
BACKUP = ARQ + '.antes-limpeza'

# (ancora, substituicao, quantas vezes DEVE casar)
TROCAS = [
    ("""  @keyframes floatUpDown {
    0%,100% { transform: translateY(0) rotate(0deg) }
    50%     { transform: translateY(-7px) rotate(1.4deg) }
  }
""", "", 1),
    ("""  @keyframes pulseRing {
    0%   { transform: scale(.55); opacity: .7 }
    100% { transform: scale(1.85); opacity: 0 }
  }
""", "", 1),
]

with io.open(ARQ, 'r', encoding='utf-8') as f:
    d = f.read()

antes = len(d)
for ancora, novo, n in TROCAS:
    c = d.count(ancora)
    if c != n:
        print('ABORTADO — a ancora casou %d vez(es), esperava %d:' % (c, n))
        print(repr(ancora[:70]))
        sys.exit(1)
    d = d.replace(ancora, novo, n)

if not os.path.exists(BACKUP):
    shutil.copy2(ARQ, BACKUP)
    print('backup  ->', BACKUP)

with io.open(ARQ, 'w', encoding='utf-8', newline='') as f:
    f.write(d)

print('OK — %d trocas aplicadas (%d -> %d bytes)' % (len(TROCAS), antes, len(d)))

# -*- coding: utf-8 -*-
"""Conta quantos arquivos ainda tem o @handle de exemplo (placeholder)."""
import io, os

ALVOS = ('@yourchannel', '@seucanal', '@yourhandle')
PULAR = ('.git', '_revisao', '_arquivo', '__pycache__', '.workbuddy-ai', 'node_modules')

n, arqs, por_alvo = 0, set(), {}
for raiz, dirs, files in os.walk('.'):
    if any(x in raiz for x in PULAR):
        continue
    for f in files:
        if not f.endswith(('.html', '.md')):
            continue
        p = os.path.join(raiz, f)
        try:
            t = io.open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        for a in ALVOS:
            c = t.count(a)
            if c:
                n += c
                arqs.add(p)
                por_alvo[a] = por_alvo.get(a, 0) + c

print('ocorrencias de placeholder :', n)
print('arquivos afetados          :', len(arqs))
for a in ALVOS:
    print('   %-14s %d' % (a, por_alvo.get(a, 0)))

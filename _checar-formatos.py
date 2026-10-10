# -*- coding: utf-8 -*-
"""
Quais shorts ja estao em 1080x1920 nativo (prontos p/ upload) e quais dependem
do modo ?rec. Isso muda a instrucao de gravacao.
"""
import io, os, re

PULAR = ('.git', '_revisao', '_arquivo', '__pycache__', '.workbuddy-ai')

prontos, com_rec, sem_nada = [], [], []
for raiz, dirs, files in os.walk('.'):
    if any(x in raiz for x in PULAR):
        continue
    for f in sorted(files):
        if not f.endswith('.html') or 'shorts' not in f:
            continue
        p = os.path.join(raiz, f)
        try:
            t = io.open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        # largura declarada no overlay (o <body> tem um cartao de 405 ou 1080)
        tem_rec = "indexOf('rec')" in t or 'indexOf("rec")' in t
        nativo = bool(re.search(r'width\s*:\s*1080|width="1080"', t))
        if nativo:
            prontos.append((p, tem_rec))
        elif tem_rec:
            com_rec.append(p)
        else:
            sem_nada.append(p)

print('=== 1080x1920 NATIVO (%d) ===' % len(prontos))
for p, r in prontos:
    print('  %-58s ?rec=%s' % (p.replace('\\', '/'), 'sim' if r else 'NAO'))
print()
print('=== cartao 405x720 COM ?rec (%d) ===' % len(com_rec))
for p in com_rec:
    print('  %s' % p.replace('\\', '/'))
print()
print('=== SEM ?rec e sem 1080 (%d) ===' % len(sem_nada))
for p in sem_nada:
    print('  %s' % p.replace('\\', '/'))

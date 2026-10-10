# -*- coding: utf-8 -*-
"""Confere: (1) sobrou algum transform-origin perigoso, (2) o diff vs backup e minimo,
(3) os arquivos continuam LF e sem NUL."""
import io
import os
import re
import glob
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(os.path.dirname(RAIZ), 'youtube-work-backup-20260917-1630')

# 1) sobrou algum?
ORIG = re.compile(r'transform-origin:\s*([^;"]+)')
SEGURO = re.compile(r'^(?:0(?:px)?\s+0(?:px)?|\d+(?:\.\d+)?px\s+\d+(?:\.\d+)?px)$')
resto = 0
for f in sorted(glob.glob(os.path.join(RAIZ, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(f, RAIZ).replace('\\', '/')
    if rel.startswith('.workbuddy-ai/'):
        continue
    txt = io.open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'style="([^"]*)"', txt):
        st = m.group(1)
        if 'transform-origin' not in st or 'fill-box' in st:
            continue
        o = ORIG.search(st)
        if o and not SEGURO.match(o.group(1).strip()):
            resto += 1
            print('AINDA PERIGOSO: %s L%d -> %s'
                  % (rel, txt.count('\n', 0, m.start()) + 1, o.group(1).strip()))
print('1) transform-origin perigoso restante: %d' % resto)

# 2) diff vs backup
print()
print('2) diff vs backup (linhas alteradas por arquivo):')
tot = 0
for f in sorted(glob.glob(os.path.join(RAIZ, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(f, RAIZ).replace('\\', '/')
    if rel.startswith('.workbuddy-ai/'):
        continue
    b = os.path.join(BACKUP, rel.replace('/', os.sep))
    if not os.path.exists(b):
        print('   %-52s NOVO' % rel)
        continue
    r = subprocess.run(['diff', b, f], capture_output=True)
    n = sum(1 for l in r.stdout.decode('utf-8', 'replace').splitlines()
            if l[:1] in '<>')
    if n:
        tot += n
        print('   %-52s %d linha(s)' % (rel, n))
print('   total: %d linha(s) alterada(s)' % tot)

# 3) LF e sem NUL
print()
ruins = []
for f in sorted(glob.glob(os.path.join(RAIZ, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(f, RAIZ).replace('\\', '/')
    if rel.startswith('.workbuddy-ai/'):
        continue
    d = open(f, 'rb').read()
    if d.count(b'\x00'):
        ruins.append('%s: %d NUL' % (rel, d.count(b'\x00')))
    if b'\r\n' in d:
        ruins.append('%s: CRLF' % rel)
print('3) arquivos com NUL ou CRLF: %s' % (ruins or 'nenhum'))

# -*- coding: utf-8 -*-
"""Lista as ocorrencias que o consertador pega mas o detector antigo NAO pegava
(keyframe sem rotate/scale) — para confirmar que remover e inofensivo."""
import io
import os
import re
import glob

RAIZ = os.path.dirname(os.path.abspath(__file__))
STYLE = re.compile(r'style="([^"]*)"')
ORIG = re.compile(r'transform-origin:\s*([^;"]+)')
ANIM = re.compile(r'animation:\s*([a-zA-Z0-9_]+)')
SEGURO = re.compile(r'^(?:0(?:px)?\s+0(?:px)?|\d+(?:\.\d+)?px\s+\d+(?:\.\d+)?px)$')


def kf(txt, nome, n=110):
    m = re.search(r'@keyframes\s+' + nome + r'\s*\{', txt)
    if not m:
        return '(NAO EXISTE)'
    j, depth = m.end(), 1
    while depth and j < len(txt):
        if txt[j] == '{':
            depth += 1
        elif txt[j] == '}':
            depth -= 1
        j += 1
    return re.sub(r'\s+', ' ', txt[m.start():j])[:n]


extra = 0
for f in sorted(glob.glob(os.path.join(RAIZ, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(f, RAIZ).replace('\\', '/')
    if rel.startswith('.workbuddy-ai/'):
        continue
    txt = io.open(f, encoding='utf-8', errors='replace').read()
    for m in STYLE.finditer(txt):
        st = m.group(1)
        if 'transform-origin' not in st or 'fill-box' in st:
            continue
        o = ORIG.search(st)
        if not o or SEGURO.match(o.group(1).strip()):
            continue
        a = ANIM.search(st)
        corpo = kf(txt, a.group(1)) if a else '(sem animation)'
        if re.search(r'rotate|scale', corpo):
            continue
        extra += 1
        linha = txt.count('\n', 0, m.start()) + 1
        print('%-46s L%-5d anim=%-13s origin=%s' % (rel, linha, a.group(1) if a else '-',
                                                    o.group(1).strip()))
        print('      kf: %s' % corpo)
print('-' * 70)
print('EXTRA (sem rotate/scale no keyframe): %d' % extra)

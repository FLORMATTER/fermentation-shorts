# -*- coding: utf-8 -*-
"""Lista TODA ocorrencia de transform-origin com palavra-chave, com contexto,
para decidir o pivo certo de cada uma. Nao altera nada."""
import io
import os
import re
import glob

RAIZ = os.path.dirname(os.path.abspath(__file__))
TAG = re.compile(r'<[a-zA-Z][^>]*style="[^"]*transform-origin[^"]*"[^>]*>')
ANIM = re.compile(r'animation:\s*([a-zA-Z0-9_]+)')
ORIG = re.compile(r'transform-origin:\s*([^;"]+)')
OK_VAL = re.compile(r'^(0(px)?\s+0(px)?|\d+(\.\d+)?px\s+\d+(\.\d+)?px)$')


def corpo_keyframe(txt, nome):
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
    return re.sub(r'\s+', ' ', txt[m.start():j])


def linhas_antes(txt, pos, n=3):
    ini = txt.rfind('\n', 0, pos)
    for _ in range(n):
        if ini <= 0:
            break
        ini = txt.rfind('\n', 0, ini)
    return txt[ini + 1:pos]


total = 0
arquivos = 0
for f in sorted(glob.glob(os.path.join(RAIZ, '*', '*.html'))):
    rel = os.path.relpath(f, RAIZ).replace('\\', '/')
    txt = io.open(f, encoding='utf-8', errors='replace').read()
    achados = []
    for m in TAG.finditer(txt):
        tag = m.group(0)
        st = re.search(r'style="([^"]*)"', tag).group(1)
        if 'fill-box' in st:
            continue
        o = ORIG.search(st)
        if not o or OK_VAL.match(o.group(1).strip()):
            continue
        a = ANIM.search(st)
        if not a:
            continue
        if not re.search(r'rotate|scale', corpo_keyframe(txt, a.group(1))):
            continue
        linha = txt.count('\n', 0, m.start()) + 1
        achados.append((linha, a.group(1), o.group(1).strip(), tag,
                        linhas_antes(txt, m.start())))
    if not achados:
        continue
    arquivos += 1
    print('=' * 78)
    print('%s   (%d ocorrencia(s))' % (rel, len(achados)))
    for linha, anim, orig, tag, antes in achados:
        total += 1
        print('  L%-5d anim=%-14s origin=%s' % (linha, anim, orig))
        print('         antes : %s' % re.sub(r'\s+', ' ', antes.strip())[-150:])
        print('         tag   : %s' % re.sub(r'\s+', ' ', tag)[:190])
print('=' * 78)
print('TOTAL: %d ocorrencia(s) em %d arquivo(s)' % (total, arquivos))

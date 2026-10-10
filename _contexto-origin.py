# -*- coding: utf-8 -*-
"""Para cada transform-origin com palavra-chave, mostra a CADEIA de <g> que envolve
o elemento (do mais interno para fora), para saber onde cai o pivo local (0,0)."""
import io
import os
import re
import glob

RAIZ = os.path.dirname(os.path.abspath(__file__))
TAG = re.compile(r'<(/?)([a-zA-Z][\w:-]*)((?:"[^"]*"|\'[^\']*\'|[^>"\'])*?)(/?)>', re.S)
ORIG = re.compile(r'transform-origin:\s*([^;"]+)')
ANIM = re.compile(r'animation:\s*([a-zA-Z0-9_]+)')
OK_VAL = re.compile(r'^(0(px)?\s+0(px)?|\d+(\.\d+)?px\s+\d+(\.\d+)?px)$')


def kf(txt, nome, n=130):
    m = re.search(r'@keyframes\s+' + nome + r'\s*\{', txt)
    if not m:
        return '(nao existe)'
    j, depth = m.end(), 1
    while depth and j < len(txt):
        if txt[j] == '{':
            depth += 1
        elif txt[j] == '}':
            depth -= 1
        j += 1
    return re.sub(r'\s+', ' ', txt[m.start():j])[:n]


def ancestrais(txt, pos):
    """Devolve a pilha de <g ...> abertos na posicao, do mais interno para fora."""
    pilha = []
    for m in TAG.finditer(txt):
        if m.start() >= pos:
            break
        fecha, nome, attrs, auto = m.group(1), m.group(2), m.group(3), m.group(4)
        if nome != 'g':
            continue
        if fecha:
            if pilha:
                pilha.pop()
        elif not auto:
            pilha.append(attrs)
    return list(reversed(pilha))


por_padrao = {}
for f in sorted(glob.glob(os.path.join(RAIZ, '*', '*.html'))):
    rel = os.path.relpath(f, RAIZ).replace('\\', '/')
    txt = io.open(f, encoding='utf-8', errors='replace').read()
    for m in TAG.finditer(txt):
        attrs = m.group(3)
        if 'transform-origin' not in attrs:
            continue
        st = re.search(r'style="([^"]*)"', attrs)
        if not st:
            continue
        st = st.group(1)
        if 'fill-box' in st:
            continue
        o = ORIG.search(st)
        if not o or OK_VAL.match(o.group(1).strip()):
            continue
        a = ANIM.search(st)
        if not a:
            continue
        nome = a.group(1)
        corpo = kf(txt, nome)
        if not re.search(r'rotate|scale', corpo):
            continue
        anc = ancestrais(txt, m.start())
        # o ancestral mais interno que tem transform
        env = next((x for x in anc if 'transform=' in x), None)
        env = re.sub(r'\s+', ' ', env).strip() if env else 'NENHUM'
        chave = (nome, o.group(1).strip(), env[:70], corpo[:90])
        por_padrao.setdefault(chave, []).append('%s:%d'
                                                % (rel, txt.count('\n', 0, m.start()) + 1))

print('PADROES ENCONTRADOS: %d' % len(por_padrao))
print()
for i, (chave, ocorr) in enumerate(sorted(por_padrao.items(),
                                          key=lambda x: -len(x[1])), 1):
    nome, orig, env, corpo = chave
    print('--- [%d]  %d ocorrencia(s)' % (i, len(ocorr)))
    print('    anim   : %s   origin: %s' % (nome, orig))
    print('    envolve: %s' % env)
    print('    kf     : %s' % corpo)
    print('    em     : %s' % ', '.join(ocorr[:6]) + (' ...' if len(ocorr) > 6 else ''))

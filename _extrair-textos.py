# -*- coding: utf-8 -*-
"""
_extrair-textos.py — lista TODA string visivel de um arquivo animado.

Passo 1 de qualquer traducao: sem o inventario completo voce perde string
(nem o Read nem o Grep mostram a linha inteira — cada cena e UMA linha de
3000+ caracteres). Ver a secao "Traduzir um video para outro idioma" da skill.

So usa regex + leitura de arquivo. Nada de regex inline no shell (ver MEMORY:
o bash do Windows come a crase e o `\\s`).

Uso:
    python _extrair-textos.py video-longo/player-video-longo-7-legumes.html
    python _extrair-textos.py alho/shorts-garlic-honey-en.html
"""
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)

ARQ = sys.argv[1]
txt = open(ARQ, encoding='utf-8').read()
print('linhas: %d  bytes: %d' % (txt.count('\n') + 1, len(txt.encode('utf-8'))))
print('=' * 70)

# ── 1. JS object keys with literal strings ────────────────────────────
for chave in ['cap', 'sub', 'nome', 'nivel', 'sal', 'tempo', 'hint', 'cor']:
    vals = re.findall(r"\b%s\s*:\s*'((?:[^'\\]|\\.)*)'" % chave, txt)
    print('\n### %s: (%d)' % (chave, len(vals)))
    for v in vals:
        print('  | ' + v)

# ── 2. filmTimes array entries ────────────────────────────────────────
m = re.search(r'const filmTimes\s*=\s*\[(.*?)\]', txt, re.S)
if m:
    vals = re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(1))
    print('\n### filmTimes: (%d)' % len(vals))
    for v in vals:
        print('  | ' + v)

# ── 3. every <text>...</text> inner content ──────────────────────────
texts = re.findall(r'<text\b[^>]*>(.*?)</text>', txt, re.S)
print('\n### <text> (%d)' % len(texts))
vistos = {}
for t in texts:
    t = t.strip()
    vistos[t] = vistos.get(t, 0) + 1
for t, n in vistos.items():
    print('  [%dx] | %s' % (n, t))

# ── 4. tspan contents (if any) ────────────────────────────────────────
ts = re.findall(r'<tspan\b[^>]*>(.*?)</tspan>', txt, re.S)
if ts:
    print('\n### <tspan> (%d)' % len(ts))
    for t in ts:
        print('  | ' + t.strip())

# ── 5. static HTML text nodes between tags ───────────────────────────
corpo = txt.split('</style>', 1)[1]
corpo = corpo.split('<script>', 1)[0]
nos = re.findall(r'>([^<>{}]+)<', corpo)
print('\n### HTML estatico (%d)' % len(nos))
for n in nos:
    n2 = ' '.join(n.split())
    if n2:
        print('  | ' + n2)

# ── 6. strings concatenadas no JS (innerHTML / textContent) ──────────
print('\n### JS: strings em innerHTML/textContent')
for m in re.finditer(r"(innerHTML|textContent)\s*=\s*([^;]+);", txt):
    print('  | %s = %s' % (m.group(1), ' '.join(m.group(2).split())[:160]))

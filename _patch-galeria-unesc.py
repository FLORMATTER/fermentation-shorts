# -*- coding: utf-8 -*-
"""
A galeria imprimia o escape do JS cru: `sub:'2% salt \\u00b7 ready...'` virava
"2% salt \u00b7 ready..." no HTML, em vez de "2% salt . ready...". 3 dos 55 subs.

Conserto no GERADOR: desfaz \\uXXXX ao extrair `cap:` e `sub:`.

3 ancoras com contagem: qualquer uma fora do esperado -> ABORTA SEM GRAVAR.
"""
import io, os, re, shutil, sys

G = os.path.join('C:/Users/Saxa/Desktop/youtube-work', '_gerar-galeria.py')
d = io.open(G, encoding='utf-8').read()
ANTES = len(d)

AJUDA = '''def _unesc(s):
    """`cap:`/`sub:` vem do JS, onde \\u00b7 e' escape. Desfaz antes de ir para o HTML."""
    return re.sub(r'\\\\u([0-9a-fA-F]{4})',
                  lambda m: chr(int(m.group(1), 16)), s)


'''

edicoes = [
    # 1. o decodificador, antes do ler_short
    ('def ler_short(caminho_rel):\n', AJUDA + 'def ler_short(caminho_rel):\n'),
    # 2. o titulo (4 espacos de indentacao, nao 8)
    ("    titulo = m.group(1) if m else ''\n",
     "    titulo = _unesc(m.group(1)) if m else ''\n"),
    # 3. o sub
    ('        sub = m.group(1)\n', '        sub = _unesc(m.group(1))\n'),
]

for i, (velho, novo) in enumerate(edicoes, 1):
    n = d.count(velho)
    if n != 1:
        print('ERRO: ancora %d casou %d vez(es), esperado 1. Nada gravado.' % (i, n))
        sys.exit(1)
    d = d.replace(velho, novo)

for t in ['def _unesc(s):', "titulo = _unesc(", 'sub = _unesc(']:
    if t not in d:
        print('ERRO: trecho novo ausente: %r. Nada gravado.' % t)
        sys.exit(1)

if len(d) <= ANTES:
    print('ERRO: nao cresceu. Nada gravado.')
    sys.exit(1)

try:
    compile(d, G, 'exec')
except SyntaxError as e:
    print('ERRO de sintaxe: %s (linha %s). Nada gravado.' % (e.msg, e.lineno))
    sys.exit(1)

shutil.copy2(G, G + '.antes-do-unesc')
with io.open(G, 'w', encoding='utf-8', newline='') as f:
    f.write(d)
print('OK: %d -> %d chars' % (ANTES, len(d)))

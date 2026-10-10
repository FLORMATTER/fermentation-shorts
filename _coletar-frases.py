# -*- coding: utf-8 -*-
"""
_coletar-frases.py — todas as frases visiveis dos videos em portugues, sem repetir.

Serve para montar UM dicionario PT->EN para a serie inteira em vez de traduzir
arquivo por arquivo. Mostra a frequencia: frase que aparece em 6 arquivos e
traduzida uma vez so.

Uso:
    python _coletar-frases.py                 # so os videos em PT (sem _arquivo/)
    python _coletar-frases.py --tudo
    python _coletar-frases.py --textos        # so os <text> (texto desenhado no SVG)
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
IGNORAR = ('.workbuddy-ai', '_revisao', 'node_modules')
PASTAS_FORA = ('aulas', 'guias', '_arquivo')

PT = re.compile(r'\b(que|para|com|nao|não|você|voce|água|agua|sal|dias|semanas|'
                r'pote|dentes?|mão|mao|fermenta|prensa|massageia|repolho|cenoura|'
                r'rabanete|beterraba|couve|alho|cebola|pepino|pronta|pronto|'
                r'crocante|bancada|esperar|volta|cor|sua|seu|isso|mais)\b', re.I)


def arquivos(tudo):
    out = []
    for base, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [x for x in dirs if x not in IGNORAR]
        rel = os.path.relpath(base, RAIZ).replace('\\', '/')
        pasta = rel.split('/')[0]
        if not tudo and pasta in PASTAS_FORA:
            continue
        for a in sorted(arqs):
            if a.endswith('.html') and a != 'galeria-shorts.html':
                out.append(os.path.join(base, a))
    return sorted(out)


def coletar(d, so_textos=False):
    """Devolve as strings visiveis do arquivo."""
    out = []
    if not so_textos:
        for chave in ('cap', 'sub', 'hint', 'nome', 'nivel', 'sal', 'tempo'):
            out += re.findall(r"\b%s\s*:\s*'((?:[^'\\]|\\.)*)'" % chave, d)
        corpo = d.split('</style>', 1)[-1].split('<script>', 1)[0]
        out += [' '.join(n.split()) for n in re.findall(r'>([^<>{}]+)<', corpo)]
    out += [t.strip() for t in re.findall(r'<text\b[^>]*>(.*?)</text>', d, re.S)]
    return [s for s in out if s.strip()]


def main():
    tudo = '--tudo' in sys.argv
    so_textos = '--textos' in sys.argv

    freq = {}
    por_arq = {}
    for p in arquivos(tudo):
        d = io.open(p, encoding='utf-8', errors='replace').read()
        rel = os.path.relpath(p, RAIZ).replace('\\', '/')
        st = coletar(d, so_textos)
        txt = ' '.join(st)
        # so entram as strings que parecem portugues
        pt = [s for s in st if PT.search(s)]
        if not pt:
            continue
        por_arq[rel] = len(set(pt))
        for s in set(pt):
            freq.setdefault(s, set()).add(rel)

    uniq = sorted(freq.items(), key=lambda x: (-len(x[1]), x[0]))
    print('arquivos em PT : %d' % len(por_arq))
    print('frases unicas  : %d' % len(uniq))
    print('=' * 78)
    for rel, n in sorted(por_arq.items(), key=lambda x: -x[1]):
        print('  %-52s %3d frase(s)' % (rel, n))
    print('=' * 78)
    for s, arqs in uniq:
        print('[%dx] %s' % (len(arqs), s))
    return 0


if __name__ == '__main__':
    sys.exit(main())

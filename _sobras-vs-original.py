# -*- coding: utf-8 -*-
"""_sobras-vs-original.py — o teste DEFINITIVO de traducao.

Ideia: nao tentar adivinhar se uma frase 'parece portugues' (heuristica de lista
de palavras falha, como ja provamos). Em vez disso, comparar o arquivo -en com o
original em portugues:

    se a MESMA string visivel aparece nos DOIS arquivos, ela nao foi traduzida.

Isso nao depende de dicionario nem de regex de idioma. E verificavel: se o script
nao acha nada, e porque nao sobrou nenhuma string igual a do original.

Uso:
    python _sobras-vs-original.py            # todos os pares
    python _sobras-vs-original.py --detalhe  # mostra tambem o que e neutro
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
IGNORAR = ('.workbuddy-ai', '_revisao', 'node_modules')


def visiveis(d):
    """Strings que o espectador ve (mesma extracao usada no _traduzir-serie)."""
    out = []
    for chave in ('cap', 'sub', 'hint', 'nome', 'nivel', 'sal', 'tempo'):
        out += re.findall(r"\b%s\s*:\s*'((?:[^'\\]|\\.)*)'" % chave, d)
    out += [t.strip() for t in re.findall(r'<text\b[^>]*>(.*?)</text>', d, re.S)]
    corpo = d.split('</style>', 1)[-1].split('<script>', 1)[0]
    out += [' '.join(n.split()) for n in re.findall(r'>([^<>{}]+)<', corpo)]
    return {s for s in out if s.strip()}


def tem_letras(s):
    """Pelo menos 2 letras seguidas -> vale a pena olhar."""
    return re.search(r'[A-Za-zÀ-ÿ]{2}', s) is not None


# iguais nos dois idiomas porque NAO TEM IDIOMA: numero, unidade, emoji,
# nome proprio, template de JS. Nao sao sobra de traducao.
NEUTRO = re.compile(
    r'^(pH|kg|g|ml|L|TOTAL: 500 g|⚡ SPEED|10 MIN|Pizza|Tacos|Sushi|'
    r'OBS|Canva|CapCut|YouTube|'
    r'\d+\s*(MIN|SEG|G|KG|ML|L|MM|CM)|'
    r'\$\{[^}]*\}|[^A-Za-zÀ-ÿ]*)$')


def pares():
    """(arquivo -en, arquivo pt) para todo -en que tenha irmao em portugues."""
    en_files = []
    for base, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [x for x in dirs if x not in IGNORAR]
        for a in arqs:
            if a.endswith('.html') and re.search(r'-en(\.|-|_)', a):
                en_files.append(os.path.join(base, a))

    out = []
    for p in sorted(en_files):
        pasta, nome = os.path.split(p)
        # remove o -en, preservando sufixos como -1080x1920
        m = re.match(r'^(.*)-en(\.html)$', nome)
        m2 = re.match(r'^(.*)-en(-[^.]+\.html)$', nome)
        cand = None
        if m2:
            cand = os.path.join(pasta, m2.group(1) + m2.group(2))
        if (not cand or not os.path.exists(cand)) and m:
            cand = os.path.join(pasta, m.group(1) + m.group(2))
        if cand and os.path.exists(cand):
            out.append((p, cand))
        else:
            out.append((p, None))
    return out


def main():
    detalhe = '--detalhe' in sys.argv
    total = 0
    limpos = 0
    sem_par = []

    for en, pt in pares():
        rel = os.path.relpath(en, RAIZ).replace('\\', '/')
        if not pt:
            sem_par.append(rel)
            continue
        s_en = visiveis(io.open(en, encoding='utf-8', errors='replace').read())
        s_pt = visiveis(io.open(pt, encoding='utf-8', errors='replace').read())
        iguais = sorted(x for x in (s_en & s_pt) if tem_letras(x))
        reais = [x for x in iguais if not NEUTRO.match(x)]
        neutras = [x for x in iguais if NEUTRO.match(x)]
        if reais:
            total += len(reais)
            print('\n%s  (%d SOBRA REAL)' % (rel, len(reais)))
            print('   original: %s' % os.path.relpath(pt, RAIZ).replace('\\', '/'))
            for s in reais:
                marca = 'PT' if re.search(r'[ãõçáéíóúâêôàÃÕÇÁÉÍÓÚÂÊÔÀ]', s) else '  '
                print('   [%s] %s' % (marca, s))
        else:
            limpos += 1
            extra = '  (+%d neutra: %s)' % (len(neutras), ', '.join(neutras)) if neutras else ''
            print('%-52s  LIMPO%s' % (rel, extra))

    print('\n' + '=' * 74)
    print('pares conferidos : %d' % (len([1 for _, p in pares() if p])))
    print('pares limpos     : %d' % limpos)
    print('STRINGS SOBRADAS : %d' % total)
    if sem_par:
        print('sem original PT  : %d  (nao da pra conferir por comparacao)' % len(sem_par))
        for s in sem_par:
            print('     - %s' % s)
    print('=' * 74)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())

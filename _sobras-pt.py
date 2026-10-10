# -*- coding: utf-8 -*-
"""_sobras-pt.py — acha portugues que sobrou nos arquivos JA traduzidos (-en.html).

Por que existe: o regex do _traduzir-serie.py termina cada alternativa com \\b.
Em Python 3 o \\b usa \\w, e letra acentuada CONTA como \\w. Entao
    \\bfermenta\\b  NAO casa em 'FERMENTACAO'
    \\bcrocante\\b  NAO casa em 'CROCANTES'
Ou seja: o relatorio 'FRASES SEM TRADUCAO: 0' nao provava nada -- ele so mostrava
o que o regex conseguia enxergar. Este script usa TRES detectores independentes:

  1. DIACRITICO  -> qualquer string visivel com a a o c cedilha etc.  (alta precisao)
  2. RADICAL     -> \\b + radical, SEM \\b no fim  -> pega plural e derivado
  3. PALAVRA     -> o regex antigo, mantido para comparar

Uso:
    python _sobras-pt.py                 # todos os -en.html
    python _sobras-pt.py <arquivo>       # um so
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
IGNORAR = ('.workbuddy-ai', '_revisao', 'node_modules')

# 1. diacriticos que so existem em portugues (ingles nao usa nenhum)
PT_DIAC = re.compile(r'[ãõçáéíóúâêôàÃÕÇÁÉÍÓÚÂÊÔÀ]')

# 2. radicais: sem \b no fim, de proposito -> pega plural/derivado
PT_RADICAL = re.compile(
    r'\b(fermenta|tingi|tinge|crocant|legum|pot[ei]s?|pront[ao]|volt|m[ãa]os?|'
    r'su[ao]s?|seu?s?|semanas?|dias?|horas?|minutos?|'
    r'cebola|cenoura|rabanete|beterraba|couve|alho|pepino|repolho|'
    r'salmoura|bancada|prensa|massagei|iodo|faca|colher|garrafa|toalha|geladeira|'
    r'vidro|tampa|peso|cor|mais|isso|sem|com|para|que|nao|não|voce|você|'
    r'água|agua|sal|só|sua|seu|nivel|tempo|nome|hint|dica|pronto)', re.I)

# 3. o regex antigo, so para comparar
PT_PALAVRA = re.compile(r'\b(que|para|com|nao|não|você|voce|água|agua|sal|dias|semanas|'
                        r'pote|dentes?|mão|mao|fermenta|prensa|massageia|repolho|cenoura|'
                        r'rabanete|beterraba|couve|alho|cebola|pepino|pronta|pronto|'
                        r'crocante|bancada|esperar|volta|cor|sua|seu|isso|mais|legume|'
                        r'tinge|salmoura|iodo|sem|só|nao|faca|água)\b', re.I)


def visiveis(d):
    """Todas as strings que o espectador ve (mesma extracao do _traduzir-serie)."""
    out = []
    for chave in ('cap', 'sub', 'hint', 'nome', 'nivel', 'sal', 'tempo'):
        out += re.findall(r"\b%s\s*:\s*'((?:[^'\\]|\\.)*)'" % chave, d)
    out += [t.strip() for t in re.findall(r'<text\b[^>]*>(.*?)</text>', d, re.S)]
    corpo = d.split('</style>', 1)[-1].split('<script>', 1)[0]
    out += [' '.join(n.split()) for n in re.findall(r'>([^<>{}]+)<', corpo)]
    return [s for s in out if s.strip()]


def arquivos_en():
    out = []
    for base, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [x for x in dirs if x not in IGNORAR]
        for a in sorted(arqs):
            if a.endswith('.html') and re.search(r'-en(\.|-|_)', a):
                out.append(os.path.join(base, a))
    return sorted(out)


def motivo(s):
    """Qual detector disparou, do mais preciso para o menos."""
    if PT_DIAC.search(s):
        return 'DIACRITICO'
    m = PT_RADICAL.search(s)
    if m:
        return 'RADICAL(%s)' % m.group(0)
    m = PT_PALAVRA.search(s)
    if m:
        return 'PALAVRA(%s)' % m.group(0)
    return None


def main():
    if len(sys.argv) > 1 and sys.argv[1].endswith('.html'):
        lista = [sys.argv[1] if os.path.isabs(sys.argv[1])
                 else os.path.join(RAIZ, sys.argv[1])]
    else:
        lista = arquivos_en()

    total = 0
    limpos = 0
    for p in lista:
        d = io.open(p, encoding='utf-8', errors='replace').read()
        rel = os.path.relpath(p, RAIZ).replace('\\', '/')
        achados = []
        for s in sorted(set(visiveis(d))):
            m = motivo(s)
            if m:
                achados.append((m, s))
        if achados:
            total += len(achados)
            print('\n%s  (%d)' % (rel, len(achados)))
            for m, s in achados:
                print('   [%-16s] %s' % (m, s))
        else:
            limpos += 1

    print('\n' + '=' * 74)
    print('arquivos varridos : %d' % len(lista))
    print('arquivos limpos   : %d' % limpos)
    print('STRINGS EM PT     : %d' % total)
    print('=' * 74)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())

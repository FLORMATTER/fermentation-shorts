# -*- coding: utf-8 -*-
"""
Em que PONTO do proprio timeline o modo `--final` congela cada animacao.

O `_revisar-cenas.py --final` injeta
    *{animation-delay:-1s!important; animation-play-state:paused!important}
Isso adianta a animacao em 1 s e pausa. Com `fill: both` o elemento so' aparece no
keyframe de 100% se a animacao durar **1 s ou menos**. Animacao de 2,4 s congela em
41% — no meio do movimento — e o elemento pode sair como FANTASMA no PNG, sem
nenhum defeito no arquivo.

Uso:  python _frozen-final.py <arquivo.html> [...]

Le somente. Nao escreve nada.
"""
import io
import re
import sys

# `animation: nome 1.6s ease-out infinite` / `.6s` / `1600ms`
RE_ANIM = re.compile(r'animation\s*:\s*([^;"}\n]+)')
RE_DUR = re.compile(r'(?<![\w.])(\d*\.?\d+)(ms|s)(?![\w])')


def duracao(txt):
    """Duracao em segundos da declaracao, ou None se nao der para ler."""
    for val, un in RE_DUR.findall(txt):
        if un == 'ms':
            return float(val) / 1000.0
        return float(val)
    return None


def analisa(caminho):
    with io.open(caminho, encoding='utf-8', errors='replace') as f:
        d = f.read()

    linhas = []
    for m in RE_ANIM.finditer(d):
        decl = m.group(1).strip()
        if decl.startswith('none') or decl.startswith('name'):
            continue
        dur = duracao(decl)
        if dur is None:
            continue
        # em que % do timeline o -1s para
        pct = 100.0 * 1.0 / dur if dur > 0 else 100.0
        linhas.append((decl, dur, min(pct, 100.0)))

    if not linhas:
        print('  (nenhuma animacao com duracao legivel)')
        return 0, 0

    # agrupa por declaracao, para nao repetir a mesma 20x
    vistos = {}
    for decl, dur, pct in linhas:
        vistos.setdefault(decl, []).append((dur, pct))

    ruins = 0
    for decl in sorted(vistos, key=lambda x: vistos[x][0][1]):
        dur, pct = vistos[decl][0]
        n = len(vistos[decl])
        if pct >= 99.9:
            marca = 'ok   '
        else:
            marca = 'CONGELA'
            ruins += 1
        print('  %s  %-34s dur=%-6.2fs  para em %5.1f%%  (%dx)'
              % (marca, decl[:34], dur, pct, n))
    return len(vistos), ruins


def main():
    alvos = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not alvos:
        print(__doc__)
        return 2

    for caminho in alvos:
        print('== %s ==' % caminho)
        try:
            total, ruins = analisa(caminho)
        except IOError as e:
            print('  nao abriu: %s' % e)
            continue
        if ruins:
            print('  -> %d de %d animacoes NAO chegam ao fim no `--final`.' % (ruins, total))
            print('     Se um elemento parecer fantasma/apagado no PNG do --final,')
            print('     rode `--no-anim` antes de chamar de defeito.')
        else:
            print('  -> todas as %d animacoes cabem no -1s: o --final e fiel.' % total)
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())

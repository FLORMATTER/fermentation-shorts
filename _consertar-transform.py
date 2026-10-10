#!/usr/bin/env python3
"""
_consertar-transform.py — conserta o bug do `transform=` + `animation` no MESMO tag.

PROBLEMA
    <g transform="translate(202,372)" style="animation:floatUpDown 3.4s infinite"> … </g>
    Em SVG o `transform` e um ATRIBUTO DE APRESENTACAO: a declaracao CSS (inclusive a
    que vem de um @keyframes) GANHA dele. Entao o elemento e desenhado na ORIGEM do
    SVG (canto superior esquerdo) em vez do lugar certo.

CORRECAO
    <g transform="translate(202,372)">
      <g style="animation:floatUpDown 3.4s infinite"> … </g>
    </g>
    O `transform` fica no <g> de FORA, a animacao no de DENTRO. Sem conflito.

So mexe em tag que tem `transform="…"` E `style="animation:X"` onde o corpo de
@keyframes X realmente anima `transform`. Se o keyframe so mexe em `opacity`, nao e bug.

Uso:
    python _consertar-transform.py            # dry-run: so mostra o que faria
    python _consertar-transform.py --apply    # grava
"""
import io
import os
import re
import sys
import glob

SKIP_DIRS = ('aulas', '_arquivo', '.workbuddy-ai')

# casa tag de abertura E de fechamento; tolera '>' dentro de valor entre aspas
ANYTAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:"[^"]*"|\'[^\']*\'|[^>"\'])*)>', re.S)


def keyframe_bodies(d):
    out = {}
    for m in re.finditer(r'@keyframes\s+([a-zA-Z0-9_]+)\s*\{', d):
        j, depth = m.end(), 1
        while depth:
            if d[j] == '{':
                depth += 1
            elif d[j] == '}':
                depth -= 1
            j += 1
        out[m.group(1)] = d[m.end():j]
    return out


def find_target(d, bod):
    """Devolve a PRIMEIRA tag conflitante (a mais a esquerda) ou None."""
    for m in ANYTAG.finditer(d):
        if m.group(1) == '/':
            continue
        name, attrs = m.group(2), m.group(3)
        mt = re.search(r'\s*transform="([^"]*)"', attrs)
        if not mt:
            continue
        ms = re.search(r'\bstyle="([^"]*)"', attrs)
        if not ms:
            continue
        anims = re.findall(r'animation:\s*([a-zA-Z0-9_]+)', ms.group(1))
        if not any('transform' in bod.get(a, '') for a in anims):
            continue
        return m, name, attrs, mt
    return None


def matching_close_end(d, open_end, name):
    """Fim da tag de fechamento que casa com a abertura que termina em `open_end`."""
    depth = 1
    for m in ANYTAG.finditer(d, open_end):
        if m.group(2) != name:
            continue
        if m.group(1) == '/':
            depth -= 1
            if depth == 0:
                return m.end()
        elif not m.group(3).rstrip().endswith('/'):
            depth += 1
    return None


def fix_text(d):
    bod = keyframe_bodies(d)
    n = 0
    while True:
        t = find_target(d, bod)
        if t is None:
            break
        m, name, attrs, mt = t
        val = mt.group(1)
        new_attrs = attrs[:mt.start()] + attrs[mt.end():]      # tira o transform
        open_tag = '<' + name + new_attrs + '>'
        outer = '<g transform="' + val + '">'

        if attrs.rstrip().endswith('/'):                        # tag auto-fechada
            d = d[:m.start()] + outer + open_tag + '</g>' + d[m.end():]
        else:                                                   # tag contentor
            ce = matching_close_end(d, m.end(), name)
            if ce is None:
                raise RuntimeError('sem </%s> para a tag em %d' % (name, m.start()))
            d = d[:m.start()] + outer + open_tag + d[m.end():ce] + '</g>' + d[ce:]

        n += 1
        if n > 500:
            raise RuntimeError('loop infinito — abortado')
    return d, n


def targets():
    out = []
    for p in glob.glob('**/*.html', recursive=True):
        if any(p.replace('\\', '/').startswith(s + '/') for s in SKIP_DIRS):
            continue
        out.append(p)
    return sorted(out)


def main():
    apply_ = '--apply' in sys.argv
    total = 0
    for p in targets():
        d = io.open(p, encoding='utf-8', newline='').read()
        try:
            novo, n = fix_text(d)
        except RuntimeError as e:
            print('  ERRO em %s: %s' % (p, e))
            continue
        if not n:
            continue
        # sanidade: a contagem de tags nao pode mudar de tamanho
        if novo.count('<') != d.count('<') + 2 * n:
            print('  AVISO %s: contagem de "<" inesperada' % p)
        print('%-52s %2d conflito(s) %s' % (p, n, 'GRAVADO' if apply_ else '(dry-run)'))
        if apply_:
            io.open(p, 'w', encoding='utf-8', newline='').write(novo)
        total += n
    print('-' * 66)
    print('TOTAL: %d conflito(s) em %s' % (total, 'ARQUIVOS GRAVADOS' if apply_ else 'DRY-RUN'))
    return 0


if __name__ == '__main__':
    sys.exit(main())

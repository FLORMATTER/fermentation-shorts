# -*- coding: utf-8 -*-
"""_provar-guarda-60s.py — a guarda nova pega o arquivo quebrado de verdade?

Roda a MESMA checagem que eu acabei de por no gerador contra o arquivo que saiu
com o bug do offset (10 cenas, 9 `</svg>`). Se ela acusar, ela serve. Se passar,
ela e' decoracao.

Uso:  python _provar-guarda-60s.py <arquivo>
"""
import io
import re
import sys


def checa(caminho):
    with io.open(caminho, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    ids = re.findall(r'<svg class="scene[^"]*" id="(s\d+)"', d)
    fecha = d.count('</svg>')
    print('  %s' % caminho)
    print('    cenas: %d (%s)' % (len(ids), ' '.join(ids)))
    print('    </svg>: %d' % fecha)
    if fecha != len(ids):
        print('    GUARDA ACUSA: %d cenas mas %d `</svg>` — cena aberta.'
              % (len(ids), fecha))
        return 1
    print('    guarda silencia (o arquivo esta fechado)')
    return 0


if __name__ == '__main__':
    sys.exit(checa(sys.argv[1]))

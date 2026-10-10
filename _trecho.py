# -*- coding: utf-8 -*-
"""
_trecho.py — mostra um pedaco de uma linha gigante.

Neste projeto as cenas ficam em UMA linha de 3000+ caracteres, entao nem o
Grep nem o Read mostram o trecho que interessa (os dois truncam). Este script
imprime uma janela de texto em volta de um termo.

Uso:
    python _trecho.py arquivo.html "NOT ONE MINUTE MORE"
    python _trecho.py arquivo.html "translate(202,510)" --antes 200 --depois 400
"""
import io
import sys


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 2:
        print(__doc__)
        return 1
    arquivo, termo = args[0], args[1]
    antes, depois = 240, 240
    if '--antes' in sys.argv:
        antes = int(sys.argv[sys.argv.index('--antes') + 1])
    if '--depois' in sys.argv:
        depois = int(sys.argv[sys.argv.index('--depois') + 1])

    d = io.open(arquivo, encoding='utf-8').read()
    i = d.find(termo)
    if i == -1:
        print('nao encontrado: %r' % termo)
        return 1
    ini = max(0, i - antes)
    fim = min(len(d), i + len(termo) + depois)
    print('linha %d | offset %d' % (d.count('\n', 0, i) + 1, i))
    print('-' * 68)
    print(d[ini:fim])
    print('-' * 68)
    return 0


if __name__ == '__main__':
    sys.exit(main())

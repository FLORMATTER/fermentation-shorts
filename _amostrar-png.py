# -*- coding: utf-8 -*-
"""
_amostrar-png.py — medir cor de verdade em vez de "achar que da' pra ver".

Uso:
    python _amostrar-png.py <png> x1,y1 x2,y2 ...
    python _amostrar-png.py <png> --grade x0,y0,x1,y1 passo

Serve para provar contraste: se dois pontos que deviam ser diferentes (jarro
vazio x salmoura) dao o mesmo RGB, o liquido NAO aparece — nao adianta olhar.

Imprime tambem a distancia entre cada par de amostras (norma em RGB).
"""
import sys
from PIL import Image

def hexa(rgb):
    return '#%02x%02x%02x' % rgb[:3]

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    arq = sys.argv[1]
    im = Image.open(arq).convert('RGB')
    print('arquivo: %s  (%dx%d)' % (arq, im.width, im.height))

    if sys.argv[2] == '--grade':
        x0, y0, x1, y1 = [int(v) for v in sys.argv[3].split(',')]
        passo = int(sys.argv[4])
        for y in range(y0, y1 + 1, passo):
            linha = []
            for x in range(x0, x1 + 1, passo):
                linha.append(hexa(im.getpixel((x, y))))
            print('  y=%-4d %s' % (y, ' '.join(linha)))
        return 0

    pontos = []
    for arg in sys.argv[2:]:
        x, y = [int(v) for v in arg.split(',')]
        cor = im.getpixel((x, y))
        pontos.append((arg, cor))
        print('  %-10s %s' % (arg, hexa(cor)))

    if len(pontos) >= 2:
        print('distancias:')
        for i in range(len(pontos) - 1):
            a, b = pontos[i][1], pontos[i + 1][1]
            d = sum((a[k] - b[k]) ** 2 for k in range(3)) ** .5
            print('  %s -> %s : %5.1f  %s' % (
                pontos[i][0], pontos[i + 1][0], d,
                'IGUAL (nao da pra ver)' if d < 12 else
                'fraco' if d < 30 else 'visivel'))
    return 0

if __name__ == '__main__':
    sys.exit(main())

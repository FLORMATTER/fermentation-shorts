"""_extrair-cena.py — imprime o bloco <svg class="scene" id="sN"> inteiro, cru.

As cenas sao UMA linha gigante, entao grep devolve a linha toda (que tem 7 cenas).
Isto aqui devolve so' a cena pedida, para usar como ancora exata.

    python _extrair-cena.py <arquivo.html> s3
"""
import re
import sys


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    arq, cena = sys.argv[1], sys.argv[2]
    d = open(arq, encoding='utf-8', newline='').read()
    m = re.search(r'<svg class="scene[^"]*"[^>]*id="%s".*?</svg>' % re.escape(cena), d, re.S)
    if not m:
        print('nao achei a cena %s em %s' % (cena, arq))
        return 1
    print(m.group(0).replace('\r\n', '\n'))
    return 0


if __name__ == '__main__':
    sys.exit(main())

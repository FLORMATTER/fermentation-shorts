# -*- coding: utf-8 -*-
"""
_checar-js.py — checa a SINTAXE do JavaScript embutido no HTML.

Por que existe: um erro de sintaxe (uma aspa desbalanceada, por exemplo, vinda de
uma traducao ou de um find-replace) derruba o arquivo inteiro — a pagina abre,
fica em branco e NAO aparece nada na tela. O `_validar-short.py` nao olha para
isso: ele confere keyframes, url(#x), hex e coordenadas.

Usa o `node --check`, que so valida a sintaxe (nao executa, entao nao precisa de DOM).

Uso:
    python _checar-js.py arquivo.html
    python _checar-js.py arquivo.html --mostrar   # imprime o JS extraido
"""
import io
import os
import re
import subprocess
import sys

NODE = r'C:\Users\Saxa\.workbuddy-ai\binaries\node\versions\22.22.2-2\node.exe'


def acha_node():
    if os.path.exists(NODE):
        return NODE
    for p in os.environ.get('PATH', '').split(os.pathsep):
        c = os.path.join(p, 'node.exe')
        if os.path.exists(c):
            return c
        c = os.path.join(p, 'node')
        if os.path.exists(c):
            return c
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 1
    arquivo = args[0]
    d = io.open(arquivo, encoding='utf-8').read()

    blocos = re.findall(r'<script[^>]*>(.*?)</script>', d, re.S)
    if not blocos:
        print('nenhum <script> em %s' % arquivo)
        return 0

    node = acha_node()
    if not node:
        print('node nao encontrado — nao da para checar a sintaxe')
        return 1

    print('%s — %d bloco(s) de <script>' % (os.path.basename(arquivo), len(blocos)))
    falhou = 0
    for i, js in enumerate(blocos):
        tmp = os.path.join(os.environ.get('TEMP', '.'), '_checar_js_%d.js' % i)
        io.open(tmp, 'w', encoding='utf-8', newline='').write(js)
        r = subprocess.run([node, '--check', tmp], capture_output=True, text=True)
        if r.returncode == 0:
            print('  [ok] bloco %d — %d linhas' % (i, js.count('\n') + 1))
        else:
            falhou += 1
            print('  [X] bloco %d — ERRO DE SINTAXE:' % i)
            for linha in (r.stderr or '').strip().splitlines()[:12]:
                print('      ' + linha)
        if '--mostrar' in sys.argv:
            print('-' * 66)
            print(js)
            print('-' * 66)
        try:
            os.remove(tmp)
        except OSError:
            pass

    if not falhou:
        print('\nOK — o JavaScript esta sintaticamente valido.')
    return 1 if falhou else 0


if __name__ == '__main__':
    sys.exit(main())

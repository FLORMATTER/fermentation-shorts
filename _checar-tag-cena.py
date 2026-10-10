"""_checar-tag-cena.py — procura o rotulo "undefined" que aparece NA TELA do video.

O motor de gravacao (`_mp4/render.js`, linha ~128) desenha `s.tag` num rotulo no topo
da cena, em TODOS os videos:

    ... + '>' + esc(s.tag) + '</text>';

Se o array `scenes` do short nao tiver o campo `tag`, `esc(undefined)` vira a string
**"undefined"** e ela sai QUEIMADA no mp4. O `_validar-short.py` nao ve isso — ele
confere animacao e keyframe, nao texto de overlay. E o proprio short nao ve: quem
escreve o rotulo e' o motor, nao o short.

Primeira versao deste script errou por isso: procurava `.tag` dentro do short (que
nunca tem) em vez de conferir se o campo existe no array `scenes`.

    python _checar-tag-cena.py            # todos os shorts da serie
    python _checar-tag-cena.py <arq>      # um so
"""
import glob
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
PULAR = ('_arquivo/', '_revisao/', 'node_modules/', '.workbuddy-ai/')


def analisa(caminho):
    d = open(caminho, encoding='utf-8', newline='').read()
    m = re.search(r'const scenes\s*=\s*\[(.*?)\];', d, re.S)
    if not m:
        return None
    itens = re.findall(r'\{[^{}]*\}', m.group(1))
    if not itens:
        return None
    faltando = [i for i, it in enumerate(itens) if not re.search(r'\btag\s*:', it)]
    return len(itens), faltando


def main():
    if len(sys.argv) > 1:
        arquivos = [sys.argv[1]]
    else:
        arquivos = []
        for f in glob.glob(os.path.join(RAIZ, '**', '*.html'), recursive=True):
            rel = os.path.relpath(f, RAIZ).replace('\\', '/')
            if any(rel.startswith(p) for p in PULAR):
                continue
            if '<svg class="scene' in open(f, encoding='utf-8', errors='replace').read():
                arquivos.append(f)
        arquivos.sort()

    quebrados = []
    for f in arquivos:
        rel = os.path.relpath(f, RAIZ).replace('\\', '/')
        r = analisa(f)
        if not r:
            continue
        n, faltando = r
        if faltando:
            print('  [X] %-50s %d/%d cena(s) sem tag -> "undefined"' % (rel, len(faltando), n))
            quebrados.append(rel)

    print('\narquivos conferidos  : %d' % len(arquivos))
    print('com rotulo quebrado  : %d' % len(quebrados))
    if quebrados:
        print('\nO .mp4 destes ja\' saiu com "undefined" queimado. Corrigir e regravar.')
    return 1 if quebrados else 0


if __name__ == '__main__':
    sys.exit(main())

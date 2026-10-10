"""_textos-cena.py — lista o texto DESENHADO dentro de cada <svg class="scene">.

    python _textos-cena.py <arquivo>.html
    python _textos-cena.py <arquivo>.html --cena s6

Por que existe: as cenas sao uma linha gigante e o `_trecho.py` devolve uma janela
de caracteres que mistura duas cenas. Para saber o que esta ESCRITO numa cena
especifica (o que o render vai mostrar), este script separa por cena e por
`<text>`, na ordem em que aparecem no arquivo.

Nao le o `cap:`/`sub:`/`tag:` do array `scenes` — esses sao a barra de legenda e
o rotulo, que sao HTML por cima. Aqui e' so o desenho.
"""
import re
import sys

SCENE = re.compile(r'<svg class="scene[^"]*"[^>]*id="(s\d)"[^>]*>([\s\S]*?)</svg>')
TEXTO = re.compile(r'<text\b[^>]*>([\s\S]*?)</text>')
TSPAN = re.compile(r'<tspan\b[^>]*>([\s\S]*?)</tspan>')


def limpa(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return ' '.join(t.split())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    arq = sys.argv[1]
    so = None
    if '--cena' in sys.argv:
        so = sys.argv[sys.argv.index('--cena') + 1]

    d = open(arq, encoding='utf-8', errors='replace').read()
    cenas = SCENE.findall(d)
    if not cenas:
        print('nenhuma <svg class="scene"> encontrada')
        return 1

    # o array scenes (barra de legenda) para dar contexto
    caps = {}
    for m in re.finditer(r"id:'(s\d)'[^}]*?cap:'([^']*)'[^}]*?sub:'([^']*)'", d):
        caps[m.group(1)] = (m.group(2), m.group(3))

    for sid, corpo in cenas:
        if so and sid != so:
            continue
        cap, sub = caps.get(sid, ('?', '?'))
        print('--- %s   cap: %s | sub: %s' % (sid, cap, sub))
        for t in TEXTO.findall(corpo):
            linhas = [limpa(x) for x in TSPAN.findall(t)] or [limpa(t)]
            linhas = [x for x in linhas if x]
            if linhas:
                print('      ' + ' / '.join(linhas))
    return 0


if __name__ == '__main__':
    sys.exit(main())

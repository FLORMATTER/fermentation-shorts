#!/usr/bin/env python3
"""
_validar-short.py — checklist automatico dos HTMLs de animacao.

Substitui o bloco de greps do README (que da falso negativo: com duas listas
vazias os tres `comm` saem vazios e parece tudo limpo, mas pode ser que
NENHUM keyframe exista e o video fique parado).

Uso:
    python _validar-short.py                 # valida todos os shorts do projeto
    python _validar-short.py arquivo.html    # valida um arquivo
    python _validar-short.py pasta/*.html    # valida varios

Sai com codigo 1 se achar qualquer problema.
"""
import re
import sys
import os
import glob

# pastas que nao sao shorts (guias de leitura, aulas, arquivo morto)
# _revisao = PNGs e folhas temporarias do _revisar-cenas.py, que sao HTML gerado:
# sem isto o validador acusa "problema" em arquivo que ele mesmo criou.
SKIP_DIRS = ('aulas', '_arquivo', '.workbuddy-ai', '_revisao', 'guias')


def find_shorts():
    out = []
    for p in glob.glob('**/*.html', recursive=True):
        if any(p.replace('\\', '/').startswith(d + '/') for d in SKIP_DIRS):
            continue
        out.append(p)
    return sorted(out)


def check(path):
    d = open(path, encoding='utf-8', errors='replace').read()
    problems = []

    a = set(re.findall(r'animation:\s*([a-zA-Z0-9_]+)', d))
    k = set(re.findall(r'@keyframes\s+([a-zA-Z0-9_]+)', d))
    u = set(re.findall(r'url\(#([a-zA-Z0-9_-]+)\)', d))
    i = set(re.findall(r'id="([a-zA-Z0-9_-]+)"', d))

    print('=' * 66)
    print(path)
    print('  animations usados :', len(a))
    print('  keyframes defs    :', len(k))

    # o falso negativo classico: animacao declarada e nenhum keyframe
    if a and not k:
        problems.append('animacoes existem mas NENHUM @keyframes -> VIDEO PARADO')

    if a - k:
        problems.append('animation sem @keyframes: %s' % sorted(a - k))
    if k - a:
        problems.append('@keyframes nunca usado: %s' % sorted(k - a))
    if u - i:
        problems.append('url(#x) sem id correspondente: %s' % sorted(u - i))

    # hex corrompido (ex.: #8b8koln). Antes de varrer, remove url(#id) e id="x"
    # — um id de gradiente pode parecer hex (#cCar) e virar falso positivo.
    scan = re.sub(r'url\(#[a-zA-Z0-9_-]+\)', '', d)
    scan = re.sub(r'id="[a-zA-Z0-9_-]+"', '', scan)
    bad = re.findall(r'#[0-9a-fA-F]{2,}[^0-9a-fA-F\s";)\'\},]', scan)
    if bad:
        problems.append('hex suspeito: %s' % bad)

    # id do SVG tem que bater com o id da lista scenes[] do JS
    sids = re.findall(r'<svg class="scene[^"]*" id="(s\d+)"', d)
    jids = re.findall(r"id:\s*'(s\d+)'", d)
    if sids != jids:
        problems.append('svg ids != js ids -> %s vs %s' % (sids, jids))

    # transform="" + animation no MESMO elemento: se o keyframe anima transform,
    # ele SUBSTITUI o atributo e o elemento pula para a origem (0,0).
    # So e bug quando o keyframe realmente mexe em transform — por isso o corpo
    # de cada keyframe e lido antes de acusar.
    bodies = {}
    for m in re.finditer(r'@keyframes\s+([a-zA-Z0-9_]+)\s*\{', d):
        j, depth = m.end(), 1
        while depth:
            if d[j] == '{':
                depth += 1
            elif d[j] == '}':
                depth -= 1
            j += 1
        bodies[m.group(1)] = d[m.end():j]

    clash = []
    for m in re.finditer(r'<([a-z]+)[^>]*transform="([^"]*)"[^>]*style="animation:([a-zA-Z0-9_]+)', d):
        if 'transform' in bodies.get(m.group(3), ''):
            clash.append('%s(%s)' % (m.group(1), m.group(3)))
    if clash:
        problems.append('transform= junto com animation no mesmo tag (%d) -> '
                        'o elemento pula para a origem: %s'
                        % (len(clash), ', '.join(sorted(set(clash)))))

    # <text> dentro de <rect>: o <rect> tem modelo de conteudo VAZIO no SVG — nao e
    # contentor. Os filhos ficam no DOM mas NADA e desenhado: o texto do cartao
    # simplesmente nao aparece, sem erro e sem aviso. Cartao = <g> com <rect> + <text>.
    rect_txt = [m for m in re.finditer(r'<rect\b[^>]*>(.*?)</rect>', d, re.S)
                if '<text' in m.group(1)]
    if rect_txt:
        problems.append('<text> dentro de <rect> (%d) -> NAO e renderizado, '
                        'use <g> em volta' % len(rect_txt))

    # transform-origin com PALAVRA-CHAVE ou %: em SVG o valor e resolvido contra o
    # viewBox (405x720), nao contra a caixa do proprio elemento. Entao "center"
    # vira (202.5,360) e "center top" vira (202.5,0) — o pivo cai longe do desenho
    # e o elemento gira/escala em volta do lugar errado.
    # SEGURO: "0 0", valor em px, ou qualquer style com transform-box:fill-box.
    # O DEFAULT (sem declarar transform-origin) ja e "0 0" no Chrome — esse esta certo.
    # So acusa quando o keyframe realmente tem rotate/scale.
    ruim = []
    for m in re.finditer(r'style="([^"]*)"', d):
        st = m.group(1)
        to = re.search(r'transform-origin:\s*([^;"]+)', st)
        if not to or 'fill-box' in st:
            continue
        val = to.group(1).strip()
        if re.fullmatch(r'0(px)?\s+0(px)?', val) or re.search(r'\d+px', val):
            continue
        an = re.search(r'animation:\s*([a-zA-Z0-9_]+)', st)
        if not an or not re.search(r'rotate|scale', bodies.get(an.group(1), '')):
            continue
        ruim.append('%s(origin:%s)' % (an.group(1), val))
    if ruim:
        problems.append('transform-origin com palavra-chave em SVG (%d) -> pivo '
                        'cai no viewBox, nao no desenho: %s'
                        % (len(ruim), ', '.join(sorted(set(ruim)))))

    # conteudo invadindo a faixa da legenda (ultimos 73px dos 405x720)
    lows = [float(y) for y in re.findall(r'<text[^>]*\by="(\d+(?:\.\d+)?)"', d)]
    low = sorted({y for y in lows if y > 645})
    if low:
        problems.append('texto abaixo de y=645 (fica sob a barra de legenda): %s' % low)

    tot = sum(int(m) for m in re.findall(r'ms:(\d+)', d))
    if tot:
        print('  duracao total     :', round(tot / 1000, 1), 's')
    print('  cenas             :', len(sids))

    if problems:
        for p in problems:
            print('  [X] ' + p)
    else:
        print('  OK — nenhum problema')
    return problems


def main():
    args = sys.argv[1:]
    targets = []
    for a in args:
        targets += glob.glob(a) if any(c in a for c in '*?[') else [a]
    if not targets:
        targets = find_shorts()

    total = 0
    for t in targets:
        if not os.path.exists(t):
            print('nao encontrado:', t)
            continue
        total += len(check(t))

    print('=' * 66)
    print('TOTAL DE PROBLEMAS:', total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())

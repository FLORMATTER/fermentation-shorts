# -*- coding: utf-8 -*-
"""Acha rotulos de topo que batem no @handle.

O _largura-texto.py compara com a borda do cartao. Aqui a comparacao e com o
watermark, no canto superior direito — caso que ele nao cobre.

ATENCAO as unidades: o texto do SVG esta no viewBox 405x720, mas o .wm e HTML
em px do cartao. Num arquivo de 1080 de largura, o SVG e multiplicado por 2,667.
Tudo tem que ser convertido para o espaco do CARTAO antes de comparar.
"""
import glob, os, re

K_BOLD, K_NORMAL = 0.62, 0.53
TEXT = re.compile(r'<text\b([^>]*)>(.*?)</text>', re.S)
ATTR = re.compile(r'([a-zA-Z-]+)\s*=\s*"([^"]*)"')
WM = re.compile(r'\.wm\s*\{([^}]*)\}', re.S)
STAGE = re.compile(r'#stage\s*\{[^}]*?width:\s*(\d+)px[^}]*?height:\s*(\d+)px', re.S)


def attrs(s):
    return dict(ATTR.findall(s))


vistos, arquivos = set(), []
for padrao in ('*/shorts*-en.html', '*/*-en.html'):
    for f in sorted(glob.glob(padrao)):
        f = f.replace('\\', '/')
        if f in vistos:
            continue
        vistos.add(f)
        if '_teste-rec' in f or 'cartao-' in os.path.basename(f):
            continue
        arquivos.append(f)

total = 0
for f in arquivos:
    d = open(f, encoding='utf-8', errors='replace').read()
    ms = STAGE.search(d)
    if not ms:
        continue
    W = int(ms.group(1))
    escala = W / 405.0

    mw = WM.search(d)
    mt = re.search(r'<div class="wm"[^>]*>(.*?)</div>', d, re.S)
    if not (mw and mt):
        continue
    css = mw.group(1)
    g = lambda p: (float(re.search(p, css).group(1)) if re.search(p, css) else 0.0)
    top, right, fs = g(r'top:\s*([\d.]+)px'), g(r'right:\s*([\d.]+)px'), g(r'font-size:\s*([\d.]+)px')
    lsem = re.search(r'letter-spacing:\s*([\d.]+)em', css)
    ls_wm = float(lsem.group(1)) * fs if lsem else 0.0

    texto_wm = mt.group(1).strip()
    wm_w = len(texto_wm) * fs * K_BOLD + len(texto_wm) * ls_wm
    wm_esq = W - right - wm_w
    wm_topo, wm_base = top, top + fs * 1.2

    achou = []
    for m in TEXT.finditer(d):
        a = attrs(m.group(1))
        txt = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if not txt or a.get('text-anchor') != 'middle':
            continue
        try:
            y = float(a.get('y', 0))
        except ValueError:
            continue
        if not (30 <= y <= 80):
            continue
        font = float(a.get('font-size', 10)) * escala
        weight = int(float(a.get('font-weight', 400)))
        ls = float(a.get('letter-spacing', 0)) * escala
        x = float(a.get('x', 202)) * escala
        yc = y * escala
        w = len(txt) * font * (K_BOLD if weight >= 700 else K_NORMAL) + len(txt) * ls
        esq, dir_ = x - w / 2, x + w / 2
        gl_topo, gl_base = yc - font * 0.73, yc + font * 0.22
        if dir_ > wm_esq and gl_topo < wm_base and gl_base > wm_topo:
            achou.append((txt, esq, dir_, dir_ - wm_esq))

    if achou:
        print('%s   (cartao %dx%s, escala %.3f)' % (f, W, ms.group(2), escala))
        print('   @handle ocupa x %.0f..%.0f' % (wm_esq, W - right))
        for txt, esq, dir_, inv in achou:
            total += 1
            print('   INVADE %3.0fpx  rotulo x %.0f..%.0f  "%s"' % (inv, esq, dir_, txt[:46]))
        print()

print('TOTAL de rotulos invadindo o @handle: %d' % total)

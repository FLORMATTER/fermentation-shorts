# -*- coding: utf-8 -*-
"""
_revisar-videolongo.py — OLHAR as cenas de um player 16:9 antes de entregar.

O _revisar-cenas.py nao serve aqui: no player do video longo os <svg> sao
montados por JavaScript, entao nao existe `<svg class="scene">` literal no
arquivo. Este script pega os blocos `body:` do JS, monta uma folha de contato
com a FAIXA PROIBIDA DA LEGENDA marcada em vermelho (y=647..720) e renderiza
em PNG no tamanho nativo (405x720).

Serve principalmente para pegar o que o validador NAO pega: texto que estoura
a largura do cartao — problema tipico ao traduzir, porque o ingles ocupa mais
espaco horizontal que o portugues.

Uso:
    python _revisar-videolongo.py video-longo/player-video-longo-7-legumes-en.html 34 39
    python _revisar-videolongo.py <arquivo> --all
    python _revisar-videolongo.py <arquivo> 39 40 --cols 1 --tag en

Saida: _revisao/<base>-<tag>-<n>.png  (uma cena por arquivo, em tamanho nativo)
"""
import io
import os
import re
import shutil
import subprocess
import sys

CHROME = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
]


def find_browser():
    for c in CHROME:
        if os.path.exists(c):
            return c
    for n in ('chrome', 'chromium', 'msedge', 'google-chrome'):
        p = shutil.which(n)
        if p:
            return p
    return None


def page(style, corpo, cap, sub, label):
    """Uma cena por pagina, com a faixa da legenda marcada e a legenda de verdade.

    O corpo vem de dentro do JS (`body:\\`...\\``) — e o CONTEUDO de um <svg>,
    entao precisa ser reembrulhado num <svg viewBox="0 0 405 720">. Sem isso o
    navegador trata <rect>/<text> como tag desconhecida de HTML e nao desenha
    nada (a cena sai preta).
    """
    return """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
%s
*{animation-delay:-1s!important;animation-play-state:paused!important}
body{background:#2b2b2b;margin:0;padding:14px;font-family:system-ui}
.lbl{color:#9ad;font-size:12px;font-weight:700;letter-spacing:.1em;margin-bottom:6px}
.box{position:relative;width:405px;height:720px;overflow:hidden;background:#000}
.box svg{position:absolute;inset:0;width:100%%;height:100%%;display:block}
/* faixa que a barra de legenda .ncap cobre: y=647..720 no espaco 405x720 */
.box::after{content:'';position:absolute;left:0;right:0;top:647px;height:73px;
  background:rgba(255,0,0,.20);border-top:1px dashed red;z-index:9}
.ncap{position:absolute;left:0;right:0;bottom:0;background:rgba(15,14,12,.86);
  color:#fff;padding:14px 22px 17px;font-size:16px;font-weight:800;
  text-align:center;line-height:1.35;z-index:5}
.ncap small{display:block;font-size:12px;font-weight:500;opacity:.72;margin-top:4px}
</style></head><body>
<div class="lbl">%s</div>
<div class="box">
<svg viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">%s</svg>
<div class="ncap">%s<small>%s</small></div>
</div></body></html>""" % (style, label, corpo, cap, sub)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 1
    arquivo = args[0]
    pedidas = [int(a) for a in args[1:] if a.isdigit()]

    cols = 3
    if '--cols' in sys.argv:
        cols = int(sys.argv[sys.argv.index('--cols') + 1])
    tag = 'x'
    if '--tag' in sys.argv:
        tag = sys.argv[sys.argv.index('--tag') + 1]

    d = io.open(arquivo, encoding='utf-8').read()
    m = re.search(r'<style>(.*?)</style>', d, re.S)
    style = m.group(1) if m else ''

    corpos = re.findall(r'body:`(.*?)`', d, re.S)
    caps = re.findall(r"cap:'((?:[^'\\]|\\.)*)'", d)
    subs = re.findall(r"sub:'((?:[^'\\]|\\.)*)'", d)
    print('blocos body: %d | caps: %d | subs: %d' % (len(corpos), len(caps), len(subs)))

    # os ultimos body: sao o cartao e o fallback do buildAll (nao tem cap literal)
    if '--all' in sys.argv or not pedidas:
        pedidas = list(range(0, 42))

    browser = find_browser()
    if not browser:
        print('nenhum Chrome/Edge encontrado')
        return 1

    raiz = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(raiz, '_revisao')
    tmp = os.path.join(out, '_tmp-vl')
    os.makedirs(tmp, exist_ok=True)
    base = os.path.splitext(os.path.basename(arquivo))[0]

    feitos = []
    for i in pedidas:
        if i >= len(corpos):
            print('  cena %d nao existe' % i)
            continue
        cap = caps[i] if i < len(caps) else ''
        sub = subs[i] if i < len(subs) else ''
        html = os.path.join(tmp, 'c%d.html' % i)
        io.open(html, 'w', encoding='utf-8', newline='').write(
            page(style, corpos[i], cap, sub, 'CENA %d' % i))
        png = os.path.join(out, '%s-%s-%02d.png' % (base, tag, i))
        subprocess.run([browser, '--headless=new', '--disable-gpu', '--no-sandbox',
                        '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--virtual-time-budget=6000',
                        '--user-data-dir=' + os.path.join(tmp, 'profile'),
                        '--screenshot=' + png,
                        '--window-size=433,806',
                        'file:///' + html.replace('\\', '/')],
                       capture_output=True)
        if os.path.exists(png):
            feitos.append(png)
            print('  -> %s' % os.path.relpath(png, raiz))

    shutil.rmtree(tmp, ignore_errors=True)
    print('\n%d PNG(s). OLHE um por um: texto estourando a largura e o que o' % len(feitos))
    print('validador nao pega. A faixa vermelha e a area que a legenda cobre.')
    return 0 if feitos else 1


if __name__ == '__main__':
    sys.exit(main())

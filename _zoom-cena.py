#!/usr/bin/env python3
"""
_zoom-cena.py — ver UMA cena AMPLIADA, para julgar o DESENHO.

A folha de contato do `_revisar-cenas.py` renderiza em tamanho nativo (405x720).
Isso basta para layout (texto estourando, card colidindo), mas NAO basta para
julgar forma: um dente de alho que virou gota, um bulbo que virou folha e uma
colher que virou potinho so' se decidem com o desenho grande.

Uso:
    python _zoom-cena.py <arquivo.html> 3              # cena 3 (0-based), 3x
    python _zoom-cena.py <arquivo.html> 3 --escala 4   # 4x
    python _zoom-cena.py <arquivo.html> 0,3,5          # varias, uma por PNG

Saida: _revisao/zoom-<nome>-c<N>.png
"""
import os
import re
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(RAIZ, '_revisao')
TMP = os.path.join(OUT, '_tmp')

CHROME_CANDIDATES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
]

# o perfil fica no temp do sistema, reaproveitado — igual ao _revisar-cenas.py
PERFIL = os.path.join(os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp',
                      'shorts-chrome-profile')


def find_browser():
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    for name in ('chrome', 'chromium', 'msedge', 'google-chrome'):
        p = shutil.which(name)
        if p:
            return p
    return None


def extract_scenes(path):
    """Devolve (css do <style>, [bloco <svg class="scene">...</svg>])."""
    d = open(path, encoding='utf-8', errors='replace').read()
    m = re.search(r'<style>(.*?)</style>', d, re.S)
    style = m.group(1) if m else ''
    blocos, idx = [], 0
    while True:
        i = d.find('<svg class="scene', idx)
        if i == -1:
            break
        j = d.find('</svg>', i) + len('</svg>')
        blocos.append(d[i:j])
        idx = j
    return style, blocos

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
%s
body{background:#2b2b2b;margin:0;padding:10px}
.box{position:relative;width:405px;height:720px;background:#fdf8ee;overflow:hidden}
.box svg{position:absolute;inset:0;width:100%%;height:100%%;opacity:1!important;
  visibility:visible!important}
/* faixa da legenda: y=647..720 no espaco 405x720 */
.box::after{content:'';position:absolute;left:0;right:0;top:647px;height:73px;
  background:rgba(255,0,0,.18);border-top:1px dashed red;z-index:9}
</style></head><body><div class="box">%s</div></body></html>"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 1
    alvo = args[0]
    cenas = [int(x) for x in (args[1] if len(args) > 1 else '0').split(',')]
    escala = 3
    if '--escala' in sys.argv:
        escala = int(sys.argv[sys.argv.index('--escala') + 1])
    congelar = '--final' in sys.argv

    nav = find_browser()
    if not nav:
        print('Nenhum Chrome/Edge encontrado.')
        return 1
    style, blocos = extract_scenes(alvo)
    if not blocos:
        print('Nenhuma <svg class="scene"> em', alvo)
        return 1

    os.makedirs(TMP, exist_ok=True)
    base = os.path.splitext(os.path.basename(alvo))[0]
    extra = ('*{animation-delay:-1s!important;animation-play-state:paused!important}'
             if congelar else '')
    feitos = []
    for c in cenas:
        if not 0 <= c < len(blocos):
            print('cena %d fora da faixa (0..%d)' % (c, len(blocos) - 1))
            continue
        html = os.path.join(TMP, 'zoom%d.html' % c)
        png = os.path.join(OUT, 'zoom-%s-c%d.png' % (base, c))
        with open(html, 'w', encoding='utf-8') as fh:
            fh.write(HTML % (style + '\n' + extra, blocos[c]))
        subprocess.run([nav, '--headless=new', '--disable-gpu', '--no-sandbox',
                        '--hide-scrollbars',
                        '--force-device-scale-factor=%d' % escala,
                        '--virtual-time-budget=8000',
                        '--user-data-dir=' + PERFIL,
                        '--screenshot=' + png,
                        '--window-size=%d,%d' % (405 + 20, 720 + 20),
                        'file:///' + html.replace('\\', '/')],
                       capture_output=True)
        if os.path.exists(png):
            feitos.append(png)
            print('  ->', png, '(%dx)' % escala)
    if not feitos:
        print('nada renderizado')
        return 1
    print('\nOLHE o PNG: forma se julga no desenho grande.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

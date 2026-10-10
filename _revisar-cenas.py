#!/usr/bin/env python3
"""
_revisar-cenas.py — OLHAR as cenas antes de entregar.

Os greps do checklist pegam keyframe faltando e url(#x) quebrado, mas NAO
pegam layout: texto que estoura a largura, card que colide, desenho que ficou
irreconhecivel. Este script extrai todas as <svg class="scene"> de um short,
monta uma folha de contato e renderiza em PNG com o Chrome headless — 4 cenas
por linha, em tamanho nativo (405x720), com a faixa da legenda marcada em
vermelho para voce ver se algo entrou ali.

Uso:
    python _revisar-cenas.py guia-geral/shorts-5-easiest-en.html
    python _revisar-cenas.py repolho/shorts-chucrute-30s.html --cols 3
    python _revisar-cenas.py alho/shorts-garlic-honey-en.html --final

Saida: _revisao-<nome>-1.png, -2.png ... na pasta _revisao/ na raiz.

--final  congela cada animacao no ESTADO FINAL (animation-delay:-1s + paused).
         E o modo para revisar LAYOUT: sem ele os elementos com
         animation-fill-mode:both aparecem invisiveis, porque o
         --virtual-time-budget NAO avanca a timeline de animacao CSS no
         --headless=new (testado: o frame sai em t=0).
--no-anim  remove as animacoes por completo (estilo base). Serve para provar
         o bug do transform= + animation, nao para revisar layout.
"""
import re
import sys
import os
import subprocess
import shutil

CHROME_CANDIDATES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
]


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
    d = open(path, encoding='utf-8', errors='replace').read()
    style = re.search(r'<style>(.*?)</style>', d, re.S)
    style = style.group(1) if style else ''

    blocks, idx = [], 0
    while True:
        i = d.find('<svg class="scene', idx)
        if i == -1:
            break
        j = d.find('</svg>', i) + len('</svg>')
        blocks.append(d[i:j])
        idx = j
    return style, blocks


def sheet_html(style, group, start, no_anim=False, final=False):
    cells = ''
    for n, b in enumerate(group):
        cells += ('<div class="cell"><div class="lbl">CENA %d</div>'
                  '<div class="box">%s</div></div>' % (start + n, b))
    # --no-anim congela as animacoes: cada elemento cai no estilo base.
    # Serve para comparar com a versao animada e provar que um elemento
    # "pulou" por causa do conflito transform= + animation.
    extra = ''
    if no_anim:
        extra = '*{animation:none!important}'
    elif final:
        # adianta cada animacao em 1s e pausa: com fill:both (ou forwards)
        # isso prende o elemento no keyframe de 100%. As infinitas param
        # 1s dentro do ciclo, que tambem serve para conferir posicao.
        extra = ('*{animation-delay:-1s!important;'
                 'animation-play-state:paused!important}')
    return """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
%s
%s
body{background:#2b2b2b;margin:0;padding:16px;font-family:system-ui}
.row{display:flex;gap:14px;align-items:flex-start}
.cell{display:flex;flex-direction:column;gap:6px}
.lbl{color:#9ad;font-size:13px;font-weight:700;letter-spacing:.1em}
.box{position:relative;width:405px;height:720px;background:#fdf8ee;overflow:hidden}
.box svg{position:absolute;inset:0;width:100%%;height:100%%;opacity:1!important;visibility:visible!important}
/* faixa da legenda: y=647..720 no espaco 405x720 */
.box::after{content:'';position:absolute;left:0;right:0;top:647px;height:73px;
  background:rgba(255,0,0,.18);border-top:1px dashed red;z-index:9}
</style></head><body><div class="row">%s</div></body></html>""" % (style, extra, cells)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    cols = 4
    if '--cols' in sys.argv:
        cols = int(sys.argv[sys.argv.index('--cols') + 1])
    no_anim = '--no-anim' in sys.argv
    final = '--final' in sys.argv

    if not args:
        print(__doc__)
        return 1
    path = args[0]

    browser = find_browser()
    if not browser:
        print('Nenhum Chrome/Edge encontrado — nao da para renderizar.')
        return 1

    style, blocks = extract_scenes(path)
    if not blocks:
        print('Nenhuma <svg class="scene"> encontrada em', path)
        return 1

    folder = os.path.dirname(os.path.abspath(path))
    base = os.path.splitext(os.path.basename(path))[0]
    print('cenas extraidas:', len(blocks), '| navegador:', browser)

    # tudo cai numa pasta unica na raiz do projeto, para nao espalhar PNG
    # dentro das pastas dos legumes
    root = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(root, '_revisao')
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, '_tmp')
    os.makedirs(tmp, exist_ok=True)

    # O perfil do Chrome NAO fica dentro do projeto e NAO e apagado.
    # Motivo: apagar essa pasta dentro do projeto trava a permissao (o sandbox
    # bloqueia o delete) e ainda enche o projeto de lixo — um perfil de Chrome
    # headless passa de 40 MB. Fica no temp do sistema, reaproveitado entre rodadas.
    perfil = os.path.join(os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp',
                          'shorts-chrome-profile')
    os.makedirs(perfil, exist_ok=True)

    made = []
    for n in range(0, len(blocks), cols):
        group = blocks[n:n + cols]
        html = os.path.join(tmp, 'sheet%d.html' % n)
        tag = '-congelado' if no_anim else ('-final' if final else '')
        png = os.path.join(outdir, '%s-%d%s.png' % (base, n // cols + 1, tag))
        open(html, 'w', encoding='utf-8').write(
            sheet_html(style, group, n, no_anim, final))

        w = cols * 419 + 32
        h = 720 + 78
        subprocess.run([browser, '--headless=new', '--disable-gpu', '--no-sandbox',
                        '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--virtual-time-budget=8000',
                        '--user-data-dir=' + perfil,
                        '--screenshot=' + png,
                        '--window-size=%d,%d' % (w, h),
                        'file:///' + html.replace('\\', '/')],
                       capture_output=True)
        if os.path.exists(png):
            made.append(png)
            print('  ->', png)

    print('\nAbra os PNGs e OLHE um por um antes de entregar.')
    return 0 if made else 1


if __name__ == '__main__':
    sys.exit(main())

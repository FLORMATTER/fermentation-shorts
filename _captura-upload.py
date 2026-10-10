# -*- coding: utf-8 -*-
"""
_captura-upload.py — tira um print do QUADRO REAL 1080x1920 de um short no
formato de upload, com a faixa de legenda (.cap) em HTML e as animacoes
congeladas no estado final.

Serve para conferir o que a gravacao do OBS vai pegar: enquadramento,
posicao do .tag / .wm / .cap e se algum texto ficou sob a faixa.

Uso:
    python _captura-upload.py beterraba/shorts-beet-garlic-en-1080x1920.html
    python _captura-upload.py <arquivo.html> --cenas 0,3,6

Saida: _revisao/<nome>-quadro-<n>.png
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
]

FINAL_CSS = ('*{animation-delay:-1s!important;'
             'animation-play-state:paused!important}')


def find_browser():
    for c in CHROME:
        if os.path.exists(c):
            return c
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 1
    path = args[0]

    cenas = [0]
    if '--cenas' in sys.argv:
        cenas = [int(x) for x in sys.argv[sys.argv.index('--cenas') + 1].split(',')]

    browser = find_browser()
    if not browser:
        print('Nenhum Chrome/Edge encontrado.')
        return 1

    root = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(root, '_revisao')
    os.makedirs(outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(path))[0]

    d = io.open(path, encoding='utf-8', newline='').read()
    if '</style>' not in d:
        print('sem </style> — nao da para injetar o estado final')
        return 1

    ids = re.findall(r'<svg class="scene[^"]*" id="(s\d+)"', d)
    made = []

    for n in cenas:
        if n >= len(ids):
            continue
        d2 = d.replace('</style>', FINAL_CSS + '\n</style>', 1)
        # tira a capa e trava a cena pedida.
        # O `render()` do JS roda no fim do arquivo e reescreve o classList a
        # partir de `i` — entao mexer so no HTML nao adianta: tem que mudar o `i`.
        d2 = d2.replace('class="cover"', 'class="cover hide"', 1)
        d2 = re.sub(r'let i = 0,', 'let i = %d,' % n, d2, count=1)

        tmp = os.path.join(outdir, '_tmp_quadro.html')
        io.open(tmp, 'w', encoding='utf-8', newline='').write(d2)
        png = os.path.join(outdir, '%s-quadro-%d.png' % (base, n))
        subprocess.run([browser, '--headless=new', '--disable-gpu', '--no-sandbox',
                        '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--virtual-time-budget=2500',
                        '--user-data-dir=' + os.path.join(outdir, '_tmpprof'),
                        '--screenshot=' + png,
                        '--window-size=1080,1920',
                        'file:///' + tmp.replace('\\', '/')],
                       capture_output=True)
        if os.path.exists(png):
            made.append(png)
            print('  ->', png)

    for junk in ('_tmp_quadro.html', '_tmpprof'):
        p = os.path.join(outdir, junk)
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        elif os.path.exists(p):
            os.remove(p)

    print('\nOLHE o PNG antes de entregar.')
    return 0 if made else 1


if __name__ == '__main__':
    sys.exit(main())

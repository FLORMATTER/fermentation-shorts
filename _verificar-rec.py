# -*- coding: utf-8 -*-
"""Renderiza com ?rec para provar que o modo gravacao funciona."""
import os, subprocess

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
OUT = '_teste-rec'


def render(rel, w, h, png, extra=''):
    png = os.path.abspath(os.path.join(OUT, png))
    prof = os.path.abspath(os.path.join(OUT, 'prof-' + os.path.basename(png)[:-4]))
    url = 'file:///' + os.path.abspath(rel).replace('\\', '/') + extra
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--no-first-run', '--disable-extensions',
                    '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--virtual-time-budget=9000',
                    '--user-data-dir=' + prof,
                    '--screenshot=' + png,
                    '--window-size=%d,%d' % (w, h), url],
                   capture_output=True, timeout=120)
    print('  ->', os.path.basename(png), 'OK' if os.path.exists(png) else 'FALHOU')


print('1) rabanete ?rec a 1080x1920')
render('rabanete/shorts-rabanete-animado-en.html', 1080, 1920, 'rec-rabanete.png', '?rec')

print('2) chucrute ?rec a 1080x1920')
render('repolho/shorts-chucrute-30s-en.html', 1080, 1920, 'rec-chucrute.png', '?rec')

print('3) video longo ?rec a 1920x1080')
render('video-longo/player-video-longo-7-legumes-en.html', 1920, 1080,
       'rec-longform.png', '?rec')

print('4) SEM ?rec (controle) a 1080x1920 — deve mostrar o cartao pequeno')
render('rabanete/shorts-rabanete-animado-en.html', 1080, 1920, 'ctrl-sem-rec.png')

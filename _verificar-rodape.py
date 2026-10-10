# -*- coding: utf-8 -*-
"""
_verificar-rodape.py — confere COM OS OLHOS as 5 cenas que foram consertadas.

O _validar-short.py mede coordenadas, mas nao ve colisao. Este script pega as
cenas 37 a 41 do player-video-longo, monta um HTML temporario com a barra de
legenda de verdade por cima e manda o _revisar-cenas.py renderizar em PNG.

Uso:
    python _verificar-rodape.py            # so gera o HTML temporario
    python _verificar-rodape.py --render   # gera e renderiza
"""
import io
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(RAIZ, 'video-longo', 'player-video-longo-7-legumes.html')
TEMP = os.path.join(RAIZ, '_temp-verificacao-rodape.html')
PY = sys.executable

txt = io.open(ARQ, encoding='utf-8').read()

# pega o bloco <style> do original (traz os @keyframes e o .ncap)
m = re.search(r'<style>(.*?)</style>', txt, re.S)
estilo = m.group(1) if m else ''

corpos = re.findall(r'body:`(.*?)`', txt, re.S)
alvo = [int(a) for a in sys.argv[1:] if a.isdigit()] or [37, 38, 39, 40, 41]
cenas = [(i, corpos[i]) for i in alvo if i < len(corpos)]
print('cenas extraidas: %s' % ', '.join(str(i) for i, _ in cenas))

partes = []
for i, corpo in cenas:
    partes.append('<svg class="scene" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">%s</svg>' % corpo)

html = '''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<style>%s
#stage{position:relative;width:405px;height:720px;overflow:hidden}
svg.scene{position:absolute;inset:0;width:100%%;height:100%%;opacity:1;visibility:visible}
</style></head><body>
<div id="stage">
%s
<div class="ncap" id="ncap">Fermented garlic in honey<small>so mel · 3 a 4 semanas</small></div>
</div>
</body></html>''' % (estilo, '\n'.join(partes))

io.open(TEMP, 'w', encoding='utf-8', newline='').write(html)
print('gerado: %s' % os.path.basename(TEMP))

if '--render' in sys.argv:
    print()
    r = subprocess.run([PY, os.path.join(RAIZ, '_revisar-cenas.py'), TEMP, '--final', '--cols', '3'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(r.stdout or '')
    print(r.stderr or '')

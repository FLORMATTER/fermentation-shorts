# -*- coding: utf-8 -*-
import io, os
G = os.path.join('C:/Users/Saxa/Desktop/youtube-work', '_gerar-galeria.py')
d = io.open(G, encoding='utf-8').read()

print('OBS em d        :', d.count('OBS'))
print('alerta velho    :', d.count('  <div class="alerta">'))
print('nao existem     :', d.count('nao existem arquivos'))
print('tupla %%        :', d.count('""" % (CSS, len(shorts), mmss(total), len(shorts) + len(ignorados),'))
print('total = sum     :', d.count("    total = sum(s['dur'] for s in shorts)\n"))

# imprime a linha 239 crua, com repr, para ver espacos invisiveis
linhas = d.split('\n')
for n in range(235, 244):
    print('%3d %r' % (n + 1, linhas[n]))

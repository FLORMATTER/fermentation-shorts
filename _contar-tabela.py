# -*- coding: utf-8 -*-
"""Conta, na propria tabela WHICH FILE TO RECORD, quantas entradas tem mp4 e quantas nao."""
import io, re

P = 'C:/Users/Saxa/Desktop/youtube-work/guias/pacote-legendas-descricoes-en.md'
d = io.open(P, encoding='utf-8').read()

i = d.index('WHICH FILE TO RECORD')
bloco = d[i:]
fim = bloco.index('**All ')
tabela = bloco[:fim]

linhas = [l for l in tabela.split('\n') if l.startswith('| ') and re.match(r'\|\s*\d+\s*\|', l)]
com, sem = [], []
for l in linhas:
    cols = [c.strip() for c in l.strip('|').split('|')]
    num = cols[0]
    mp4 = cols[-1]
    (com if mp4 == '\u2705' else sem).append((num, cols[1]))

print('linhas na tabela : %d' % len(linhas))
print('com mp4 (check)  : %d' % len(com))
print('sem mp4          : %d  -> %s' % (len(sem), sem))
print()
print('entradas numeradas: %s..%s' % (linhas[0].strip('|').split('|')[0].strip(),
                                      linhas[-1].strip('|').split('|')[0].strip()))
print('SHORTS (com mp4) : %d' % len(com))

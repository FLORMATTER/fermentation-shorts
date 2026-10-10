# -*- coding: utf-8 -*-
"""
_consertar-legenda-beterraba-alho.py — a barra de legenda repetia o TITULO.

Achado ao TOCAR o mp4 (nao pelo validador, nao pelo render das cenas):

    titulo na cena        barra queimada no mp4
    READY IN 1 TO 2 WEEKS  "Ready in 1 to 2 weeks"     <- a MESMA frase
    2% SALT, NOT MORE      "2% salt, weighed"
    ONE LAYER AT A TIME    "Layer it, do not mix it"
    THE GARLIC MELLOWS OUT "The garlic mellows out"    <- a MESMA frase

O arquivo foi desenhado como player proprio: cada cena ja' tem titulo + sub +
selo dentro do SVG. Os campos `cap`/`sub` do array `scenes` foram escritos como
descricao da cena, e o motor do mp4 (`_mp4/render.js`) desenha os DOIS — entao
cada cena saiu dizendo a mesma coisa duas vezes, em dois tamanhos.

Conserto: a barra passa a carregar o DETALHE, o titulo continua a MANCHETE.
Nenhuma frase da barra repete o titulo da cena. As duracoes, os `tag` e as
cores NAO mudam.

Regex no bloco `const scenes = [...]` inteiro (ancora de whitespace e' fragil
num array alinhado a mao).
"""
import io
import re
import sys

ARQ = 'beterraba/shorts-beet-garlic-en-1080x1920.html'

NOVO = """const scenes = [
  { id:'s0', ms:6000, tag:'BEETS+GARLIC 1 / 8', cap:'One beet, one garlic head',   sub:'2% salt \\u00b7 ready in 1 to 2 weeks',          color:'#a01e52' },
  { id:'s1', ms:6500, tag:'BEETS+GARLIC 2 / 8', cap:'Skin off, 2 cm wedges',       sub:'grated beet goes to mush \\u2014 wedges stay crunchy', color:'#8f2450' },
  { id:'s2', ms:6500, tag:'BEETS+GARLIC 3 / 8', cap:'One smash per clove',         sub:'that is what releases the oil',             color:'#c2551f' },
  { id:'s3', ms:7500, tag:'BEETS+GARLIC 4 / 8', cap:'Beet, garlic, beet, garlic',   sub:'layered, so you can pull out what you want', color:'#a01e52' },
  { id:'s4', ms:7000, tag:'BEETS+GARLIC 5 / 8', cap:'20 g of salt per 1 kg',       sub:'coarse salt \\u2014 iodine stalls the ferment', color:'#ba7517' },
  { id:'s5', ms:7000, tag:'BEETS+GARLIC 6 / 8', cap:'Day 1 sharp, week 2 sweet',   sub:'betalain from the beet dyes the garlic',    color:'#0f6e56' },
  { id:'s6', ms:7000, tag:'BEETS+GARLIC 7 / 8', cap:'One week out, one week cold', sub:'18-22 \\u00b0C \\u00b7 burp the jar daily',        color:'#0f6e56' },
  { id:'s7', ms:6500, tag:'BEETS+GARLIC 8 / 8', cap:'Salads, burgers, eggs',       sub:'keeps for months in the fridge',            color:'#3d1f33' }
];"""


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))
    eol = '\r\n' if crlf else '\n'

    padrao = re.compile(r'const scenes = \[.*?\n\];', re.S)
    achados = padrao.findall(d)
    print('bloco `const scenes` encontrado %d vez(es)' % len(achados))
    if len(achados) != 1:
        print('ABORTADO — nao sei qual bloco trocar.')
        return 1

    velho = achados[0]
    # guardar as duracoes e os tags originais, para provar que nao mudaram
    ms_antes = re.findall(r"ms:(\d+)", velho)
    tag_antes = re.findall(r"tag:'([^']+)'", velho)

    novo = NOVO.replace('\n', eol)
    ms_depois = re.findall(r"ms:(\d+)", novo)
    tag_depois = re.findall(r"tag:'([^']+)'", novo)
    if ms_antes != ms_depois:
        print('ABORTADO — as duracoes mudaram: %s -> %s' % (ms_antes, ms_depois))
        return 1
    if tag_antes != tag_depois:
        print('ABORTADO — os tags mudaram: %s -> %s' % (tag_antes, tag_depois))
        return 1
    print('duracoes preservadas: %s' % ','.join(ms_antes))
    print('tags preservados    : %d' % len(tag_depois))

    # provar que as caps VELHAS sumiram (as novas nao podem repetir o titulo)
    caps_velhas = re.findall(r"cap:'([^']+)'", velho)
    caps_novas = re.findall(r"cap:'([^']+)'", novo)
    repetidas = [c for c in caps_novas if c in caps_velhas]
    print('caps novas que repetem uma antiga: %d' % len(repetidas))
    for c in repetidas:
        print('   REPETIDA: %r' % c)
    print('caps novas:')
    for c in caps_novas:
        print('   %2d car  %s' % (len(c), c))
    if repetidas:
        print('ABORTADO — a barra continuaria dizendo a mesma coisa.')
        return 1

    d = d.replace(velho, novo, 1)

    with io.open(ARQ + '.antes-da-legenda', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %s (backup .antes-da-legenda)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())

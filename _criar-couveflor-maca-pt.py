# -*- coding: utf-8 -*-
"""_criar-couveflor-maca-pt.py — o ORIGINAL PT do short COUVE-FLOR + MACA (#20).

    python _criar-couveflor-maca-pt.py

Por que: o #20 nasceu em INGLES (19/09) e a serie e' **original PT + irmao `-en`**.

Por que NAO sai do PT do #18: o #18 tem a geometria da CENOURA, o #20 tem a da
couve-flor (a nuvem de circulos creme, a folha verde, o talo). Mesmo sendo o mesmo
template de motor, o desenho e' outro — entao o PT tem de sair do proprio `-en`
do #20.

Duas diferencas de metodo em relacao ao `_criar-cenoura-maca-pt.py`:
  - o bloco `const scenes` e' trocado por REGEX, nao por ancora literal. Ele tem
    7 linhas com alinhamento a espaco que muda de arquivo para arquivo, e copiar
    isso a mao e' a maneira mais facil de errar. O regex casa o bloco inteiro.
  - o resto continua ancora exata, contada, abortando sem gravar.
"""
import io
import re
import sys

ORIGEM = 'couve-flor/shorts-cauliflower-apple-en.html'
DESTINO = 'couve-flor/shorts-cauliflower-apple.html'

# (rotulo, velho, novo, quantas_vezes_deve_casar)
TROCAS = [
    ('idioma do html', '<html lang="en">', '<html lang="pt-BR">', 1),
    ('titulo da aba',
     '<title>Shorts animado — Cauliflower with apple (fermented)</title>',
     '<title>Shorts animado — Couve-flor com maçã (fermentada)</title>', 1),

    ('selo (badge)', '🥦 + APPLE', '🥦 + MAÇÃ', 1),
    ('tag estatica', '>SCENE 1 / 7</div>', '>CENA 1 / 7</div>', 1),

    ('rotulo do florete', '>small</text>', '>pequenos</text>', 1),
    ('rotulo da maca', '>thick</text>', '>grossa</text>', 1),

    ('rotulo da agua', '>of water</text>', '>de água</text>', 1),
    ('rotulo do sal', '>of salt</text>', '>de sal</text>', 1),
    ('rotulo da salmoura', '>2.5% brine</text>', '>salmoura de 2,5%</text>', 1),

    ('rotulo acucar', '>sugar + yeast</text>', '>açúcar + levedura</text>', 1),
    ('rotulo couve-flor', '>dense + slow</text>', '>densa + lenta</text>', 1),
    ('caixa da manchete', '>THE APPLE STARTS IT</text>',
     '>A MAÇÃ INICIA</text>', 1),
    ('caixa do detalhe',
     '>sugar feeds the bacteria - acid comes sooner</text>',
     '>o açúcar alimenta a bactéria - ácido antes</text>', 1),

    ('ar nos floretes', '>air in the florets - weigh them down</text>',
     '>ar nos floretes - ponha peso em cima</text>', 1),

    ('pilula dos dias', '>5 TO 7 DAYS</text>', '>5 A 7 DIAS</text>', 1),

    ('resultado', '>Crisp and a little sweet</text>',
     '>Crocante e um pouco doce</text>', 1),
    ('o cheiro mente', '>the jar smells worse than it tastes</text>',
     '>o pote cheira pior do que come</text>', 1),

    ('barra estatica',
     '<div class="cap" id="cap">Cauliflower and apple<small>the apple is a starter, not a flavour</small></div>',
     '<div class="cap" id="cap">Couve-flor com maçã<small>a maçã é starter, não sabor</small></div>', 1),
    ('botao pause (botao + JS)', '⏸ Pause', '⏸ Pausar', 2),
    ('botao assistir', "'▶ Watch'", "'▶ Assistir'", 1),
]

SCENES_NOVO = """const scenes = [
  { id:'s0', ms:5600, tag:'COUVE-FLOR 1 / 7', cap:'Couve-flor com maçã', sub:'a maçã é starter, não sabor', color:'#5c7a29' },
  { id:'s1', ms:6200, tag:'COUVE-FLOR 2 / 7', cap:'Couve-flor pequena, maçã grossa', sub:'floretes iguais fermentam igual - a maçã amolece antes', color:'#5c7a29' },
  { id:'s2', ms:5800, tag:'COUVE-FLOR 3 / 7', cap:'25 g de sal por litro', sub:'salmoura de 2,5% - a maçã não muda o sal', color:'#378add' },
  { id:'s3', ms:7000, tag:'COUVE-FLOR 4 / 7', cap:'A maçã inicia', sub:'o açúcar alimenta a bactéria - ácido no dia 1, não no 3', color:'#a32d2d' },
  { id:'s4', ms:6600, tag:'COUVE-FLOR 5 / 7', cap:'Ar nos floretes', sub:'é daí que vem o cheiro de enxofre', color:'#1d9e75' },
  { id:'s5', ms:6000, tag:'COUVE-FLOR 6 / 7', cap:'5 a 7 dias, prove no 4º', sub:'a geladeira para o enxofre', color:'#5f5e5a' },
  { id:'s6', ms:6600, tag:'COUVE-FLOR 7 / 7', cap:'O cheiro mente', sub:'abra, espere 5 minutos - o sulfeto sai', color:'#3b6d11' }
];"""


def main():
    with io.open(ORIGEM, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    crlf = d.count('\r\n')
    eol = '\r\n' if crlf else '\n'
    print('origem     : %s (%d bytes)' % (ORIGEM, len(d)))
    print('fim de linha: %s' % ('CRLF' if crlf else 'LF'))

    falhou = False
    for i, (rotulo, velho, novo, esperado) in enumerate(TROCAS, 1):
        c = d.count(velho)
        marca = 'ok ' if c == esperado else 'ERRO'
        print('  %2d. %-26s casou %d (esperado %d) %s' % (i, rotulo, c, esperado, marca))
        if c != esperado:
            falhou = True
            continue
        d = d.replace(velho, novo)

    # --- barra de legenda por regex (o alinhamento a espaco muda de arquivo para arquivo)
    m = re.search(r'const scenes = \[.*?\n\];', d, re.S)
    if not m:
        print('  ERRO: nao achei o bloco `const scenes`')
        falhou = True
    else:
        velho_bloco = m.group(0)
        ms_antes = re.findall(r'ms:(\d+)', velho_bloco)
        cor_antes = re.findall(r"color:'([^']+)'", velho_bloco)
        novo_bloco = SCENES_NOVO.replace('\n', eol)
        ms_depois = re.findall(r'ms:(\d+)', novo_bloco)
        cor_depois = re.findall(r"color:'([^']+)'", novo_bloco)
        print('  21. %-26s %d cenas' % ('barra de legenda', len(ms_antes)))
        if ms_antes != ms_depois:
            print('      ERRO: as duracoes mudaram! %s -> %s' % (ms_antes, ms_depois))
            falhou = True
        elif cor_antes != cor_depois:
            print('      ERRO: as cores da barra mudaram! %s -> %s' % (cor_antes, cor_depois))
            falhou = True
        else:
            print('      ok  duracoes (%s) e cores iguais' % ', '.join(ms_depois))
            d = d.replace(velho_bloco, novo_bloco, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    # ---- prova de que so' o IDIOMA mudou
    a = io.open(ORIGEM, 'r', encoding='utf-8', newline='').read()
    esq = lambda s: re.findall(r'(?:ms|color|id|fill|stroke|font-size|viewBox)[:=]"?(#?\w[\w%., -]*)', s)
    if esq(a) != esq(d):
        print('\nAVISO: o esqueleto (ms/color/id/fill/...) mudou — conferir!')
        return 1
    print('\nesqueleto identico (ms, color, id, fill, stroke, font-size)')

    with io.open(DESTINO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: %s (%d bytes)' % (DESTINO, len(d)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

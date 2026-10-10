# -*- coding: utf-8 -*-
"""_criar-cenoura-maca-pt.py — o ORIGINAL PT do short CENOURA + MACA (#18).

    python _criar-cenoura-maca-pt.py

Por que: o #18 nasceu em INGLES (pedido do usuario em 19/09) e a convencao da
serie e' **original PT + irmao `-en`**. Aqui o PT e' reconstruido a partir do
`-en`, que ja' esta correto e validado.

Como: lista de ancoras CONTADAS. Cada ancora diz quantas vezes deve casar; se
alguma casar diferente, o script **aborta sem gravar**. Isso e' necessario aqui
porque `⏸ Pause` aparece DUAS vezes no arquivo (o botao e o `textContent` do JS)
— uma ancora de contagem 1 falharia, e uma de "troca tudo" passaria batido se o
arquivo mudasse.

So' o IDIOMA muda. Geometria, cores, duracoes, `color:` da barra e o motor JS
saem provados iguais — o script compara os dois arquivos no fim e avisa se
alguma coisa alem de texto mudou.

O que NAO muda de proposito: `🥕` do selo (emoji), as cores, e os numeros
('1 L', '20 g') — que sao iguais nos dois idiomas.
"""
import io
import re
import sys

ORIGEM = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'cenoura/shorts-carrot-apple.html'

# (rotulo, velho, novo, quantas_vezes_deve_casar)
TROCAS = [
    # ---------------------------------------------------------------- cabecalho
    ('idioma do html', '<html lang="en">', '<html lang="pt-BR">', 1),
    ('titulo da aba',
     '<title>Shorts animado — Carrot with apple (fermented)</title>',
     '<title>Shorts animado — Cenoura com maçã (fermentada)</title>', 1),

    # ---------------------------------------------------------------- selo e tag
    ('selo (badge)', '🥕 + APPLE', '🥕 + MAÇÃ', 1),
    ('tag estatica', '>SCENE 1 / 7</div>', '>CENA 1 / 7</div>', 1),

    # ---------------------------------------------------------------- cena 2 (s1)
    ('rotulo do corte fino', '>thin</text>', '>fina</text>', 1),
    ('rotulo do corte grosso', '>thick</text>', '>grossa</text>', 1),

    # ---------------------------------------------------------------- cena 3 (s2)
    ('rotulo da agua', '>of water</text>', '>de água</text>', 1),
    ('rotulo do sal', '>of salt</text>', '>de sal</text>', 1),
    ('rotulo da salmoura', '>2% brine</text>', '>salmoura de 2%</text>', 1),

    # ---------------------------------------------------------------- cena 4 (s3)
    ('rotulo da maca', '>sugar + yeast</text>', '>açúcar + levedura</text>', 1),
    ('rotulo da cenoura', '>dense + slow</text>', '>densa + lenta</text>', 1),
    ('caixa da manchete', '>THE APPLE MAKES IT FIZZY</text>',
     '>A MAÇÃ FAZ ESPUMA</text>', 1),
    ('caixa do detalhe', '>sugar plus the yeast on the skin</text>',
     '>o açúcar mais a levedura da casca</text>', 1),

    # ---------------------------------------------------------------- cena 5 (s4)
    ('a maca boia', '>the apple floats - keep it down</text>',
     '>a maçã boia - mantenha afundada</text>', 1),

    # ---------------------------------------------------------------- cena 6 (s5)
    ('pilula dos dias', '>ONLY 4 TO 5 DAYS</text>', '>SÓ 4 A 5 DIAS</text>', 1),

    # ---------------------------------------------------------------- cena 7 (s6)
    ('resultado', '>Fizzy and a little sweet</text>',
     '>Espumante e um pouco doce</text>', 1),
    ('aviso de alcool', '>0.5% to 2% alcohol - keep it cold</text>',
     '>0,5% a 2% de álcool - mantenha frio</text>', 1),

    # ---------------------------------------------------------------- barra e botoes
    ('barra estatica',
     '<div class="cap" id="cap">Carrot with apple<small>the sweet one - and it fizzes</small></div>',
     '<div class="cap" id="cap">Cenoura com maçã<small>a doce - e faz espuma</small></div>', 1),
    ('botao pause (botao + JS)', '⏸ Pause', '⏸ Pausar', 2),
    ('botao assistir', "'▶ Watch'", "'▶ Assistir'", 1),

    # ---------------------------------------------------------------- barra de legenda
    ('barra de legenda (7 cenas)',
     '''const scenes = [
  { id:'s0', ms:5400, tag:'CARROT 1 / 7', cap:'Carrot with apple', sub:'the sweet one - and it fizzes', color:'#d97706' },
  { id:'s1', ms:6200, tag:'CARROT 2 / 7', cap:'Cut the carrot thin, the apple thick', sub:'the carrot is dense, the apple is not', color:'#ba7517' },
  { id:'s2', ms:5800, tag:'CARROT 3 / 7', cap:'2% brine', sub:'1 litre of water + 20 g of salt', color:'#378add' },
  { id:'s3', ms:6800, tag:'CARROT 4 / 7', cap:'The apple is sugar and wild yeast', sub:'that is what makes it fizz so fast', color:'#a32d2d' },
  { id:'s4', ms:6200, tag:'CARROT 5 / 7', cap:'Everything under the brine', sub:'apple floats - keep it down', color:'#1d9e75' },
  { id:'s5', ms:5800, tag:'CARROT 6 / 7', cap:'Only 4 to 5 days', sub:'the apple makes it faster than carrot', color:'#5f5e5a' },
  { id:'s6', ms:6600, tag:'CARROT 7 / 7', cap:'Fizzy and a little sweet', sub:'0.5% to 2% alcohol - keep it cold', color:'#3b6d11' }
];''',
     '''const scenes = [
  { id:'s0', ms:5400, tag:'CENA 1 / 7', cap:'Cenoura com maçã', sub:'a doce - e faz espuma', color:'#d97706' },
  { id:'s1', ms:6200, tag:'CENA 2 / 7', cap:'Corte a cenoura fina, a maçã grossa', sub:'a cenoura é densa, a maçã não', color:'#ba7517' },
  { id:'s2', ms:5800, tag:'CENA 3 / 7', cap:'Salmoura de 2%', sub:'1 litro de água + 20 g de sal', color:'#378add' },
  { id:'s3', ms:6800, tag:'CENA 4 / 7', cap:'A maçã é açúcar e levedura selvagem', sub:'é isso que faz espumar tão rápido', color:'#a32d2d' },
  { id:'s4', ms:6200, tag:'CENA 5 / 7', cap:'Tudo embaixo da salmoura', sub:'a maçã boia - mantenha afundada', color:'#1d9e75' },
  { id:'s5', ms:5800, tag:'CENA 6 / 7', cap:'Só 4 a 5 dias', sub:'a maçã acelera mais que a cenoura', color:'#5f5e5a' },
  { id:'s6', ms:6600, tag:'CENA 7 / 7', cap:'Espumante e um pouco doce', sub:'0,5% a 2% de álcool - mantenha frio', color:'#3b6d11' }
];''', 1),
]


def main():
    with io.open(ORIGEM, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    crlf = d.count('\r\n')
    eol = '\r\n' if crlf else '\n'
    print('origem     : %s (%d bytes)' % (ORIGEM, len(d)))
    print('fim de linha: %s' % ('CRLF' if crlf else 'LF'))

    falhou = False
    for i, (rotulo, velho, novo, esperado) in enumerate(TROCAS, 1):
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        c = d.count(v)
        marca = 'ok ' if c == esperado else 'ERRO'
        print('  %2d. %-26s casou %d (esperado %d) %s' % (i, rotulo, c, esperado, marca))
        if c != esperado:
            falhou = True
            continue
        d = d.replace(v, n)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    # ---- prova de que so' o IDIOMA mudou: o "esqueleto" tem de ser identico
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

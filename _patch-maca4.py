# -*- coding: utf-8 -*-
"""
_patch-maca4.py — os ajustes que o ZOOM 3x mostrou no #27.

A folha de contato em tamanho nativo nao decide FORMA; o zoom decide. O que ele
mostrou:

  1. ALHO lia como CEBOLA: as linhas dos gomos eram `#c2b191` sobre `#f2e9d8`,
     contraste baixo demais. Escurecer.
  2. FACA encostando na borda direita (a alca terminava exatamente em x=405).
     Deslocar para a esquerda.
  3. LEVEDURA parecia MACHUCADO: ponto escuro EM CIMA da maca le' como mancha na
     fruta, nao como levedura. Agora: celula com anel, no CONTORNO da maca, em
     cor que nao e' a da fruta.

Ancora com contagem esperada: ABORTA SEM GRAVAR se alguma nao casar.
"""
import io
import os
import sys

ALVO = '_criar-maca-alho-cenoura.py'

# ---- 1. o alho escurece ----------------------------------------------------
ALHO_ANTES = "ALHO_ESC = '#c2b191'"
ALHO_DEPOIS = "ALHO_ESC = '#a89468'"

# ---- 2. a faca sai da borda -----------------------------------------------
FACA_ANTES = r'    <g transform="translate(342,382) rotate(-12) scale(0.7)">@FACA@</g>'
FACA_DEPOIS = r'    <g transform="translate(330,382) rotate(-12) scale(0.7)">@FACA@</g>'

# ---- 3. a levedura vira celula com anel, fora da maca ---------------------
# O `'\n    '` do original e' BARRA + N no arquivo (esta' dentro de uma string
# Python la'), entao aqui a ancora precisa de `\\n` para casar os dois caracteres.
LEV_ANTES = (
    'def leveduras(pontos, cor=MACA_ESC):\n'
    '    """Pontinhos de levedura selvagem (a que vive na casca da maca)."""\n'
    "    return '\\n    '.join(\n"
    '        f\'<circle cx="{p[0]:g}" cy="{p[1]:g}" r="{p[2]:g}" fill="{cor}"\'\n'
    "        f' opacity=\".55\"/>' for p in pontos)"
)

LEV_DEPOIS = (
    'def leveduras(pontos, cor=\'#a8842e\'):\n'
    '    """Levedura selvagem: celula com anel, no CONTORNO da maca.\n'
    '\n'
    '    Ponto escuro EM CIMA da maca lia como MACHUCADO, nao como levedura (o\n'
    '    zoom 3x mostrou). Agora fica fora da silhueta, com anel, e numa cor que\n'
    '    nao e\' a da fruta.\n'
    '    """\n'
    '    saida = []\n'
    '    for x, y, r in pontos:\n'
    '        saida.append(\n'
    '            f\'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="#f9edc9"\'\n'
    '            f\' stroke="{cor}" stroke-width="2"/>\'\n'
    '            f\'<circle cx="{x - r * 0.5:g}" cy="{y - r * 0.5:g}" r="{r * 0.42:g}"\'\n'
    '            f\' fill="{cor}" opacity=".5"/>\')\n'
    "    return '\\n    '.join(saida)"
)

# ---- 3b. e os pontos vao para o contorno ---------------------------------
PONTOS_ANTES = (
    "     .replace('@PONTOS@', leveduras([(150, 340, 5), (256, 352, 4.4), (168, 424, 4),\n"
    '                                     (244, 420, 5), (204, 322, 4.2), (140, 388, 4.6),\n'
    '                                     (268, 392, 4.2)]))'
)
PONTOS_DEPOIS = (
    "     .replace('@PONTOS@', leveduras([(118, 338, 5.4), (286, 348, 5),\n"
    '                                     (126, 428, 4.6), (282, 424, 5.2),\n'
    '                                     (168, 288, 4.4), (252, 294, 4.6),\n'
    '                                     (196, 450, 4.6)]))'
)

EDICOES = [
    (ALHO_ANTES, ALHO_DEPOIS, 1),
    (FACA_ANTES, FACA_DEPOIS, 1),
    (LEV_ANTES, LEV_DEPOIS, 1),
    (PONTOS_ANTES, PONTOS_DEPOIS, 1),
]


def main():
    if not os.path.exists(ALVO):
        print('ABORTA: nao achei %s' % ALVO)
        return 1
    with io.open(ALVO, encoding='utf-8', newline='') as f:
        d = f.read()
    antes = len(d.encode('utf-8'))

    for old, new, esperado in EDICOES:
        n = d.count(old)
        if n != esperado:
            print('ABORTA: ancora casou %d vez(es), esperava %d:' % (n, esperado))
            print('   %r' % old[:140])
            return 1
        d = d.replace(old, new, esperado)
        print('  ok  %d vez(es)  %s' % (n, old.split('\n')[0][:64]))

    compile(d, ALVO, 'exec')
    tmp = ALVO + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(d)
    os.replace(tmp, ALVO)
    print()
    print('gravado: %s  %d -> %d bytes' % (ALVO, antes, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

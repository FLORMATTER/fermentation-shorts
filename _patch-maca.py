# -*- coding: utf-8 -*-
"""
_patch-maca.py — poe os 3 keyframes que faltavam no #27.

O gerador abortou com `keyframe nunca usado: ['chop2x', 'pour2x', 'tick']`. O
template traz 6 keyframes e a convencao da serie e' usar os 6. As cenas novas
usavam so' riseFast, wobble e pulseBadge.

  chop2x (1.7s) -> FACA cortando a maca        (cena 2, o motor)
  tick   (2.2s) -> AMPULHETA balancando        (cena 4, o jarro parado)
  pour2x (1.6s) -> GRAOS DE SAL caindo         (cena 6, a salmoura)

Ancora com contagem esperada: ABORTA SEM GRAVAR se alguma nao casar.
"""
import io
import os
import sys

ALVO = '_criar-maca-alho-cenoura.py'

HELPERS = '''def faca(x, y, rot=0):
    """Faca de cozinha: lamina LARGA (estreita le' como termometro)."""
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g})">'
            '<g style="animation:chop2x 1.7s ease-in-out infinite">'
            '<path d="M-92,-13 L22,-13 L22,13 L-62,13 Q-92,13 -92,-1 Z"'
            ' fill="#cdd6dc" stroke="#7a8a92" stroke-width="2.5"'
            ' stroke-linejoin="round"/>'
            '<path d="M-88,-9 L20,-9 L20,-2 L-88,-2 Z" fill="#eef3f6"/>'
            '<rect x="22" y="-15" width="9" height="30" rx="3" fill="#9aa8b0"'
            ' stroke="#6f7d85" stroke-width="2"/>'
            '<rect x="31" y="-12" width="46" height="24" rx="8" fill="#8a5a34"'
            ' stroke="#5e3a1f" stroke-width="2.5"/>'
            '<circle cx="44" cy="0" r="2.6" fill="#5e3a1f"/>'
            '<circle cx="62" cy="0" r="2.6" fill="#5e3a1f"/>'
            '</g></g>')


def sal_graos(x, y, s=1.0):
    """Graos de sal caindo — o `pour2x` da serie."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<g style="animation:pour2x 1.6s ease-out infinite">'
            '<rect x="-3" y="-6" width="6" height="6" rx="1.5" fill="#fff"'
            ' stroke="#c9bfa4" stroke-width="1.2"/>'
            '<rect x="8" y="4" width="6" height="6" rx="1.5" fill="#fff"'
            ' stroke="#c9bfa4" stroke-width="1.2"/>'
            '<rect x="-9" y="12" width="6" height="6" rx="1.5" fill="#fff"'
            ' stroke="#c9bfa4" stroke-width="1.2"/>'
            '</g></g>')


'''

EDICOES = [
    # 1. os dois helpers novos, logo depois do ampulheta().
    #    Ancora SEM aspas: dentro de r-string a barra nao e' processada, entao
    #    `\"` vira barra + aspas literal e a ancora nunca casa (custou 1 rodada).
    ('\n\n\n# --------------------------------------------------- cena 1: o gancho (o conflito)',
     '\n\n\n' + HELPERS
     + '# --------------------------------------------------- cena 1: o gancho (o conflito)',
     1),

    # 2a. a faca entra na cena 2, ao lado da maca
    (r'    <g transform="translate(202,378)">@MACA@</g>'
     '\n'
     r'    @PONTOS@',
     r'    <g transform="translate(202,378)">@MACA@</g>'
     '\n'
     r'    <g transform="translate(322,334)">@FACA@</g>'
     '\n'
     r'    @PONTOS@',
     1),

    # 2b. ...e o token tem de ser substituido (o bug da 1a versao foi esquecer isso).
    #     O replace novo vai NA MESMA LINHA: a linha do `.replace('@PONTOS@'...)` nao
    #     termina com ` \`, entao uma linha nova comecando por `.replace` quebra a
    #     expressao (IndentationError). Custou 1 rodada.
    (r"     .replace('@PONTOS@', leveduras([(150, 340, 5), (256, 352, 4.4), (168, 424, 4),"
     '\n'
     r'                                     (244, 420, 5), (204, 322, 4.2), (140, 388, 4.6),'
     '\n'
     r'                                     (268, 392, 4.2)]))',
     r"     .replace('@PONTOS@', leveduras([(150, 340, 5), (256, 352, 4.4), (168, 424, 4),"
     '\n'
     r'                                     (244, 420, 5), (204, 322, 4.2), (140, 388, 4.6),'
     '\n'
     r'                                     (268, 392, 4.2)])).replace('
     r"'@FACA@', faca(0, 0, 30))",
     1),

    # 3. a ampulheta ganha o `tick`
    (r'    <g transform="translate(300,400)">@AMPULHETA@</g>',
     r'    <g transform="translate(300,400)">'
     r'<g style="animation:tick 2.2s ease-in-out infinite">@AMPULHETA@</g></g>',
     1),

    # 4a. graos de sal caindo dentro da salmoura
    (r'    <g transform="translate(292,352)">'
     '\n'
     r'      <rect x="-64" y="-64" width="128" height="128" rx="14" fill="#eef7e6"',
     r'    <g transform="translate(292,296)">@SAL@</g>'
     '\n'
     r'    <g transform="translate(292,352)">'
     '\n'
     r'      <rect x="-64" y="-64" width="128" height="128" rx="14" fill="#eef7e6"',
     1),

    # 4b. ...e o token do sal (mesma linha, pelo mesmo motivo do 2b)
    (r"     .replace('@ALHO_P@', alho(0, 0, 0.5))",
     r"     .replace('@ALHO_P@', alho(0, 0, 0.5)).replace('@SAL@', sal_graos(0, 0, 1.0))",
     1),
]


def main():
    if not os.path.exists(ALVO):
        print('ABORTA: nao achei %s' % ALVO)
        return 1
    with io.open(ALVO, encoding='utf-8', newline='') as f:
        d = f.read()
    antes = len(d.encode('utf-8'))
    eol = '\r\n' if d.count('\r\n') else '\n'

    for old, new, esperado in EDICOES:
        n = d.count(old)
        if n != esperado:
            print('ABORTA: ancora casou %d vez(es), esperava %d:' % (n, esperado))
            print('   %r' % old[:110])
            return 1
        d = d.replace(old, new, esperado)
        print('  ok  %d vez(es)  <- %r' % (n, old[:60].replace('\n', ' ')))

    # os 6 keyframes tem de aparecer agora
    for kf in ('chop2x', 'pour2x', 'tick', 'riseFast', 'wobble', 'pulseBadge'):
        if ('animation:%s' % kf) not in d and ('animation:%s ' % kf) not in d:
            print('ABORTA: o keyframe %s continua sem uso' % kf)
            return 1

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

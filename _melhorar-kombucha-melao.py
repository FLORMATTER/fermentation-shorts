# -*- coding: utf-8 -*-
"""_melhorar-kombucha-melao.py — conserta as FORMAS do short maca+melao.

O render em tamanho nativo mostrou quatro leituras erradas:

  cena 0/3 — o melao cortado lê como **LARANJA**: a casca verde e' fina demais e a
             polpa domina o circulo. Casca grossa resolve;
  cena 5   — o melao inteiro lê como **KIWI**: casca VERDE (cantalupo e' BEGE) e a
             rede e' uma grade simetrica (parece bola de tenis). Bege + rede
             irregular;
  cena 5   — a faca lê como **TERMOMETRO**: lamina estreita demais. Lamina larga;
  cena 2   — o fio de kombucha FLUTUA acima do jarro e os pedacos de melao somem
             no liquido (cores vizinhas). Fio mais comprido + contraste nos pedacos.

    python _melhorar-kombucha-melao.py
"""
import io
import re
import sys

ALVO = '_criar-kombucha-melao.py'

MELAO_METADE = '''def melao_metade(x, y, s=1.0):
    """Meio melao visto do CORTE: casca, casca palida, faixa branca, polpa.

    A CASCA tem de ser GROSSA e escura: casca fina faz o desenho ler como
    LARANJA (1o render). Ordem importa — cada circulo por cima do anterior.
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<circle r="78" fill="#8f9c53" stroke="#6f7c3d" stroke-width="3"/>'
            '<circle r="69" fill="#c3cd93"/>'
            '<circle r="62" fill="#ece6cc"/>'
            '<circle r="53" fill="#f0a24a"/>'
            '<circle r="53" fill="#f7bb72" opacity=".28"/>'
            '<ellipse rx="18" ry="12" fill="#f7dcb0"/>'
            '<ellipse cx="-6" cy="-3" rx="3.2" ry="4.6" fill="#d99a4a"/>'
            '<ellipse cx="6" cy="4" rx="3.2" ry="4.6" fill="#d99a4a"/>'
            '<ellipse cx="1" cy="-6" rx="3.2" ry="4.6" fill="#d99a4a"/>'
            '<ellipse cx="-3" cy="6" rx="3.2" ry="4.6" fill="#d99a4a"/>'
            '</g>')'''

MELAO_INTEIRO = '''def melao_inteiro(x, y, s=1.0):
    """Melao inteiro: casca BEGE com a rede em relevo.

    Verde faz ler KIWI (1o render) — cantalupo e' BEGE. E a rede tem de ser
    IRREGULAR: uma grade simetrica le' como bola de tenis. Por isso cada corda
    tem o seu proprio bojo, e as verticais e as horizontais nao se espelham.
    """
    R = 76
    rede = []
    for c, bojo in ((-58, 4), (-37, 8), (-13, 5), (11, 9), (34, 6), (55, 3)):
        h = (R * R - c * c) ** 0.5 * 0.95
        rede.append(f'<path d="M{c},{-h:.1f} Q{c + bojo},0 {c},{h:.1f}" fill="none"'
                    ' stroke="#f7f0dc" stroke-width="3.6" opacity=".95"'
                    ' stroke-linecap="round"/>')
    for c, bojo in ((-50, 6), (-28, 4), (-4, 8), (20, 5), (43, 7)):
        h = (R * R - c * c) ** 0.5 * 0.95
        rede.append(f'<path d="M{-h:.1f},{c} Q0,{c + bojo:.1f} {h:.1f},{c}" fill="none"'
                    ' stroke="#f7f0dc" stroke-width="3.6" opacity=".95"'
                    ' stroke-linecap="round"/>')
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<circle r="{R}" fill="#cbb98c" stroke="#a8935f" stroke-width="3.5"/>'
            f'<circle r="{R - 3}" fill="#e2d3ad"/>'
            + ''.join(rede) +
            '<ellipse cy="-72" rx="7" ry="5" fill="#b8a373"/>'
            '</g>')'''

COLHER = '''def colher_prova(x, y, s=1.0):
    """Colher de prova com kombucha na cuia, mergulhando (`chop2x`)."""
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<g style="animation:chop2x 1.6s ease-in-out infinite">'
            '<path d="M2,-66 L11,-62 L4,2 L-5,0 Z" fill="#c9d8c0" stroke="#5c7a29"'
            ' stroke-width="2.5" stroke-linejoin="round"/>'
            '<ellipse cx="-6" cy="16" rx="27" ry="17" fill="#c9d8c0"'
            ' stroke="#5c7a29" stroke-width="3"/>'
            '<ellipse cx="-6" cy="16" rx="19" ry="11" fill="#d9a441"/>'
            '</g></g>')'''

FACA = '''def faca(x, y, rot=0):
    """Faca de cozinha: lamina LARGA, afiada de um lado, com cabo e rebites.

    Lamina estreita le' como TERMOMETRO — foi o que o 1o render mostrou.
    """
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g})">'
            '<g style="animation:chop2x 1.7s ease-in-out infinite">'
            '<path d="M-15,-68 L15,-64 L17,30 Q17,38 8,38 L-15,38 Z"'
            ' fill="#cdd6dc" stroke="#7a8a92" stroke-width="2.5"'
            ' stroke-linejoin="round"/>'
            '<path d="M-15,-68 L15,-64 L16,-24 L-15,-26 Z" fill="#eef3f6"/>'
            '<path d="M-15,30 L17,30" stroke="#9aa8b0" stroke-width="2"/>'
            '<rect x="-13" y="38" width="26" height="52" rx="9" fill="#8a5a34"'
            ' stroke="#5e3a1f" stroke-width="2.5"/>'
            '<circle cx="0" cy="53" r="2.6" fill="#5e3a1f"/>'
            '<circle cx="0" cy="69" r="2.6" fill="#5e3a1f"/>'
            '</g></g>')'''

TROCAS_BLOCO = [
    ('melao_metade', MELAO_METADE, r'\n\ndef melao_inteiro\('),
    ('melao_inteiro', MELAO_INTEIRO, r'\n\ndef maca\('),
    ('colher_prova', COLHER, r'\n\ndef faca\('),
    ('faca', FACA, r'\n\ndef gota\('),
]

TROCAS_TEXTO = [
    # o fio de kombucha tinha 26 px e ficava 84 px acima da boca do jarro
    ('''    <g transform="translate(202,148)">
      <g style="animation:pour2x 1.6s ease-out infinite">
        <path d="M-14,-4 L14,-4 L14,12 Q0,24 -14,12 Z" fill="#d9a441" opacity=".9"/>
      </g>
    </g>''',
     '''    <g transform="translate(202,206)">
      <g style="animation:pour2x 1.6s ease-out infinite">
        <path d="M-9,-46 L9,-46 L13,8 Q0,20 -13,8 Z" fill="#d9a441" opacity=".92"/>
      </g>
    </g>''', 1),
    # os pedacos sumiam: liquido claro, pedaco escuro
    ('.replace(\'@JARRA@\', jarra(\'#f2b878\'))',
     '.replace(\'@JARRA@\', jarra(\'#f8dfb8\'))', 1),
    ('fill="#f0a24a" stroke="#c9803a" stroke-width="2.5" stroke-linejoin="round"',
     'fill="#e07b2e" stroke="#b45c17" stroke-width="2.5" stroke-linejoin="round"', 2),
    ('fill="#f7bb72" stroke="#c9803a" stroke-width="2.5" stroke-linejoin="round"',
     'fill="#f0a24a" stroke="#b45c17" stroke-width="2.5" stroke-linejoin="round"', 1),
    ('.replace(\'@COLHER@\', colher_prova(0, 0))',
     '.replace(\'@COLHER@\', colher_prova(0, 0, 1.35))', 1),
]


def troca_bloco(d, nome, novo, fim):
    pat = re.compile(r'def %s\(.*?\n(?=%s)' % (nome, fim), re.S)
    if len(pat.findall(d)) != 1:
        print('ERRO: bloco %s casou %d vez(es)' % (nome, len(pat.findall(d))))
        return None
    return pat.sub(lambda m: novo + '\n', d, count=1)


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    print('%s: %d bytes' % (ALVO, len(d.encode('utf-8'))))

    for nome, novo, fim in TROCAS_BLOCO:
        d2 = troca_bloco(d, nome, novo, fim)
        if d2 is None:
            print('NADA FOI GRAVADO.')
            return 1
        d = d2
        print('  ok: bloco %s' % nome)

    for velho, novo, esperado in TROCAS_TEXTO:
        c = d.count(velho)
        if c != esperado:
            print('ERRO: ancora casou %d (esperado %d): %r'
                  % (c, esperado, velho[:60]))
            print('NADA FOI GRAVADO.')
            return 1
        d = d.replace(velho, novo)
    print('  ok: %d ajustes de texto' % len(TROCAS_TEXTO))

    # nenhuma funcao pode ter sumido nem duplicado
    for nome in ('melao_metade', 'melao_inteiro', 'maca', 'garrafa', 'jarra',
                 'bolhas', 'medidor', 'colher_prova', 'faca', 'gota',
                 'escala_ph', 'escala_ph_vertical'):
        n = len(re.findall(r'^def %s\(' % nome, d, re.M))
        if n != 1:
            print('ERRO: `def %s` aparece %d vez(es)' % (nome, n))
            return 1

    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: -> %d bytes | 12 helpers intactos | compila' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())

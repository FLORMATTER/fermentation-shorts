# -*- coding: utf-8 -*-
"""_melhorar-pepino2.py — 2a passada de FORMA no short pepino+alho (no GERADOR).

O que o zoom em 3x mostrou depois da 1a passada:

  cena 0 — os dentes ficaram assimetricos, mas ainda leem como BAGA/pingo. Faltava
           a FAIXA CLARA da FACE DO CORTE (o lado reto do dente descascado): e' ela
           que diz "dente cortado" em vez de "fruta";
  cena 3 — os 5 dentes separados resolveram a concha, mas sozinhos leem como FLOR
           (petalas abertas) e o colo fica FLUTUANDO. Falta a CASCA: uma silhueta
           palida, pontilhada, que amarra os dentes num bulbo e liga o colo.

    python _melhorar-pepino2.py
"""
import io
import re
import sys

ALVO = '_criar-pepino-alho.py'

DENTE = '''def dente(x, y, fill, stroke, s=1.0, w=2.5):
    """Dente de alho DESCASCADO — a casca (barriga) + a FACE DO CORTE.

    Gota simetrica le' como pingo d'agua (1o render); a linha da base nao bastou
    (2o); o lado reto sozinho ainda le' como baga (3o). O que faltava era a FAIXA
    CLARA do corte, do lado reto — e' ela que faz ler "dente cortado".
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<path d="M-5,-24 C7,-18 16,-7 16,5 C16,16 10,22 1,22'
            ' L-12,22 C-16,22 -17,17 -17,7 L-16,-9 C-15,-17 -11,-21 -5,-24 Z"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="{w/s:g}"'
            ' stroke-linejoin="round"/>'
            '<path d="M-5,-24 C-11,-21 -15,-17 -16,-9 L-17,7 C-17,16 -16,20 -12,22'
            ' L-5,22 C-2,8 -1,-8 -5,-24 Z" fill="#ffffff" opacity=".42"/>'
            '<path d="M-5,-24 C-1,-8 -2,8 -5,22" fill="none"'
            f' stroke="{stroke}" stroke-width="{w*0.7/s:g}" opacity=".3"/>'
            '</g>')'''

CRAVO = '''def cravo(cx, cy, rot, w, h, fill, stroke='#b08f4e', sw=3):
    """Um dente COM CASCA, visto de frente — a peca de construcao do bulbo."""
    return (f'<g transform="translate({cx:g},{cy:g}) rotate({rot:g})">'
            f'<path d="M0,{-h:g}'
            f' C{w*0.62:g},{-h*0.42:g} {w*0.52:g},{-h*0.10:g} {w*0.50:g},0'
            f' C{w*0.62:g},{h*0.50:g} {w*0.42:g},{h*0.86:g} {w*0.36:g},{h*0.86:g}'
            f' L{-w*0.36:g},{h*0.86:g}'
            f' C{-w*0.42:g},{h*0.86:g} {-w*0.62:g},{h*0.50:g} {-w*0.50:g},0'
            f' C{-w*0.52:g},{-h*0.10:g} {-w*0.62:g},{-h*0.42:g} 0,{-h:g} Z"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"'
            ' stroke-linejoin="round"/>'
            '</g>')'''

BULBO = '''def bulbo_alho(x, y):
    """Bulbo = CASCA (silhueta palida pontilhada) + 5 DENTES + colo.

    Silhueta unica com lobulos le' como CONCHA (2o render). Dentes separados leem
    como FLOR de petalas abertas, com o colo flutuando (3o render). A CASCA
    resolve os dois. Mas o bulbo tem de ser ATARRAQUADO — mais LARGO que ALTO:
    alto e bicudo le' como BOTAO/cebola (4o render). Alho de verdade e' baixo, o
    terco de cima e' so' casca e os dentes aparecem embaixo.
    """
    casca = ('<path d="M0,-62 C-16,-50 -28,-36 -40,-18 C-56,-4 -64,10 -60,26'
             ' C-54,46 -30,60 0,60 C30,60 54,46 60,26 C64,10 56,-4 40,-18'
             ' C28,-36 16,-50 0,-62 Z" fill="#f9f2e0" stroke="#cbb98c"'
             ' stroke-width="2.5" stroke-dasharray="6 5"/>')
    colo = ('<path d="M-9,-60 L-6,-78 L6,-78 L9,-60 Z" fill="#e6d9b6"'
            ' stroke="#b08f4e" stroke-width="3" stroke-linejoin="round"/>'
            '<line x1="0" y1="-78" x2="0" y2="-92" stroke="#b08f4e"'
            ' stroke-width="3" stroke-linecap="round"/>')
    dentes = [(-46, 32, -16, 28, 28, '#e6d9b6'),
              (46, 32, 16, 28, 28, '#e6d9b6'),
              (-29, 24, -7, 34, 36, '#f2e6c9'),
              (29, 24, 7, 34, 36, '#f2e6c9'),
              (0, 20, 0, 40, 42, '#f7eed6')]
    corpo = ''.join(cravo(*d) for d in dentes)
    return (f'<g transform="translate({x:g},{y:g})">'
            '<g style="animation:wobble 2.7s ease-in-out infinite">'
            + casca + colo + corpo + '</g></g>')


def lab(x, y, rot, cor='#1d9e75', t=1.0):
    """Uma bacteria lactica: BASTONETE. Nao e' bolinha — circulos soltos liam
    como pontos aleatorios no render."""
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g})">'
            f'<rect x="{-9*t:g}" y="{-3.6*t:g}" width="{18*t:g}" height="{7.2*t:g}"'
            f' rx="{3.6*t:g}" fill="{cor}" opacity=".85"/>'
            '</g>')


def nuvem_lab():
    """Os bastonetes em volta do bulbo. Ficam ATRAS dele (o token vem antes)."""
    pos = [(112, 200, -18), (84, 268, 12), (114, 340, -8), (294, 196, 20),
           (322, 266, -14), (292, 342, 8), (196, 104, 4), (268, 118, -22)]
    return '\\n    '.join(lab(*p) for p in pos)'''


def troca_bloco(d, nome, novo, fim):
    """Troca o bloco `def <nome>(...)` inteiro ate' o terminador `fim`.

    ATENCAO: o bloco de `bulbo_alho` VAI ATE' a linha `# --- cena 1`, entao ele
    engole `cravo`, `lab` e `nuvem_lab`. Por isso o texto de substituicao tem de
    trazer os tres de volta — senao o gerador morre com NameError.
    """
    pat = re.compile(r'def %s\(.*?\n(?=%s)' % (nome, fim), re.S)
    if len(pat.findall(d)) != 1:
        print('ERRO: bloco %s casou %d vez(es)' % (nome, len(pat.findall(d))))
        return None
    return pat.sub(lambda m: novo + '\n', d, count=1)


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    print('%s: %d bytes' % (ALVO, len(d.encode('utf-8'))))

    # `cravo` fica ANTES do bloco do bulbo, entao nao e' engolido: o BULBO traz
    # so' bulbo_alho + lab + nuvem_lab de volta. Incluir o CRAVO aqui criaria
    # uma 2a definicao de `cravo` (foi o que a checagem pegou).
    for nome, novo, fim in (('dente', DENTE, r'\n\ndef colher_sal\('),
                            ('bulbo_alho', BULBO, r'\n\n# ---')):
        d2 = troca_bloco(d, nome, novo, fim)
        if d2 is None:
            return 1
        d = d2
        print('  ok: bloco %s trocado' % nome)

    # os 3 helpers que o bloco do bulbo engole TEM de voltar
    for nome in ('cravo', 'lab', 'nuvem_lab', 'colher_sal', 'fatia'):
        n = len(re.findall(r'^def %s\(' % nome, d, re.M))
        if n != 1:
            print('ERRO: `def %s` aparece %d vez(es) — o bloco engoliu' % (nome, n))
            return 1
    print('  ok: cravo, lab, nuvem_lab, colher_sal, fatia presentes')

    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: -> %d bytes | compila' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())

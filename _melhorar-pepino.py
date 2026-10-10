# -*- coding: utf-8 -*-
"""_melhorar-pepino.py — conserta as FORMAS do short pepino+alho, no GERADOR.

O render em 3x (`_zoom-cena.py`) mostrou tres coisas que o tamanho nativo
escondia:

  cena 0 — os dentes de alho leem como PINGO D'AGUA (gota simetrica). A linha da
           base nao bastou: o contorno INTEIRO tem de ser assimetrico. Alho
           descascado tem LADO RETO (o corte) e barriga do outro lado;
  cena 0 — as rodelas de pepino eram elipses lisas: sem casca + miolo + semente
           nao se le' "pepino", le' "azeitona";
  cena 3 — o bulbo era UMA silhueta com 8 lobulos -> le' como CONCHA/pinha, e as
           duas curvas internas viram NERVURA de folha. Alho se le' pelos DENTES:
           varios, lado a lado, cada um com o SEU contorno. Os 4 circulos verdes
           soltos liam como pontos aleatorios — viraram bastonetes (LAB).

Conserto no gerador, nao no HTML: o gerador e' a fonte da verdade.

    python _melhorar-pepino.py

Aborta SEM GRAVAR se qualquer ancora nao casar exatamente 1 vez.
"""
import io
import re
import sys

ALVO = '_criar-pepino-alho.py'


# ------------------------------------------------------------------ helpers
FATIA = '''def fatia(cx, cy, rot, r, cor='#639922'):
    """Uma rodela de pepino: casca escura, miolo claro, sementes.

    Elipse lisa le' como azeitona — foi o defeito do 2o render. O que faz ler
    "pepino" e' o anel de casca + o miolo palido + as sementes.
    """
    return (f'<g transform="translate({cx:g},{cy:g}) rotate({rot:g})">'
            f'<ellipse rx="{r:g}" ry="{r*0.44:g}" fill="{cor}"'
            f' stroke="#2f5c0d" stroke-width="2.5"/>'
            f'<ellipse rx="{r*0.66:g}" ry="{r*0.29:g}" fill="#e2f0cc"/>'
            f'<ellipse cx="{-r*0.36:g}" rx="{r*0.09:g}" ry="{r*0.10:g}" fill="#a9c97e"/>'
            f'<ellipse cx="{r*0.36:g}" rx="{r*0.09:g}" ry="{r*0.10:g}" fill="#a9c97e"/>'
            f'<ellipse cy="{-r*0.17:g}" rx="{r*0.09:g}" ry="{r*0.10:g}" fill="#a9c97e"/>'
            f'<ellipse cy="{r*0.17:g}" rx="{r*0.09:g}" ry="{r*0.10:g}" fill="#a9c97e"/>'
            '</g>')'''

DENTE = '''def dente(x, y, fill, stroke, s=1.0, w=2.5):
    """Dente de alho DESCASCADO: lado esquerdo RETO (o corte), barriga a' direita.

    O que faz ler "alho" nao e' a ponta nem a base: e' o LADO RETO. Uma gota
    simetrica le' como pingo d'agua (1o render); so' a linha da base nao bastou
    (2o render). O contorno inteiro tem de ser assimetrico.
    """
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            '<path d="M0,-22 C7,-16 13,-5 13,7 C13,16 8,21 1,21'
            ' L-9,21 C-13,21 -13,16 -13,7 L-10,-14 Z"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="{w/s:g}"'
            ' stroke-linejoin="round"/>'
            '<path d="M-9,19 C-11,8 -9,-4 -7,-12" fill="none"'
            f' stroke="{stroke}" stroke-width="{w*0.8/s:g}" opacity=".5"'
            ' stroke-linecap="round"/>'
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
    """Bulbo inteiro = 5 DENTES (os de fora atras, o do meio na frente) + o colo.

    Uma silhueta unica com lobulos le' como CONCHA/pinha, e as curvas internas
    viram nervura de folha — foi o defeito do 2o render. Alho se le' pelos dentes
    separados, cada um com o SEU contorno.
    """
    dentes = [(-54, 26, -30, 24, 42, '#e6d9b6'),
              (54, 26, 30, 24, 42, '#e6d9b6'),
              (-30, 16, -15, 30, 54, '#f2e6c9'),
              (30, 16, 15, 30, 54, '#f2e6c9'),
              (0, 6, 0, 34, 62, '#f7eed6')]
    corpo = ''.join(cravo(*d) for d in dentes)
    colo = ('<path d="M-9,-56 L-7,-84 L7,-84 L9,-56 Z" fill="#e6d9b6"'
            ' stroke="#b08f4e" stroke-width="3" stroke-linejoin="round"/>'
            '<line x1="0" y1="-84" x2="0" y2="-98" stroke="#b08f4e"'
            ' stroke-width="3" stroke-linecap="round"/>')
    return (f'<g transform="translate({x:g},{y:g})">'
            '<g style="animation:wobble 2.7s ease-in-out infinite">'
            + corpo + colo + '</g></g>')


def lab(x, y, rot, cor='#1d9e75', t=1.0):
    """Uma bacteria lactica: BASTONETE. Nao e' bolinha — 4 circulos soltos liam
    como pontos aleatorios no render."""
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g})">'
            f'<rect x="{-9*t:g}" y="{-3.6*t:g}" width="{18*t:g}" height="{7.2*t:g}"'
            f' rx="{3.6*t:g}" fill="{cor}" opacity=".85"/>'
            '</g>')


def nuvem_lab():
    """Os bastonetes em volta do bulbo. Ficam ATRAS dele (o token vem antes)."""
    pos = [(118, 182, -18), (92, 254, 12), (124, 328, -8), (286, 178, 20),
           (312, 256, -14), (280, 330, 8), (202, 112, 4)]
    return '\\n    '.join(lab(*p) for p in pos)'''

S0 = '''def s0(t):
    return \'\'\'    <rect width="405" height="720" fill="#f6fbf3"/>
    <circle cx="202" cy="290" r="158" fill="#e1f5ee" opacity=".55"/>
    <g transform="translate(202,290)">
      <g style="animation:wobble 2.9s ease-in-out infinite">
        <path d="M-78,-96 L-78,88 Q-78,110 -56,110 L56,110 Q78,110 78,88 L78,-96 Z" fill="#eef8f0" stroke="#3b6d11" stroke-width="4"/>
        <rect x="-86" y="-114" width="172" height="22" rx="8" fill="#dcecd6" stroke="#3b6d11" stroke-width="4"/>
        <path d="M-72,-62 L-72,84 Q-72,104 -50,104 L50,104 Q72,104 72,84 L72,-62 Z" fill="#cde5bf"/>
        <ellipse cx="-52" cy="6" rx="9" ry="56" fill="#fff" opacity=".35"/>
        @F1@
        @F2@
        @F3@
        @D1@
        @D2@
        @D3@
        <g style="animation:riseFast 1.5s ease-out infinite">
          <circle cx="-44" cy="66" r="4" fill="#fff" opacity=".85"/>
          <circle cx="8" cy="78" r="3.4" fill="#fff" opacity=".8"/>
        </g>
        <g style="animation:riseFast 1.5s ease-out .5s infinite">
          <circle cx="-14" cy="84" r="3.8" fill="#fff" opacity=".65"/>
          <circle cx="38" cy="80" r="3.2" fill="#fff" opacity=".6"/>
        </g>
      </g>
    </g>
    <g transform="translate(202,516)">
      <rect x="-166" y="-44" width="332" height="88" rx="12" fill="#fff" stroke="#3b6d11" stroke-width="3"/>
      <text x="0" y="-8" text-anchor="middle" font-size="21" font-weight="800" fill="#2f5c0d" font-family="system-ui">THE GARLIC TURNS BLUE</text>
      <text x="0" y="22" text-anchor="middle" font-size="14" font-weight="600" fill="#6b8f3a" font-family="system-ui">that is the acid working</text>
    </g>\'\'\'.replace('@F1@', fatia(-26, -22, -12, 38)) \\
     .replace('@F2@', fatia(28, -6, 10, 36)) \\
     .replace('@F3@', fatia(-6, 16, -3, 36)) \\
     .replace('@D1@', dente(-36, 72, '#3a8fb0', '#1f5f7d')) \\
     .replace('@D2@', dente(4, 80, '#3a8fb0', '#1f5f7d')) \\
     .replace('@D3@', dente(44, 62, '#f2e6c9', '#b08f4e'))'''

S3 = '''def s3(t):
    return \'\'\'    <rect width="405" height="720" fill="#f6fbf3"/>
    @LABS@
    @BULBO@
    <g transform="translate(202,414)">
      <rect x="-168" y="-40" width="336" height="80" rx="12" fill="#fff" stroke="#1d9e75" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="17" font-weight="800" fill="#0f6e56" font-family="system-ui">LEUCONOSTOC + WEISSELLA</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#4a8a6e" font-family="system-ui">the bacteria that start the ferment</text>
    </g>
    <g transform="translate(202,520)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#2f5c0d" font-family="system-ui">THEY RIDE IN ON THE GARLIC</text>
    </g>\'\'\'.replace('@LABS@', nuvem_lab()) \\
     .replace('@BULBO@', bulbo_alho(202, 244))'''


def troca_bloco(d, nome, novo, fim):
    """Troca o bloco `def <nome>(...)` inteiro.

    `fim` e' o que VEM DEPOIS do bloco (o `def` seguinte ou a linha de comentario
    da proxima cena). Nao da' para ancorar so' em "linha em branco + #": o `#`
    seguinte ao `dente` e' o da cena 1, entao o bloco engoliria `colher_sal` e
    `bulbo_alho` inteiros. Ja' aconteceu — o script abortou antes de gravar.
    """
    pat = re.compile(r'def %s\(.*?\n(?=%s)' % (nome, fim), re.S)
    achados = pat.findall(d)
    if len(achados) != 1:
        print('ERRO: bloco %s casou %d vez(es)' % (nome, len(achados)))
        return None
    return pat.sub(lambda m: novo + '\n', d, count=1)


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    print('%s: %d bytes, %s' % (ALVO, len(d.encode('utf-8')),
                                'CRLF' if eol == '\r\n' else 'LF'))

    # ATENCAO ao lookahead: o `.*?\n` JA' consome um \n, entao aqui sobram DOIS.
    # Com `\n\n\n` no lookahead o bloco nunca casa (off-by-one que custou uma rodada).
    for nome, novo, fim in (
            ('dente', FATIA + '\n\n\n' + DENTE, r'\n\ndef colher_sal\('),
            ('bulbo_alho', CRAVO + '\n\n\n' + BULBO, r'\n\n# ---'),
            ('s0', S0, r'\n\n# ---'),
            ('s3', S3, r'\n\n# ---')):
        d2 = troca_bloco(d, nome, novo, fim)
        if d2 is None:
            return 1
        d = d2
        print('  ok: bloco %s trocado' % nome)

    # a cor do desenho e' AZUL; "jade" (verde) contradizia o proprio desenho
    velho = 'sulfur plus acid, and the clove turns jade'
    if d.count(velho) != 1:
        print('ERRO: a frase do "jade" casou %d vez(es)' % d.count(velho))
        return 1
    d = d.replace(velho, 'sulfur plus acid, and the clove changes colour')
    print('  ok: "jade" -> "changes colour"')

    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: %d -> %d bytes | compila' % (21618, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

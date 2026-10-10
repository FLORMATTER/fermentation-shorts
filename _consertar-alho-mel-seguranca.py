# -*- coding: utf-8 -*-
"""_consertar-alho-mel-seguranca.py — poe o aviso de botulismo no #9 (alho com mel).

    python _consertar-alho-mel-seguranca.py

Por que: o #9 (`alho/shorts-garlic-honey-en.html`) esta pronto, renderizado e no
pacote — mas a cena 7 mandava **"Keep it at room temperature"** e NAO avisava do
unico risco documentado desse fermento.

O que a pesquisa diz (scienceinsights.org, CDC/FSIS citados na fonte):
  - mel e alho SAO carreadores conhecidos de esporos de Clostridium botulinum;
  - o esporo so' acorda com TRES coisas juntas: sem oxigenio + 4-60 °C + pH > 4,6;
  - o mel tem pouca agua disponivel, mas o alho solta agua e isso derruba essa
    barreira (acima de 0,93 de atividade de agua ela enfraquece);
  - a janela perigosa e' o comeco, ANTES de a fermentacao baixar o pH;
  - abaixo de 4 °C o esporo nao germina — e' o que a geladeira garante;
  - **bebe menor de 1 ano: nunca, em nenhuma preparacao** (o intestino imaturo
    deixa o esporo colonizar e produzir toxina dentro do corpo).

O conserto e' cirurgico: o cartao da cena 7 (3 linhas, y 564/586/606) passa a ser
o cartao de seguranca. A linha "Keep it at room temperature" sai — e' justamente o
conselho que a fonte aponta como o risco. A contagem de cenas (8), as duracoes e a
barra de legenda NAO mudam, entao o pacote e o plano continuam valendo.

⚠ Isto muda o video: o mp4 precisa ser REGERADO depois.
"""
import io
import re
import sys

ARQ = 'alho/shorts-garlic-honey-en.html'

TROCAS = [
    ('linha 1 do cartao -> a regra do bebe',
     '<text x="202" y="564" text-anchor="middle" font-size="12" font-weight="900" fill="#3d3222" font-family="system-ui">Keep it at room temperature</text>',
     '<text x="202" y="564" text-anchor="middle" font-size="12" font-weight="900" fill="#a01e52" font-family="system-ui">⚠ NEVER GIVE IT TO A BABY</text>', 1),
    ('linha 2 do cartao -> o motivo',
     '<text x="202" y="586" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">Dark place. Loose lid for the first days</text>',
     '<text x="202" y="586" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">Honey can carry botulism spores</text>', 1),
    ('linha 3 do cartao -> o frio',
     '<text x="202" y="606" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">it will foam up and can overflow</text>',
     '<text x="202" y="606" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">When in doubt, keep it cold</text>', 1),
    ('a barra da cena 7 carrega o detalhe',
     "cap:'3 to 4 weeks minimum', sub:'the slowest ferment of them all'",
     "cap:'3 to 4 weeks minimum', sub:'under 1 year old, never'", 1),
]


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    print('%s (%d bytes, %s)' % (ARQ, len(d), 'CRLF' if eol == '\r\n' else 'LF'))

    antes_ms = re.findall(r'ms:(\d+)', d)
    antes_cenas = len(re.findall(r'<svg class="scene', d))

    falhou = False
    for i, (rotulo, velho, novo, esperado) in enumerate(TROCAS, 1):
        c = d.count(velho)
        if c != esperado:
            print('  %d. %-34s casou %d (esperado %d) ERRO' % (i, rotulo, c, esperado))
            falhou = True
            continue
        d = d.replace(velho, novo)
        print('  %d. %-34s ok (%d)' % (i, rotulo, c))

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    if re.findall(r'ms:(\d+)', d) != antes_ms:
        print('\nABORTADO: as duracoes mudaram.')
        return 1
    if len(re.findall(r'<svg class="scene', d)) != antes_cenas:
        print('\nABORTADO: o numero de cenas mudou.')
        return 1
    print('  duracoes e numero de cenas: iguais (%d cenas, %s s)'
          % (antes_cenas, sum(int(x) for x in antes_ms) / 1000))

    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %d bytes' % len(d))
    print('AGORA REGERAR O MP4:')
    print('  node _gerar-mp4.js --w=1080 --fps=30 --kbps=3000 --cfr=1 %s' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())

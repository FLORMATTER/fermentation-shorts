"""_pacote-fps.py — o pacote dizia "constant 30 fps" para os 8 do lote, e nao e' 30.

O retimar preserva a DURACAO distribuindo os quadros que sobreviveram, entao a taxa
efetiva fica logo abaixo de 30 (29,6 a 30,0). O numero certo e' o que o
`_mp4/inspecionar.py` mede no arquivo, nao o alvo.

Oito ancoras contadas. Aborta sem gravar se alguma nao casar uma vez.
"""
import sys

ARQ = 'guias/pacote-legendas-descricoes-en.md'
d = open(ARQ, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in d else '\n'
print('%s: fim de linha %s' % (ARQ, 'CRLF' if nl == '\r\n' else 'LF'))
orig = d

# (caminho, segundos, taxa efetiva medida)
CERTOS = [
    ('repolho/shorts-chucrute-30s-en', '30.0', '29.6'),
    ('repolho/shorts-repolho-maos-canva-en', '52.0', '29.9'),
    ('beterraba/shorts-beterraba-svg-puro-en', '44.0', '30.0'),
    ('couve-flor/shorts-couveflor-animado-en', '43.5', '29.8'),
    ('rabanete/shorts-rabanete-animado-en', '40.5', '29.8'),
    ('beterraba/shorts-beterraba-couve-en', '52.0', '29.8'),
    ('guia-geral/shorts-5-easiest-en', '49.0', '29.9'),
    ('cores/shorts-3-colors-en', '53.5', '29.9'),
]

TROCAS = []
for caminho, seg, fps in CERTOS:
    velho = ('**The .mp4 is already rendered:** `%s.mp4`\n'
             '(1080x1920 vertical, H.264, %s s, constant 30 fps) - no screen recording needed.\n'
             % (caminho, seg))
    novo = ('**The .mp4 is already rendered:** `%s.mp4`\n'
            '(1080x1920 vertical, H.264, %s s, constant %s fps) - no screen recording needed.\n'
            % (caminho, seg, fps))
    TROCAS.append((velho, novo))

for i, (velho, novo) in enumerate(TROCAS, 1):
    v = velho.replace('\n', nl)
    nv = novo.replace('\n', nl)
    n = d.count(v)
    print('troca %d: casou %d vez(es)  <- %s' % (i, n, velho.split('/')[-1][:40]))
    if n != 1:
        print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
        sys.exit(1)
    d = d.replace(v, nv, 1)

assert d != orig
open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %s (%d -> %d bytes)' % (ARQ, len(orig), len(d)))

"""_consertar-tag-cena.py — tira o "undefined" que sai QUEIMADO no video.

O que aconteceu: o motor de gravacao desenha `s.tag` no rotulo do topo da cena. Os
dois arquivos do `shorts-chucrute-30s` nunca tiveram esse campo (nem o EN nem o PT),
entao o video saiu com a palavra **undefined** escrita em cima de todas as 5 cenas —
e nem o `_validar-short.py` nem o proprio short podiam ver isso, porque quem escreve
o rotulo e' o motor.

Duas correcoes, de proposito:

  1. O SHORT ganha o `tag` que faltava, seguindo a convencao da serie:
     EN "SAUERKRAUT n / 5" (igual ao `shorts-repolho-maos-canva-en`),
     PT "CHUCRUTE n / 5"    (igual ao `shorts-repolho-maos-canva`).
  2. O MOTOR passa a NAO desenhar o rotulo quando o campo nao existe. Assim um short
     novo que esqueca o `tag` sai sem rotulo — feio, mas nao sai escrito "undefined".

Onze ancoras contadas (5 + 5 + 1). Aborta sem gravar se alguma nao casar uma vez.
"""
import sys

TROCAS = []
for arq, nome in [('repolho/shorts-chucrute-30s-en.html', 'SAUERKRAUT'),
                  ('repolho/shorts-chucrute-30s.html', 'CHUCRUTE')]:
    for n in range(5):
        TROCAS.append((arq,
                       "{ id:'s%d', ms:6000, cap:" % n,
                       "{ id:'s%d', ms:6000, tag:'%s %d / 5', cap:" % (n, nome, n + 1)))

TROCAS.append((
    '_mp4/render.js',
    """            '<text x="202" y="31" text-anchor="middle" font-size="10" font-weight="800" ' +
            'fill="#2c2c2a" opacity=".5" letter-spacing="2" ' + F + '>' + esc(s.tag) + '</text>';
""",
    """            /* Sem o campo `tag` o rotulo sairia escrito "undefined" no video. Nao
               desenhar nada e' feio; "undefined" e' defeito. */
            (s.tag ?
              '<text x="202" y="31" text-anchor="middle" font-size="10" font-weight="800" ' +
              'fill="#2c2c2a" opacity=".5" letter-spacing="2" ' + F + '>' + esc(s.tag) + '</text>'
              : '');
"""))

POR_ARQ = {}
for arq, velho, novo in TROCAS:
    POR_ARQ.setdefault(arq, []).append((velho, novo))

falhou = False
for arq, pares in POR_ARQ.items():
    d = open(arq, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in d else '\n'
    print('%s (fim de linha %s)' % (arq, 'CRLF' if nl == '\r\n' else 'LF'))
    orig = d
    for i, (velho, novo) in enumerate(pares, 1):
        v = velho.replace('\n', nl)
        nv = novo.replace('\n', nl)
        n = d.count(v)
        print('  troca %2d: casou %d vez(es)  <- %s' % (i, n, velho.split('\n')[0][:52]))
        if n != 1:
            print('  ABORTADO: nada foi gravado em %s' % arq)
            falhou = True
            break
        d = d.replace(v, nv, 1)
    if falhou:
        continue
    assert d != orig
    open(arq, 'w', encoding='utf-8', newline='').write(d)
    print('  gravado: %d -> %d bytes' % (len(orig), len(d)))

sys.exit(1 if falhou else 0)

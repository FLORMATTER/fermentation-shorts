# -*- coding: utf-8 -*-
"""
_consertar-rotulos-en.py — dois bugs reais nos shorts em ingles.

BUG A — 73 rotulos de topo em portugues.
  O rotulo do topo (`.tag`, o `tag:` do array `scenes`) fica VISIVEL na tela
  durante o video inteiro. Em 12 arquivos `-en.html`, a cena 1 esta em ingles e
  as cenas 2 em diante ficaram em portugues: `CENA 2 / 7`, `BETERRABA + COUVE 3 / 8`,
  `CEBOLA+BETERRABA 4 / 8`... O prefixo ingles da propria cena 1 de cada arquivo e
  a referencia do que deveria estar nas outras.

BUG B — o video da couve chama a couve de CABBAGE.
  `beterraba/shorts-beterraba-couve-en.html` diz CABBAGE em 16 strings visiveis,
  mas o desenho e COUVE (kale): o gradiente se chama `kaleLeaf2` e o texto fala de
  "THICK STALK". O pacote do YouTube (entrada #8) diz KALE, e CABBAGE ja e o nome
  do repolho (`Repolho -> CABBAGE` no README). Dois videos diferentes dizendo
  CABBAGE e exatamente a confusao que a regra "um legume por rodada" evita.

Uso:
    python _consertar-rotulos-en.py            # dry-run
    python _consertar-rotulos-en.py --apply
"""
import io
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

# ── BUG A: (arquivo, prefixo PT, prefixo EN, quantas vezes) ─────────────────
ROTULOS = [
    ('beterraba/shorts-beterraba-animado-en.html',    "tag:'CENA ",               "tag:'SCENE ",       6),
    ('beterraba/shorts-beterraba-camadas-en.html',    "tag:'CENA ",               "tag:'SCENE ",       5),
    ('beterraba/shorts-beterraba-couve-en.html',      "tag:'BETERRABA + COUVE ",  "tag:'BEET + KALE ", 7),
    ('beterraba/shorts-beterraba-melancia-en.html',   "tag:'CENA ",               "tag:'SCENE ",       6),
    ('beterraba/shorts-beterraba-svg-puro-en.html',   "tag:'BETERRABA ",          "tag:'BEET ",        6),
    ('cebola/shorts-cebola-beterraba-en.html',        "tag:'CEBOLA+BETERRABA ",   "tag:'ONION+BEET ",  7),
    ('cenoura/shorts-cenoura-animado-en.html',        "tag:'CENA ",               "tag:'SCENE ",       6),
    ('couve-flor/shorts-couveflor-animado-en.html',   "tag:'COUVE-FLOR ",         "tag:'CAULIFLOWER ", 6),
    ('pepino/shorts-pepino-speed-en.html',            "tag:'CENA ",               "tag:'SCENE ",       6),
    ('rabanete/shorts-rabanete-animado-en.html',      "tag:'RABANETE ",           "tag:'RADISH ",      6),
    ('repolho/shorts-repolho-animado-en.html',        "tag:'CENA ",               "tag:'SCENE ",       5),
    ('repolho/shorts-repolho-maos-canva-en.html',     "tag:'CHUCRUTE ",           "tag:'SAUERKRAUT ",  7),
]

# ── BUG B: couve (kale) chamada de CABBAGE ──────────────────────────────────
# A ordem importa: CABBAGE (9) -> KALE, depois Cabbage (1) -> Kale,
# depois cabbage (6) -> kale.
COUVE_ARQ = 'beterraba/shorts-beterraba-couve-en.html'
COUVE_TROCAS = [
    ('CABBAGE', 'KALE', 9),
    ('Cabbage', 'Kale', 1),
    ('cabbage', 'kale', 6),
]


def ler(p):
    bruto = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in bruto else '\n'
    return bruto.replace('\r\n', '\n'), nl


def gravar(p, d, nl):
    saida = d if nl == '\n' else d.replace('\n', nl)
    io.open(p, 'w', encoding='utf-8', newline='').write(saida)


def troca(d, velho, novo, n):
    c = d.count(velho)
    assert c == n, '%d ocorrencia(s) de %r, esperado %d' % (c, velho, n)
    return d.replace(velho, novo, n)


def main():
    aplicar = '--apply' in sys.argv
    total = 0
    falhas = []

    # ── BUG A ──
    print('── BUG A: rotulos de topo em portugues ──')
    for rel, velho, novo, n in ROTULOS:
        p = os.path.join(RAIZ, rel.replace('/', os.sep))
        if not os.path.exists(p):
            print('  FALTA  %s' % rel)
            falhas.append(rel)
            continue
        d, nl = ler(p)
        try:
            d2 = troca(d, velho, novo, n)
        except AssertionError as e:
            print('  ABORTOU %s\n     %s' % (rel, e))
            falhas.append(rel)
            continue
        print('  %-52s %-24s -> %s  (%d)' % (os.path.basename(rel), velho[5:],
                                             novo[5:], n))
        total += n
        if aplicar:
            bk = p + '.antes-do-tag'
            if not os.path.exists(bk):
                shutil.copy2(p, bk)
            gravar(p, d2, nl)

    # ── BUG B ──
    print('\n── BUG B: couve chamada de CABBAGE ──')
    p = os.path.join(RAIZ, COUVE_ARQ.replace('/', os.sep))
    if os.path.exists(p):
        d, nl = ler(p)
        try:
            for velho, novo, n in COUVE_TROCAS:
                d = troca(d, velho, novo, n)
                print('  %-20s -> %-20s (%d)' % (velho, novo, n))
                total += n
            if aplicar:
                bk = p + '.antes-do-kale'
                if not os.path.exists(bk):
                    shutil.copy2(p, bk)
                gravar(p, d, nl)
        except AssertionError as e:
            print('  ABORTOU %s\n     %s' % (COUVE_ARQ, e))
            falhas.append(COUVE_ARQ)
    else:
        print('  FALTA  %s' % COUVE_ARQ)

    print()
    if falhas:
        print('PAROU COM PENDENCIA em %d arquivo(s): %s' % (len(falhas), falhas))
        return 1
    if aplicar:
        print('OK — %d trocas aplicadas' % total)
    else:
        print('DRY-RUN — %d trocas prontas. Rode com --apply.' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
_registrar-couveflor-maca-plano.py — Semana 12 no plano de postagem.

Contagem do topo sobe (20 videos, 42 arquivos de conteudo — medido).

A nota da Semana 12 avisa que a couve-flor ja' apareceu no #5 e diz o que fazer
para nao parecer o mesmo video.
"""
import io
import sys

ARQ = 'guias/plano-de-postagem.md'

SEMANA = """### Semana 12 — o cheiro da couve-flor
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Couve-flor + maçã ⚠️ | `couve-flor/shorts-cauliflower-apple-en.html` | **#20** | `IT WILL NOT SMELL` |

**Couve-flor pela SEGUNDA vez** (#5). O que a salva é que ela não repete nada do #5: lá é
floretes, quebrar com a mão, 2,5% de sal, massagem e 7–10 dias; **aqui é a maçã como starter
e a química do enxofre** — glucosinolatos → mirosinase → H₂S, com o **pH regulando a enzima**.

**Poste depois do #5 e em outra semana.** Sozinha, parece o mesmo legume duas vezes — e a
capa do #5 (`IT'S NOT 2%. IT'S 2.5%`) e a desta (`IT WILL NOT SMELL`) já são diferentes o
bastante para não competirem no mesmo dia.

A partir daqui o ritmo é o mesmo: **um vídeo por post**, sempre nos mesmos dois dias da
semana. O 20º é a couve-flor com maçã — o primeiro da série que explica o CHEIRO, e não a
receita.
"""

ANCORAS = [
    (
        'contagem do topo',
        '## ⚠️ Antes de tudo: você tem 19 vídeos, não 41 arquivos',
        '## ⚠️ Antes de tudo: você tem 20 vídeos, não 42 arquivos',
    ),
    (
        'titulo das semanas',
        '## 📅 As 11 semanas',
        '## 📅 As 12 semanas',
    ),
    (
        'Semana 12 + fechamento',
        'A partir daqui o ritmo é o mesmo: **um vídeo por post**, sempre nos mesmos dois dias da\n'
        'semana. O 19º é a beterraba com alho — o primeiro da série em que o legume principal é\n'
        'coadjuvante.',
        SEMANA,
    ),
]


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))
    eol = '\r\n' if crlf else '\n'

    falhou = False
    for rotulo, velho, novo in ANCORAS:
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        q = d.count(v)
        print('%-28s casou %d vez(es)' % (rotulo, q))
        if q != 1:
            falhou = True
            continue
        d = d.replace(v, n, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    with io.open(ARQ + '.antes-do-20', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %s (backup .antes-do-20)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())

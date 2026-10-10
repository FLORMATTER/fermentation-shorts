# -*- coding: utf-8 -*-
"""
_registrar-beterraba-alho-plano.py — Semana 11 no plano de postagem.

O arquivo tinha 9 semanas quando foi escrito pela primeira vez ("As 8 semanas"),
depois 10. Agora 11. A contagem do topo tambem sobe (19 videos, 41 arquivos de
conteudo — medido, nao chutado).

A nota da Semana 11 avisa que esta e' a QUARTA beterraba e diz o que fazer para
o feed nao mostrar tres potes roxos na mesma semana.
"""
import io
import sys

ARQ = 'guias/plano-de-postagem.md'

SEMANA = """### Semana 11 — beterraba e alho, em camadas
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Beterraba + alho ⚠️ | `beterraba/shorts-beet-garlic-en-1080x1920.html` | **#19** | `LAYER IT, DO NOT MIX IT` |

**Esta é a QUARTA beterraba** (#3 pura, #4 com melancia, #8 com couve). O que a salva é
que o assunto não é a beterraba — é o **alho**: a alicina que arde crua e vira doce em
duas semanas, e a regra de **camadas em vez de mistura**. A beterraba entra como tinta:
a **betalaina** sai dela e pinta o alho de roxo.

**Por isso: espalhe.** Não poste esta perto do #3 nem do #8. Três potes de beterraba na
mesma semana é exatamente o padrão que o YouTube chama de conteúdo em massa — e a
substância aqui é diferente, mas a **capa** não é.

A partir daqui o ritmo é o mesmo: **um vídeo por post**, sempre nos mesmos dois dias da
semana. O 19º é a beterraba com alho — o primeiro da série em que o legume principal é
coadjuvante.
"""

ANCORAS = [
    (
        'contagem do topo',
        '## ⚠️ Antes de tudo: você tem 18 vídeos, não 40 arquivos',
        '## ⚠️ Antes de tudo: você tem 19 vídeos, não 41 arquivos',
    ),
    (
        'titulo das semanas',
        '## 📅 As 10 semanas',
        '## 📅 As 11 semanas',
    ),
    (
        'Semana 11 + fechamento',
        'A partir daqui o ritmo é o mesmo: **um vídeo por post**, sempre nos mesmos dois dias da\n'
        'semana. O 18º é a cenoura com maçã — o primeiro da série que encosta no assunto\n'
        '"álcool" de propósito.',
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

    with io.open(ARQ + '.antes-do-19', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %s (backup .antes-do-19)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())

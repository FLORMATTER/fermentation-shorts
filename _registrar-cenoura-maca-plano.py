# -*- coding: utf-8 -*-
"""
_registrar-cenoura-maca-plano.py — poe o video novo no plano de postagem.

Tres coisas:
  1. a contagem do topo (15 -> 18 videos; 37 -> 40 arquivos de conteudo, medido)
  2. "As 8 semanas" -> "As 10 semanas" (o titulo ja' estava errado: o arquivo
     tinha 9 semanas; agora tem 10)
  3. a Semana 10 com a cenoura + maca, e a frase de fechamento que dizia
     "O 15o e' o brocolis com laranja" — estava obsoleta.

Ponto delicado: a cenoura ja' existe no #12. O plano proibe repetir legume. A
nota da Semana 10 explica por que o #18 nao e' repeticao e obriga a ordem
(#12 antes). Sem isso o plano se contradiz.
"""
import io
import sys

ARQ = 'guias/plano-de-postagem.md'

SEMANA = """### Semana 10 — o que o açúcar faz num legume denso
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Cenoura + maçã ⚠️ | `cenoura/shorts-carrot-apple-en.html` | **#18** | `THE APPLE MAKES IT FIZZY` |

O #18 **é legume repetido** — a cenoura já apareceu no #12. Postar assim mesmo, mas
**só depois do #12**, e a diferença é de substância, não de estilo: o #12 ensina a
cenoura sozinha (5 a 7 dias, crocante, sem gás); este responde o que muda quando entra
açúcar — 4 a 5 dias, jarro com gás, e o aviso de que fermentação de fruta chega a
**0,5–2% de álcool**. Sem o #12 antes, o #18 vira "a mesma cenoura duas vezes".

A partir daqui o ritmo é o mesmo: **um vídeo por post**, sempre nos mesmos dois dias da
semana. O 18º é a cenoura com maçã — o primeiro da série que encosta no assunto
"álcool" de propósito.
"""

ANCORAS = [
    (
        'contagem do topo',
        '## ⚠️ Antes de tudo: você tem 15 vídeos, não 37',
        '## ⚠️ Antes de tudo: você tem 18 vídeos, não 40 arquivos',
    ),
    (
        'titulo das semanas',
        '## 📅 As 8 semanas',
        '## 📅 As 10 semanas',
    ),
    (
        'Semana 10 + fechamento',
        'O #17 **continua** o vídeo do pepino (#6): o primeiro ensina a folha de louro, este\n'
        'desmonta a ideia de que a maçã é o que segura a crocância. Postar depois do #6.\n\n'
        'A partir daqui o ritmo é o mesmo: **um legume novo por post**, sempre nos mesmos\n'
        'dois dias da semana. O 15º é o brócolis com laranja.',
        'O #17 **continua** o vídeo do pepino (#6): o primeiro ensina a folha de louro, este\n'
        'desmonta a ideia de que a maçã é o que segura a crocância. Postar depois do #6.\n\n'
        + SEMANA,
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
        quantos = d.count(v)
        print('%-26s casou %d vez(es)' % (rotulo, quantos))
        if quantos != 1:
            falhou = True
            continue
        d = d.replace(v, n, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    with io.open(ARQ + '.antes-do-18', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())

    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)

    print('\ngravado: %s (backup .antes-do-18)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())

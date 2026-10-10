"""_adicionar-pepino-maca-indices.py — README + plano de postagem ganham o #17.

    python _adicionar-pepino-maca-indices.py

Contagem exata em cada ancora; aborta sem gravar se alguma nao casar 1 vez.
"""
import sys

TROCAS = [
    ('README.md', [
        ("| `pepino/` | 1 short | |",
         "| `pepino/` | 2 shorts | Pepino (o mais rápido da série) e pepino + maçã — nº 17 |"),
    ]),
    ('guias/plano-de-postagem.md', [
        ("""| 1 | Brócolis + laranja | `brocolis/shorts-broccoli-orange-en.html` | **#15** | `IT WILL SMELL LIKE SULFUR` |

A partir daqui""",
         """| 1 | Brócolis + laranja | `brocolis/shorts-broccoli-orange-en.html` | **#15** | `IT WILL SMELL LIKE SULFUR` |

### Semana 9 — o açúcar não é tanino
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Pepino + maçã | `pepino/shorts-pepino-apple-en.html` | **#17** | `SUGAR IS NOT TANNIN` |

O #17 **continua** o vídeo do pepino (#6): o primeiro ensina a folha de louro, este
desmonta a ideia de que a maçã é o que segura a crocância. Postar depois do #6.

A partir daqui"""),
    ]),
]


def main():
    for arq, trocas in TROCAS:
        d = open(arq, encoding='utf-8', newline='').read()
        nl = '\r\n' if '\r\n' in d else '\n'
        print('%s (fim de linha %s)' % (arq, 'CRLF' if nl == '\r\n' else 'LF'))
        orig = d
        for i, (velho, novo) in enumerate(trocas, 1):
            v = velho.replace('\n', nl)
            nv = novo.replace('\n', nl)
            n = d.count(v)
            print('  troca %d: casou %d vez(es)' % (i, n))
            if n != 1:
                print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
                return 1
            d = d.replace(v, nv, 1)
        assert d != orig
        open(arq, 'w', encoding='utf-8', newline='').write(d)
        print('  gravado (%d -> %d bytes)' % (len(orig), len(d)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

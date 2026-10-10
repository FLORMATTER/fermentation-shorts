# -*- coding: utf-8 -*-
"""_memoria-28.py — sobe os contadores do MEMORY.md do projeto para 28.

O MEMORY.md vive no teto (3.000 chars), entao aqui so' entram CONTADORES. O
detalhe tecnico das armadilhas do #28 vai para a skill, que e' onde o proprio
cabecalho do arquivo diz que ele mora.

Uso:  python _memoria-28.py            # dry-run
      python _memoria-28.py --apply
"""
import io
import sys

ALVO = '.workbuddy-ai/memory/MEMORY.md'

TRABALHO = [
    ('## 📊 Catálogo — 27 entradas', '## 📊 Catálogo — 28 entradas'),
    ('**#22–#27 são só EN**', '**#22–#28 são só EN**'),
    ('`guias/plano-de-postagem.md` (17 semanas)', '`guias/plano-de-postagem.md` (18 semanas)'),
    ('**Com mp4: 26 dos 27.**', '**Com mp4: 27 dos 28.**'),
    ('de #22–#27.', 'de #22–#28.'),
]


def main():
    aplicar = '--apply' in sys.argv
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d)

    for velho, novo in TRABALHO:
        n = d.count(velho)
        print('  %-46s %d vez(es)  ->  %s' % (velho[:46], n, novo[:34]))
        if n != 1:
            print('ABORTA: ancora casou %d vez(es), esperava 1.' % n)
            return 1
    for velho, novo in TRABALHO:
        d = d.replace(velho, novo, 1)

    for trecho in ('28 entradas', '#22–#28', '18 semanas', '27 dos 28', 'de #22–#28.'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" depois da troca.' % trecho)
            return 1
    if '27 entradas' in d or '26 dos 27' in d:
        print('ABORTA: contador velho ainda no arquivo.')
        return 1

    print('  %s %d -> %d chars' % (ALVO, antes, len(d)))
    if len(d) > 3000:
        print('ABORTA: passou do teto de 3.000 chars (%d).' % len(d))
        return 1
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: MEMORY.md em 28.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

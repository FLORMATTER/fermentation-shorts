# -*- coding: utf-8 -*-
"""_analisar-keyframes.py — DIAGNOSTICO (nao altera nada).

Para cada arquivo que o `_validar-short.py` acusa de "@keyframes nunca usado",
diz se o nome do keyframe aparece em ALGUM outro lugar do arquivo alem da propria
definicao. Se nao aparecer, e' codigo morto e a remocao e' segura; se aparecer, o
validador esta' dando falso positivo (o JS pode aplicar a animacao por
`style.animation`, que o validador nao ve).

    python _analisar-keyframes.py
"""
import io
import os
import re
import sys

IGNORAR_PASTAS = ('.workbuddy-ai', '_revisao', 'node_modules', '_arquivo')


def arquivos():
    fora = []
    for base, dirs, nomes in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
        for n in nomes:
            if n.endswith('.html'):
                fora.append(os.path.join(base, n).replace('\\', '/').lstrip('./'))
    return sorted(fora)


def main():
    total_orf = 0
    seguros = []
    suspeitos = []
    for arq in arquivos():
        with io.open(arq, 'r', encoding='utf-8', newline='') as fh:
            d = fh.read()
        defs = set(re.findall(r'@keyframes\s+([\w-]+)', d))
        usados = set(re.findall(r'animation:\s*([\w-]+)', d))
        # tambem conta `animation-name:` e qualquer citacao em string do JS
        usados |= set(re.findall(r'animation-name:\s*([\w-]+)', d))
        orfaos = defs - usados
        if not orfaos:
            continue
        total_orf += len(orfaos)
        for kf in sorted(orfaos):
            # quantas vezes o nome aparece no arquivo, FORA da definicao?
            ocorr = len(re.findall(r'\b%s\b' % re.escape(kf), d))
            # 1 = so' a definicao. >1 = alguem cita (JS, comentario, style inline)
            if ocorr == 1:
                seguros.append((arq, kf))
            else:
                suspeitos.append((arq, kf, ocorr))
        print('%-58s %d orfao(s): %s' % (arq, len(orfaos), sorted(orfaos)))

    print()
    print('=' * 74)
    print('arquivos com orfao : %d' % len({a for a, _ in seguros + [(s[0], s[1]) for s in suspeitos]}))
    print('keyframes orfaos   : %d' % total_orf)
    print('  so a definicao   : %d  <- remocao SEGURA' % len(seguros))
    print('  citado em outro  : %d  <- CONFERIR a mao' % len(suspeitos))
    if suspeitos:
        print()
        print('CITADOS EM OUTRO LUGAR (nao remover sem olhar):')
        for arq, kf, n in suspeitos:
            print('  %-52s %-16s %dx' % (arq, kf, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())

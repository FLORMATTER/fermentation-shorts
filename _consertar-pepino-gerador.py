# -*- coding: utf-8 -*-
"""_consertar-pepino-gerador.py — conserta a sintaxe do `_criar-pepino-alho.py`.

O gerador foi convertido de formatacao `%` para `.replace()` com tokens, e a
conversao deixou o `)` de fechamento do `''' % (...)` orfao:

    return '''...'''
    ).replace('@D1@', ...)          <- SyntaxError: unmatched ')'

O conserto e' ESTRUTURAL, nao textual: toda linha que comeca com `).replace(`
e' juntada na linha anterior, sem o `)` inicial.

E o `%%` das strings virou literal (nao ha mais formatacao `%`), entao volta a `%`.

    python _consertar-pepino-gerador.py

Aborta SEM GRAVAR se a contagem nao bater ou se o resultado nao compilar.
"""
import io
import sys

ALVO = '_criar-pepino-alho.py'
ESPERA_JUNTAR = 5   # s0, s1, s2, s3, s6
ESPERA_PCT = 3      # 2%%, 3.5-5%%, 96%%


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    print('%s: %d bytes, %s' % (ALVO, len(d.encode('utf-8')),
                                'CRLF' if eol == '\r\n' else 'LF'))

    linhas = d.split(eol)
    saida = []
    juntou = 0
    for ln in linhas:
        s = ln.lstrip()
        if s.startswith(').replace(') and saida:
            saida[-1] = saida[-1] + s[1:]
            juntou += 1
            continue
        saida.append(ln)
    d2 = eol.join(saida)

    pct = d2.count('%%')
    d2 = d2.replace('%%', '%')

    if juntou != ESPERA_JUNTAR:
        print('ERRO: juntei %d linhas (esperado %d)' % (juntou, ESPERA_JUNTAR))
        return 1
    if pct != ESPERA_PCT:
        print('ERRO: achei %d "%%%%" (esperado %d)' % (pct, ESPERA_PCT))
        return 1

    # prova real: o Python tem de compilar o resultado
    try:
        compile(d2, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila ainda: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d2)
    print('OK: %d linhas juntadas | %d "%%%%"->"%%" | compila | %d bytes'
          % (juntou, pct, len(d2.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

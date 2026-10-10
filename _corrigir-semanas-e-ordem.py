# -*- coding: utf-8 -*-
"""_corrigir-semanas-e-ordem.py — dois consertos no registro de ontem/hoje.

1. Eu escrevi **"As 15 semanas"** no plano, mas com a Semana 14 o plano tem **14**.
   Contagem errada por copiar o número da tabela do PACOTE (que numera diferente).
2. As entradas #18, #19 e #20 do pacote têm **nota de ordenação** ("poste o #12
   primeiro") porque repetem legume. O #22 (pepino pela 3a vez) e o #23 (melancia
   2a, maçã 3a) ficaram sem essa nota — é a defesa contra "conteúdo inautêntico".

    python _corrigir-semanas-e-ordem.py
"""
import io
import sys

PLANO = 'guias/plano-de-postagem.md'
PACOTE = 'guias/pacote-legendas-descricoes-en.md'

NOTA_22 = '''
**Order matters: post #6 and #17 first, and never in the same week.** This is the third
cucumber in the series. What makes it a different video is the **garlic**, not the cucumber
- but if the feed shows three cucumber jars in one week, the pattern reads as mass-produced
even though the content is not.'''

NOTA_23 = '''
**Spread it out.** Watermelon already appears in #4, and apple in #18 and #20. Post this one
**weeks away from those three**. What makes it new is that it is the first **drink** in the
series - that is the hook, not the fruit.'''

ANCORA_22 = ('> This one was **built in English** - there is no Portuguese original. The subject '
             'is the\n> garlic, not the cucumber: cucumber already appears in #6 (the bay leaf) '
             'and #17 (the\n> apple), so this entry deliberately does not repeat either of those '
             'tricks.')

ANCORA_23 = ('> ⚠️ **Pressure warning.** Unlike every other entry, this one can make a mess. '
             'Keep the\n> "open it once a day" line in the description - it is the safety note, '
             'not filler.')

ANCORA_PLANO_ORDEM = ('**O pepino volta pela terceira vez** (#6 e #17) — e por isso o assunto '
                      'aqui **não é o\npepino, é o alho**.')

NOVO_PLANO_ORDEM = (ANCORA_PLANO_ORDEM + ' **Poste depois do #6 e do #17, e em outra semana** — '
                    'três\npotes de pepino na mesma semana leem como linha de produção, mesmo o '
                    'conteúdo sendo\ndiferente. O kombucha, pelo mesmo motivo, fica **longe do #4, '
                    'do #18 e do #20**.')

TROCAS = [
    (PLANO, '## 📅 As 15 semanas', '## 📅 As 14 semanas', 1),
    (PLANO, ANCORA_PLANO_ORDEM, NOVO_PLANO_ORDEM, 1),
    (PACOTE, ANCORA_22, ANCORA_22 + '\n' + NOTA_22, 1),
    (PACOTE, ANCORA_23, ANCORA_23 + '\n' + NOTA_23, 1),
]


def main():
    cache = {}
    for caminho in (PLANO, PACOTE):
        with io.open(caminho, 'r', encoding='utf-8', newline='') as fh:
            cache[caminho] = fh.read()

    for caminho, velho, novo, esperado in TROCAS:
        d = cache[caminho]
        eol = '\r\n' if d.count('\r\n') else '\n'
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        c = d.count(v)
        if c != esperado:
            print('ERRO em %s: ancora casou %d (esperado %d): %r'
                  % (caminho, c, esperado, velho[:60]))
            print('NADA FOI GRAVADO.')
            return 1
        cache[caminho] = d.replace(v, n)
        print('  ok: %s  <- %r' % (caminho, velho[:45]))

    for caminho, d in cache.items():
        with io.open(caminho, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d)
        print('  gravado: %s (%d bytes)' % (caminho, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

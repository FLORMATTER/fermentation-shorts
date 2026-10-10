# -*- coding: utf-8 -*-
"""_atualizar-memoria-pao.py — MEMORY.md do projeto: 20 -> 21 entradas, originais PT prontos.

    python _atualizar-memoria-pao.py

O que muda e por que:
  A. catálogo 20 -> 21 e "sem original PT" -> "todos com PT" (#18/#19/#20 foram criados);
  B. mp4 "19 dos 20" -> "20 dos 21" (o #21 saiu);
  C. plano "12 semanas" -> "13 semanas";
  D. duas lições novas: conserto tem de VOLTAR para o gerador; botão não é texto extraível;
  E. "Resolvidos": contagem do idioma (20 pares / 16 limpos / 6 benignas);
  F. sai a pendência "não têm original PT".

Ancoras contadas, aborta SEM GRAVAR.
"""
import io
import sys

ALVO = '.workbuddy-ai/memory/MEMORY.md'

TROCAS = [
    # ---------------------------------------------------------------- A
    ('catalogo 20 -> 21',
     '## 📊 Catálogo — 20 entradas no pacote\n'
     '\n'
     'A numeração é a da tabela "WHICH FILE TO RECORD" de\n'
     '`guias/pacote-legendas-descricoes-en.md` — **#1 a #20**. Fora dela só existem',
     '## 📊 Catálogo — 21 entradas no pacote\n'
     '\n'
     'A numeração é a da tabela "WHICH FILE TO RECORD" de\n'
     '`guias/pacote-legendas-descricoes-en.md` — **#1 a #21**. Fora dela só existem', 1),

    ('entradas recentes + PT',
     '**#17** pepino+maçã (**tem** PT) · **#18** cenoura+maçã · **#19** beterraba+alho ·\n'
     '**#20** couve-flor+maçã. As três últimas **nasceram em inglês — sem original PT**.',
     '**#17** pepino+maçã · **#18** cenoura+maçã · **#19** beterraba+alho ·\n'
     '**#20** couve-flor+maçã · **#21** pão/levain (`pao/`, o **1º não-legume** da série).\n'
     '**Todos com original PT** — a série é original PT + irmão `-en`.\n'
     '\n'
     '**Regra do `-en` que já custou erro:** o PT **preserva o sufixo** — o par do\n'
     '`beterraba/shorts-beet-garlic-en-1080x1920.html` é `.../shorts-beet-garlic-1080x1920.html`\n'
     '(tira só o `-en`). É assim que o `_sobras-vs-original.py` pareia.', 1),

    # ---------------------------------------------------------------- C
    ('plano 12 -> 13 semanas',
     'Plano em `guias/plano-de-postagem.md` (**12 semanas**);',
     'Plano em `guias/plano-de-postagem.md` (**13 semanas**);', 1),

    # ---------------------------------------------------------------- B
    ('mp4 19/20 -> 20/21',
     '- **Com mp4 — 19 dos 20.** Falta só o **#13**',
     '- **Com mp4 — 20 dos 21.** Falta só o **#13**', 1),

    # ---------------------------------------------------------------- D
    ('licoes novas (gerador / botao)',
     '- **A galeria fica velha:** `_gerar-galeria.py` depois de criar/consertar qualquer short.\n'
     '\n'
     '## ✅ Resolvidos (não reabrir)',
     '- **A galeria fica velha:** `_gerar-galeria.py` depois de criar/consertar qualquer short.\n'
     '- **Conserto feito por script separado tem de VOLTAR para o gerador** — senão regerar o\n'
     '  short desfaz o conserto (`CONTRASTE` no `_criar-pao.py`). O gerador é a fonte da verdade.\n'
     '- **Botão não é texto extraível** — `⏸ Pause` não está em `cap:`/`sub:` nem é nó de texto\n'
     '  do corpo, então o extrator **não o vê**; quem pega é **comparar os dois arquivos**\n'
     '  (`_sobras-vs-original.py`).\n'
     '- **String que é PREFIXO de duas entradas** casa 2 vezes: a nota "no Portuguese original"\n'
     '  servia ao #18 **e** ao #20 — a âncora do #20 precisou do contexto de baixo.\n'
     '\n'
     '## ✅ Resolvidos (não reabrir)', 1),

    # ---------------------------------------------------------------- E
    ('resolvidos: idioma',
     'legado). Idioma: **16 pares PT/EN limpos, 0 strings sobradas** (`_sobras-vs-original.py`).',
     'legado). Idioma: **20 pares, 16 limpos, 0 tradução faltando** — as 6 "sobras" são\n'
     '**benignas** (`?play`, `@yourhandle`, `@yourchannel` ×3 = placeholder igual nos dois\n'
     'idiomas; `🍞 + LEVAIN` = "levain" é a mesma palavra).', 1),

    # ---------------------------------------------------------------- F
    ('sai a pendencia do PT',
     '- **#18, #19 e #20 não têm original PT** — nasceram em inglês (19/09).\n'
     '- **3 variantes de estilo sem mp4** — oferecido, não aprovado.',
     '- **3 variantes de estilo sem mp4** — oferecido, não aprovado.', 1),
]


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    antes = len(d.encode('utf-8'))
    print('%s (%d bytes, %s)\n' % (ALVO, antes, 'CRLF' if eol == '\r\n' else 'LF'))

    for i, (rotulo, velho, novo, esperado) in enumerate(TROCAS, 1):
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        c = d.count(v)
        if c != esperado:
            print('  %d. %-32s casou %d (esperado %d)  ERRO' % (i, rotulo, c, esperado))
            print('\nABORTADO — nada foi gravado.')
            return 1
        d = d.replace(v, n)
        print('  %d. %-32s ok (%d)' % (i, rotulo, c))

    # provas
    provas = [
        ('21 entradas', '## 📊 Catálogo — 21 entradas no pacote' in d),
        ('#1 a #21', '**#1 a #21**' in d),
        ('20 dos 21', '20 dos 21' in d),
        ('13 semanas', '**13 semanas**' in d),
        ('sem pendencia PT', 'não têm original PT' not in d),
        ('sem "19 dos 20"', '19 dos 20' not in d),
        ('sem "12 semanas"', '**12 semanas**' not in d),
        ('sem "16 pares PT/EN limpos"', '16 pares PT/EN limpos' not in d),
    ]
    ruins = [n for n, ok in provas if not ok]
    if ruins:
        print('\nABORTADO — prova falhou: %s' % ruins)
        return 1
    print('\n  provas: %d/%d ok' % (len(provas), len(provas)))

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('  gravado: %d -> %d bytes' % (antes, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

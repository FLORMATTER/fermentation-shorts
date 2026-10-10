# -*- coding: utf-8 -*-
"""
_skill-beterraba-alho.py — tres correcoes na skill, num arquivo so'.

1. erro (k): a barra de legenda do mp4 pode repetir o titulo que ja' esta na cena.
2. o filtro do lote escondia video (a regra do `-1080x1920`).
3. a linha "o render de verdade leva ~4,5 min" esta' OBSOLETA — com `--passo=60`
   sao ~2 min para 54 s de video. (A tabela antiga trocava 720 com 1080 e dizia
   4,5 min; a memoria ja' registrou o erro, a linha ficou para tras.)

Varias edicoes no MESMO arquivo: contagem exata e aborta sem gravar.
"""
import io
import sys

ARQ = r'C:\Users\Saxa\.workbuddy-ai\skills\shorts-svg-animado\SKILL.md'

ERRO_K = """**(k) 🆕 A barra de legenda pode repetir o título que já está na cena.**
O motor do mp4 (`_mp4/render.js`) desenha `s.cap` e `s.sub` numa barra escura embaixo. Se o
short **também** tem título dentro do SVG — é o caso dos shorts que nasceram como player
próprio, já no formato de upload —, a mesma frase aparece **duas vezes, em dois tamanhos**.

Achado em 19/09 no `beterraba/shorts-beet-garlic-en-1080x1920`:

| título na cena | barra queimada no mp4 |
|---|---|
| `READY IN 1 TO 2 WEEKS` | "Ready in 1 to 2 weeks" |
| `THE GARLIC MELLOWS OUT` | "The garlic mellows out" |
| `2% SALT, NOT MORE` | "2% salt, weighed" |
| `ONE LAYER AT A TIME` | "Layer it, do not mix it" |

**A divisão certa:** a **manchete** fica no título da cena; a barra carrega o **detalhe**
que o título não diz — a quantidade, o porquê, o tempo. Nunca a mesma frase.

```
título na cena : 2% SALT, NOT MORE
barra (certo)  : "20 g of salt per 1 kg" / "coarse salt - iodine stalls the ferment"
```

**Conferir é TOCAR o mp4** (`node _mp4/quadros-mp4.js <arq>.mp4 8`). Nem o
`_validar-short.py` nem o `_revisar-cenas.py` veem essa barra: ela **não existe no short**,
é injetada na gravação — o mesmo ponto cego do erro (i).

> ⚠️ Ao consertar, **provar que durações e `tag` não mudaram**. Reescrever o array `scenes`
> inteiro é fácil de errar. O `_consertar-legenda-beterraba-alho.py` compara as duas listas
> (ms e tag) e **aborta sem gravar** se divergirem — usar esse padrão.

"""

NOTA_FILTRO = """
> 🔴 **Filtro que esconde trabalho é pior que filtro nenhum.** O `_gerar-mp4.js` negava todo
> arquivo terminado em `-1080x1920.html` como "variante do mesmo vídeo". Só que o sufixo vem
> **depois** do `-en`, então a regra do `-en` (`/-en\\.html$/`) também não reconhecia o nome —
> e o arquivo era filtrado **duas vezes**. Medido: dos 2 arquivos `-1080x1920` da série,
> **nenhum tem gêmeo 405×720**; os dois são vídeos próprios
> (`beterraba/shorts-beet-garlic-en` e `repolho/shorts-sauerkraut-en`) e ficaram **sem mp4
> e fora do pacote** por 2 dias.
>
> Conserto: tirar o sufixo **antes** das outras regras, e só tratar como variante se o
> **gêmeo existir** (`fs.existsSync`). Testar o filtro contra casos que devem passar **e**
> casos que devem continuar filtrados — 7 casos, não 1.
"""

ANCORAS = [
    (
        'erro (k)',
        'e perguntar **de quem é cada cor**. Verde que era do pepino em vídeo de cenoura faz o\n'
        'short parecer re-skin — mas **a folha da cenoura continua verde**, é de propósito.\n\n'
        '## 📐 Formato de UPLOAD (1080×1920) — o short que já sai pronto',
        'e perguntar **de quem é cada cor**. Verde que era do pepino em vídeo de cenoura faz o\n'
        'short parecer re-skin — mas **a folha da cenoura continua verde**, é de propósito.\n\n'
        + ERRO_K +
        '## 📐 Formato de UPLOAD (1080×1920) — o short que já sai pronto',
    ),
    (
        'nota do filtro do lote',
        'O render de verdade leva ~4,5 min; o curto leva ~35 s. Mantém as 8 cenas (o peso de\n'
        'cada uma é o que importa) e só encurta a duração. **Apagar o teste depois** — senão um\n'
        '`--todos` futuro o pega como se fosse um short de verdade.',
        'O render de verdade leva **~2 min** para ~55 s de vídeo com `--passo=60` (a tabela antiga\n'
        'dizia 4,5 min — ver a curva do `--passo`); o curto leva ~35 s. Mantém as 8 cenas (o peso\n'
        'de cada uma é o que importa) e só encurta a duração. **Apagar o teste depois** — senão um\n'
        '`--todos` futuro o pega como se fosse um short de verdade.\n'
        + NOTA_FILTRO,
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
        print('%-24s casou %d vez(es)' % (rotulo, q))
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

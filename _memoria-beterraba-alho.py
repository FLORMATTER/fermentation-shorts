# -*- coding: utf-8 -*-
"""
_memoria-beterraba-alho.py — memoria do projeto com o video #19 (beterraba + alho).

MEMORY.md : catalogo 18 -> 19, mp4 17/18 -> 18/19, e duas regras novas
            (o filtro que escondia video, e a legenda que repetia o titulo).
log do dia: secao nova, acrescentada no fim.
"""
import io
import sys

MEM = '.workbuddy-ai/memory/MEMORY.md'
LOG = '.workbuddy-ai/memory/2026-09-19.md'

ANCORAS = [
    (
        'titulo do catalogo',
        '## 📊 Catálogo — 18 entradas no pacote',
        '## 📊 Catálogo — 19 entradas no pacote',
    ),
    (
        'entrada do #19',
        'Plano em `guias/plano-de-postagem.md`; upload em `guias/guia-de-upload.md`.',
        '**#19 — beterraba + alho** (`beterraba/shorts-beet-garlic-en-1080x1920.html`, 54 s, 8 cenas):\n'
        'não é sobre a beterraba, é sobre o **alho** — a alicina arde crua e vira doce em duas\n'
        'semanas, e a regra é **camadas em vez de mistura** (beterraba, alho, beterraba, alho).\n'
        'A beterraba entra como tinta: a **betalaina** sai dela e pinta o alho de roxo.\n'
        '**Sem original PT**, e já nasceu no formato de upload. É a **4ª beterraba** (#3, #4, #8)\n'
        '— espalhar na grade, não postar colado no #3 nem no #8.\n\n'
        'Plano em `guias/plano-de-postagem.md`; upload em `guias/guia-de-upload.md`.',
    ),
    (
        'contagem de mp4',
        '- **Com mp4 — 17 dos 18.**',
        '- **Com mp4 — 18 dos 19.**',
    ),
    (
        'regra do filtro que escondia video',
        '- **"Dá pra ver" não é medida — medir o pixel.**',
        '- **Filtro que esconde trabalho é pior que filtro nenhum.** O `_gerar-mp4.js` negava\n'
        '  todo arquivo terminado em `-1080x1920.html` como "variante do mesmo vídeo". Mas o\n'
        '  sufixo vem **depois** do `-en`, então a regra do `-en` também não o reconhecia — e\n'
        '  dois vídeos de verdade sumiram do lote: `beterraba/shorts-beet-garlic-en-1080x1920`\n'
        '  e `repolho/shorts-sauerkraut-en-1080x1920`. Agora o sufixo só marca variante se o\n'
        '  **gêmeo sem ele existir**. Ao mexer num filtro, listar o que ele esconde.\n'
        '- **A barra de legenda pode repetir o título da cena.** O motor do mp4 desenha `cap`/`sub`\n'
        '  do array `scenes`, e o short também tem títulos dentro do SVG. No #19 a barra dizia\n'
        '  `Ready in 1 to 2 weeks` embaixo do título `READY IN 1 TO 2 WEEKS` — a mesma frase duas\n'
        '  vezes, em dois tamanhos. **Só aparece ao tocar o mp4.** Regra: a barra carrega o\n'
        '  **detalhe**, o título carrega a **manchete**; nunca a mesma frase.\n'
        '- **"Dá pra ver" não é medida — medir o pixel.**',
    ),
    (
        'pendencia do PT do #19',
        '- **O #18 (cenoura + maçã) não tem original PT** — nasceu em inglês (19/09).',
        '- **O #18 (cenoura + maçã) não tem original PT** — nasceu em inglês (19/09).\n'
        '- **O #19 (beterraba + alho) não tem original PT** — idem.',
    ),
]

LOG_TEXTO = """

---

## 🧄 #19 — beterraba + alho (a quarta beterraba, e por que ela passa) — 19/09

Pedido: *"ok, de beterraba com garlic ...inglish"* (resposta em inglês).

**Descoberta: o vídeo JÁ EXISTIA.** `beterraba/shorts-beet-garlic-en-1080x1920.html` —
8 cenas, 54 s, 18 animações, `_validar-short.py` limpo, na galeria desde 17/09. Estava
**sem mp4 e fora do pacote** por causa de um bug de filtro (abaixo). Não recriei nada:
verifiquei, consertei um defeito de legenda, renderizei e registrei.

**Substância (conferida no render):** a beterraba cortada em **cunhas de 2 cm, nunca
ralada** (ralada vira papa); o alho **amassado uma vez** com o lado da lâmina (a alicina
sai no óleo — é o sabor); **camadas em vez de mistura** (beterraba, alho, beterraba,
alho), prensando a cada camada; **2% de sal = 20 g por 1 kg**, sal grosso **não iodado**
(o iodo freia a fermentação); semana 1 na bancada a 18–22 °C, tudo submerso, arrotando o
pote todo dia; semana 2 na geladeira. A cor sai da **betalaina** — o pigmento vaza da
beterraba e pinta o alho de roxo. O alho arde cru no dia 1 e está doce na semana 2.

### 🐛 Dois defeitos, nenhum deles pego pelo validador

**1. O filtro do lote escondia dois vídeos de verdade.** `_gerar-mp4.js` negava todo
arquivo terminado em `-1080x1920.html` ("variante do mesmo vídeo"). Só que o sufixo vem
**depois** do `-en` — então a regra do `-en` (`/-en\\.html$/`) também não reconhecia o
nome, e o arquivo era filtrado **duas vezes**. Medido: dos 2 arquivos `-1080x1920` da
série, **nenhum tem gêmeo 405×720** — os dois são vídeos próprios. Conserto: tirar o
sufixo **antes** das outras regras, e só tratar como variante se o **gêmeo existir**.
Testado contra 7 casos (2 próprios, 5 que devem continuar filtrados). **Filtro que
esconde trabalho é pior que filtro nenhum.**

**2. A barra de legenda repetia o título da cena.** Visto ao **tocar o mp4**:

| título na cena | barra queimada |
|---|---|
| `READY IN 1 TO 2 WEEKS` | "Ready in 1 to 2 weeks" |
| `THE GARLIC MELLOWS OUT` | "The garlic mellows out" |
| `2% SALT, NOT MORE` | "2% salt, weighed" |
| `ONE LAYER AT A TIME` | "Layer it, do not mix it" |

O arquivo foi desenhado como player próprio: cada cena já tem título + sub + selo dentro
do SVG. Os campos `cap`/`sub` foram escritos como *descrição* da cena, e o motor do mp4
desenha os dois — cada cena dizia a mesma coisa duas vezes, em dois tamanhos. Conserto
(`_consertar-legenda-beterraba-alho.py`): a **barra carrega o detalhe, o título carrega a
manchete**. Durações e `tag` provados iguais antes/depois (o script aborta se mudarem);
as 8 caps novas têm 19–27 caracteres e nenhuma repete uma antiga.

**mp4:** `beterraba/shorts-beet-garlic-en-1080x1920.mp4` — 1080×1920, H.264, **54,0 s**,
**1608/1620 quadros (99%)**, 15,4 MB, 29,78 q/s. Bruto 113 s com `--passo=60`. Conferido
**tocando**: 8 quadros, barra nova sem repetição, `BEETS+GARLIC n / 8` correto.

**Registrado em 3 lugares:** a pasta, a galeria (43 shorts, 0 bugs) e o pacote
(`_registrar-beterraba-alho.py`, 6 âncoras) + o plano
(`_registrar-beterraba-alho-plano.py`, 3 âncoras → Semana 11).

**A ressalva que ficou escrita nos dois guias:** esta é a **4ª beterraba** (#3, #4, #8).
O que a salva é o assunto ser o **alho**, não a beterraba — mas a **capa** não é
diferente. Ordem: **espalhar na grade**, nunca colada no #3 ou no #8.

**Ficou pendente:** o original PT do #19.
"""


def troca(caminho, ancoras):
    with io.open(caminho, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('%s — fim de linha: %d CRLF / %d LF' % (caminho, crlf, lf))
    eol = '\r\n' if crlf else '\n'
    falhou = False
    for rotulo, velho, novo in ancoras:
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        q = d.count(v)
        print('   %-38s casou %d vez(es)' % (rotulo, q))
        if q != 1:
            falhou = True
            continue
        d = d.replace(v, n, 1)
    if falhou:
        print('   ABORTADO — nada gravado.')
        return None
    return d


def main():
    novo = troca(MEM, ANCORAS)
    if novo is None:
        return 1
    with io.open(MEM + '.antes-do-19', 'w', encoding='utf-8', newline='') as fh:
        with io.open(MEM, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(MEM, 'w', encoding='utf-8', newline='') as fh:
        fh.write(novo)
    print('gravado: %s' % MEM)

    with io.open(LOG, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    if '#19 — beterraba + alho' in d:
        print('log: ja tinha a secao, nao dupliquei')
    else:
        with io.open(LOG, 'a', encoding='utf-8', newline='') as fh:
            fh.write(LOG_TEXTO.replace('\n', eol))
        print('gravado: %s (acrescentado)' % LOG)
    return 0


if __name__ == '__main__':
    sys.exit(main())

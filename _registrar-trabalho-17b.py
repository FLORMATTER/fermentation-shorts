# -*- coding: utf-8 -*-
"""
_registrar-trabalho-17b.py — registra o trabalho da segunda metade de 17/09.

  1. .workbuddy-ai/memory/MEMORY.md      -> os dois bugs de texto visivel, o video
                                            #14 e os ajustes nas ferramentas
  2. .workbuddy-ai/memory/2026-09-17.md  -> append do log do dia
  3. ~/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md -> o `tag:` no inventario
                                            de traducao + o bloco de aviso

Uso:
    python _registrar-trabalho-17b.py            # dry-run
    python _registrar-trabalho-17b.py --apply
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
MEM = os.path.join(RAIZ, '.workbuddy-ai', 'memory')
SKILL = os.path.join(os.path.expanduser('~'), '.workbuddy-ai', 'skills',
                     'shorts-svg-animado', 'SKILL.md')


# ── 1. MEMORY.md ────────────────────────────────────────────────────────────
MEM_ANCORA = """são **teste**, não publicar. Guia do zero: `guias/guia-obs-passo-a-passo.md`."""

MEM_NOVO = """são **teste**, não publicar. Guia do zero: `guias/guia-obs-passo-a-passo.md`.

## 🔴 O texto que fica NA TELA — o buraco que a tradução deixou (17/09)

**73 rótulos de topo em português, em 12 dos 15 arquivos `-en.html`.** O `tag:` do
array `scenes` vira o `.tag` do HTML — o **rótulo do topo, visível o vídeo inteiro**.
A cena 1 de cada arquivo estava em inglês; as cenas 2 em diante ficaram em português:
`CENA 2 / 7`, `BETERRABA + COUVE 3 / 8`, `CEBOLA+BETERRABA 4 / 8`, `CHUCRUTE 5 / 8`,
`RABANETE 6 / 7`, `COUVE-FLOR 7 / 7`.

**A regra que resolve sem inventar:** o prefixo inglês da **própria cena 1** do arquivo
é a referência (`SCENE 1 / 7` → `SCENE N / 7`; `BEET 1 / 7` → `BEET N / 7`).
Script: `_consertar-rotulos-en.py` (73 trocas, âncora contada por arquivo).

**Ordem em que o texto visível é esquecido** (do mais para o menos):
`<text>` do SVG → `cap:`/`sub:` → **`tag:`** ← foi este → `.cap`/`.cover`/`.tag` do HTML.

## 🥬 CABBAGE ≠ couve (17/09)

`beterraba/shorts-beterraba-couve-en.html` chamava a couve de **CABBAGE** em 16 strings
visíveis. Três coisas erradas ao mesmo tempo:
1. o desenho é **couve** — o gradiente se chama `kaleLeaf2` e o texto fala de "THICK STALK";
2. o pacote do YouTube diz **KALE** (entrada #8);
3. **CABBAGE já é o repolho** (`Repolho → CABBAGE` no README). Dois vídeos diferentes
   dizendo CABBAGE é exatamente a confusão que a regra "um legume por rodada" evita.

Corrigido para KALE. **Nome e cor não se decidem por grep do texto — ler o desenho**
(id de gradiente, path, comentário).

## 📊 Vídeo #14 — 3 cores (17/09)

`cores/shorts-3-colors-en.html` — alho + cebola + beterraba. **Ângulo novo, não
re-render:** por que cada um muda de cor (beterraba = betalaína que dissolve; cebola
roxa = antocianina que reage ao ácido; alho = **não é pigmento**, é reação de enxofre
com aminoácidos) e por que o azul do alho não é mofo. Fecha com "cor por dentro =
trabalhando; mofo por cima = joga fora". Postar **depois** dos três individuais
(#3, #9, #10). Semana 7, dia 2. Pacote na entrada #14.

**Lição de desenho:** se a cena promete uma cor, a cor tem que aparecer no **quadro
parado**. A 1ª versão tinha os 4 dentes creme animando para azul/verde — o
`--virtual-time-budget` do headless **não avança a timeline de animação**, então o PNG
saiu creme e o texto prometia azul. Corrigido: 1 creme + 1 azul + 1 verde **estáticos**
+ 1 animando.

## 🧰 Ajustes nas ferramentas (17/09)

- **`_revisar-cenas.py`**: o perfil do Chrome saiu de `_revisao/_tmp/profile` para o
  **temp do sistema** e **não é mais apagado**. Motivo: apagar essa pasta dentro do
  projeto travava a permissão (o sandbox bloqueia o delete) e o perfil passa de 40 MB.
- **`_validar-short.py`**: `SKIP_DIRS` ganhou **`_revisao`** e **`guias`**. Sem isso o
  validador varria as folhas temporárias que ele mesmo gera e acusava "problema" em
  HTML gerado — 8 falsos positivos."""


# ── 2. log do dia ───────────────────────────────────────────────────────────
LOG = """
---

## 🎬 17/09 (noite, 2ª parte) — vídeo novo + 89 correções de texto na tela

**Pedido:** `ok,faz mais um video de fermentacao em ingles com capcut,,sendo de alho
e cebola e beterraba`.

### Dois bugs achados de passagem (e grandes)

**1. 73 rótulos de topo em português, em 12 arquivos `-en.html`.** O `tag:` do array
`scenes` é o rótulo que fica na tela o vídeo inteiro. A cena 1 de cada arquivo estava
traduzida; as cenas 2 em diante nunca foram. Corrigido com `_consertar-rotulos-en.py`
(12 arquivos, 73 trocas, âncora contada, backup `.antes-do-tag`).

**2. A couve chamada de CABBAGE.** `beterraba/shorts-beterraba-couve-en.html` dizia
CABBAGE em 16 strings visíveis — mas o desenho é couve (`kaleLeaf2`), o pacote diz KALE
e CABBAGE já é o repolho. Corrigido para KALE (16 trocas, backup `.antes-do-kale`).

### Vídeo novo

`cores/shorts-3-colors-en.html` — 8 cenas, 53,5 s, 405×720 com o bloco `?rec`.
Tema: os três mudam de cor, cada um por um motivo diferente. Validado: **0 problemas**,
JS válido, **0 colisões** de rótulo com o `@handle`. Cenas renderizadas e olhadas —
foi assim que apareceu o problema do alho (dentes creme num texto que promete azul),
corrigido com 1 dente azul e 1 verde estáticos.

### Metadados

Entrada **#14** no pacote (título, 3 alternativas, descrição com os 3 mecanismos e o
aviso de mofo, hashtags), linha na QUICK CHART, linha em "WHICH FILE TO RECORD", nota
nas variantes explicando que é ângulo novo, e a Semana 7 dia 2 no plano de postagem.
Contagens atualizadas para 14 vídeos em `README.md` e `plano-de-postagem.md`.

### Ferramentas

- `_revisar-cenas.py`: perfil do Chrome movido para o temp do sistema e sem delete.
- `_validar-short.py`: `SKIP_DIRS` ganhou `_revisao` e `guias` (8 falsos positivos
  a menos — o validador estava acusando as folhas temporárias que ele mesmo gera).
"""


# ── 3. SKILL.md ─────────────────────────────────────────────────────────────
SK_INV_VELHO = """3. no JS: `cap:`/`sub:` de cada cena, `nome`/`nivel`/`sal`/`tempo`/`hint`, o array"""

SK_INV_NOVO = """3. no JS: **`tag:`**/`cap:`/`sub:` de cada cena — ⚠️ o **`tag:`** é o mais
   esquecido de todos, ver o bloco vermelho abaixo —, `nome`/`nivel`/`sal`/`tempo`/`hint`, o array"""

SK_AVISO_VELHO = "**Duas conversões que precisam entrar junto:**"

SK_AVISO_NOVO = """### 🔴 O `tag:` é o texto visível mais esquecido de todos

O `tag:` do array `scenes` vai para o `.tag` do HTML — é o **rótulo do topo, visível o
vídeo inteiro**. Numa tradução de série é o campo que passa batido, e o padrão do erro
é sempre o mesmo: a **cena 1** de cada arquivo está traduzida (foi feita à mão) e as
**cenas 2 em diante** ficam no idioma original. Aconteceu em **73 rótulos de 12
arquivos** numa série de 15.

```bash
# acha rótulo de topo com palavra do idioma original
for f in $(grep -rl "tag:'" --include='*-en.html' . | sort); do
  n=$(grep -oE "tag:'[^']*'" "$f" | grep -icE "CENA|CEBOLA|BETERRABA|REPOLHO|COUVE|CHUCRUTE")
  [ "$n" != "0" ] && echo "$f ($n)"
done
```

**A regra que resolve sem inventar nada:** o prefixo da **própria cena 1** do arquivo é
a referência. `SCENE 1 / 7` → `SCENE N / 7`; `BEET 1 / 7` → `BEET N / 7`;
`ONION+BEET 1 / 8` → `ONION+BEET N / 8`. Nunca inventar um rótulo novo — copiar o da
cena 1. Script pronto no projeto: `_consertar-rotulos-en.py`.

**Ordem em que o texto visível é esquecido** (do mais para o menos):
`<text>` do SVG → `cap:`/`sub:` → **`tag:`** → `.cap`/`.cover`/`.tag` do HTML.

**Duas conversões que precisam entrar junto:**"""


PLANO = [
    (os.path.join(MEM, 'MEMORY.md'), [(MEM_ANCORA, MEM_NOVO)]),
    (os.path.join(MEM, '2026-09-17.md'), None),
    (SKILL, [
        (SK_INV_VELHO, SK_INV_NOVO),
        (SK_AVISO_VELHO, SK_AVISO_NOVO),
    ]),
]


def ler(p):
    bruto = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in bruto else '\n'
    return bruto.replace('\r\n', '\n'), nl


def gravar(p, d, nl):
    saida = d if nl == '\n' else d.replace('\n', nl)
    io.open(p, 'w', encoding='utf-8', newline='').write(saida)


def main():
    aplicar = '--apply' in sys.argv
    total = 0
    for caminho, edicoes in PLANO:
        if not os.path.exists(caminho):
            print('FALTA  %s' % caminho)
            return 1
        d, nl = ler(caminho)
        antes = len(d)

        if edicoes is None:
            if LOG.strip() in d:
                print('%-46s ja tem o bloco — pulando' % os.path.basename(caminho))
                continue
            d = d.rstrip('\n') + '\n' + LOG
            n = 1
        else:
            for velho, novo in edicoes:
                c = d.count(velho)
                if c != 1:
                    print('ABORTOU %s\n  ancora com %d ocorrencia(s):\n  %s' % (
                        os.path.basename(caminho), c, velho[:110]))
                    return 1
                d = d.replace(velho, novo, 1)
            n = len(edicoes)

        print('%-46s %d -> %d bytes  (%d edicoes)' % (
            os.path.basename(caminho), antes, len(d), n))
        total += n
        if aplicar:
            gravar(caminho, d, nl)

    if aplicar:
        print('\nOK — %d edicoes aplicadas' % total)
    else:
        print('\nDRY-RUN — %d edicoes. Rode com --apply.' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())

# -*- coding: utf-8 -*-
"""_memoria-pao.py — registra no log do dia o pao (#21), os 3 originais PT e a seguranca do mel.

    python _memoria-pao.py

Append-only, com trava de idempotencia: se o titulo ja' estiver no arquivo, nao escreve.
"""
import io
import sys

ALVO = '.workbuddy-ai/memory/2026-09-19.md'

TITULO = '## 🍞 Pão (#21): o primeiro vídeo realmente novo desde o #20'

NOTA = TITULO + '''

Pedido: *"os 3 tres ..e faca mais video de fermentacao de pao e fermentacao de garlic com mel ."*

### 1. Os 3 originais PT que faltavam (#18, #19, #20)

A convenção da série é **original PT + irmão `-en`**; os três tinham nascido só em inglês.

| entrada | original PT criado | script | provas |
|---|---|---|---|
| #18 cenoura+maçã | `cenoura/shorts-carrot-apple.html` | `_criar-cenoura-maca-pt.py` (21 âncoras) | 7 cenas, 42,8 s |
| #19 beterraba+alho | `beterraba/shorts-beet-garlic-1080x1920.html` | `_criar-beterraba-alho-pt.py` (71 âncoras) | 8 cenas, 54,0 s, 18/18 |
| #20 couve-flor+maçã | `couve-flor/shorts-cauliflower-apple.html` | `_criar-couveflor-maca-pt.py` (20 âncoras) | 7 cenas, 43,8 s |

- O **#19 preserva o sufixo `-1080x1920`** — é assim que o `_sobras-vs-original.py` pareia
  (tira só o `-en`).
- **Âncora contada:** `⏸ Pause` aparece **2×** (o botão *e* o `textContent` do JS). A âncora
  declara o número esperado e **aborta sem gravar** se não casar. No #19, `BEET`/`GARLIC`
  aparecem **2×** cada (os rótulos de camada) e `WEEK 2` **2×**.
- **Medido antes de escrever:** `_inverter-dicionario.py` provou que o dicionário de 617
  pares tem **579 pares 1:1** (só `Cabbage` ← `Repolho`|`Couve` é ambíguo), e o
  `_traduzir-para-pt.py` rodou a seco no #18 trocando **só 7 strings** — o dicionário não
  cobre conteúdo novo. Por isso o PT foi escrito **à mão com âncoras contadas**, que é o
  padrão verificado da série.
- **Prova de que só o idioma mudou:** `re.findall(r'(?:ms|color|id|fill|stroke|font-size|viewBox)[:=]"?(#?\\w[\\w%., -]*)')`
  comparado entre os dois arquivos — igual = nada além de texto mudou.

### 2. Pão / levain (#21) — `pao/`

Não existia **nada** de pão na série (nenhum arquivo `pao`/`bread`/`sourdough`/`fermento`).

`_criar-pao.py` gera **EN e PT de uma vez**, a partir do template do #18. As 7 cenas saem por
**regex** (`<svg class="scene" ... id="sN">...</svg>`), só a 1ª linha levando o recuo da cena.

**Substância pesquisada:** o levain é simbiose de levedura selvagem + bactérias láticas
(**~100:1**); a levedura faz CO₂/etanol e **levanta**, as láticas fazem lático (suave) e
acético (agudo); **a temperatura manda** (30-35 °C mais suave, 20-24 °C mais ácido);
alimentar **1:1:1 por PESO, não volume**; a rede de glúten prende o gás; o **teste da
colher**; **5 a 10 dias**; rosa/laranja = mofo (joga fora), líquido escuro = álcool (mistura).

### 3. Os 3 defeitos de contraste — medidos, não olhados

`_medir-contraste-pao.py` compõe a `opacity` sobre o fundo e imprime a **distância RGB**
(limite ~130 = "dá pra ver"):

| onde | antes | depois |
|---|---|---|
| cena 0 pote de vidro sobre o halo | **52** FRACO | — |
| cena 0 levain DENTRO do pote | **66** FRACO — o pote lia como **bloco vazio** | **154** |
| cena 2 levain × farinha | **14** INVISÍVEL — eram o **MESMO círculo** | **141** |
| cena 4 massa sobre o halo | **2** INVISÍVEL — a massa **era** o halo | **131** |

Consertos: levain vira trigo escuro `#d9b872`; os três círculos ganham cores **distintas**
(trigo / creme `#fbf7ec` / azul `#6fb0dd`); a massa vira `#d4ad64` sobre halo `.35`; a rede de
glúten escurece; saem os três rótulos `"1"` (o `1 : 1 : 1` já diz); e a **"colher" era um
pirulito** (cabo fino + bolinha) — redesenhada com cabo e cuia.

### 4. O conserto voltou para o GERADOR (senão regerar desfazia)

`CONTRASTE` (12 trocas) e a tradução dos **botões** foram dobradas dentro do `_criar-pao.py`.
**Por quê:** o gerador é a fonte da verdade — sem isso, regerar o short desfazia o conserto e
o pote voltava a ler como bloco vazio.

- Os botões (`⏸ Pause`, `▶ Watch`) **não** estão em `cap:`/`sub:` nem são nó de texto do
  corpo, então o extrator **não os vê** — quem pegou foi o `_sobras-vs-original.py`, que
  **compara os dois arquivos**. PT agora: `⏸ Pausar` ×2, `▶ Assistir` ×1.
- As entradas com quebra de linha usam `\\n` e o laço converte para o `eol` do arquivo.
- **Prova de que não regrediu:** o EN saiu com md5 **idêntico** (`4a810617…`) e o `diff` do PT
  mostrou **exatamente 3 linhas** (as dos botões). O `.mp4` do EN continua válido — o
  conteúdo do EN não mudou.

### 5. Alho + mel (#9): o defeito era de SEGURANÇA, não de conteúdo

O vídeo **já existia** (#9, no pacote, com mp4, Semana 2 do plano) — então **não duplicar**.
O furo real: o cartão de conservação dizia **"Keep it at room temperature"** e **não avisava
do botulismo**. Trocado por:

```
⚠ NEVER GIVE IT TO A BABY
Honey can carry botulism spores
When in doubt, keep it cold
```

e a barra da cena 7 virou `sub:'under 1 year old, never'`. **Base:** mel e alho **ambos**
carregam esporos de *C. botulinum*; o esporo precisa de **sem oxigênio + 4-60 °C + pH > 4,6**;
o alho solta água e **derruba a barreira de atividade de água** do mel; a janela perigosa é
**antes** de a fermentação baixar o pH; **abaixo de 4 °C** não germina; **nunca para bebê
de menos de 1 ano**. O script **prova** que durações e nº de cenas não mudaram (8 cenas,
52,5 s), então pacote e plano continuam válidos.

### 6. Registro e limpeza

- `_registrar-pao.py`: #21 no pacote, na tabela de arquivos, no quadro rápido, na galeria
  (`ROTULO` + `ORDEM`) e a **Semana 13** no plano. Consertou também um defeito meu: os
  **#18/#19/#20 estavam sem cabeçalho numerado** — liam como continuação do #17.
- `_nota-pt-original.py`: os três ainda diziam *"no Portuguese original"*. Agora têm a nota
  certa. **Armadilha:** a string `"…no Portuguese original** - it was built in English."` é
  **prefixo de DUAS entradas** (#18 e #20) — a âncora do #20 leva o contexto de baixo.
- `_rewrap-notas.py`: o nome de arquivo comprido do #19/#20 empurrava a 1ª linha para 100
  colunas; re-embrulhado em ~85, como o #17/#18/#21.

**Estado final:** galeria **49 shorts, 0 bugs, 19 avisos**; tags de cena **44 arquivos,
0 quebrados**; pacote **21 entradas** (cabeçalhos 1..21 completos); `_sobras-vs-original.py`
**20 pares, 16 limpos, 6 strings** — todas **benignas** (`?play`, `@yourhandle`,
`@yourchannel` ×3 = placeholder igual nos dois idiomas; `🍞 + LEVAIN` = "levain" é a mesma
palavra). **Zero tradução faltando.**

**Ficou pendente:** 19 avisos de keyframe não usado (oferecido, não aprovado); o aviso de
álcool no PT do #4 (oferecido, não aprovado).
'''


def main():
    try:
        with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
            d = fh.read()
    except IOError:
        print('ERRO: nao achei %s' % ALVO)
        return 1

    if TITULO in d:
        print('ja\' registrado — nada a fazer (%d bytes)' % len(d.encode('utf-8')))
        return 0

    eol = '\r\n' if d.count('\r\n') else '\n'
    novo = d.rstrip() + eol + eol + NOTA.replace('\n', eol).rstrip() + eol

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(novo)
    print('%s: %d -> %d bytes' % (ALVO, len(d.encode('utf-8')),
                                  len(novo.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

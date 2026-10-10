# -*- coding: utf-8 -*-
"""_memoria-melao.py — anexa o registro do #24 no log do dia (append-only).

    python _memoria-melao.py
"""
import io
import sys

LOG = '.workbuddy-ai/memory/2026-09-22.md'

TEXTO = '''

---

## 🍈 #24 — kombucha de maçã com melão (EN-only, pedido do usuário)

`kombucha/shorts-apple-melon-en.html` + `.mp4` (9,2 MB, 44,6 s, 1080×1920, 1311/1338
amostras -> 29,395 q/s CFR). Gerador `_criar-kombucha-melao.py` (fonte da verdade).

### O assunto é o pH, não a fruta

Para **não** ser o #23 com outra roupa, o vídeo foi construído sobre um fato que nenhum
outro da série usa: **o melão é a única fruta que NÃO é ácida.**

| | pH | |
|---|---|---|
| Melão (cantalupo) | **6,0–6,7** | a mesma faixa da carne crua — **acima** da linha |
| Maçã | 2,9–3,3 (cartão: 3,0) | ~**2.500×** mais ácida |
| Kombucha pronta | 2,5–3,5 | é ela que puxa o pote para baixo de 4,6 |
| Linha de segurança | **4,6** | acima dela as bactérias ruins crescem |

A **casca rendada** é carregador conhecido de *Salmonella* / *Listeria* -> a cena 6 é
**"WASH THE RIND FIRST"**, que é o ponto do vídeo, não enfeite.

### 🐛 O erro (l) — número no cartão que não fecha com a conta

O cartão da cena 3 dizia **"ABOUT 1800 TIMES MORE ACID"** enquanto mostrava **3.0** e
**6.4** na própria tela. A conta é 10^(6,4−3,0) = 10^3,4 ≈ **2.512** -> "about 2500".
O subtítulo explicava a escala com "3 points is a thousand", que também não batia.
Conserto no gerador por `_corrigir-melao-acido.py` (2 âncoras contadas, aborta sem
gravar): `1800 -> 2500` e o subtítulo -> **"each pH point is ten times more acid"**.
**Regra nova: conferir a aritmética do que o próprio cartão mostra.**

### 🐛 Forma — o melão lido como 4 coisas erradas

Só o **zoom** pegou (grep e validador não veem forma):

| Render | Leu como | Conserto |
|---|---|---|
| 1º | **laranja** | casca mais grossa |
| 2º | **kiwi** (bola marrom uniforme) | casca **bege** + rede irregular |
| 3º | **waffle / bola de tênis** (grade simétrica) | **SUTURAS** — as lombadas de cima a baixo |
| faca | **termômetro** | lâmina mais larga |
| caldo | flutuava acima do pote | fluxo mais longo e mais baixo |

**A lição:** o que faz ler "melão" não é a rede, são as **lombadas**. Com elas a rede pode
ser esparsa e ondulada — que é como o cantalupo realmente parece.

### 🔴 O lookahead errou por UM `\\n` — de novo

`_melhorar-melao2.py` abortou com `ERRO: bloco melao_inteiro casou 0 vez(es)` porque o
padrão era `def melao_inteiro\\(.*?\\n(?=\\n\\n\\ndef maca\\()`. O `.*?\\n` **já consome um
`\\n`**, então no lookahead sobram **dois**, não três. É a **terceira** vez que esse erro
aparece (antes: `dente`, `bulbo_alho`) — por isso ele virou regra no `MEMORY.md`.

### ✅ Registro e verificação

- `_registrar-melao.py` — 9 âncoras contadas em 2 arquivos, **valida tudo antes de gravar**;
  confere no fim que o pacote tem 24 entradas (1..24) e o plano 15 semanas (1..15).
- Pacote: entrada **#24**, linha do QUICK CHART, ordem de postagem **semana 15**, linha 24
  da tabela, contagem -> "**All 23 Shorts are already rendered — every entry except #13**"
  (24 entradas − o #13 = 23 Shorts: a contagem antiga "23 dos 23" era frouxa).
- Plano: **15 semanas**, `24 vídeos, não 47 arquivos` (contados: 47 `.html` nas pastas),
  Semana 15 com o #24 **sozinho** + a nota de ordenação (**longe do #23**).
- Galeria regerada: **52 shorts**, 0 bugs, 19 avisos.
- `_validar-short.py` série: 25 acusações, todas conhecidas e benignas; o novo não aparece.
- `_sobras-vs-original.py`: o novo entra em "sem original PT" (correto, é EN-only).
- Quadro real do `.mp4`: tag `KOMBUCHA n / 7` queimada certa, barra de legenda com o
  detalhe, **sem marca d'água**, e o cartão já mostra **2500**.
'''


def main():
    with io.open(LOG, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    if '#24 — kombucha de maçã com melão' in d:
        print('JA REGISTRADO — nada a fazer')
        return 0
    with io.open(LOG, 'a', encoding='utf-8', newline='') as fh:
        fh.write(TEXTO)
    with io.open(LOG, 'r', encoding='utf-8', newline='') as fh:
        novo = fh.read()
    print('OK: log %d -> %d bytes' % (len(d.encode('utf-8')), len(novo.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

# -*- coding: utf-8 -*-
"""_memoria-beterraba-cenoura.py — log do dia + MEMORY.md do #25.

    python _memoria-beterraba-cenoura.py
"""
import io
import os
import sys

PASTA = '.workbuddy-ai/memory'
LOG = os.path.join(PASTA, '2026-09-23.md')
MEM = os.path.join(PASTA, 'MEMORY.md')

LOG_TEXTO = '''# 2026-09-23 — #25: beterraba + cenoura

## 🟣🥕 O vídeo

`beterraba/shorts-beet-carrot-en.html` + `.mp4` (8,4 MB, 45,2 s, 1080×1920,
**1356/1356 amostras = 100%**, 30,000 q/s exatos). Gerador `_criar-beterraba-cenoura.py`.

**Combinação nova de verdade:** beterraba já estava em #3/#4/#8/#14/#19 e cenoura em
#12/#18 — mas **nunca juntas**. Mesmo assim o assunto tinha de ser novo (regra da série:
"o formato pode repetir, a substância não").

### O assunto: a cenoura salva o vermelho

Achado numa fonte que é exatamente sobre esse par — **MDPI Applied Sciences 2023, 13,
6113**, fermentação lática de suco de beterraba, de cenoura e da **mistura 1:1** (2% de
sal, 28 °C, 7 dias):

| Dado | Valor |
|---|---|
| **Degradação das betalainas na MISTURA** | **significativamente MENOR** — os autores atribuem à **proteção antioxidante dos carotenoides** |
| pH final | todas **abaixo de 4,5**; mínimo **3,3** |
| Sólidos solúveis ("extract") | beterraba > mistura > cenoura |
| pH da cenoura | o **maior** dos três |
| Cor | beterraba o mais escuro (L* 2,5–7,5), cenoura o mais claro (L* 31–37) |
| Recomendação dos autores | 4 a 5 dias |

Completado com a tabela de pH de alimentos (FDA/webpal): **beterraba 5,30–6,60**,
**cenoura 5,88–6,40** — as duas **ACIMA de 4,6**, ou seja, nenhuma se protege sozinha e o
ácido tem de ser fabricado. Açúcar: beterraba ~**7 g/100 g** contra cenoura ~**4,7 g/100 g**
→ ~**50% mais**.

**A espinha do vídeo:** beterraba = combustível (açúcar → ácido lático), cenoura = escudo
(carotenoides → seguram a oxidação da betanina).

## 🐛 Quatro defeitos de FORMA (só o render pegou)

| Objeto | Leu como | Conserto |
|---|---|---|
| colher de sal | **folha de papel flutuando** | desenhei só a cuia de perfil → **cuia + CABO** |
| faca | **tubo de ensaio** | em pé, lâmina estreita vertical → **deitada** (lâmina 2× a largura + bolster + cabo com rebites) e girada |
| relógio | **bússola** | 4 marcas → **12**, horas mais compridas |
| folha de beterraba/cenoura | **broto** | limbo fino → limbo **largo com nervura** |

E um quinto, que **não é forma**: na barra de pH, "BEET" (5,3) e "CARROT" (5,9) estão a
0,6 de pH = **37 px**, e "CARROT" a 13 px tem ~47 px → saiu **"BEETCARROT"**. Não é texto
longo demais para a caixa (erro (h)): é a **posição**, que vem do dado. Conserto: `dy`
escalonando o rótulo na vertical.

## 🔴 O erro (k) em 3 das 7 cenas — e o verificador

A barra de legenda do mp4 repetia o título que já estava na cena em **s0, s2 e s3**, e em
duas delas a sublinha era quase a mesma frase. Eu mesmo escrevi os dois lados.

**O verificador que pega** (`acha_repeticoes`): varre **todos os `<text>` de cada cena** e
compara com o `cap`. Dois furos que ele já teve:

1. **Selecionar "o título" por `font-size` não funciona.** A 1ª versão procurava
   `font-size="18"` e a conta não fechou: a cena do sal titula com **46 px** (é o "2%") e a
   do truque com **17 px**.
2. **Verificador que nunca falha não prova nada.** Rodei a checagem **no arquivo ANTES do
   conserto** e exigi que acusasse: **3 antes, 0 depois**. Foi assim que se soube que
   funcionava.

## 🐛 Um furo meu de regex

Generalizar o padrão de troca de bloco para servir dois tipos —
`r'(?:def|TEXTOS = )%s\\(?.*?\\n' % nome` — produz **`TEXTOS = TEXTOS`** e **nunca casa**.
Cada bloco tem de ter o **padrão completo**, escrito por extenso.

## ✅ O `--passo=150` dá 100% dos quadros

Os renders anteriores (passo padrão 60 ms) perdiam ~2% (1338 → 1311 amostras no #24).
Com **`--passo=150`: 1356/1356 = 100%** e 30,000 q/s **exatos**, sem retimar nada.
Custa mais tempo (~45 s de vídeo ≈ **3 min 40**), mas entrega o arquivo certo de primeira.

## 📌 Registro e verificação

- `_registrar-beterraba-cenoura.py` — 9 âncoras contadas em 2 arquivos, valida tudo antes
  de gravar; confere no fim 25 entradas (1..25) no pacote e 15 semanas (1..15) no plano.
- Pacote: entrada **#25**, linha do QUICK CHART, semana 15 (que agora tem os **dois**
  vídeos novos, dia 1 = #24 e dia 2 = #25), linha 25 da tabela, contagem → "All **24**
  Shorts are already rendered — every entry except #13".
- Plano: `25 vídeos, não 48 arquivos` (contados: 48 `.html`), Semana 15 com a nota de
  ordenação do #25 (**longe dos cinco vídeos de beterraba**).
- Galeria: **53 shorts**, 0 bugs, 19 avisos. `_validar-short.py` série: 25 acusações (as
  mesmas de antes — o novo não aparece). `_sobras-vs-original.py`: o novo entra em
  "sem original PT" (correto, é EN-only).
- Quadro real do `.mp4`: tag `BEET+CARROT n / 7`, **nenhuma barra repetindo o título**,
  **sem marca d'água**.

## 🧠 Skill atualizada (103.203 → 105.889 bytes)

3 inserts: o **verificador do erro (k)** com os dois furos, as **lições de forma** (colher,
faca, relógio, folha, rótulos colidindo) e o **3º furo da troca de bloco por regex**.
'''

TROCAS = (
    ('## 📊 Catálogo — 24 entradas no pacote',
     '## 📊 Catálogo — 25 entradas no pacote', 1),
    ('  **#24** kombucha maçã+melão (2ª bebida, 1º **melão** da série).',
     '  **#24** kombucha maçã+melão (2ª bebida, 1º **melão** da série) ·\n'
     '  **#25** beterraba+cenoura (`beterraba/`, 1º par **beterraba+cenoura**).', 1),
    ('— **#22, #23 e #24 são\n  só EN**',
     '— **#22, #23, #24 e #25 são\n  só EN**', 1),
    ('O driver **retima sozinho** e confere a duração (`--sem-retimar` desliga). `--passo`\n'
     'padrão **60 ms**; `150` só para 100%. **Conferir é TOCAR:**\n'
     '`node _mp4/quadros-mp4.js <arq>.mp4 8`.',
     'O driver **retima sozinho** e confere a duração (`--sem-retimar` desliga).\n'
     '**`--passo=150` é o certo para entregar:** com o padrão 60 ms o `MediaRecorder`\n'
     'descarta ~2% dos quadros (1338 -> 1311 no #24); com **150 ms deu 1356/1356 = 100%**\n'
     'e 30,000 q/s exatos (#25). Custa ~**3 min 40** por vídeo de 45 s.\n'
     '**Conferir é TOCAR:** `node _mp4/quadros-mp4.js <arq>.mp4 8`.', 1),
    ('- **Com mp4 — 23 dos 24.**', '- **Com mp4 — 24 dos 25.**', 1),
    ('- **#22, #23 e #24 não têm versão PT** — oferecido, não aprovado.',
     '- **#22, #23, #24 e #25 não têm versão PT** — oferecido, não aprovado.', 1),
)


def main():
    os.makedirs(PASTA, exist_ok=True)

    # --- 1) log do dia (append-only; cria se nao existir)
    if os.path.exists(LOG):
        with io.open(LOG, 'r', encoding='utf-8', newline='') as fh:
            atual = fh.read()
    else:
        atual = ''
    if '#25: beterraba + cenoura' in atual:
        print('  log: ja registrado')
    else:
        with io.open(LOG, 'a', encoding='utf-8', newline='') as fh:
            fh.write(('\n\n---\n\n' if atual else '') + LOG_TEXTO)
        print('  log: %d -> %d bytes'
              % (len(atual.encode('utf-8')),
                 len(io.open(LOG, encoding='utf-8').read().encode('utf-8'))))

    # --- 2) MEMORY.md: confere todas as ancoras antes de gravar
    with io.open(MEM, 'r', encoding='utf-8', newline='') as fh:
        m = fh.read()
    antes = len(m.encode('utf-8'))
    for velho, novo, n in TROCAS:
        achou = m.count(velho)
        if achou != n:
            print('ERRO: ancora casou %d vez(es), esperava %d:\n  %s'
                  % (achou, n, velho.split('\n')[0][:70]))
            return 1
    for velho, novo, n in TROCAS:
        m = m.replace(velho, novo, n)
        print('  ok: %s' % velho.split('\n')[0][:56])

    for proibido in ('24 entradas no pacote', 'Com mp4 — 23 dos 24',
                     '#22, #23 e #24 são', '#22, #23 e #24 não têm'):
        if proibido in m:
            print('ERRO: sobrou "%s"' % proibido)
            return 1
    for exigido in ('25 entradas no pacote', '#25** beterraba+cenoura',
                    'Com mp4 — 24 dos 25', 'passo=150', '#22, #23, #24 e #25'):
        if exigido not in m:
            print('ERRO: faltou "%s"' % exigido)
            return 1
    if len(m.encode('utf-8')) <= antes:
        print('ERRO: o MEMORY.md nao cresceu')
        return 1

    with io.open(MEM, 'w', encoding='utf-8', newline='') as fh:
        fh.write(m)
    print('OK: MEMORY.md %d -> %d bytes' % (antes, len(m.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

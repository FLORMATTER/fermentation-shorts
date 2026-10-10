# -*- coding: utf-8 -*-
"""_skill-zoom.py — grava na skill as licoes de FORMA desta sessao.

    python _skill-zoom.py

Duas insercoes na SKILL.md:
  1. a secao do `_zoom-cena.py` + as 4 leituras erradas do dente/bulbo de alho;
  2. o caso espelhado do selo: texto GRANDE demais para o cartao.
"""
import io
import sys

SK = ('C:/Users/Saxa/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md')

SECAO = '''### 👁️ A FORMA passa por 3 ou 4 leituras erradas — e só o ZOOM mostra

O `_revisar-cenas.py` renderiza a folha de contato em **tamanho nativo (405×720)**. Isso
basta para **layout** (texto estourando, card colidindo) e **não basta para forma**: a
405×720 um dente de alho de 26 px é um borrão.

```bash
python _zoom-cena.py <arquivo>.html 3 --escala 3     # uma cena, 3x
python _zoom-cena.py <arquivo>.html 0,3,5            # várias, uma por PNG
```

**Caso real — `pepino/shorts-cucumber-garlic-en.html`.** O mesmo dente de alho precisou de
**quatro** versões, e cada leitura errada só apareceu no render:

| Versão | O que o olho leu | O que faltava |
|---|---|---|
| 1 | **pingo d'água** | o dente era uma gota simétrica |
| 2 | pingo d'água ainda | a linha da base não basta — o **contorno** tem de ser assimétrico |
| 3 | **baga** | faltava a **faixa clara da FACE DO CORTE**, do lado reto |
| 4 | dente de alho ✔ | — |

**O que faz ler "dente de alho descascado":** lado esquerdo **RETO** (o corte), barriga
curva à direita, base chata e — o detalhe que decide — uma **faixa clara** (`#ffffff` a 42%
de opacidade) colada nesse lado reto. Sem a faixa, lê como fruta.

E o bulbo, na mesma sessão, levou outras quatro:

| Versão | O que o olho leu | O que faltava |
|---|---|---|
| 1 | **concha / pinha** | o bulbo era UMA silhueta com 8 lóbulos |
| 2 | **flor de pétalas**, colo flutuando | 5 dentes separados, mas nada que os juntasse |
| 3 | **botão / cebola** | casca resolvida, mas o bulbo estava alto e bicudo |
| 4 | bulbo de alho ✔ | **atarracado**: 124 de largura × 122 de altura |

**O bulbo são TRÊS camadas, nesta ordem:** a **casca** (silhueta pálida com
`stroke-dasharray` para ler como papel), o **colo** (trapézio + cabinho seco) e os **5
dentes** por cima — os de fora atrás e mais curtos, o do meio na frente e mais alto. Uma
silhueta só vira concha; dentes soltos viram flor; **é a casca que amarra**.

**E o bulbo é o caso INVERSO da caixa:** o contentor não pode ser mais largo que alto, mas o
**bulbo** não pode ser mais alto que largo — alto e bicudo lê como **botão de flor**. Alho
de verdade é baixo, com o terço de cima só de casca e os dentes aparecendo embaixo.

**Rodela de pepino ≠ elipse.** Elipse lisa lê como **azeitona**. O que faz ler "pepino" é o
**anel de casca escura + miolo pálido + sementes** (4 elipses pequenas dentro).

**A regra que fica:** quando o desenho "não parece", **não é a cor** — é a **forma**, e forma
só se julga **grande**. Ordem: `_revisar-cenas.py` (layout) → `_zoom-cena.py` (forma) →
corrigir **no GERADOR** → regerar.

### 🔧 Trocar um BLOCO de função no gerador — dois furos de regex

Quando o conserto é grande (reescrever `dente()`, `bulbo_alho()`, uma cena inteira), o certo
é trocar o **bloco** por regex em vez de reescrever o arquivo à mão. Dois furos que já
custaram rodada:

1. **Off-by-one no lookahead.** `re.compile(r'def x\\(.*?\\n(?=\\n\\n\\ndef y)', re.S)` **nunca
   casa**: o `.*?\\n` **já consome** um `\\n`, então o lookahead precisa de **um a menos** —
   `(?=\\n\\ndef y)`. Sintoma: `casou 0 vez(es)` num bloco que está lá.
2. **A âncora `\\n\\n#` engole as funções seguintes.** `def bulbo_alho(...)` termina antes do
   comentário `# --- cena 1`, então um bloco ancorado em `\\n\\n#` **leva junto** `lab()` e
   `nuvem_lab()`. Se o texto de substituição não trouxer os três de volta, o gerador morre
   com `NameError` — ou pior, cria **duas** definições do mesmo nome.
   **Defesa:** depois de trocar, **contar `^def <nome>`** de todas as funções vizinhas e
   abortar se alguma sumir ou duplicar. Foi assim que a 2ª definição de `cravo` apareceu.

**E o `%` do Python:** uma string SVG com `%` solto (`3.5 - 5%`) que passa por formatação
`%` estoura com `ValueError: unsupported format character`. Em SVG, usar **tokens**
(`@GARRAFA@`) + `.replace()`, e **f-string** nos helpers. Nunca `%`-format em string de SVG.

### Partículas — atenção'''

SELO = '''- **O caso espelhado: texto GRANDE demais para o cartão.** O selo estreito é caixa
  pequena com texto normal; o outro lado é **texto grande com caixa normal**. Em
  `kombucha/shorts-watermelon-apple-en.html` (cena 4) o título `WHY THE APPLE AND NOT THE
  MELON` (33 caracteres, 17 px) **encostava nos dois lados** do cartão de 340 — sem estourar,
  mas com folga zero. Conserto igual: encurtar o inglês → **`THE APPLE, NOT THE MELON`**.
  **O sintoma é o texto tocar as duas bordas.** Folga zero já é defeito, mesmo que o
  validador passe — ele mede coordenada, não largura de texto.
- Comparar com o **render do original PT**'''


def main():
    with io.open(SK, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    antes = len(d.encode('utf-8'))
    print('SKILL.md: %d bytes, %s' % (antes, 'CRLF' if eol == '\r\n' else 'LF'))

    for velho, novo, rotulo in (
            ('### Partículas — atenção', SECAO, 'secao do zoom'),
            ('- Comparar com o **render do original PT**', SELO, 'selo largo demais')):
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        c = d.count(v)
        if c != 1:
            print('ERRO: ancora "%s" casou %d vez(es)' % (rotulo, c))
            return 1
        d = d.replace(v, n)
        print('  ok: %s' % rotulo)

    with io.open(SK, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: %d -> %d bytes' % (antes, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

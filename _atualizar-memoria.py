# -*- coding: utf-8 -*-
"""_atualizar-memoria.py — 3 ancoras no MEMORY.md do projeto.

Edicoes paralelas no mesmo arquivo se sobrescrevem (ja aconteceu 2x em 17/09).
Aqui cada ancora e conferida e o script ABORTA sem gravar se alguma nao casar.
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(RAIZ, '.workbuddy-ai', 'memory', 'MEMORY.md')
d = io.open(ALVO, encoding='utf-8').read()
orig = d

# ── A) scripts novos no bloco de comandos ──────────────────────────────
A_velho = """python _conferir-origin.py                     # sobrou transform-origin? NUL/CRLF?
python _gerar-galeria.py                       # REGERAR depois de criar/consertar short
```"""
A_novo = """python _conferir-origin.py                     # sobrou transform-origin? NUL/CRLF?
python _gerar-galeria.py                       # REGERAR depois de criar/consertar short
python _sobras-vs-original.py                  # O TESTE DE IDIOMA (compara -en com o PT)
python _traduzir-serie.py --cobertura          # o que falta no dicionario
python _traduzir-serie.py --apply              # traduz a serie inteira pelo dicionario
python _largura-texto.py <arquivos>            # TRIAGEM de texto largo (nao decide)
python _localizar-selo.py <arquivo>            # em que cena esta cada selo suspeito
```"""

# ── B) regra nova depois dos bullets de armadilha ──────────────────────
B_velho = """- **`_validar-short.py` e `_analisar-rodape.py` leem o `y` CRU.** Texto dentro de
  `<g transform="translate(0,392)"><text y="0">` tem y real 392 e passa como "0".
  Para isso existe o `_y-absoluto.py`, que acumula os `translate()` aninhados."""
B_novo = """- **`_validar-short.py` e `_analisar-rodape.py` leem o `y` CRU.** Texto dentro de
  `<g transform="translate(0,392)"><text y="0">` tem y real 392 e passa como "0".
  Para isso existe o `_y-absoluto.py`, que acumula os `translate()` aninhados.
- **Para verificar IDIOMA, comparar com o original — nunca adivinhar por lista de
  palavras.** Ver a seção "🌍 Série inteira em inglês" abaixo.
- **`_largura-texto.py` é TRIAGEM, não veredito.** Ele ignora o `letter-spacing` e já deu
  falso positivo e falso negativo com números idênticos. **Renderizar e olhar é
  obrigatório.**"""

# ── C) secao nova sobre a serie ────────────────────────────────────────
C_velho = """**O PT ainda tem o bug** — não consertar sem o usuário pedir."""
C_novo = """**O PT ainda tem o bug** — não consertar sem o usuário pedir.

## 🌍 Série inteira em inglês + a lição do verificador (17/09/2026)

**14 shorts** ganharam irmão `-en.html` (o PT nunca é tocado):

```
beterraba/  shorts-beterraba-animado, -camadas, -couve, -melancia, -svg-puro
cebola/     shorts-cebola-beterraba          cenoura/  shorts-cenoura-animado
couve-flor/ shorts-couveflor-animado         pepino/   shorts-pepino-speed
rabanete/   shorts-rabanete-animado
repolho/    cartao-8-cenas-chucrute, shorts-chucrute-30s,
            shorts-repolho-animado, shorts-repolho-maos-canva
```

Feito com **um dicionário único** (`_dicionario-pt-en.py`, **617 frases**) aplicado por
`_traduzir-serie.py`. O vocabulário se repete muito na série — traduzir uma frase uma vez
vale para todos os vídeos.

### 🔴 REGRA: verificar idioma COMPARANDO com o original

O detector antigo (regex de palavras PT) anunciava **"FRASES SEM TRADUÇÃO: 0"** e **era
falso**: 151 frases nunca tinham sido traduzidas.

**Causa:** o regex terminava cada alternativa com `\\b`. Em Python 3 o `\\b` usa `\\w` e
**letra acentuada CONTA como `\\w`** → `\\bfermenta\\b` **não casa** em `FERMENTAÇÃO`
(depois do `a` vem `Ç`, que também é letra) e `\\bcrocante\\b` não casa em `CROCANTES`.

**Solução:** `_sobras-vs-original.py` extrai as strings visíveis do `-en` e do PT e aponta
**toda string que ficou idêntica**. Não depende de lista de palavras nem de regex de
idioma. **Usar sempre como verificação final.** Resultado: **15 pares limpos, 0 sobra**.

Sobram só strings **neutras** (iguais porque não têm idioma): `pH`, `kg`, `10 MIN`,
`Pizza`, `Tacos`, `${cap.nome}`.

**O aplicador tinha um 2º furo:** as âncoras `'Frase'` / `>Frase</text>` / `>Frase<` não
pegavam nó de texto seguido de outra tag (`>CHUCRUTE<br>`, `>EM <span>`). Foram
adicionadas `>%s<br>` e `>%s <`, mais `troca_nos_html()` — que só troca **dentro do corpo
do HTML** (de `</style>` até `<script>`), porque dentro do `<script>` o `>` e o `<` são
operadores de comparação.

### 📐 Selo com texto mais largo que a caixa (o erro (h))

**9 selos** estouravam nos dois lados depois da tradução — o inglês é mais largo que o
português. **Conserto: encurtar o INGLÊS, não alargar a caixa** — a caixa já ocupa 83% do
cartão (337 de 405). Num caso o texto pedia **409 px, mais que o cartão inteiro (405)**,
então alargar era impossível.

Exemplos: `THE SALT TURNS IT INTO A PRESERVE` → **`THE SALT PRESERVES IT`**;
`THE CABBAGE ABSORBS THE COLOUR OF THE BEET` → **`THE CABBAGE SOAKS UP THE COLOUR`**.

**O `_largura-texto.py` NÃO decide.** Dois selos com números idênticos
(30 car · 20px → 372 px, caixa 337) deram resultados **opostos**: um cabia, o outro
estourava. A estimativa ignora o `letter-spacing`. **Renderizar e olhar é obrigatório.**"""

for rot, velho, novo in (('A scripts', A_velho, A_novo),
                         ('B regras', B_velho, B_novo),
                         ('C secao serie', C_velho, C_novo)):
    c = d.count(velho)
    if c != 1:
        print('ABORTADO: ancora %s casou %d vez(es), esperado 1.' % (rot, c))
        sys.exit(1)
    d = d.replace(velho, novo, 1)
    print('ok ancora %s' % rot)

io.open(ALVO, 'w', encoding='utf-8', newline='').write(d)
print('\ngravado: %d -> %d bytes' % (len(orig.encode('utf-8')), len(d.encode('utf-8'))))
print('NUL: %d' % d.count(chr(0)))

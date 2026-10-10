# -*- coding: utf-8 -*-
"""
_memoria-couveflor-maca.py — memoria do projeto com o video #20 (couve-flor + maca).

MEMORY.md : catalogo 19 -> 20, mp4 18/19 -> 19/20, a entrada nova, e a licao do
            contraste claro-sobre-claro + a do jarro deitado.
log do dia: secao nova no fim.
"""
import io
import sys

MEM = '.workbuddy-ai/memory/MEMORY.md'
LOG = '.workbuddy-ai/memory/2026-09-19.md'

ANCORAS = [
    (
        'titulo do catalogo',
        '## 📊 Catálogo — 19 entradas no pacote',
        '## 📊 Catálogo — 20 entradas no pacote',
    ),
    (
        'entrada do #20',
        'Plano em `guias/plano-de-postagem.md`; upload em `guias/guia-de-upload.md`.',
        '**#20 — couve-flor + maçã** (`couve-flor/shorts-cauliflower-apple-en.html`, 43,8 s, 7 cenas):\n'
        'a maçã como **starter** e a química do enxofre. Couve-flor é 90% água, parede densa e\n'
        'quase sem açúcar → a bactéria demora → **janela lenta = janela dos glucosinolatos**, que\n'
        'viram **H₂S** (cheiro de ovo podre, normal). O açúcar da maçã antecipa o ácido, e **o pH é\n'
        'quem regula a mirosinase** — ácido mais cedo, cheiro mais curto. Extra: os dois **boiam**,\n'
        'e o florete **prende ar** (ar = mais H₂S); e o pote **cheira pior do que come**.\n'
        '**Sem original PT.** É a **2ª couve-flor** (#5) — o #5 ensina floretes/2,5%/massagem,\n'
        'este ensina o cheiro. Postar depois do #5, em outra semana.\n\n'
        'Plano em `guias/plano-de-postagem.md`; upload em `guias/guia-de-upload.md`.',
    ),
    (
        'contagem de mp4',
        '- **Com mp4 — 18 dos 19.**',
        '- **Com mp4 — 19 dos 20.**',
    ),
    (
        'licao do claro-sobre-claro',
        '  Medir com `_amostrar-png.py <png> x,y x,y` (PIL no venv\n'
        '  `~/.workbuddy-ai/binaries/python/envs/default`). **Abaixo de ~130 não se lê.**',
        '  Medir com `_amostrar-png.py <png> x,y x,y` (PIL no venv\n'
        '  `~/.workbuddy-ai/binaries/python/envs/default`). **Abaixo de ~130 não se lê.**\n'
        '  No #20 foi o inverso do #18: **claro sobre claro**. Florete creme `#faf8ee` sobre o\n'
        '  círculo `#d8e3bd` deu **45** — a couve-flor virou mancha sem forma. O conserto NÃO foi\n'
        '  escurecer o fundo: foi dar **contorno** ao florete (`#93a663`, 2,5 px), que é o que\n'
        '  define a forma (147). Círculos sobrepostos COM contorno leem como floretes individuais —\n'
        '  que é literalmente o que couve-flor é.',
    ),
    (
        'licao do jarro deitado',
        '- **Filtro que esconde trabalho é pior que filtro nenhum.**',
        '- **Contentor mais LARGO que ALTO não lê como pote — lê como caixa.** O jarro herdado do\n'
        '  #18 media 208×168 (deitado). Nem salmoura mais clara nem base de vidro consertaram: o\n'
        '  olho lia caixa verde. O conserto foi a **proporção** — 156×224, mais alto que largo, com\n'
        '  uma base de vidro aparecendo. Antes de ajustar cor, conferir a **silhueta**.\n'
        '- **Filtro que esconde trabalho é pior que filtro nenhum.**',
    ),
    (
        'pendencia do PT do #20',
        '- **O #19 (beterraba + alho) não tem original PT** — idem.',
        '- **O #19 (beterraba + alho) não tem original PT** — idem.\n'
        '- **O #20 (couve-flor + maçã) não tem original PT** — idem.',
    ),
]

LOG_TEXTO = """

---

## 🥦 #20 — couve-flor + maçã (o cheiro não é defeito, é química) — 19/09

Pedido: *"ok.. mais faca fermentacao ...de couve flor..com com maca .."* (resposta em PT-BR —
o usuário escreveu em português e não pediu inglês desta vez).

**Substância (pesquisada, não inventada).** Duas fontes: fermenthive.com e sourchad.com
(químico analítico). O #5 já ensina floretes, quebrar com a mão, 2,5% de sal, massagem e
7–10 dias — então **este vídeo não repete nada disso**. O assunto é a maçã e o enxofre:

- couve-flor é **90% água**, parede celular **densa**, quase sem açúcar → a bactéria demora
  a pegar (5–7 dias, contra 3–5 do repolho). **O começo lento é o problema.**
- nessa janela lenta os **glucosinolatos** encontram a **mirosinase** e viram isotiocianatos
  e **H₂S** — o cheiro de ovo podre. É normal, não é podridão.
- **o pH regula a mirosinase.** Ácido mais cedo = janela do enxofre mais curta.
- **a maçã é um STARTER, não um sabor:** açúcar para a bactéria, e levedura na casca.
- os floretes têm superfície irregular e **prendem bolha de ar**; ar = mais H₂S. Por isso a
  couve-flor flutua **e** segura ar — pior que quase todo legume.
- **o pote cheira pior do que come:** é H₂S acumulado. Abrir e esperar 5 minutos resolve.
- 2,5% de sal (25 g/L), pH alvo 3,6–4,0, 18–20 °C.

**Feito com** `_criar-couveflor-maca.py` a partir do template do **#18** (cenoura + maçã) —
mesmo conceito "legume + maçã", a maçã já desenhada, validador limpo. O **desenho da couve-flor**
veio do #5: nuvem de círculos creme + folhas verdes + talo. Extração das cenas por **regex**
(evita adivinhar indentação), não por âncora escrita à mão.

### 🐛 Três defeitos, todos achados OLHANDO o render

1. **Floretes pálidos demais.** Creme `#faf8ee` sobre o círculo `#d8e3bd` a .6 → **distância
   45** (limiar ~130). A couve-flor saiu como mancha clara sem forma. O conserto **não** foi
   escurecer o fundo — foi dar **contorno** (`#93a663`, 2,5 px): **147**. E os círculos
   sobrepostos com contorno passaram a ler como floretes individuais. É o **inverso** do #18,
   onde o problema era escuro-sobre-claro.
2. **O pote lia como CAIXA VERDE.** A salmoura ia até y=100 de um jarro que acaba em 110 —
   sobrava vidro invisível, e a tampa (`#c9d9a4`) fica a distância 31 da salmoura, então sumia.
3. **A causa real do nº 2: o jarro era mais LARGO que ALTO** (208×168 — deitado). Nenhuma cor
   conserta isso. Refiz como **156×224**, mais alto que largo, com base de vidro aparecendo.
   **Antes de mexer em cor, conferir a silhueta.**

**mp4:** `couve-flor/shorts-cauliflower-apple-en.mp4` — 1080×1920, H.264, **43,8 s**,
**1270/1314 quadros (97%)**, 5,1 MB, **29,0 q/s** constante. Bruto 112,8 s com `--passo=60`.
Conferido **tocando**: 8 quadros, rótulos `CAULI+APPLE n / 7`, barra sem repetir o título.

**Registrado em 3 lugares:** a pasta, a galeria (44 shorts, 0 bugs) e o pacote
(`_registrar-couveflor-maca.py`, 6 âncoras → entrada **#20**) + o plano
(`_registrar-couveflor-maca-plano.py`, 3 âncoras → Semana 12).

**A ressalva escrita nos dois guias:** é a **2ª couve-flor** (#5). Passa porque não repete
nenhum ensinamento do #5 — mas postar **depois do #5 e em outra semana**.

**Ficou pendente:** o original PT do #20.
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
        print('   %-34s casou %d vez(es)' % (rotulo, q))
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
    with io.open(MEM + '.antes-do-20', 'w', encoding='utf-8', newline='') as fh:
        with io.open(MEM, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(MEM, 'w', encoding='utf-8', newline='') as fh:
        fh.write(novo)
    print('gravado: %s' % MEM)

    with io.open(LOG, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    if '#20 — couve-flor + maçã' in d:
        print('log: ja tinha a secao, nao dupliquei')
    else:
        with io.open(LOG, 'a', encoding='utf-8', newline='') as fh:
            fh.write(LOG_TEXTO.replace('\n', eol))
        print('gravado: %s (acrescentado)' % LOG)
    return 0


if __name__ == '__main__':
    sys.exit(main())

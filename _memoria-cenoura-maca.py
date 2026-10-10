# -*- coding: utf-8 -*-
"""
_memoria-cenoura-maca.py — atualiza a memoria do projeto com o video novo.

Mexe em DOIS arquivos:
  .workbuddy-ai/memory/MEMORY.md      (estado do projeto — reescrito por ancoras)
  .workbuddy-ai/memory/2026-09-19.md  (log do dia — acrescentado no fim)

Regra do usuario: varias edicoes no MESMO arquivo so com contagem e abortando
sem gravar se alguma ancora nao casar. E' o que este script faz.
"""
import io
import sys

MEM = '.workbuddy-ai/memory/MEMORY.md'
LOG = '.workbuddy-ai/memory/2026-09-19.md'

# ------------------------------------------------------------- MEMORY.md
ANCORAS_MEM = [
    (
        'titulo do catalogo',
        '## 📊 Catálogo — 18 vídeos',
        '## 📊 Catálogo — 18 entradas no pacote',
    ),
    (
        'paragrafo do catalogo',
        '13 no pacote `guias/pacote-legendas-descricoes-en.md` + **#14** `cores/shorts-3-colors-en`\n'
        '+ **#15** `brocolis/shorts-broccoli-orange-en` + **#16** `mosquito/shorts-mosquito-trap-en`\n'
        '(**side track, não é fermentação**) + **#17** `pepino/shorts-pepino-apple-en`\n'
        '+ **#18** `pepino/shorts-pepino-speed-en`.',
        'A numeração que os guias usam é a da tabela "WHICH FILE TO RECORD" de\n'
        '`guias/pacote-legendas-descricoes-en.md` — **#1 a #18**. Fora dela só existem\n'
        '**variantes de estilo** (mesmo vídeo, outra casca). `mosquito/shorts-mosquito-trap-en`\n'
        'é **side track, não é fermentação**.',
    ),
    (
        'entrada do #18 (cenoura + maca)',
        'Plano em `guias/plano-de-postagem.md`; upload em `guias/guia-de-upload.md`.',
        '**#18 — cenoura + maçã** (`cenoura/shorts-carrot-apple-en.html`, 19/09, 42,8 s, 7 cenas):\n'
        'o que o açúcar faz num legume **denso** — 4 a 5 dias em vez de 5 a 7, jarro com gás, e o\n'
        'aviso honesto de **0,5–2% de álcool** (fermentação de fruta não é sauerkraut). Nasceu do\n'
        'template do #17 (`pepino/shorts-pepino-apple-en`), por `_criar-cenoura-maca.py`.\n'
        '**Sem original PT.** É **legume repetido** (a cenoura já é o #12) — o pacote e o plano\n'
        'explicam por que mesmo assim vale, e obrigam a postar **depois do #12**.\n\n'
        'Plano em `guias/plano-de-postagem.md`; upload em `guias/guia-de-upload.md`.',
    ),
    (
        'contagem de mp4',
        '**Com mp4 — 16 dos 17.**',
        '**Com mp4 — 17 dos 18.**',
    ),
    (
        'regra do da-pra-ver nao e medida',
        '- **Layout e cor não se veem com grep** — renderizar e olhar é obrigatório\n'
        '  (`_revisar-cenas.py <arq> --final`). `--no-anim` só serve para provar o bug do `transform=`.',
        '- **Layout e cor não se veem com grep** — renderizar e olhar é obrigatório\n'
        '  (`_revisar-cenas.py <arq> --final`). `--no-anim` só serve para provar o bug do `transform=`.\n'
        '- **"Dá pra ver" não é medida — medir o pixel.** O pote do #18 saiu com a salmoura\n'
        '  `#fac775` a `opacity=".7"` sobre jarro creme: **distância 95** contra **132** do\n'
        '  template, e o pote parecia **vazio** numa cena que diz "everything under the brine".\n'
        '  Medir com `_amostrar-png.py <png> x,y x,y` (PIL no venv\n'
        '  `~/.workbuddy-ai/binaries/python/envs/default`). **Abaixo de ~130 não se lê.**',
    ),
    (
        'pendencia do PT do #18',
        '- **O PT do #4 (melancia + beterraba) não tem o aviso de álcool** que o EN ganhou.',
        '- **O PT do #4 (melancia + beterraba) não tem o aviso de álcool** que o EN ganhou.\n'
        '- **O #18 (cenoura + maçã) não tem original PT** — nasceu em inglês (19/09).',
    ),
]

# ---------------------------------------------------------------- log do dia
LOG_TEXTO = """

---

## 🥕 #18 — cenoura + maçã (o que o açúcar faz num legume denso) — 19/09

Pedido: *"um video de fermentacao de maca com cenoura ... em inglish"* (resposta em inglês).

**Substância (pesquisada, não inventada):** a cenoura é **densa e pobre em açúcar** → lenta,
5–7 dias, quase sem gás. A maçã traz **duas** coisas: **açúcar** (as bactérias comem) e
**levedura selvagem da casca** (é o que faz as bolhas). Resultado: **4–5 dias** e jarro com
gás. Regras próprias: **corte a cenoura FINA e a maçã GROSSA** (denso precisa de área;
maçã amolece rápido); **a maçã BOIA** — o que fica acima da salmoura é onde nasce mofo.
Nota honesta que virou a cena 7: fermentação de fruta chega a **0,5–2% de álcool**, contra
quase zero de um chucrute pobre em açúcar. Se o jarro espuma muito, não é só CO₂.

**Feito com** `_criar-cenoura-maca.py` (13 âncoras, todas casaram de primeira), a partir do
**template do #17** (`pepino/shorts-pepino-apple-en.html`) — mesmo conceito "legume + maçã",
a maçã já estava desenhada. O template da cenoura (`shorts-cenoura-animado-en`) é do estilo
antigo, mais pobre; **não usar**.

**Dois defeitos achados olhando o render — nenhum deles o validador pega:**

1. **A salmoura estava invisível.** `#fac775` a `opacity=".7"` sobre um jarro creme
   `#fdf9f2` dá `#fbd69a`: **distância 95** do jarro. O template do pepino tem **132**
   (`#83d6b9` sobre `#f4faf3`). A cena 4 diz *"everything under the brine"* e o pote
   parecia **vazio** — a mensagem se perdia. A **ordem de desenho estava certa**; era
   contraste. Conserto (`_consertar-salmoura-cenoura.py`): jarro → `#fffdf7`, salmoura
   `#fac775` a **opacidade 1**, palitos → `#e0801f`/`#8a4b12`. Depois: **142** contra o
   jarro, **114** contra os palitos. O `_validar-short.py` passou limpo ANTES e DEPOIS —
   ele mede coordenada, não contraste.
2. **Verde do pepino sobrou no vídeo da cenoura.** A pílula da cena 5 (`#e1f5ee`/`#1d9e75`)
   e o jato da cena 2 (`#5dcaa5`) continuavam na cor do template. O projeto tem regra de
   **cor por ingrediente, para os vídeos não ficarem iguais no feed** — pílula verde num
   vídeo de cenoura faz o short parecer re-skin. Conserto
   (`_consertar-paleta-cenoura.py`): pílula → âmbar `#faeeda`/`#ba7517`/`#4a2606`, jato →
   azul `#378add` (a cena 2 é a cena da água). **A folha da cenoura ficou verde** — é de
   propósito.

**Ferramenta nova:** `_amostrar-png.py` — mede a cor de verdade num PNG em vez de confiar
no olho. Foi ele que provou o defeito 1 (e provou o conserto). Fica na raiz.

**mp4:** `cenoura/shorts-carrot-apple-en.mp4` — 1080×1920, H.264, **42,8 s**, **1258/1284
quadros (98%)**, 5,0 MB, 29,4 q/s constante. Bruto 97,0 s com `--passo=60`. Conferido
**tocando**: 8 quadros extraídos, rótulos `CARROT n / 7` corretos, sem "undefined".

**Registrado em 3 lugares:** a pasta, a galeria (`_gerar-galeria.py` → 43 shorts, 0 bugs)
e o pacote de publicação (`_registrar-cenoura-maca.py`, 6 âncoras) + o plano
(`_registrar-cenoura-maca-plano.py`, 3 âncoras). O pacote ganhou uma nota obrigatória na
seção VARIANTS: **#18 é legume repetido** (a cenoura já é o #12) — só postar **depois do
#12**, senão vira "a mesma cenoura duas vezes".

**Ficou pendente:** o original PT do #18 (nasceu em inglês).
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
    novo_mem = troca(MEM, ANCORAS_MEM)
    if novo_mem is None:
        return 1
    with io.open(MEM + '.antes-do-18', 'w', encoding='utf-8', newline='') as fh:
        with io.open(MEM, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(MEM, 'w', encoding='utf-8', newline='') as fh:
        fh.write(novo_mem)
    print('gravado: %s' % MEM)

    # log do dia — so' acrescenta
    with io.open(LOG, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    if '#18 — cenoura + maçã' in d:
        print('log: ja tinha a secao, nao dupliquei')
    else:
        with io.open(LOG, 'a', encoding='utf-8', newline='') as fh:
            fh.write(LOG_TEXTO.replace('\n', eol))
        print('gravado: %s (acrescentado)' % LOG)
    return 0


if __name__ == '__main__':
    sys.exit(main())

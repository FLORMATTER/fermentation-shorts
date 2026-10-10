# -*- coding: utf-8 -*-
"""
Duas correcoes na skill shorts-svg-animado, achadas ao revisar o video #15:

1. O render comum (--virtual-time-budget) NAO e "sempre 0%": e INCONSISTENTE.
   Mesmo arquivo, texto visivel numa rodada e em branco na outra.
2. A folha do _revisar-cenas.py extrai so os <svg class="scene"> — ela NAO mostra
   o .tag, que e justamente onde mora o bug de traducao mais grave da serie.
"""
import io, os, shutil, sys

ARQ = os.path.join(os.path.expanduser('~'), '.workbuddy-ai', 'skills',
                   'shorts-svg-animado', 'SKILL.md')

TROCAS = [
    # 1 — o render comum e inconsistente, nao "sempre 0%"
    ("""> Ele é inútil para isso: o PNG sai sempre no estado **0%**, e como os elementos de texto
> usam `animation-fill-mode: both` eles aparecem **invisíveis** — parece bug do arquivo e
> não é. A única forma confiável de congelar a animação é **injetar CSS antes de capturar**:""",
     """> Ele é inútil para isso: o PNG costuma sair no estado **0%**, e como os elementos de texto
> usam `animation-fill-mode: both` eles aparecem **invisíveis** — parece bug do arquivo e
> não é.
>
> 🔴 **E não é confiável nem para dizer "está ok".** O resultado é **inconsistente**: o
> mesmo arquivo pode sair com o texto visível numa rodada e em branco na seguinte. Visto
> em 17/09 — as cenas 2 e 3 de `brocolis/shorts-broccoli-orange-en.html` saíram **sem
> texto nenhum** na rodada com `--cols 2` e **com todo o texto** na rodada com `--cols 4`,
> sem uma linha ter mudado. **Nunca concluir nada do render comum** — nem "quebrou" nem
> "está ok". Para conferir texto, só `--final` ou `--no-anim`.
>
> A única forma confiável de congelar a animação é **injetar CSS antes de capturar**:""", 1),

    # 2 — a folha de revisao nao mostra o .tag
    ("""**cenas 2 em diante** ficam no idioma original. Aconteceu em **73 rótulos de 12
arquivos** numa série de 15.""",
     """**cenas 2 em diante** ficam no idioma original. Aconteceu em **73 rótulos de 12
arquivos** numa série de 15.

> ⚠️ **O render NÃO mostra o `tag:` — e é por isso que ele passa batido.** A folha do
> `_revisar-cenas.py` extrai **só** os `<svg class="scene">`. O `.tag`, a marca d'água
> (`@handle`), a barra de legenda (`.cap`), a capa e os botões são HTML **por cima** e
> **não aparecem na folha**; a faixa vermelha pontilhada só marca onde a legenda vai
> entrar (`y = 647..720`). Ou seja: a regra "renderize e olhe" **não cobre este campo**.
> Para conferir o `tag:` a única via é ler o array `scenes` no `<script>` — ou o grep
> abaixo.""", 1),
]

with io.open(ARQ, 'r', encoding='utf-8') as f:
    d = f.read()

antes = len(d)
for ancora, novo, n in TROCAS:
    c = d.count(ancora)
    if c != n:
        print('ABORTADO — a ancora casou %d vez(es), esperava %d:' % (c, n))
        print('   ' + repr(ancora[:90]))
        sys.exit(1)

for ancora, novo, n in TROCAS:
    d = d.replace(ancora, novo, n)

bk = ARQ + '.antes-do-video15'
if not os.path.exists(bk):
    shutil.copy2(ARQ, bk)
    print('backup  ->', bk)

with io.open(ARQ, 'w', encoding='utf-8', newline='') as f:
    f.write(d)

# integridade: nenhum byte NUL, contagem de cercas de codigo estavel
nul = d.count('\x00')
print('OK — %d trocas  (%d -> %d bytes)  NUL=%d  cercas=%d'
      % (len(TROCAS), antes, len(d), nul, d.count('```') // 2))
if nul:
    sys.exit(1)

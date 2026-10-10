# -*- coding: utf-8 -*-
"""
Adiciona a secao da GALERIA na skill, logo antes do A/B de render.

1 ancora com contagem: se nao casar 1 vez, ABORTA SEM GRAVAR.
"""
import io, os, shutil, sys

S = os.path.expanduser('~/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md')
d = io.open(S, encoding='utf-8').read()
ANTES = len(d)

ANCORA = '## \U0001f9ea Provar que um refactor n\u00e3o mudou nada \u2014 A/B de render\n'

NOVO = """## \U0001f5bc\ufe0f A galeria (`_gerar-galeria.py`) \u2014 o 3\u00ba lugar do registro

```bash
python _gerar-galeria.py        # -> galeria-shorts.html
```

Varre as pastas de `ORDEM` + `aulas` + `guias`, **so' `.html`**, e monta o catalogo visual.
**Video novo entra em 3 lugares** \u2014 a pasta, o pacote + plano, e **aqui**. Esquecer a
galeria e' o erro mais facil de cometer, porque ela nao quebra: fica velha.

**Armadilha 1 \u2014 os numeros do topo saem de uma tupla `%` e trocam em silencio.** Em 26/09 o
alerta mostrou *"66 dos shorts ja tem .mp4"* e o lead mostrou *"27 arquivos HTML+SVG"*: os
dois argumentos estavam **invertidos**, e cada frase ficou com o numero da outra. Um numero
errado que "parece plausivel" passa. **Conserto:** o gerador agora tem autochecagem antes de
gravar \u2014 confere a frase do alerta, confere `html.count('class="b mp4"') == com_mp4` e a
frase do lead. Dispara `SystemExit` **antes** de escrever o arquivo.

**Armadilha 2 \u2014 `cap:`/`sub:` vem do JS e trazem `\\uXXXX` cru.** A galeria imprimia
`2% salt \\u00b7 ready...` em vez de `2% salt \u00b7 ready...` (3 de 55 subs). **Conserto:** o
`_unesc()` decodifica ao extrair.

**Armadilha 3 \u2014 o alerta mentia sobre o mp4.** Dizia "nao existem arquivos `.mp4` neste
projeto" e mandava gravar com OBS, quando o `_gerar-mp4.js` ja' gera os `.mp4`. Agora ele
**conta** quantos shorts tem mp4 e cada cartao ganha o selo **`.mp4 pronto`**.

> \u26a0\ufe0f **Para PROVAR uma guarda da galeria, a copia defeituosa tem de rodar na RAIZ do
> projeto.** `RAIZ = os.path.dirname(os.path.abspath(__file__))` \u2014 uma copia em
> `_revisao/` varre **0 shorts**, os dois numeros empatam em **0** e a guarda parece cega
> (foi um falso "guarda NAO provada" em 26/09). Redirecionar a `SAIDA` da copia para
> `_revisao/` e deixar o `.py` na raiz.

"""

n = d.count(ANCORA)
if n != 1:
    print('ERRO: ancora casou %d vez(es), esperado 1. Nada gravado.' % n)
    sys.exit(1)

d = d.replace(ANCORA, NOVO + ANCORA)

for t in ['A galeria (`_gerar-galeria.py`)', 'Armadilha 1', 'Armadilha 3',
          'tem de rodar na RAIZ']:
    if t not in d:
        print('ERRO: trecho novo ausente: %r. Nada gravado.' % t)
        sys.exit(1)

if len(d) <= ANTES:
    print('ERRO: nao cresceu. Nada gravado.')
    sys.exit(1)

shutil.copy2(S, S + '.antes-da-galeria')
with io.open(S, 'w', encoding='utf-8', newline='') as f:
    f.write(d)
print('OK: %d -> %d chars (+%d)' % (ANTES, len(d), len(d) - ANTES))

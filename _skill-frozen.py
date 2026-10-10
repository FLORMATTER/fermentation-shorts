# -*- coding: utf-8 -*-
"""
Corrige a skill `shorts-svg-animado` com as licoes do #26 (23/09/2026):

A. O comentario do FINAL_CSS afirmava que o `-1s` trava no keyframe de 100%. FALSO para
   animacao > 1 s. Corrigido.
B. Bloco novo: em que ponto o `--final` congela (medido) + a regra "contraste se julga
   com --no-anim" + o `_frozen-final.py`.
C. Item 4 na lista dos furos do regex de bloco: o lookahead prescrito no item 1 tambem
   falha, porque ENTRE CENAS HA UMA LINHA DE COMENTARIO.

Padrao do projeto: ancora com contagem esperada, ABORTA SEM GRAVAR se nao casar.
"""
import io
import os
import re
import sys

ALVO = os.path.join(os.path.expanduser('~'), '.workbuddy-ai', 'skills',
                    'shorts-svg-animado', 'SKILL.md')

# ---------------------------------------------------------------- textos novos

BLOCO_CONGELA = """\
>
> 🔴 **O `-1s` não põe o elemento no fim — põe no segundo 1.** Com `fill: both` ele só
> chega ao keyframe de 100% se a animação durar **1 s ou menos**. Medido com
> `python _frozen-final.py <arquivo>`: no template `cenoura/shorts-carrot-apple-en.html`
> **9 das 10** animações não terminam (o `wobble 2.4s` para em **41,7%**, o `tick 2.2s`
> em **45,5%**); no `kombucha/shorts-beet-watermelon-en.html` são **14 de 14** (o
> `pour2x 1.6s` para em **62,5%**).
>
> **Consequência prática:** um elemento no meio de um fade-in sai **apagado / fantasma**
> no PNG do `--final`, e **não há defeito nenhum no arquivo**. Aconteceu em 23/09 com a
> xícara de açúcar do #26: o `--final` mostrou um copo quase invisível, eu quase escrevi
> um conserto de contraste — e o `--no-anim` mostrou a xícara **perfeita**.
>
> **Regra:** `--final` julga **LAYOUT** (onde cada coisa está). **Contraste e presença**
> se julgam com `--no-anim`, e ele vem **antes** de chamar qualquer coisa de defeito.
>
> ```bash
> python _frozen-final.py <arquivo.html>   # em que % do timeline o --final para cada animação
> ```
"""

ITEM4 = """\
4. **Ancorar no SEPARADOR, não no nome do próximo `def`.** Entre duas cenas há **uma linha
   de comentário** (`\\n\\n# ---- cena 3: ...`), então o lookahead `(?=\\n\\ndef s2\\()` do item 1
   **também nunca casa** — foi a **4ª vez** que esse mesmo erro custou uma rodada. O padrão
   que funciona **sem saber o nome do próximo bloco**:
   ```python
   def bloco(nome):
       return re.compile(r'def %s\\(t\\):.*?\\n(?=\\n\\n(?:#|TEXTOS))' % nome, re.S)
   d = bloco('s1').sub(lambda m: novo + eol, d, count=1)   # repõe o \\n consumido
   ```
   **E o `\\n` que o `.*?\\n` come:** a substituição tem de **repor** esse `\\n`
   (`novo + eol`), senão as cenas colam uma na outra.
"""

# ---------------------------------------------------------------- edicoes

EDICOES = [
    # A. o comentario errado
    (r'# adianta 1s e pausa -> com fill:both (ou forwards) o elemento trava no keyframe de 100%',
     r"# adianta 1s e pausa -> trava no 100% SO' se a animacao durar <= 1s (ver _frozen-final.py)",
     1),

    # B. o bloco do ponto de congelamento
    (r'É o modo **`--final`** do `_revisar-cenas.py` (`--no-anim` continua sendo o outro extremo,'
     '\n'
     r'com `animation:none`, para o diagnóstico do bug (f)).',
     r'É o modo **`--final`** do `_revisar-cenas.py` (`--no-anim` continua sendo o outro extremo,'
     '\n'
     r'com `animation:none`, para o diagnóstico do bug (f)).'
     '\n'
     + BLOCO_CONGELA.rstrip('\n'),
     1),

    # C. item 4 na lista dos furos do regex de bloco
    (r'   COMPLETO, escrito por extenso**, em vez de montar um generico com `%`.'
     '\n'
     '\n'
     r'**E o `%` do Python:**',
     r'   COMPLETO, escrito por extenso**, em vez de montar um generico com `%`.'
     '\n'
     '\n'
     + ITEM4.rstrip('\n')
     + '\n'
     '\n'
     r'**E o `%` do Python:**',
     1),
]


def main():
    if not os.path.exists(ALVO):
        print('ABORTA: nao achei %s' % ALVO)
        return 1

    with io.open(ALVO, encoding='utf-8', newline='') as f:
        d = f.read()
    antes_chars = len(d)
    antes_bytes = len(d.encode('utf-8'))
    eol = '\r\n' if d.count('\r\n') > d.count('\n') / 2 else '\n'
    print('arquivo : %s' % ALVO)
    print('eol     : %r' % eol)
    print('antes   : %d chars / %d bytes' % (antes_chars, antes_bytes))
    print()
    for old, new, esperado in EDICOES:
        n = d.count(old)
        if n != esperado:
            print('ABORTA: ancora casou %d vez(es), esperava %d:' % (n, esperado))
            print('   %r' % old[:100])
            return 1
        d = d.replace(old, new, esperado)
        print('  ok  %d vez(es)  <- %r' % (n, old[:62].replace('\n', ' ')))

    # checagem final
    for bom in ('_frozen-final.py', 'Ancorar no SEPARADOR', '62,5%', '41,7%'):
        if bom not in d:
            print('ABORTA: nao achei %r no resultado' % bom)
            return 1
    if 'trava no keyframe de 100%' in d:
        print('ABORTA: a afirmacao errada continua no arquivo')
        return 1

    tmp = ALVO + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(d)
    os.replace(tmp, ALVO)

    print()
    print('gravado: %d -> %d bytes (+%d)'
          % (antes_bytes, len(d.encode('utf-8')),
             len(d.encode('utf-8')) - antes_bytes))
    return 0


if __name__ == '__main__':
    sys.exit(main())

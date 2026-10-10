# -*- coding: utf-8 -*-
"""_skill-kvass.py — 2 edicoes contadas na SKILL.md (as armadilhas do #28).

Uso:  python _skill-kvass.py            # dry-run
      python _skill-kvass.py --apply
"""
import io
import sys

ALVO = 'C:/Users/Saxa/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md'

CABECALHO_VELHO = '### 🔴 Os 4 furos do gerador (custaram retrabalho no #27)'

CABECALHO_NOVO = ('### 🔴 Armadilhas do gerador\n'
                  '\n'
                  '*Sem contagem no titulo de proposito: a lista so\' cresce.*')

FIM_VELHO = """4. **`compile(d, ALVO, 'exec')` antes de gravar.** Pega indentação e parêntese
   desbalanceado por centavos — e o **gerador é a fonte da verdade**: todo conserto feito
   por script tem de voltar para ele."""

FIM_NOVO = """4. **`compile(d, ALVO, 'exec')` antes de gravar.** Pega indentação e parêntese
   desbalanceado por centavos — e o **gerador é a fonte da verdade**: todo conserto feito
   por script tem de voltar para ele.

5. **Token de desenho SEM grupo de posição desenha na ORIGEM.** Um `@SAL@` solto no
   corpo da cena (sem `<g transform="translate(...)">` em volta) põe o desenho no canto
   superior esquerdo do cartão — e nada acusa: o validador, o contador de keyframe e o
   guarda de token passam todos. **Todo `@DESENHO@` entra dentro de um grupo com
   `translate`.** (No #28 o `@SAL@` ficou solto e o sal cairia no canto.)

6. **Objeto solto AO LADO do sujeito lê como coisa nenhuma.** A tampa+airlock do #28
   ficou em `translate(300,344)`, ao lado do jarro, e no render virou **cogumelo/êmbolo**.
   Objeto que pertence a outro **encosta nele** (a tampa na boca do jarro). E se o sujeito
   está dentro de um grupo animado, o objeto vai **DENTRO do mesmo grupo**: o `wobble` é
   `rotate(±2.5deg)`, então fora dele a tampa **descola a cada ciclo**.
   Para casar a largura: `48 × 0.93 = 44.6 = 62 × 0.72` (escala do objeto × escala do
   sujeito).

7. **Desenho dentro de painel: medir a CAIXA, não confiar no olho.** Os cubos do #28 iam
   até `y=72` num painel que acaba em `64` — 8 px de vazamento, invisível na folha de
   contato e óbvio no zoom. Antes de fechar um painel de ±N, conferir o maior `x`/`y` do
   desenho contra N."""

TRABALHO = [(CABECALHO_VELHO, CABECALHO_NOVO, 1), (FIM_VELHO, FIM_NOVO, 1)]


def main():
    aplicar = '--apply' in sys.argv
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d)

    for velho, _, esperado in TRABALHO:
        n = d.count(velho)
        print('  %-58s %d vez(es) (esperava %d)'
              % (velho.strip().split('\n')[0][:58], n, esperado))
        if n != esperado:
            print('ABORTA: nada foi gravado.')
            return 1
    for velho, novo, _ in TRABALHO:
        d = d.replace(velho, novo, 1)

    for trecho in ('Armadilhas do gerador', 'desenha na ORIGEM',
                   'lê como coisa nenhuma', 'medir a CAIXA'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" depois da troca.' % trecho)
            return 1
    if 'Os 4 furos do gerador' in d:
        print('ABORTA: o cabecalho velho continua la.')
        return 1

    print('  %s %d -> %d bytes' % (ALVO.split('/')[-1], antes, len(d.encode('utf-8'))))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: 3 armadilhas novas na skill.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

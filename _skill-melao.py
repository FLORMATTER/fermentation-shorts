# -*- coding: utf-8 -*-
"""_skill-melao.py — 2 inserts contados no SKILL.md da skill shorts-svg-animado.

Insere:
  1. a licao de FORMA do melao (as suturas, nao a rede);
  2. a licao do NUMERO que nao fecha com a conta (erro do #24).

O arquivo e' editado UMA vez, por script com contagem — duas edicoes no mesmo
arquivo na mesma mensagem se sobrescrevem.

    python _skill-melao.py
"""
import io
import os
import sys

SKILL = os.path.expanduser('~/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md')

FORMA = '''**Melão inteiro ≠ bola com grade.** A 1ª versão era bege com uma **grade simétrica** e leu
como **waffle / bola de tênis**; a 2ª, bola lisa, leu como **bola**; a 3ª, marrom uniforme,
como **kiwi**; a 4ª, laranja demais, como **laranja**. O que faz ler "melão" **não é a
rede** — são as **SUTURAS**: as lombadas que correm de cima a baixo e dão a forma. Com elas
a rede pode ser **esparsa e ondulada** (que é como o cantalupo realmente parece) em vez de
grade. E a faca: lâmina estreita lê como **termômetro** — alargar.

'''

NUMERO = '''### 🔢 Número no cartão tem de fechar com a CONTA

Um selo pode estar bonito, caber na caixa e ainda estar **errado**. O #24 estampava
**"ABOUT 1800 TIMES MORE ACID"** enquanto o próprio cartão mostrava **3.0** e **6.4** —
a conta é 10^(6,4−3,0) = 10^3,4 ≈ **2500**. Ninguém vê isso com grep: o texto existe, o
tamanho cabe, o validador passa. **Ao escrever um número derivado, calcular e conferir
contra os outros números que estão na MESMA tela** — e conferir a frase de apoio também
(o subtítulo "3 points is a thousand" não batia com 3,4 pontos).

'''

# (ancora, texto a PREPOR, quantas vezes)
INSERTS = (
    ('**A regra que fica:** quando o desenho "não parece", **não é a cor** — é a **forma**, e forma',
     FORMA, 1),
    ('### 🔧 Trocar um BLOCO de função no gerador — dois furos de regex',
     NUMERO, 1),
)


def main():
    with io.open(SKILL, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d.encode('utf-8'))

    # --- 1) confere todas as ancoras antes de gravar
    for ancora, texto, n in INSERTS:
        achou = d.count(ancora)
        if achou != n:
            print('ERRO: ancora casou %d vez(es), esperava %d:\n  %s'
                  % (achou, n, ancora[:70]))
            return 1

    # --- 2) aplica
    for ancora, texto, n in INSERTS:
        d = d.replace(ancora, texto + ancora, n)
        print('  ok: +%d bytes antes de "%s..."' % (len(texto.encode('utf-8')), ancora[:40]))

    # --- 3) sanidade: as ancoras continuam la', e o tamanho cresceu
    for ancora, _, _ in INSERTS:
        if d.count(ancora) != 1:
            print('ERRO: a ancora sumiu/duplicou depois da troca')
            return 1
    if len(d.encode('utf-8')) <= antes:
        print('ERRO: o arquivo nao cresceu')
        return 1

    with io.open(SKILL, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: 2 inserts | %d -> %d bytes' % (antes, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())

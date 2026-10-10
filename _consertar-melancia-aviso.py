"""_consertar-melancia-aviso.py — poe o AVISO DE ALCOOL no short beterraba+melancia.

O problema: o pacote de publicacao abre com "I fermented beetroot with watermelon
— and it turned into ALCOHOL" e marca o video como "o mais perigoso da serie,
aviso obrigatorio". Mas o VIDEO nunca diz a palavra: ele termina em
"Purple, sweet and tangy / but do not let it go past day 3". Titulo e video nao
combinam — quem clicar por causa do titulo nao ve o aviso.

Tres trocas, com contagem exata. Aborta sem gravar se qualquer ancora nao casar
exatamente uma vez.
"""
import shutil
import sys

ARQ = 'beterraba/shorts-beterraba-melancia-en.html'

TROCAS = [
    # 1. o porque da pressa: melancia e' quase toda agua e acucar
    ("sub:'watermelon ferments VERY fast'",
     "sub:'watermelon is all water and sugar'"),
    # 2. a barra de legenda passa a carregar o aviso
    ("cap:'It turned purple and sweet', sub:'do not let it go past day 3'",
     "cap:'Then it turns into alcohol', sub:'if it smells like alcohol, you went too far'"),
    # 3. e o desenho tambem (a linha de baixo do cartao da cena 7)
    ('>but do not let it go past day 3</text>',
     '>past day 3 it becomes alcohol</text>'),
]

d = open(ARQ, encoding='utf-8', newline='').read()
orig = d
for i, (velho, novo) in enumerate(TROCAS, 1):
    n = d.count(velho)
    print('troca %d: casou %d vez(es)' % (i, n))
    if n != 1:
        print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
        sys.exit(1)
    d = d.replace(velho, novo, 1)

assert d != orig
shutil.copyfile(ARQ, ARQ + '.antes-do-aviso-alcool')
open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %s (%d -> %d bytes)' % (ARQ, len(orig), len(d)))
print('backup : %s.antes-do-aviso-alcool' % ARQ)

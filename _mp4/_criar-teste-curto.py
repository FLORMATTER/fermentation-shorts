# _mp4/_criar-teste-curto.py
# Cria uma copia curta do short para MEDIR o render rapido.
# O render de verdade leva ~60 s; este leva ~8 s, entao a iteracao fica 7x mais barata.
# Mantem as 8 cenas (o peso de cada cena e o que importa), so encurta a duracao.
import io, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(RAIZ, 'mosquito', 'shorts-mosquito-trap-en.html')
DEST = os.path.join(RAIZ, '_mp4', 'teste-8s.html')
DIV = 8

with io.open(ORIG, encoding='utf-8') as f:
    d = f.read()

ms = re.findall(r'\bms\s*:\s*(\d+)', d)
assert ms, 'nao achei nenhum ms: no arquivo'
total_antes = sum(int(x) for x in ms)

def troca(m):
    return 'ms:' + str(max(700, int(m.group(1)) // DIV))

novo, n = re.subn(r'\bms\s*:\s*(\d+)', troca, d)
assert n == len(ms), 'substitui %d de %d' % (n, len(ms))

total_depois = sum(int(x) for x in re.findall(r'\bms\s*:\s*(\d+)', novo))
with io.open(DEST, 'w', encoding='utf-8', newline='') as f:
    f.write(novo)

print('cenas com ms: %d' % n)
print('duracao: %.1f s -> %.1f s' % (total_antes / 1000.0, total_depois / 1000.0))
print('escrito: %s (%d bytes)' % (DEST, len(novo.encode('utf-8'))))

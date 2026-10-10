# -*- coding: utf-8 -*-
"""
Prova a autochecagem nova do _gerar-galeria.py contra a versao COM o defeito.

Regra da memoria: "Verificador que nunca falha nao prova nada". E a 1a versao desta
prova deu falso "guarda nao provada" porque rodava a copia em _revisao/ -> o RAIZ vinha
errado, a galeria ficava com 0 shorts e os dois numeros empatavam em 0.

Agora a copia defeituosa fica na RAIZ (RAIZ = pasta do proprio arquivo) e escreve a saida
em _revisao/, para nao passar por cima da galeria boa.
"""
import io, os, subprocess, sys

RAIZ = 'C:/Users/Saxa/Desktop/youtube-work'
PY = 'C:/Users/Saxa/.workbuddy-ai/binaries/python/versions/3.13.12/python.exe'
BOM = os.path.join(RAIZ, '_gerar-galeria.py')
MAU = os.path.join(RAIZ, '_galeria-invertida.py')   # na RAIZ de proposito

CERTO = '""" % (CSS, len(shorts), mmss(total), len(shorts) + len(ignorados), com_mp4,'
ERRADO = '""" % (CSS, len(shorts), mmss(total), com_mp4, len(shorts) + len(ignorados),'
SAIDA_OK = "SAIDA = os.path.join(RAIZ, 'galeria-shorts.html')"
SAIDA_TMP = "SAIDA = os.path.join(RAIZ, '_revisao', 'galeria-invertida.html')"

d = io.open(BOM, encoding='utf-8').read()
for nome, alvo in (('tupla', CERTO), ('SAIDA', SAIDA_OK)):
    if d.count(alvo) != 1:
        print('ERRO: nao achei %s no gerador (%d ocorrencias).' % (nome, d.count(alvo)))
        sys.exit(1)

mau = d.replace(CERTO, ERRADO).replace(SAIDA_OK, SAIDA_TMP)
with io.open(MAU, 'w', encoding='utf-8', newline='') as f:
    f.write(mau)

r = subprocess.run([PY, MAU], cwd=RAIZ, capture_output=True, text=True)
saida = (r.stdout or '') + (r.stderr or '')
print('--- versao COM o defeito (args invertidos) ---')
print('exit=%d' % r.returncode)
print(saida.strip()[:500])

acusa = ('o alerta nao mostra' in saida) or ('o lead nao mostra' in saida) \
        or ('selos no HTML' in saida)
print()
print('A GUARDA ACUSA? %s' % ('SIM' if acusa else 'NAO'))

r2 = subprocess.run([PY, BOM], cwd=RAIZ, capture_output=True, text=True)
saida2 = (r2.stdout or '') + (r2.stderr or '')
print()
print('--- versao boa ---')
print('exit=%d' % r2.returncode)
print(saida2.strip()[:300])
print()
print('A guarda silencia no arquivo bom? %s' % ('SIM' if r2.returncode == 0 else 'NAO'))

os.remove(MAU)
print('(copia defeituosa removida)')

ok = acusa and r.returncode != 0 and r2.returncode == 0
print()
print('RESULTADO: %s' % ('guarda PROVADA' if ok else 'guarda NAO provada'))
sys.exit(0 if ok else 1)

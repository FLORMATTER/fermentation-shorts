# -*- coding: utf-8 -*-
"""
_gerar-galeria.py estava dizendo "nao existem arquivos .mp4 neste projeto" e mandando
gravar com OBS. Falso: existem 28 .mp4 (o proprio _gerar-mp4.js gera, sem OBS).

Conserto no GERADOR (regra 12 da memoria): a galeria passa a (a) marcar no cartao quais
shorts ja tem .mp4 e (b) contar isso no alerta.

5 ancoras com contagem: se qualquer uma nao casar exatamente 1 vez, ABORTA SEM GRAVAR.
"""
import io, os, re, shutil, sys

G = os.path.join('C:/Users/Saxa/Desktop/youtube-work', '_gerar-galeria.py')

with io.open(G, 'r', encoding='utf-8') as f:
    d = f.read()
ANTES = len(d)

edicoes = []

# ---- 1. CSS: classe do selo .mp4 -------------------------------------------------
edicoes.append((
    '.b.up{color:#8ff0c0;border-color:#2f6b52;background:#173026}\n',
    '.b.up{color:#8ff0c0;border-color:#2f6b52;background:#173026}\n'
    '.b.mp4{color:#ffc9e0;border-color:#6b2f4f;background:#2a1220}\n',
))

# ---- 2. ler_short: o short tem .mp4 ao lado? -------------------------------------
edicoes.append((
    "        'kb': os.path.getsize(caminho) // 1024,\n",
    "        'kb': os.path.getsize(caminho) // 1024,\n"
    "        'mp4': os.path.exists(os.path.join(RAIZ, caminho_rel[:-5] + '.mp4')),\n",
))

# ---- 3. card(): selo quando o .mp4 existe ----------------------------------------
edicoes.append((
    "    if s['upload']:\n"
    "        badges.append('<span class=\"b up\">1080&times;1920 pronto</span>')\n",
    "    if s['upload']:\n"
    "        badges.append('<span class=\"b up\">1080&times;1920 pronto</span>')\n"
    "    if s['mp4']:\n"
    "        badges.append('<span class=\"b mp4\" title=\"arquivo .mp4 renderizado na mesma'\n"
    "                      ' pasta, mesmo nome do .html\">.mp4 pronto</span>')\n",
))

# ---- 4. contagem dos que tem mp4 -------------------------------------------------
edicoes.append((
    "    total = sum(s['dur'] for s in shorts)\n",
    "    total = sum(s['dur'] for s in shorts)\n"
    "    com_mp4 = sum(1 for s in shorts if s['mp4'])\n",
))

# ---- 5. o alerta falso -----------------------------------------------------------
ALERTA_VELHO = """  <div class="alerta">
    <b>Atencao:</b> nao existem arquivos <code>.mp4</code> neste projeto.
    Cada short e um <b>arquivo HTML+SVG que se anima sozinho</b> - o video de verdade
    voce grava. Clique num cartao para abrir o short e depois grave com o OBS
    (Fonte de Navegador, 1080&times;1920) ou pelo CapCut.<br>
    Os que estao marcados <b>1080&times;1920 pronto</b> ja saem no formato de upload,
    sem borda. Os demais sao o cartao 405&times;720 usado para conferir na tela.
  </div>
"""

ALERTA_NOVO = """  <div class="alerta">
    <b>Como isto vira video:</b> %d dos shorts ja tem <code>.mp4</code> renderizado na
    mesma pasta, com o mesmo nome do <code>.html</code> - e' esse arquivo que sobe no
    YouTube. Os demais sao o <b>arquivo HTML+SVG que se anima sozinho</b>: abra o cartao
    e renderize com <code>node _gerar-mp4.js</code> (headless Chrome, sem OBS).<br>
    Os que estao marcados <b>1080&times;1920 pronto</b> ja saem no formato de upload,
    sem borda. Os demais sao o cartao 405&times;720 usado para conferir na tela.
  </div>
"""
edicoes.append((ALERTA_VELHO, ALERTA_NOVO))

# ---- 6. a tupla do % precisa do novo argumento, na posicao certa ----------------
edicoes.append((
    '""" % (CSS, len(shorts), mmss(total), len(shorts) + len(ignorados),',
    '""" % (CSS, len(shorts), mmss(total), com_mp4, len(shorts) + len(ignorados),',
))

for i, (velho, novo) in enumerate(edicoes, 1):
    n = d.count(velho)
    if n != 1:
        print('ERRO: ancora %d casou %d vez(es), esperado 1. Nada gravado.' % (i, n))
        sys.exit(1)
    d = d.replace(velho, novo)

# ---- provas ---------------------------------------------------------------------
if len(d) <= ANTES:
    print('ERRO: nao cresceu. Nada gravado.')
    sys.exit(1)

for t in ["'mp4': os.path.exists(", '.b.mp4{', 'com_mp4 = sum(', 'ja tem <code>.mp4</code>',
          'com_mp4, len(shorts) + len(ignorados)', '.mp4 pronto']:
    if t not in d:
        print('ERRO: trecho novo ausente: %r. Nada gravado.' % t)
        sys.exit(1)

if 'nao existem arquivos' in d:
    print('ERRO: o alerta falso continua no arquivo. Nada gravado.')
    sys.exit(1)

# a INSTRUCAO velha tem de sumir. Cuidado: o texto novo diz "sem OBS" de proposito,
# entao a guarda tem de procurar a frase, nao a palavra.
if 'grave com o OBS' in d or 'ou pelo CapCut' in d:
    print('ERRO: a instrucao de gravar com OBS continua no arquivo. Nada gravado.')
    sys.exit(1)
if 'sem OBS' not in d:
    print('ERRO: o alerta novo nao entrou. Nada gravado.')
    sys.exit(1)

# compila antes de gravar
try:
    compile(d, G, 'exec')
except SyntaxError as e:
    print('ERRO de sintaxe: %s (linha %s). Nada gravado.' % (e.msg, e.lineno))
    sys.exit(1)

shutil.copy2(G, G + '.antes-do-mp4')
with io.open(G, 'w', encoding='utf-8', newline='') as f:
    f.write(d)

print('OK: %d -> %d chars, %d ancoras aplicadas' % (ANTES, len(d), len(edicoes)))

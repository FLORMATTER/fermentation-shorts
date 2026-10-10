# -*- coding: utf-8 -*-
"""
Gera a galeria de TODOS os shorts animados do projeto: galeria-shorts.html

- Le cada .html da arvore, extrai: cenas, duracao (soma dos ms), idioma, formato de
  upload (1080x1920) e a legenda da primeira cena (que serve de titulo).
- Roda o _validar-short.py e marca quais arquivos tem problema conhecido.
- Escreve uma pagina unica, tema escuro, com link para abrir cada short.

Uso:  python _gerar-galeria.py
"""
import io
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, 'galeria-shorts.html')

# pastas que NAO sao shorts animados (aulas/guias/arquivo morto entram com rotulo proprio)
ROTULO = {
    'repolho': 'Repolho / Chucrute',
    'beterraba': 'Beterraba',
    'cebola': 'Cebola',
    'alho': 'Alho',
    'cenoura': 'Cenoura',
    'couve-flor': 'Couve-flor',
    'pepino': 'Pepino',
    'rabanete': 'Rabanete',
    'pao': 'Pão / Levain',
    'kombucha': 'Kombucha',
    'guia-geral': 'Guia geral',
    'video-longo': 'Video longo (16:9)',
    'cores': 'Cores (alho + cebola + beterraba)',
    'brocolis': 'Brocolis + laranja',
    'mosquito': 'Mosquito trap (DIY)',
    '_arquivo': 'Arquivo morto (versoes antigas)',
}
ORDEM = ['guia-geral', 'repolho', 'beterraba', 'cebola', 'alho', 'cenoura',
         'couve-flor', 'pepino', 'rabanete', 'cores', 'brocolis', 'pao', 'kombucha', 'mosquito',
         'video-longo', '_arquivo']
# pastas que tambem sao varridas, mas nunca geram cartao (nao tem cena animada)
PASTAS_SCAN = ORDEM + ['aulas', 'guias']

# o validador marca coisas inofensivas junto com os bugs de verdade
LEVES = ('nunca usado', 'hex suspeito')


def separa(linhas):
    """Divide as marcacoes do validador em bugs reais e avisos inofensivos."""
    bugs, avisos = [], []
    for l in linhas:
        (avisos if any(k in l for k in LEVES) else bugs).append(l)
    return bugs, avisos


def problemas_do_validador():
    """Roda o validador e devolve {arquivo: [linhas de problema]}."""
    try:
        r = subprocess.run([sys.executable, os.path.join(RAIZ, '_validar-short.py')],
                           capture_output=True, cwd=RAIZ)
        txt = r.stdout.decode('utf-8', 'replace')
    except Exception as e:
        print('aviso: nao consegui rodar o validador:', e)
        return {}
    out, atual = {}, None
    for linha in txt.splitlines():
        s = linha.strip()
        if s.endswith('.html') and '\\' in s or s.endswith('.html') and '/' in s:
            atual = s.replace('\\', '/')
            out.setdefault(atual, [])
        elif atual and s.startswith('[X]'):
            out[atual].append(s[4:].strip())
    return out


def _unesc(s):
    """`cap:`/`sub:` vem do JS, onde \u00b7 e' escape. Desfaz antes de ir para o HTML."""
    return re.sub(r'\\u([0-9a-fA-F]{4})',
                  lambda m: chr(int(m.group(1), 16)), s)


def ler_short(caminho_rel):
    """Extrai os dados de um short. Devolve None se nao for cena animada."""
    caminho = os.path.join(RAIZ, caminho_rel)
    d = io.open(caminho, encoding='utf-8', errors='replace').read()

    cenas = len(re.findall(r'<svg class="scene', d))
    ms = [int(x) for x in re.findall(r'\bms\s*:\s*(\d+)', d)]
    dur = sum(ms) / 1000.0
    if cenas == 0 or dur == 0:
        return None

    m = re.search(r"cap:'([^']*)'", d)
    titulo = _unesc(m.group(1)) if m else ''
    if not titulo:
        m = re.search(r'<title>([^<]*)</title>', d)
        titulo = m.group(1).strip() if m else ''
    if not titulo:
        titulo = os.path.basename(caminho_rel).replace('.html', '')

    sub = ''
    m = re.search(r"sub:'([^']*)'", d)
    if m:
        sub = _unesc(m.group(1))

    pt = len(re.findall(r'\b(que|para|com|nao|você|água|sal|dias|semanas)\b', d, re.I))
    en = len(re.findall(r'\b(the|and|with|you|water|salt|days|weeks)\b', d, re.I))
    idioma = 'EN' if en > pt else 'PT'

    return {
        'arquivo': caminho_rel,
        'pasta': caminho_rel.split('/')[0],
        'nome': os.path.basename(caminho_rel),
        'titulo': titulo,
        'sub': sub,
        'cenas': cenas,
        'dur': dur,
        'idioma': idioma,
        'upload': re.search(r'width:1080px', d) is not None,
        'kb': os.path.getsize(caminho) // 1024,
        'mp4': os.path.exists(os.path.join(RAIZ, caminho_rel[:-5] + '.mp4')),
    }


def mmss(s):
    return '%d:%02d' % (int(s) // 60, int(s) % 60)


def card(s, probs):
    bugs, avisos = separa(probs)
    badges = []
    if s['upload']:
        badges.append('<span class="b up">1080&times;1920 pronto</span>')
    if s['mp4']:
        badges.append('<span class="b mp4" title="arquivo .mp4 renderizado na mesma'
                      ' pasta, mesmo nome do .html">.mp4 pronto</span>')
    badges.append('<span class="b %s">%s</span>' % ('pt' if s['idioma'] == 'PT' else 'en',
                                                    s['idioma']))
    if bugs:
        badges.append('<span class="b bug" title="%s">%d bug(s) real(is)</span>'
                      % (re.sub(r'"', '', ' | '.join(bugs))[:300], len(bugs)))
    else:
        badges.append('<span class="b ok">sem bug real</span>')
    if avisos:
        badges.append('<span class="b aviso" title="%s">%d aviso(s)</span>'
                      % (re.sub(r'"', '', ' | '.join(avisos))[:300], len(avisos)))

    sub = ('<p class="sub">%s</p>' % s['sub']) if s['sub'] else ''
    return """    <a class="card" href="%(arq)s" target="_blank" rel="noopener">
      <div class="thumb"><span class="play">&#9654;</span><span class="dur">%(dur)s</span></div>
      <div class="info">
        <h3>%(tit)s</h3>
        %(sub)s
        <p class="meta">%(cenas)d cenas &middot; %(kb)d KB &middot; <code>%(nome)s</code></p>
        <p class="badges">%(bad)s</p>
      </div>
    </a>""" % {'arq': s['arquivo'], 'dur': mmss(s['dur']), 'tit': s['titulo'],
               'sub': sub, 'cenas': s['cenas'], 'kb': s['kb'], 'nome': s['nome'],
               'bad': ''.join(badges)}


CSS = """
:root{--bg:#141110;--bg2:#1d1917;--card:#231e1b;--line:#3a322d;--tx:#f2e9e2;
      --tx2:#a89a8f;--ac:#e0714f;--up:#4fbf8b;--bug:#e0b04f;}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);
     font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
     padding:40px 28px 80px}
.wrap{max-width:1240px;margin:0 auto}
h1{font-size:30px;letter-spacing:-.5px;margin-bottom:10px}
.lead{color:var(--tx2);max-width:760px;margin-bottom:8px}
.alerta{background:#2a1f14;border:1px solid #6b4a22;border-radius:12px;
        padding:16px 20px;margin:22px 0 34px;font-size:14.5px;color:#f0d9b8}
.alerta b{color:#ffd9a0}
h2{font-size:13px;text-transform:uppercase;letter-spacing:1.6px;color:var(--ac);
   margin:42px 0 16px;padding-bottom:9px;border-bottom:1px solid var(--line)}
h2 small{color:var(--tx2);text-transform:none;letter-spacing:0;font-weight:400}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(272px,1fr));gap:16px}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;
      overflow:hidden;text-decoration:none;color:inherit;transition:.16s}
.card:hover{transform:translateY(-3px);border-color:var(--ac)}
.thumb{height:112px;background:linear-gradient(135deg,#33281f,#241d18);
       display:flex;align-items:center;justify-content:center;position:relative}
.play{width:44px;height:44px;border-radius:50%;background:rgba(224,113,79,.92);
      color:#fff;display:flex;align-items:center;justify-content:center;font-size:16px;
      padding-left:3px}
.dur{position:absolute;right:10px;bottom:8px;background:rgba(0,0,0,.65);
     border-radius:5px;padding:1px 7px;font-size:12px;color:#fff}
.info{padding:14px 16px 16px}
h3{font-size:16px;line-height:1.3;margin-bottom:4px}
.sub{font-size:13px;color:var(--tx2);margin-bottom:8px}
.meta{font-size:11.5px;color:var(--tx2);margin-bottom:10px}
code{font-family:ui-monospace,Consolas,monospace;font-size:11px;color:#c8b6a8}
.badges{display:flex;flex-wrap:wrap;gap:6px}
.b{font-size:10.5px;padding:2px 8px;border-radius:20px;border:1px solid}
.b.up{color:#8ff0c0;border-color:#2f6b52;background:#173026}
.b.mp4{color:#ffc9e0;border-color:#6b2f4f;background:#2a1220}
.b.pt{color:#ffd0a8;border-color:#6b4a2a;background:#2a1e12}
.b.en{color:#a8d0ff;border-color:#2a4a6b;background:#12212e}
.b.ok{color:#9ee0c0;border-color:#2f5a48;background:#14251e}
.b.bug{color:#ffd88f;border-color:#6b5a22;background:#2a2412}
.b.aviso{color:#c9bda8;border-color:#4a4238;background:#221e18}
footer{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);
       color:var(--tx2);font-size:13px}
"""


def main():
    probs = problemas_do_validador()
    shorts, ignorados = [], []
    for pasta in PASTAS_SCAN:
        d = os.path.join(RAIZ, pasta)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith('.html'):
                continue
            rel = pasta + '/' + f
            s = ler_short(rel)
            if s is None:
                ignorados.append(rel)
            else:
                s['probs'] = probs.get(rel.replace('/', '\\'), probs.get(rel, []))
                shorts.append(s)

    shorts.sort(key=lambda s: (not s['upload'], -s['dur']))
    prontos = [s for s in shorts if s['upload']]
    resto = [s for s in shorts if not s['upload']]

    total = sum(s['dur'] for s in shorts)
    com_mp4 = sum(1 for s in shorts if s['mp4'])
    partes = ["""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Galeria dos shorts animados - fermentacao</title>
<style>%s</style>
</head>
<body>
<div class="wrap">
  <h1>Galeria dos shorts animados</h1>
  <p class="lead">%d shorts animados &middot; %s de animacao no total &middot;
     %d arquivos HTML+SVG.</p>

  <div class="alerta">
    <b>Como isto vira video:</b> %d dos shorts ja tem <code>.mp4</code> renderizado na
    mesma pasta, com o mesmo nome do <code>.html</code> - e' esse arquivo que sobe no
    YouTube. Os demais sao o <b>arquivo HTML+SVG que se anima sozinho</b>: abra o cartao
    e renderize com <code>node _gerar-mp4.js</code> (headless Chrome, sem OBS).<br>
    Os que estao marcados <b>1080&times;1920 pronto</b> ja saem no formato de upload,
    sem borda. Os demais sao o cartao 405&times;720 usado para conferir na tela.
  </div>

  <h2>Prontos para subir no YouTube <small>- ja no formato 1080&times;1920</small></h2>
  <div class="grid">
%s
  </div>
""" % (CSS, len(shorts), mmss(total), len(shorts) + len(ignorados), com_mp4,
            '\n'.join(card(s, s['probs']) for s in prontos))]

    for pasta in ORDEM:
        grupo = [s for s in resto if s['pasta'] == pasta]
        if not grupo:
            continue
        partes.append("""  <h2>%s <small>- %d short(s)</small></h2>
  <div class="grid">
%s
  </div>
""" % (ROTULO.get(pasta, pasta), len(grupo),
            '\n'.join(card(s, s['probs']) for s in grupo)))

    partes.append("""  <footer>
    Gerado por <code>_gerar-galeria.py</code>. A validacao vem do
    <code>_validar-short.py</code>.<br>
    %d arquivo(s) na pasta nao entram na galeria (sao aulas, guias ou paginas sem cena):
    %s
  </footer>
</div>
</body>
</html>
""" % (len(ignorados), ', '.join('<code>%s</code>' % i for i in ignorados) or '-'))

    html = ''.join(partes)

    # autochecagem: os numeros do topo tem de fechar com a conta. Ja inverteram 1x
    # (o alerta mostrou a contagem de ARQUIVOS e o lead mostrou a de mp4).
    if '%d dos shorts ja tem' % com_mp4 not in html:
        raise SystemExit('ERRO: o alerta nao mostra %d shorts com mp4.' % com_mp4)
    if html.count('class="b mp4"') != com_mp4:
        raise SystemExit('ERRO: o alerta diz %d com mp4 mas ha %d selos no HTML.'
                         % (com_mp4, html.count('class="b mp4"')))
    if '%d arquivos HTML+SVG' % (len(shorts) + len(ignorados)) not in html:
        raise SystemExit('ERRO: o lead nao mostra %d arquivos HTML+SVG.'
                         % (len(shorts) + len(ignorados)))

    with io.open(SAIDA, 'w', encoding='utf-8', newline='') as fh:
        fh.write(html)

    print('galeria : %s' % SAIDA)
    print('shorts  : %d (%d prontos p/ upload, %d cartao 405x720)'
          % (len(shorts), len(prontos), len(resto)))
    print('duracao : %s' % mmss(total))
    print('fora    : %d' % len(ignorados))
    com_bug = [(s, separa(s['probs'])[0]) for s in shorts]
    com_bug = [(s, b) for s, b in com_bug if b]
    print('com bug : %d arquivo(s)' % len(com_bug))
    for s, b in sorted(com_bug, key=lambda x: -len(x[1])):
        print('   %-52s %d' % (s['arquivo'], len(b)))
    n_av = sum(1 for s in shorts if separa(s['probs'])[1])
    print('so aviso: %d arquivo(s)' % n_av)


if __name__ == '__main__':
    main()

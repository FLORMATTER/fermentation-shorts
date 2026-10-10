# -*- coding: utf-8 -*-
"""Le os textos visiveis de cada short PT para eu saber sobre o que cada um fala."""
import re, glob, os

def visiveis(d):
    """Textos que aparecem na tela: <text> do SVG + nos de texto do HTML."""
    fora = []
    # SVG <text>
    for m in re.finditer(r'<text[^>]*>(.*?)</text>', d, re.S):
        t = re.sub(r'<[^>]+>', '', m.group(1))
        t = re.sub(r'\s+', ' ', t).strip()
        if t:
            fora.append(t)
    # nos de texto do HTML (entre </style> e <script>)
    ini = d.find('</style>')
    fim = d.find('<script>')
    if ini < 0:
        ini = 0
    if fim < 0:
        fim = len(d)
    corpo = d[ini:fim]
    for m in re.finditer(r'>([^<>]{2,})<', corpo):
        t = re.sub(r'\s+', ' ', m.group(1)).strip()
        if t and re.search(r'[A-Za-zÀ-ÿ]', t):
            fora.append(t)
    # dedup preservando ordem
    visto, saida = set(), []
    for t in fora:
        if t not in visto:
            visto.add(t)
            saida.append(t)
    return saida

alvos = sorted(glob.glob('*/shorts*.html') + glob.glob('*/*.html'))
alvos = [a for a in alvos
         if '-en' not in os.path.basename(a)
         and '_arquivo' not in a
         and 'galeria' not in a
         and 'guia-capcut' not in a
         and 'aula' not in a
         and 'pacote' not in a]

for f in alvos:
    d = open(f, encoding='utf-8', errors='replace').read()
    v = visiveis(d)
    print('=' * 70)
    print('ARQUIVO:', f)
    print('CENAS:', len(re.findall(r'class="scene"', d)), ' TAM:', len(d))
    print('TEXTOS (%d):' % len(v))
    for t in v[:28]:
        print('   -', t[:90])
    print()

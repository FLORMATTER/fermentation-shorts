# -*- coding: utf-8 -*-
"""
_traduzir-serie.py — aplica o dicionario PT->EN em todos os videos da serie.

Como funciona: para cada frase do dicionario, substitui as TRES formas ancoradas
    'Frase'          -> literal de string do JS
    >Frase</text>    -> texto desenhado dentro do SVG
    >Frase<          -> no de texto do HTML
As ancoras evitam casar por engano: 'Couve' nao casa dentro de 'Couve-flor' e
'7 dias' nao casa dentro de '7 dias e esta pronto'.

Uso:
    python _traduzir-serie.py --cobertura   # SO lista o que falta traduzir
    python _traduzir-serie.py               # dry-run: mostra o que faria
    python _traduzir-serie.py --apply       # grava os irmaos -en

Os originais em portugues NUNCA sao alterados: o resultado vai para
<nome>-en.html, na mesma pasta.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
IGNORAR = ('.workbuddy-ai', '_revisao', 'node_modules')
PASTAS_FORA = ('aulas', 'guias', '_arquivo')

# o video longo em PT ja tem versao -en; nao traduzir de novo
PULAR = ('video-longo/player-video-longo-7-legumes.html',)

PT = re.compile(r'\b(que|para|com|nao|não|você|voce|água|agua|sal|dias|semanas|'
                r'pote|dentes?|mão|mao|fermenta|prensa|massageia|repolho|cenoura|'
                r'rabanete|beterraba|couve|alho|cebola|pepino|pronta|pronto|'
                r'crocante|bancada|esperar|volta|cor|sua|seu|isso|mais|legume|'
                r'tinge|salmoura|iodo|sem|só|nao|faca|água)\b', re.I)

# strings que sao iguais nos dois idiomas de proposito: nao sao sobra
NEUTRO_IGUAL = re.compile(
    r'^(pH|kg|g|ml|L|Pizza|Tacos|Sushi|OBS|Canva|CapCut|YouTube|'
    r'\d+\s*(MIN|SEG|G|KG|ML|L|MM|CM)|'
    r'\$\{[^}]*\}|[^A-Za-zÀ-ÿ]*)$')

# iguais nos dois idiomas porque NAO TEM IDIOMA (numero, unidade, emoji)
NEUTRO_EXATO = {
    'TOTAL: 500 g', '⚡ SPEED', 'pH', 'kg', '10 MIN',
    'Pizza', 'Tacos', 'OBS', 'Canva', 'CapCut',
}


def tem_letras(s):
    """Pelo menos 2 letras seguidas -> vale a pena conferir."""
    return re.search(r'[A-Za-zÀ-ÿ]{2}', s) is not None


def carrega_dic():
    caminho = os.path.join(RAIZ, '_dicionario-pt-en.py')
    ns = {'__name__': 'dic'}
    exec(compile(io.open(caminho, encoding='utf-8').read(), caminho, 'exec'), ns)
    return ns['DIC']


def arquivos():
    out = []
    for base, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [x for x in dirs if x not in IGNORAR]
        rel = os.path.relpath(base, RAIZ).replace('\\', '/')
        pasta = rel.split('/')[0]
        if pasta in PASTAS_FORA:
            continue
        for a in sorted(arqs):
            if not a.endswith('.html') or a == 'galeria-shorts.html':
                continue
            # ja em ingles: -en.html, -en-1080x1920.html, ...
            if re.search(r'-en(\.|-|_)', a):
                continue
            p = os.path.join(base, a)
            r = os.path.relpath(p, RAIZ).replace('\\', '/')
            if r in PULAR:
                continue
            out.append(p)
    return sorted(out)


def visiveis(d):
    """Todas as strings que o espectador ve."""
    out = []
    for chave in ('cap', 'sub', 'hint', 'nome', 'nivel', 'sal', 'tempo'):
        out += re.findall(r"\b%s\s*:\s*'((?:[^'\\]|\\.)*)'" % chave, d)
    out += [t.strip() for t in re.findall(r'<text\b[^>]*>(.*?)</text>', d, re.S)]
    corpo = d.split('</style>', 1)[-1].split('<script>', 1)[0]
    out += [' '.join(n.split()) for n in re.findall(r'>([^<>{}]+)<', corpo)]
    return [s for s in out if s.strip()]


def troca_nos_html(d, pt, en):
    """Troca a frase quando ela e um NO DE TEXTO do HTML (entre duas tags).

    Necessario porque as formas literais nao pegam '>EM <span>' nem
    '>CHUCRUTE<br>' -- foi assim que 'CHUCRUTE / EM / 7 DIAS' ficou em
    portugues no cartao do chucrute.

    A troca e limitada ao corpo do HTML (de </style> ate <script>). Isso e
    proposital: dentro do <script>, '>' e '<' sao operadores de comparacao e
    uma troca solta ali quebraria o JavaScript.
    """
    ini = d.find('</style>')
    if ini < 0:
        return d, 0
    fim = d.find('<script>')
    if fim < 0:
        fim = len(d)
    corpo = d[ini:fim]
    padrao = re.compile(r'(?<=>)(\s*)' + re.escape(pt) + r'(\s*)(?=<)')
    novo, k = padrao.subn(lambda m: m.group(1) + en + m.group(2), corpo)
    if k:
        d = d[:ini] + novo + d[fim:]
    return d, k


def aplica(d, dic):
    """Aplica o dicionario. Da frase mais longa para a mais curta.

    Cinco formas ancoradas por frase. As ancoras sao o que impede
    'Couve' de casar dentro de 'Couve-flor'.
    """
    n = 0
    for pt, en in sorted(dic, key=lambda x: -len(x[0])):
        for velho, novo in (("'%s'" % pt, "'%s'" % en),
                            ('>%s</text>' % pt, '>%s</text>' % en),
                            ('>%s<' % pt, '>%s<' % en),
                            ('>%s<br>' % pt, '>%s<br>' % en),
                            ('>%s <' % pt, '>%s <' % en)):
            c = d.count(velho)
            if c:
                d = d.replace(velho, novo)
                n += c
        d, k = troca_nos_html(d, pt, en)
        n += k
    return d, n


def main():
    modo = 'cobertura' if '--cobertura' in sys.argv else ('apply' if '--apply' in sys.argv else 'dry')
    dic = carrega_dic()
    print('dicionario: %d frase(s)' % len(dic))

    faltando = {}
    feitos = []
    for p in arquivos():
        d = io.open(p, encoding='utf-8', errors='replace').read()
        rel = os.path.relpath(p, RAIZ).replace('\\', '/')

        if modo == 'cobertura':
            for s in set(visiveis(d)):
                if PT.search(s) and s not in {k for k, _ in dic}:
                    faltando.setdefault(s, set()).add(rel)
            continue

        novo, n = aplica(d, dic)
        novo = novo.replace('lang="pt-BR"', 'lang="en"')
        dest = p[:-5] + '-en.html'

        # SOBRA = string visivel que ficou IDENTICA ao original em portugues.
        # Nao adivinha idioma: compara os dois arquivos. O filtro antigo por
        # lista de palavras tinha ponto cego (\bfermenta\b nao casa
        # 'FERMENTACAO') e por isso aprovava arquivo meio traduzido.
        sobra = sorted(s for s in (set(visiveis(novo)) & set(visiveis(d)))
                       if tem_letras(s)
                       and not NEUTRO_IGUAL.match(s)
                       and s not in NEUTRO_EXATO)
        # decimais com virgula que escaparam (mostrar a FRASE, nao so o digito)
        virg = sorted({s for s in visiveis(novo) if re.search(r'\d,\d', s)})

        print('\n%s' % rel)
        print('  substituicoes : %d' % n)
        print('  destino       : %s' % os.path.relpath(dest, RAIZ))
        if sobra:
            print('  [X] SOBROU PORTUGUES (%d):' % len(sobra))
            for s in sobra:
                print('        | ' + s)
        else:
            print('  ok: nenhuma frase em portugues sobrando')
        if virg:
            print('  [X] decimal com virgula: %s' % virg)

        if modo == 'apply' and not sobra and not virg:
            io.open(dest, 'w', encoding='utf-8', newline='').write(novo)
            feitos.append(dest)

    if modo == 'cobertura':
        print('\n' + '=' * 74)
        print('FRASES SEM TRADUCAO: %d' % len(faltando))
        print('=' * 74)
        for s, arqs in sorted(faltando.items(), key=lambda x: (-len(x[1]), x[0])):
            print('[%dx] %s' % (len(arqs), s))
        return 1 if faltando else 0

    if modo == 'apply':
        print('\n' + '=' * 74)
        print('gravados: %d arquivo(s)' % len(feitos))
        for f in feitos:
            print('  ' + os.path.relpath(f, RAIZ))
    else:
        print('\n(dry-run — nada foi gravado. Use --apply para gravar.)')
    return 0


if __name__ == '__main__':
    sys.exit(main())

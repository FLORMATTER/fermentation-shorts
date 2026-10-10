# -*- coding: utf-8 -*-
"""_traduzir-para-pt.py — volta um short -en para o original PT.

    python _traduzir-para-pt.py <arquivo-en.html> --destino=<arquivo-pt.html>
    python _traduzir-para-pt.py <arquivo-en.html> --destino=<pt.html> --apply

Por que existe: o #18, #19 e #20 nasceram em INGLES (pedido do usuario) e a
convencao da serie e' **original PT + irmao `-en`**. Reescrever 617 frases a mao
seria refazer o trabalho do `_dicionario-pt-en.py`. Aqui o dicionario e' usado ao
CONTRARIO.

O que muda em relacao ao `_traduzir-serie.py` (PT->EN):
  - so' aplica os pares **1:1**. O `Cabbage` vem de 'Repolho' E de 'Couve'; na
    volta nao ha' como saber qual, entao ele NAO e' aplicado sozinho — se
    aparecer, sai na lista de sobras para decisao a mao.
  - `lang="en"` volta para `lang="pt-BR"`.
  - **Nada de conversao automatica de numero.** Trocar `.` por `,` num regex
    global quebraria `stroke-width="2.5"` no CSS/SVG. O `_dicionario-pt-en.py`
    ja' guarda os pares de numero ('2,5%' / '2.5%'); o que faltar e' REPORTADO
    (coluna "decimal"), nao adivinhado.

Verificacao (a mesma licao que custou uma rodada na serie): a sobra NAO e'
adivinhada por lista de palavras. Ela e' a string visivel que ficou **identica**
nos dois arquivos. Se sobrou ingles, ela aparece.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

# PT que NAO podem ser aplicados automaticamente na volta (ambiguidade real).
# 'Cabbage' <- 'Repolho' | 'Couve'  ->  decidir olhando o arquivo.
AMBIGUOS = {'Cabbage'}

# iguais nos dois idiomas porque NAO TEM IDIOMA (numero, unidade, sigla, emoji)
NEUTRO_IGUAL = re.compile(
    r'^(pH|kg|g|ml|L|Pizza|Tacos|Sushi|OBS|Canva|CapCut|YouTube|'
    r'\d+\s*(MIN|SEG|G|KG|ML|L|MM|CM)|'
    r'\$\{[^}]*\}|[^A-Za-zÀ-ÿ]*)$')
NEUTRO_EXATO = {
    'TOTAL: 500 g', '⚡ SPEED', 'pH', 'kg', '10 MIN',
    'Pizza', 'Tacos', 'OBS', 'Canva', 'CapCut',
}


def tem_letras(s):
    return re.search(r'[A-Za-zÀ-ÿ]{2}', s) is not None


def carrega_dic():
    caminho = os.path.join(RAIZ, '_dicionario-pt-en.py')
    ns = {'__name__': 'dic'}
    exec(compile(io.open(caminho, encoding='utf-8', newline='').read(),
                 caminho, 'exec'), ns)
    return ns['DIC']


def monta_reverso(dic):
    """EN -> PT, so' onde o par e' 1:1. Devolve (mapa, ambiguos_vistos)."""
    por_en = {}
    colidiu = set()
    for pt, en in dic:
        if en in por_en and por_en[en] != pt:
            colidiu.add(en)
        por_en.setdefault(en, pt)
    for en in list(colidiu) + list(AMBIGUOS):
        por_en.pop(en, None)
    return por_en, colidiu


def visiveis(d):
    """Todas as strings que o espectador ve (mesma definicao do _traduzir-serie)."""
    out = []
    for chave in ('cap', 'sub', 'hint', 'nome', 'nivel', 'sal', 'tempo', 'tag'):
        out += re.findall(r"\b%s\s*:\s*'((?:[^'\\]|\\.)*)'" % chave, d)
    out += [t.strip() for t in re.findall(r'<text\b[^>]*>(.*?)</text>', d, re.S)]
    corpo = d.split('</style>', 1)[-1].split('<script>', 1)[0]
    out += [' '.join(n.split()) for n in re.findall(r'>([^<>{}]+)<', corpo)]
    return [s for s in out if s.strip()]


def troca_nos_html(d, en, pt):
    """Troca a frase quando ela e' um NO DE TEXTO do HTML (entre duas tags).

    Limitado ao corpo do HTML (de </style> ate <script>): dentro do <script>,
    '>' e '<' sao operadores de comparacao.
    """
    ini = d.find('</style>')
    if ini < 0:
        return d, 0
    fim = d.find('<script>')
    if fim < 0:
        fim = len(d)
    corpo = d[ini:fim]
    padrao = re.compile(r'(?<=>)(\s*)' + re.escape(en) + r'(\s*)(?=<)')
    novo, k = padrao.subn(lambda m: m.group(1) + pt + m.group(2), corpo)
    if k:
        d = d[:ini] + novo + d[fim:]
    return d, k


def aplica(d, reverso):
    """Aplica o dicionario invertido, da frase MAIS LONGA para a mais curta.

    As ancoras sao as mesmas cinco do PT->EN, so' que trocadas de lado:
        'Frase'        literal de string do JS
        >Frase</text>  texto desenhado no SVG
        >Frase<        no de texto do HTML
        >Frase<br>     no seguido de quebra
        >Frase <       no seguido de outra tag
    """
    n = 0
    for en in sorted(reverso, key=lambda x: -len(x)):
        pt = reverso[en]
        for velho, novo in (("'%s'" % en, "'%s'" % pt),
                            ('>%s</text>' % en, '>%s</text>' % pt),
                            ('>%s<' % en, '>%s<' % pt),
                            ('>%s<br>' % en, '>%s<br>' % pt),
                            ('>%s <' % en, '>%s <' % pt)):
            c = d.count(velho)
            if c:
                d = d.replace(velho, novo)
                n += c
        d, k = troca_nos_html(d, en, pt)
        n += k
    return d, n


def main():
    arqs = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not arqs:
        print(__doc__)
        return 2
    origem = arqs[0]
    dest = None
    for a in sys.argv[1:]:
        if a.startswith('--destino='):
            dest = a.split('=', 1)[1]
    if not dest:
        print('falta --destino=<arquivo.html>')
        return 2
    gravar = '--apply' in sys.argv

    dic = carrega_dic()
    reverso, colidiu = monta_reverso(dic)
    print('dicionario : %d pares' % len(dic))
    print('aplicaveis : %d (1:1)' % len(reverso))
    print('ambiguos   : %s' % ', '.join(sorted(colidiu | AMBIGUOS)))
    print('origem     : %s' % origem)
    print('destino    : %s' % dest)

    en = io.open(origem, encoding='utf-8', newline='').read()
    crlf = en.count('\r\n')
    eol = '\r\n' if crlf else '\n'
    print('fim de linha: %s' % ('CRLF' if crlf else 'LF'))

    pt, n = aplica(en, reverso)
    pt = pt.replace('lang="en"', 'lang="pt-BR"')

    # SOBRA = string visivel que ficou IDENTICA nos dois. Nao adivinha idioma.
    sobra = sorted(s for s in (set(visiveis(pt)) & set(visiveis(en)))
                   if tem_letras(s)
                   and not NEUTRO_IGUAL.match(s)
                   and s not in NEUTRO_EXATO)
    decimal = sorted({s for s in visiveis(pt) if re.search(r'\d\.\d', s)})
    faltando = sorted({s for s in visiveis(pt)
                       if s in AMBIGUOS or s in colidiu})

    print('\nsubstituicoes: %d' % n)
    if sobra:
        print('[X] NAO TRADUZIDO (%d) — ainda identico ao ingles:' % len(sobra))
        for s in sobra:
            print('      | ' + s)
    else:
        print('ok: nenhuma string visivel ficou igual ao ingles')
    if faltando:
        print('[X] AMBIGUO — decidir a mao: %s' % faltando)
    if decimal:
        print('[!] decimal com PONTO no texto visivel (conferir):')
        for s in decimal:
            print('      | ' + s)

    if gravar and not sobra and not faltando:
        io.open(dest, 'w', encoding='utf-8', newline='').write(pt)
        print('\ngravado: %s' % dest)
        return 0
    if gravar:
        print('\nNAO GRAVADO: ha sobra ou ambiguidade acima.')
        return 1
    print('\n(dry-run — use --apply para gravar)')
    return 0


if __name__ == '__main__':
    sys.exit(main())

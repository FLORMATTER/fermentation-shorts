# -*- coding: utf-8 -*-
"""_provar-keyframes.py — PROVA que tirar os keyframes mortos nao mudou 1 pixel.

O argumento "o nome nao aparece em nenhum outro lugar, entao e' codigo morto" e'
bom, mas nao e' prova. Esta e':

  1. le o `_keyframes-removidos.txt` e RECONSTROI a versao ANTES de cada arquivo
     (uma copia em `_revisao/ab-antes-<nome>.html` com as regras reinseridas);
  2. renderiza as cenas das DUAS versoes com `_revisar-cenas.py --final` — o modo
     que congela no ESTADO FINAL, que e' justamente onde um keyframe que faltasse
     apareceria (elemento parado em opacity 0, fora do lugar, etc.);
  3. compara os PNGs BYTE A BYTE.

Todos identicos = remover as regras nao mexeu em nada na tela.

CONTROLE NEGATIVO (`--teste`): um verificador que nunca acusa nada nao prova nada.
O `--teste` monta de proposito uma versao com um keyframe USADO arrancado e exige
que a comparacao acuse diferenca. So' depois disso o "identico" dos outros vale.

ARMADILHA ja' paga: descobrir os PNGs novos por `os.listdir` antes/depois NAO
funciona — varios `-final.png` desses shorts ja' existiam de sessoes anteriores, o
render sobrescreve o arquivo e o nome nao aparece como novo. Tem de ler os caminhos
que o proprio `_revisar-cenas.py` imprime (`-> caminho`).

    python _provar-keyframes.py            # prova todos os arquivos do registro
    python _provar-keyframes.py --teste    # so' o controle negativo
    python _provar-keyframes.py --manter   # nao apaga as copias ab-antes-*
"""
import glob
import importlib.util
import io
import os
import re
import subprocess
import sys
import time

REGISTRO = '_keyframes-removidos.txt'
PASTA = '_revisao'
ALVO_TESTE = 'cenoura/shorts-cenoura-animado.html'


def le_registro():
    """{arquivo: [trecho, ...]} — o que o _limpar-keyframes.py tirou."""
    d = io.open(REGISTRO, encoding='utf-8').read()
    blocos = re.findall(r'/\* === (.+?) :: @keyframes ([\w-]+) === \*/\n(.*?)(?=\n/\* === |\Z)',
                        d, re.S)
    fora = {}
    for arq, kf, trecho in blocos:
        fora.setdefault(arq, []).append((kf, trecho.strip('\n')))
    return fora


def carrega_limpar():
    """Importa o _limpar-keyframes.py (o nome tem hifen, entao nao da' import direto)."""
    spec = importlib.util.spec_from_file_location('_limpar', '_limpar-keyframes.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def renderiza(alvo, tentativas=3):
    """Roda o _revisar-cenas.py --final e devolve os PNGs que ELE diz que criou."""
    for t in range(tentativas):
        r = subprocess.run([sys.executable, '_revisar-cenas.py', alvo, '--final'],
                           capture_output=True, text=True)
        pngs = [p.strip() for p in re.findall(r'-> (.+\.png)', r.stdout or '')]
        if pngs:
            return pngs, r.returncode
        time.sleep(2)          # o Chrome as vezes nao solta o perfil de primeira
    return [], 1


def compara(alvo_antes, alvo_depois, rotulo):
    """Renderiza os dois e compara folha a folha. Devolve (ok, lista_de_diferencas)."""
    png_antes, rc1 = renderiza(alvo_antes)
    png_depois, rc2 = renderiza(alvo_depois)
    if not png_antes or not png_depois:
        return None, ['render nao produziu PNG (rc %d/%d)' % (rc1, rc2)]
    if len(png_antes) != len(png_depois):
        return None, ['%d folhas antes vs %d depois' % (len(png_antes), len(png_depois))]
    difs = []
    for pa, pd in zip(png_antes, png_depois):
        a = io.open(pa, 'rb').read()
        b = io.open(pd, 'rb').read()
        if a != b:
            difs.append('%s (%d vs %d bytes)' % (os.path.basename(pd), len(a), len(b)))
    return (not difs), difs


def teste():
    """CONTROLE NEGATIVO: arranca um keyframe USADO e exige que a comparacao acuse."""
    limpar = carrega_limpar()
    d = io.open(ALVO_TESTE, 'r', encoding='utf-8', newline='').read()
    usados = sorted(set(re.findall(r'animation:\s*([\w-]+)', d)))
    if not usados:
        print('[!] nenhum `animation:` em %s' % ALVO_TESTE)
        return 1
    kf = usados[0]
    quebrado, trecho = limpar.recorta_regra(d, kf)
    if quebrado is None:
        print('[!] nao consegui arrancar "%s"' % kf)
        return 1
    copia = os.path.join(PASTA, '_teste-quebrado-%s.html'
                         % os.path.splitext(os.path.basename(ALVO_TESTE))[0])
    with io.open(copia, 'w', encoding='utf-8', newline='') as fh:
        fh.write(quebrado)

    print('CONTROLE NEGATIVO: arranquei o keyframe USADO "%s" de %s' % (kf, ALVO_TESTE))
    print('  (a comparacao TEM de acusar diferenca — se disser "identico", ela nao presta)')
    ok, difs = compara(copia, ALVO_TESTE, 'teste')
    print()
    if ok:
        print('  [X] FALHOU: disse "identico" com um keyframe usado arrancado.')
        print('      A comparacao nao enxerga diferenca — o "identico" dos outros nao vale.')
        return 1
    print('  [ok] PROVADO: a comparacao acusou a diferenca.')
    for x in difs:
        print('       %s' % x)
    for p in glob.glob(os.path.join(PASTA, '_teste-quebrado-*')):
        try:
            os.remove(p)
        except OSError:
            pass
    return 0


def ruido(arquivos):
    """A/A: renderiza o MESMO arquivo varias vezes. Mede o ruido do proprio render.

    Sem isto, uma diferenca de 4 bytes num PNG nao quer dizer nada: pode ser
    anti-aliasing. Se o A/A ja' produz mais de um tamanho para a MESMA entrada, o
    "MUDOU" do A/B com essa mesma magnitude nao vale nada.

        python _provar-keyframes.py --ruido --vezes 4 <arquivo>
    """
    if not arquivos:
        arquivos = [ALVO_TESTE]
    vezes = 3
    if '--vezes' in sys.argv:
        vezes = int(sys.argv[sys.argv.index('--vezes') + 1])

    for arq in arquivos:
        vistos = []
        for i in range(vezes):
            pngs, rc = renderiza(arq)
            if not pngs:
                print('[!] %s: render %d nao deu PNG' % (arq, i + 1))
                vistos = None
                break
            vistos.append(tuple(os.path.getsize(p) for p in pngs))
        if vistos is None:
            continue
        distintos = sorted(set(vistos))
        if len(distintos) > 1:
            print('[X] %-46s A/A INSTAVEL: %s' % (arq, ' | '.join(str(t) for t in distintos)))
            print('    -> o render nao e deterministico nesta cena: diferenca de poucos')
            print('       bytes NAO prova nada (a mesma entrada da resultados diferentes)')
        else:
            print('[ok] %-45s A/A estavel em %d render(s): %s'
                  % (arq, vezes, distintos[0]))
    return 0


def posicionais():
    """Args que sao caminho de arquivo. O valor de `--vezes` NAO e' arquivo."""
    fora = []
    it = iter(sys.argv[1:])
    for a in it:
        if a == '--vezes':
            next(it, None)          # consome o numero
            continue
        if not a.startswith('--'):
            fora.append(a)
    return fora


def main():
    manter = '--manter' in sys.argv
    os.makedirs(PASTA, exist_ok=True)
    os.makedirs(os.path.join(PASTA, '_tmp'), exist_ok=True)

    if '--teste' in sys.argv:
        return teste()
    if '--ruido' in sys.argv:
        return ruido(posicionais())

    alvos = posicionais()
    registro = le_registro()
    if alvos:
        registro = {k: v for k, v in registro.items() if k in alvos}
    if not registro:
        print('nada no %s' % REGISTRO)
        return 1

    iguais = diferentes = falhas = 0
    linhas = []
    copias = []

    for arq in sorted(registro):
        trechos = registro[arq]
        d = io.open(arq, 'r', encoding='utf-8', newline='').read()
        pos = d.rfind('</style>')
        if pos < 0:
            print('[!] %s: nao achei </style>' % arq)
            falhas += 1
            continue
        enxerto = '\n' + '\n'.join(t for _, t in trechos) + '\n'
        base = os.path.splitext(os.path.basename(arq))[0]
        copia = os.path.join(PASTA, 'ab-antes-%s.html' % base)
        with io.open(copia, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d[:pos] + enxerto + d[pos:])
        copias.append(copia)

        ok, difs = compara(copia, arq, arq)
        nomes = ', '.join(k for k, _ in trechos)
        if ok is None:
            falhas += 1
            print('[!] %-52s %s' % (arq, difs[0]))
            linhas.append('%s | FALHA: %s' % (arq, difs[0]))
        elif ok:
            iguais += 1
            print('[ok] %-52s identico  [%s]' % (arq, nomes))
            linhas.append('%s | identico | removidos: %s' % (arq, nomes))
        else:
            diferentes += 1
            print('[X] %-52s MUDOU: %s' % (arq, '; '.join(difs)))
            linhas.append('%s | MUDOU: %s' % (arq, '; '.join(difs)))

    print()
    print('=' * 74)
    print('arquivos identicos  : %d' % iguais)
    print('arquivos que mudaram: %d' % diferentes)
    print('falhas de render    : %d' % falhas)
    print('conclusao: %s' % ('remover os keyframes NAO mexeu em 1 pixel'
                              if not diferentes and not falhas
                              else 'CONFERIR — houve diferenca ou falha'))

    with io.open('_prova-keyframes.txt', 'w', encoding='utf-8', newline='') as fh:
        fh.write('# prova A/B: versao COM os keyframes x versao SEM eles\n'
                 '# render: _revisar-cenas.py --final (estado final congelado)\n'
                 '# identico = remover a regra nao mudou 1 pixel\n'
                 '# controle negativo em `python _provar-keyframes.py --teste`\n\n'
                 + '\n'.join(linhas) + '\n')
    print('relatorio: _prova-keyframes.txt')

    if not manter:
        # so' as copias da prova: os PNGs do render ficam (sao os PNGs de revisao do short)
        alvos_apagar = list(copias) + glob.glob(os.path.join(PASTA, 'ab-antes-*.png'))
        for p in alvos_apagar:
            try:
                os.remove(p)
            except OSError:
                pass
        print('copias da prova apagadas (%d arquivo(s))' % len(alvos_apagar))
    return 0 if not diferentes and not falhas else 1


if __name__ == '__main__':
    sys.exit(main())

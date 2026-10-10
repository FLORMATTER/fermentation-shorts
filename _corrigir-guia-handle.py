# -*- coding: utf-8 -*-
"""_corrigir-guia-handle.py — tira dos guias a ideia de que o @yourchannel sai no video.

    python _corrigir-guia-handle.py

O QUE ESTAVA ERRADO
-------------------
Os guias foram escritos quando a unica saida era GRAVAR o HTML pelo OBS. Nesse
caminho a marca d'agua e' mesmo desenhada na tela (o `?rec` esconde so' a capa e
os botoes — ver o IIFE no fim do short), entao o aviso fazia sentido.

So' que hoje **20 dos 21 videos ja' tem mp4 renderizado**, e o motor do mp4
(`_mp4/render.js`, linha ~119) faz:

    var marcaPlaceholder = /@yourchannel|@seucanal|@yourhandle/i.test(marca);
    if (marcaPlaceholder) L("marca d'agua OMITIDA no mp4 ...");
    ...
    if (!marcaPlaceholder && marca) { /* so' desenha se NAO for placeholder */ }

Ou seja: **subindo o mp4, o video sai limpo**. O `@yourchannel` so' aparece quando
se abre o HTML no navegador. Conferido num quadro real do `pao/shorts-sourdough-en.mp4`:
o canto superior direito esta' vazio.

Consequencia pratica: os guias mandavam trocar o handle em "28"/"30" arquivos ANTES
de publicar — trabalho que **nao e' necessario** para os Shorts. Medido agora: sao
**50 arquivos** com placeholder (24 @yourchannel, 20 @seucanal, 6 @yourhandle).

Ancoras contadas por arquivo, aborta SEM GRAVAR.
"""
import io
import sys

ARQUIVOS = [
    ('guias/plano-de-postagem.md', [
        ('intro: falta gravar',
         'Você já tem os vídeos prontos. Falta **gravar, editar e subir**. Este arquivo é a\n'
         'ponte: diz **qual arquivo abrir**, **com qual título postar** e **em que ordem**.',
         '**Os vídeos já estão prontos E gravados.** 20 dos 21 têm `.mp4` renderizado\n'
         '(1080×1920, H.264, sem marca d\'água) — para os Shorts você **não precisa do OBS**.\n'
         'Este arquivo diz **qual arquivo subir**, **com qual título** e **em que ordem**.\n'
         '\n'
         '> **O único que ainda precisa de gravação é o #13** (vídeo longo, Semana 7). E ele\n'
         '> só chega daqui a 7 semanas — até lá o OBS é opcional.', 1),

        ('secao do @yourchannel',
         '## 🖊️ Antes de gravar: troque o @yourchannel\n'
         '\n'
         'Todos os shorts vêm com **`@yourchannel`** escrito no canto superior. É um\n'
         'espaço reservado. Troque pelo **@ do seu canal** antes de gravar — senão sai\n'
         '"@yourchannel" no vídeo publicado.\n'
         '\n'
         'São **28 arquivos**. Peça que eu troque todos de uma vez — é rápido.',
         '## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo\n'
         '\n'
         'Os shorts vêm com **`@yourchannel`** no canto superior. É um espaço reservado.\n'
         '\n'
         '**Subindo o `.mp4` pronto, não precisa fazer nada.** O motor que gera o mp4\n'
         '**detecta o placeholder e omite a marca d\'água** — conferido no quadro real: o\n'
         'canto superior sai **limpo**. O `@yourchannel` aparece **só** quando você abre o\n'
         'HTML no navegador para assistir.\n'
         '\n'
         'Ele sairia no vídeo em **um** caso: se você **gravar pelo OBS** (o caminho do\n'
         'vídeo longo, #13) — aí a marca d\'água é desenhada na tela e o `?rec` **não** a\n'
         'esconde. Nesse caso, troque o @ **antes** de gravar.\n'
         '\n'
         'São **50 arquivos** com placeholder (24 `@yourchannel`, 20 `@seucanal`,\n'
         '6 `@yourhandle`). Peça que eu troque todos de uma vez — é rápido.', 1),
    ]),

    ('guias/guia-de-upload.md', [
        ('tabela: o @handle',
         '| **@handle** | o `@algumacoisa` | é o `@yourchannel` que está escrito **dentro dos vídeos** |',
         '| **@handle** | o `@algumacoisa` | é a marca d\'água dos shorts — que **não** sai no `.mp4` pronto (ver `plano-de-postagem.md`) |', 1),

        ('troco nos 30 arquivos',
         '**Se você criar o canal, me diga o @handle** que eu troco nos 30 arquivos de uma vez\n'
         '(hoje eles mostram `@yourchannel` / `@seucanal`).',
         '**Se você criar o canal, me diga o @handle** que eu troco nos **50 arquivos** de uma\n'
         'vez (hoje eles mostram `@yourchannel` / `@seucanal` / `@yourhandle`).\n'
         '\n'
         '⚠️ **Isto não trava a publicação.** Para os Shorts, o `.mp4` já pronto sai **sem**\n'
         'marca d\'água. O handle só precisa estar certo se você for **gravar pelo OBS**.', 1),

        ('nota dos 30 arquivos',
         'Isso troca o `@yourchannel` nos **30 arquivos** de uma vez, com backup de cada um.',
         'Isso troca o placeholder nos **50 arquivos** de uma vez, com backup de cada um.\n'
         '**Lembrando:** para os Shorts já renderizados isto é opcional — o `.mp4` sai limpo.', 1),
    ]),
]


def main():
    falhou = False
    for arq, trocas in ARQUIVOS:
        with io.open(arq, 'r', encoding='utf-8', newline='') as fh:
            d = fh.read()
        eol = '\r\n' if d.count('\r\n') else '\n'
        antes = len(d.encode('utf-8'))
        print('\n%s (%d bytes, %s)' % (arq, antes, 'CRLF' if eol == '\r\n' else 'LF'))

        # flag POR ARQUIVO: um erro num arquivo nao pode impedir a gravacao do outro
        ruim_este = False
        for i, (rotulo, velho, novo, esperado) in enumerate(trocas, 1):
            v = velho.replace('\n', eol)
            n = novo.replace('\n', eol)
            c = d.count(v)
            if c != esperado:
                print('  %d. %-24s casou %d (esperado %d)  ERRO' % (i, rotulo, c, esperado))
                ruim_este = True
                continue
            d = d.replace(v, n)
            print('  %d. %-24s ok (%d)' % (i, rotulo, c))

        if ruim_este:
            falhou = True
            print('  -> nao gravado')
            continue

        # prova: nao pode ter sobrado numero velho nem a negacao
        ruins = []
        if '28 arquivos' in d:
            ruins.append('"28 arquivos"')
        if '30 arquivos' in d:
            ruins.append('"30 arquivos"')
        if 'no vídeo publicado' in d:
            ruins.append('"no vídeo publicado"')
        if ruins:
            print('  ERRO: sobrou %s' % ruins)
            falhou = True
            continue

        with io.open(arq, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d)
        print('  gravado: %d -> %d bytes' % (antes, len(d.encode('utf-8'))))

    if falhou:
        print('\nTERMINOU COM ERRO — confira acima.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

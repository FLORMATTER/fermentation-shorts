# -*- coding: utf-8 -*-
"""
_consertar-guia-gravacao.py — alinha as guias de GRAVACAO com o modo ?rec.

Dois problemas reais nas guias:

 1. `guias/como-virar-video-de-verdade.md` mandava usar **"Captura de tela"** no OBS.
    Num monitor deitado (1920x1080) isso grava o Short DEITADO e com borda. O certo
    e **Fonte de Navegador** em 1080x1920.

 2. Tres guias ainda mandavam usar `?play` na URL. O `?play` so inicia sozinho —
    NAO esconde a capa. Para gravar, o certo e `?rec` (esconde a capa e os botoes,
    preenche 1080x1920 e inicia sozinho).

Uso:
    python _consertar-guia-gravacao.py            # dry-run, so mostra
    python _consertar-guia-gravacao.py --apply    # grava (backup .antes-do-rec2)
"""
import io
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))


def troca(d, velho, novo, n=1):
    """Substitui exigindo a contagem exata — aborta o arquivo inteiro se nao casar."""
    c = d.count(velho)
    assert c == n, 'ancora com %d ocorrencia(s), esperado %d:\n%s' % (
        c, n, velho[:120])
    return d.replace(velho, novo, n)


# ─────────────────────────────────────────────────────────────────────────────
# 1. guias/como-virar-video-de-verdade.md  — o erro do "Captura de tela"
# ─────────────────────────────────────────────────────────────────────────────
OPCAO_B_VELHA = """### Opção B — OBS Studio (grátis, é o melhor) ⭐ RECOMENDO
1. Baixe em **obsproject.com** e instale
2. Abra o OBS
3. Em "Fontes", clique no **+** → **Captura de tela** → OK
4. Vá em **Configurações → Saída**:
   - Resolução: **1080x1920** (vertical!) ou **1080x1080**
   - FPS: **30**
5. Aperte **Iniciar Gravação**
6. Volte no navegador e dê play na animação
7. Quando acabar, **Parar Gravação**"""

OPCAO_B_NOVA = """### Opção B — OBS Studio (grátis, é o melhor) ⭐ RECOMENDO

1. Baixe em **obsproject.com** e instale
2. Abra o OBS
3. Em **Fontes**, clique no **+** → **Navegador** (Browser)
4. No campo **URL**, cole o caminho do arquivo com `file:///` na frente e **`?rec` no fim**:
   ```
   file:///C:/Users/Saxa/Desktop/youtube-work/rabanete/shorts-rabanete-animado-en.html?rec
   ```
   - **Largura:** `1080` · **Altura:** `1920`
5. Vá em **Configurações → Vídeo**:
   - Base (canvas) e Saída: **1080x1920**
   - FPS: **30**
6. Aperte **Iniciar Gravação**
7. **Espere 3 segundos** → clique com o **botão direito na fonte → Atualizar**
   (a animação recomeça do zero)
8. Quando acabar, **Parar Gravação**

> **Por que `?rec` na URL:** ele esconde a capa e os botões de play (que apareceriam
> no vídeo) e faz a animação começar sozinha. Sem `?rec`, o arquivo abre como short
> normal, só para assistir.
>
> ⚠️ **Por que NÃO usar "Captura de tela":** ela grava o monitor inteiro. Num monitor
> deitado (1920x1080) o Short vertical sai **deitado e com borda preta dos lados**.
> A Fonte de Navegador desenha a página fora da tela, no tamanho certo — sem crop,
> sem zoom e sem perda de qualidade."""

PARTE4_VELHA = """# PARTE 4 — POSTAR NO YOUTUBE

1. Abra o **app do YouTube** no celular"""

PARTE4_NOVA = """# PARTE 4 — POSTAR NO YOUTUBE

> **Guia completo de upload** — pelo computador, campo por campo, dizendo o que colar
> em cada um: `guias/guia-de-upload.md`. O resumo abaixo é o caminho pelo celular.

1. Abra o **app do YouTube** no celular"""


# ─────────────────────────────────────────────────────────────────────────────
# 2..4  — `?play` -> `?rec` nas guias que ainda estavam desatualizadas
# ─────────────────────────────────────────────────────────────────────────────
URL_GUIA_VELHA = ('     file:///C:/Users/Saxa/Desktop/youtube-work/'
                  'guia-geral/shorts-5-easiest-en.html?play')
URL_GUIA_NOVA = ('     file:///C:/Users/Saxa/Desktop/youtube-work/'
                 'guia-geral/shorts-5-easiest-en.html?rec')

EXPL_GUIA_VELHA = """O `?play` no fim da URL faz a animação **começar sozinha 1,5 s depois de carregar**.
Sem ele, você teria que clicar no ▶ dentro da fonte — e isso exige
*botão direito na fonte → Interagir*."""

EXPL_GUIA_NOVA = """O `?rec` no fim da URL faz a animação **começar sozinha**, **esconde a capa** e
**esconde os botões de play** — que senão apareceriam no vídeo. Sem ele, você teria que
clicar no ▶ dentro da fonte, e isso exige *botão direito na fonte → Interagir*.

> `?play` também inicia sozinho (1,5 s depois de carregar), mas **não esconde a capa**.
> Para gravar, use sempre `?rec`."""

URL_SAUER_VELHA = ('file:///C:/Users/Saxa/Desktop/youtube-work/repolho/'
                   'shorts-sauerkraut-en-1080x1920.html?play')
URL_SAUER_NOVA = ('file:///C:/Users/Saxa/Desktop/youtube-work/repolho/'
                  'shorts-sauerkraut-en-1080x1920.html?rec')

EXPL_SAUER_VELHA = ('O `?play` no fim da URL faz a animação começar sozinha 1,5 s '
                    'depois de carregar.')
EXPL_SAUER_NOVA = ('O `?rec` no fim da URL faz a animação começar sozinha e **esconde a '
                   'capa e os botões de play** (que senão apareceriam no vídeo). '
                   '`?play` também inicia sozinho, mas não esconde a capa.')

README_VELHO = 'Navegador do OBS, 1080 × 1920, com `?play` na URL) — é o mesmo procedimento para os'
README_NOVO = 'Navegador do OBS, 1080 × 1920, com `?rec` na URL) — é o mesmo procedimento para os'


PLANO = [
    ('guias/como-virar-video-de-verdade.md', [
        (OPCAO_B_VELHA, OPCAO_B_NOVA),
        (PARTE4_VELHA, PARTE4_NOVA),
    ]),
    ('guia-geral/como-gravar-e-publicar.md', [
        (URL_GUIA_VELHA, URL_GUIA_NOVA),
        (EXPL_GUIA_VELHA, EXPL_GUIA_NOVA),
    ]),
    ('repolho/como-gravar-sauerkraut.md', [
        (URL_SAUER_VELHA, URL_SAUER_NOVA),
        (EXPL_SAUER_VELHA, EXPL_SAUER_NOVA),
    ]),
    ('README.md', [
        (README_VELHO, README_NOVO),
    ]),
]


def main():
    aplicar = '--apply' in sys.argv
    total = 0

    for rel, edicoes in PLANO:
        caminho = os.path.join(RAIZ, rel.replace('/', os.sep))
        if not os.path.exists(caminho):
            print('FALTA  %s' % rel)
            return 1

        bruto = io.open(caminho, 'rb').read().decode('utf-8')
        nl = '\r\n' if '\r\n' in bruto else '\n'
        d = bruto.replace('\r\n', '\n')
        antes = len(d)

        try:
            for velho, novo in edicoes:
                d = troca(d, velho, novo, 1)
        except AssertionError as e:
            print('ABORTOU %s\n  %s' % (rel, e))
            return 1

        print('%-42s %d -> %d bytes  (%d edicoes)' % (
            rel, antes, len(d), len(edicoes)))
        total += len(edicoes)

        if aplicar:
            bk = caminho + '.antes-do-rec2'
            if not os.path.exists(bk):
                shutil.copy2(caminho, bk)
            saida = d if nl == '\n' else d.replace('\n', nl)
            io.open(caminho, 'w', encoding='utf-8', newline='').write(saida)

    if aplicar:
        print('\nOK — %d edicoes aplicadas' % total)
    else:
        print('\nDRY-RUN — %d edicoes prontas. Rode com --apply para gravar.' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())

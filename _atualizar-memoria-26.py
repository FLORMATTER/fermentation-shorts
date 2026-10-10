# -*- coding: utf-8 -*-
"""
Fecha o #26 (kombucha de beterraba com melancia):
  - contadores do MEMORY.md: 25 -> 26 entradas, 24 -> 25 com mp4, 15 -> 16 semanas,
    beterraba 6 -> 7, PT pendente #22-#25 -> #22-#26
  - 2 regras novas (a do lookahead ganhou a 4a manifestacao; a do --final congelado)
  - enxuga o texto para o arquivo NAO passar de 3.000 chars

Padrao do projeto: toda ancora tem contagem esperada e o script ABORTA SEM GRAVAR
se alguma nao casar. Nada de heredoc (o \n e o acento se perdem no caminho).
"""
import io
import os
import sys

ALVO = '.workbuddy-ai/memory/MEMORY.md'
TETO = 3000

# (ancora, substituto, quantas vezes tem de casar)  -- ancora em r-string: o arquivo
# documenta regex, entao tem \n LITERAL (barra + n) no meio do texto.
EDICOES = [
    # --- contadores ---
    (r'## 📊 Catálogo — 25 entradas',
     r'## 📊 Catálogo — 26 entradas', 1),

    (r'**#22–#25 são só EN**',
     r'**#22–#26 são só EN**', 1),

    (r'`guias/plano-de-postagem.md` (15 semanas)',
     r'`guias/plano-de-postagem.md` (16 semanas)', 1),

    (r'⚠️ Variantes (beterraba 6, repolho 4):',
     r'⚠️ Variantes (beterraba 7, repolho 4):', 1),

    (r'**Com mp4: 24 dos 25**',
     r'**Com mp4: 25 dos 26**', 1),

    (r'1356/1356 = 100%). Conferir é',
     r'100% (#21 e #26 conferidos). Conferir é', 1),

    (r'PT do #4 sem aviso de álcool; PT de #22–#25.',
     r'PT do #4 sem aviso de álcool; PT de #22–#26.', 1),

    # --- regra 1: o --final congela em -1s (quase custou conserto de defeito fantasma) ---
    (r'1. **Layout, cor e FORMA não se veem com grep** — renderizar e olhar (`_revisar-cenas.py'
     '\n'
     r'   --final`, `_zoom-cena.py`).',
     r'1. **Layout, cor e FORMA não se veem com grep** — renderizar e olhar (`_revisar-cenas.py'
     '\n'
     r'   --final`, `_zoom-cena.py`). `--final` congela em `-1s`: cor com `--no-anim`.', 1),

    # --- regra 12 enxuta, para abrir espaco ---
    (r'12. **A galeria fica velha** (rodar `_gerar-galeria.py` depois de mexer num short) e'
     '\n'
     r'    **conserto por script tem de VOLTAR para o gerador** — ele é a fonte da verdade.',
     r'12. **A galeria fica velha** (rodar `_gerar-galeria.py`) e **conserto por script VOLTA'
     '\n'
     r'    para o gerador** — ele é a fonte da verdade.', 1),

    # --- regra 4: 4a manifestacao do lookahead, com causa nova (linha de comentario) ---
    (r'4. **Regex de bloco: o lookahead erra por UM `\n`** — `(?=\n\n\ndef y)` nunca casa (custou'
     '\n'
     r'   3×). E `\n\n#` engole as funções seguintes.',
     r'4. **Regex de bloco: ancorar no SEPARADOR, não no próximo `def`** — entre cenas há'
     '\n'
     r'   comentário, então `(?=\n\ndef y)` nunca casa (4×). Use `(?=\n\n(?:#|TEXTOS))`.', 1),

    # --- enxugar (o arquivo tem teto de 3.000 chars) ---
    (r'Detalhe técnico vive na skill **`shorts-svg-animado`**. Aqui: **estado do projeto**,'
     '\n'
     r'**regra do usuário** e o **lembrete de 1 linha** de cada regra que já custou retrabalho.'
     '\n'
     r'Logs: `YYYY-MM-DD.md`.',
     r'Detalhe técnico vive na skill **`shorts-svg-animado`**; aqui: estado do projeto, regra do'
     '\n'
     r'usuário e o lembrete de 1 linha de cada regra que custou retrabalho. Logs: `YYYY-MM-DD.md`.', 1),

    (r'**Nada gravado; o canal não existe e o nome não foi escolhido.** OBS não instalado. Não'
     '\n'
     r'aprovado:',
     r'**Nada gravado; canal e nome não escolhidos.** OBS não instalado. Não aprovado:', 1),

    # --- 1 char de folga: o teto e' 3.000 e tinha ficado em 3.001 ---
    (r'2. **"Dá pra ver" não é medida — medir o pixel** (piso ~130; falha nos dois sentidos).',
     r'2. **"Dá pra ver" não é medida — medir o pixel** (piso ~130; falha nos 2 sentidos).', 1),
]


def main():
    if not os.path.exists(ALVO):
        print('ABORTA: nao achei %s' % ALVO)
        return 1

    with io.open(ALVO, encoding='utf-8', newline='') as f:
        d = f.read()
    antes = len(d)

    for old, new, esperado in EDICOES:
        n = d.count(old)
        if n != esperado:
            print('ABORTA: ancora casou %d vez(es), esperava %d:' % (n, esperado))
            print('   %r' % old[:90])
            return 1
        d = d.replace(old, new, esperado)
        print('  ok  %-58s %d vez(es)' % (old.replace('\n', ' ')[:58], n))

    if len(d) > TETO:
        print('ABORTA: ficou com %d chars, teto %d' % (len(d), TETO))
        return 1

    # checagem final: os numeros novos estao la e os velhos nao
    for bom in ('26 entradas', '25 dos 26', '16 semanas', 'beterraba 7',
                '#22–#26', '(?:#|TEXTOS)', '--no-anim'):
        if bom not in d:
            print('ABORTA: nao achei %r no resultado' % bom)
            return 1
    for ruim in ('25 entradas', '24 dos 25', 'beterraba 6', '(15 semanas)'):
        if ruim in d:
            print('ABORTA: sobrou %r' % ruim)
            return 1

    tmp = ALVO + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(d)
    os.replace(tmp, ALVO)

    print()
    print('%s  %d -> %d chars (%.0f%% do teto de %d)  |  %d bytes'
          % (ALVO, antes, len(d), 100.0 * len(d) / TETO, TETO, len(d.encode('utf-8'))))
    print('gravado: MEMORY.md em 26 entradas.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

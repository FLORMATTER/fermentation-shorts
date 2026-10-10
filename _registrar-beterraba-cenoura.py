# -*- coding: utf-8 -*-
"""_registrar-beterraba-cenoura.py — registra o #25 nos 3 lugares.

Videos novos entram em 3 lugares:
  1. a pasta                      -> ja' feito (beterraba/shorts-beet-carrot-en.html)
  2. _gerar-galeria.py            -> NADA A FAZER: a galeria varre as pastas de ORDEM
  3. pacote + plano de postagem   -> este script

Padrao do projeto: confere TODAS as ancoras primeiro e so' escreve se todas
casarem — assim um erro num arquivo nao deixa os outros meio-registrados.

    python _registrar-beterraba-cenoura.py
"""
import io
import re
import sys

PACOTE = 'guias/pacote-legendas-descricoes-en.md'
PLANO = 'guias/plano-de-postagem.md'

# ----------------------------------------------------------------- entrada #25
ENTRADA = '''# 25. BEETROOT + CARROT — THE CARROT SAVES THE RED

### Title
```
Beetroot and carrot: the carrot protects the red
```

**Alternatives:**
- `Why fermented beetroot keeps its colour when carrot is in the jar`
- `Beetroot and carrot: one makes the acid, one saves the colour`
- `Two roots, two jobs - and neither one is acid`

### Description
```
Both of these are LOW-ACID vegetables. Raw beetroot sits at pH 5.3 to 6.6 and raw carrot
at 5.9 to 6.4 - both above 4.6, which is the line where the bacteria that spoil food stop.
Neither one is protecting itself. The acid has to be MADE, and that is what the sugar is
for.

The two roots do different jobs:

- BEETROOT IS THE FUEL. It carries about 7 g of sugar per 100 g; carrot carries about
  4.7 g. That is roughly 50% more. The lactic bacteria eat that sugar and give back
  lactic acid, which is what pulls the jar down under 4.6. Cut the beet THIN so the sugar
  comes out fast.
- CARROT IS THE SHIELD. Its carotenoids are antioxidants, and they slow the oxidation that
  destroys the beetroot's red pigment, betanin. Cut the carrot THICK - it is there for
  crunch, not for sugar.

That second point is the whole reason to put these two in the same jar. In a 2023 study of
lactic-fermented beetroot, carrot and beetroot-carrot juice (1:1, 2% salt), pigment loss
was significantly LOWER in the mixed juice than in beetroot on its own - the authors put it
down to antioxidant protection from the carotenoids. Beetroot alone fades. Beetroot with
carrot does not.

Then:

- 2% salt by weight - 20 g of salt per 1 kg of vegetables. Weigh it.
- Use salt WITHOUT iodine. Iodine is antibacterial and it stalls the bacteria you are
  trying to grow.
- 5 to 7 days at room temperature, out of the sun. Taste it: sour means ready, still sweet
  means wait.
- Then the fridge. Cold slows the bacteria down - it does not stop them.
```

### Hashtags
```
#beetroot #carrot #fermentation #fermentedvegetables #lacticacid
```

File: `beterraba/shorts-beet-carrot-en.html`
**The .mp4 is already rendered:** `beterraba/shorts-beet-carrot-en.mp4`
(1080x1920 vertical, H.264, 45.2 s, constant 30 fps) - no screen recording needed.

> This is the **sixth beetroot** in the series (#3, #4, #8, #14, #19) and the **third
> carrot** (#12, #18). What makes it new is neither vegetable - it is the **pair**. The
> subject is that the carrot protects the beetroot's colour, and that both are low-acid
> foods which have to make their own acid from the sugar.
>
> ⚠️ **Ordering note.** Post it **weeks away from #3, #4, #8, #14 and #19** (beetroot) and
> from #12 and #18 (carrot). Six beetroot videos read as a production line even when the
> science is different - which is exactly the pattern YouTube's "inauthentic content" rule
> is looking for.

---
'''

# --------------------------------------------------------------- nota da semana
NOTA = '''**Esta semana tem os dois vídeos novos.** O #24 (kombucha de maçã com melão) abre a
semana e o #25 (beterraba com cenoura) fecha.

**A beterraba volta pela SEXTA vez** (#3, #4, #8, #14, #19) e a **cenoura pela TERCEIRA**
(#12, #18). Poste **semanas depois desses cinco** — seis vídeos de beterraba leem como
linha de produção mesmo com a ciência diferente, e é exatamente esse o padrão que a regra
de "conteúdo inautêntico" do YouTube procura.

O que este ensina e nenhum outro ensina: **as duas são hortaliças de BAIXA ACIDEZ**
(beterraba pH 5,3–6,6; cenoura 5,9–6,4 — as duas **acima de 4,6**), então **nenhuma está se
protegendo** e o ácido tem de ser **fabricado**. A **beterraba é o combustível** (~7 g de
açúcar por 100 g contra ~4,7 g da cenoura, ~50% mais) e a **cenoura é o escudo**: os
carotenoides são antioxidantes e **seguram a oxidação que destrói a betanina**, o pigmento
vermelho. Num estudo de 2023 (suco de beterraba, de cenoura e da mistura 1:1, com 2% de
sal), a perda de pigmento foi **significativamente MENOR na mistura** — os autores atribuem
isso à proteção dos carotenoides. Beterraba sozinha desbota; com cenoura, não.

⚠️ **Use sal sem iodo.** O iodo é antibacteriano e atrasa justamente as bactérias que você
quer cultivar — é o detalhe que a cena 3 do vídeo ensina.'''

# (arquivo, ancora, substituto, quantas vezes)
TROCAS = (
    # --- pacote: entrada nova antes do QUICK CHART
    (PACOTE,
     '# 📋 QUICK CHART — check before recording',
     ENTRADA + '\n# 📋 QUICK CHART — check before recording', 1),

    # --- pacote: linha do QUICK CHART
    (PACOTE,
     '| Apple + melon kombucha | none | 1-3 d | `THE MELON IS NOT ACID` |',
     '| Apple + melon kombucha | none | 1-3 d | `THE MELON IS NOT ACID` |\n'
     '| Beetroot + carrot | 2% | 5-7 d | `THE CARROT SAVES THE RED` |', 1),

    # --- pacote: ordem de postagem (semana 15 fica com os dois)
    (PACOTE,
     '| **15** | Apple + melon kombucha |',
     '| **15** | Apple + melon kombucha + Beetroot and carrot |', 1),

    # --- pacote: tabela "WHICH FILE TO RECORD"
    (PACOTE,
     '| 24 | Apple + melon kombucha 🆕 ⚠️ | `kombucha/shorts-apple-melon-en.html` | ✅ |',
     '| 24 | Apple + melon kombucha 🆕 ⚠️ | `kombucha/shorts-apple-melon-en.html` | ✅ |\n'
     '| 25 | Beetroot + carrot 🆕 | `beterraba/shorts-beet-carrot-en.html` | ✅ |', 1),

    # --- pacote: a contagem (25 entradas - o #13 = 24 Shorts)
    (PACOTE,
     '**All 23 Shorts are already rendered — every entry except #13.**',
     '**All 24 Shorts are already rendered — every entry except #13.**', 1),

    # --- plano: a contagem do topo
    (PLANO,
     '**Os vídeos já estão prontos E gravados.** Todos os 23 Shorts têm',
     '**Os vídeos já estão prontos E gravados.** Todos os 24 Shorts têm', 1),

    # --- plano: o aviso de "nao sao 47 arquivos" (agora sao 48)
    (PLANO,
     '## ⚠️ Antes de tudo: você tem 24 vídeos, não 47 arquivos',
     '## ⚠️ Antes de tudo: você tem 25 vídeos, não 48 arquivos', 1),

    # --- plano: a semana 15 ganha o segundo video
    (PLANO,
     '| 1 | Kombucha de maçã com melão 🆕 | `kombucha/shorts-apple-melon-en.html` | **#24** | `THE MELON IS NOT ACID` |',
     '| 1 | Kombucha de maçã com melão 🆕 | `kombucha/shorts-apple-melon-en.html` | **#24** | `THE MELON IS NOT ACID` |\n'
     '| 2 | Beterraba com cenoura 🆕 | `beterraba/shorts-beet-carrot-en.html` | **#25** | `THE CARROT SAVES THE RED` |', 1),

    # --- plano: a nota da semana (a antiga dizia "um video so'")
    (PLANO,
     '**Esta semana tem um vídeo só.** O #24 é o último que está pronto — o dia 2 fica livre para\no próximo que você fizer (ou para o #13, o vídeo longo, se você já tiver gravado).',
     NOTA, 1),
)


def main():
    conteudo = {}
    for nome in (PACOTE, PLANO):
        with io.open(nome, 'r', encoding='utf-8', newline='') as fh:
            conteudo[nome] = fh.read()

    # --- 1) confere TODAS as ancoras antes de escrever qualquer coisa
    problemas = []
    for nome, velho, novo, n in TROCAS:
        achou = conteudo[nome].count(velho)
        if achou != n:
            problemas.append('%s: ancora casou %d vez(es), esperava %d:\n    %s'
                             % (nome, achou, n, velho.split('\n')[0][:70]))
    if problemas:
        print('ERRO — nada foi gravado:')
        for p in problemas:
            print('  ' + p)
        return 1

    # --- 2) aplica
    for nome, velho, novo, n in TROCAS:
        conteudo[nome] = conteudo[nome].replace(velho, novo, n)

    # --- 3) sanidade: os numeros antigos nao podem sobrar
    for nome, proibido in ((PACOTE, 'All 23 Shorts'),
                           (PLANO, 'Todos os 23 Shorts'),
                           (PLANO, 'você tem 24 vídeos'),
                           (PLANO, 'um vídeo só')):
        if proibido in conteudo[nome]:
            print('ERRO: sobrou "%s" em %s' % (proibido, nome))
            return 1

    # --- 4) o pacote tem de terminar com 25 entradas, numeradas 1..25
    nums = [int(m) for m in re.findall(r'^# (\d+)\. ', conteudo[PACOTE], re.M)]
    if nums != list(range(1, 26)):
        print('ERRO: entradas do pacote = %s' % (nums or 'nenhuma'))
        return 1

    # --- 5) o plano tem de terminar com 15 semanas, numeradas 1..15
    sem = [int(m) for m in re.findall(r'^### Semana (\d+)', conteudo[PLANO], re.M)]
    if sem != list(range(1, 16)):
        print('ERRO: semanas do plano = %s' % (sem or 'nenhuma'))
        return 1

    # --- 6) a entrada NOVA tem de ter os 4 campos (as antigas tem formatos
    #        variados, entao validar so' a #25)
    nova = conteudo[PACOTE].split('# 25. ', 1)[1].split('# 📋 QUICK CHART', 1)[0]
    for campo in ('### Title', '### Description', '### Hashtags', 'File: `',
                  '**The .mp4 is already rendered:**'):
        if campo not in nova:
            print('ERRO: a entrada #25 nao tem %s' % campo)
            return 1
    print('  conferido: entrada #25 com Title/Description/Hashtags/File/mp4')

    # --- 7) grava
    for nome in (PACOTE, PLANO):
        with io.open(nome, 'w', encoding='utf-8', newline='') as fh:
            fh.write(conteudo[nome])
        print('  gravado: %s | %d bytes' % (nome, len(conteudo[nome].encode('utf-8'))))

    print('OK: #25 registrado | %d trocas | pacote 25 entradas | plano 15 semanas'
          % len(TROCAS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
